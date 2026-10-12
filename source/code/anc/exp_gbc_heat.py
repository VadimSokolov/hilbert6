"""End-to-end GBC for the heat-equation initial-condition problem.

This is the experiment the paper was missing: it executes Algorithm 1 rather than
evaluating its asymptotic formulas. The heat equation is chosen because the exact
posterior is conjugate and available in closed form, so the GBC output can be
scored against ground truth rather than against another approximation.

What it measures
  1. Whether GBC with the one-step summary of Definition 5.4 recovers the exact
     posterior, in per-mode Wasserstein-1 and in credible-interval coverage.
  2. The simulation budget: error against M at fixed J, testing the linear-in-J
     claim of Theorem 12.3 against the quadratic that the pre-correction proof
     supported.
  3. The factor T in the one-step direction bar e_j = T (I*I)^{-1} e_j. Run at
     T != 1, where the pre-correction constant is wrong by 1/T, and at T = 1,
     where the two coincide and the error is invisible.
  4. Wall-clock cost against preconditioned Crank-Nicolson MCMC, the standard
     sampler for this class of problem.

Conventions follow the manuscript: the design is uniform on the space-time
cylinder [0,T] x Omega whose measure is T, the adjoint is with respect to
unnormalised L^2, so the Fisher information for N observations is (N/T)<h,I*I h>
and the Bernstein-von Mises covariance is T(I*I)^{-1}, with diagonal 1/iota_j.

Run: python3 -u exp_gbc_heat.py --rep 1 [--T 1.0] [--quick]
"""
import argparse, json, os, time
import numpy as np

# numpy 2.0 removed np.trapz; hopper has 1.24, local may have 2.x
_trapz = getattr(np, 'trapezoid', None) or np.trapz

# ----------------------------------------------------------------------------- model
NU = 0.01          # viscosity, as in fig_heat_stokes.py and Table 1
ALPHA = 3.0        # prior decay exponent, sigma_{0,j}^2 = rho^2 lambda_j^{-alpha}
RHO = 1.0


def lam(k):
    """Laplace eigenvalues on the 1-torus."""
    return 4.0 * np.pi**2 * k**2


def iota(k, T, T0=0.0):
    """Per-mode information, eq:iota: (1/(T-T0)) int_{T0}^T e^{-2 nu lambda t} dt."""
    l = lam(k)
    return (np.exp(-2 * NU * l * T0) - np.exp(-2 * NU * l * T)) / (2 * NU * l * (T - T0))


def design(t, x, kvec, T):
    """Phi_{ij} = e^{-nu lambda_j t_i} sqrt(2) cos(2 pi k_j x_i}), the linearised
    forward map evaluated at the design points. For the heat equation I = L is
    linear, so Phi is exact rather than a linearisation."""
    return np.exp(-NU * lam(kvec)[None, :] * t[:, None]) * np.sqrt(2.0) * np.cos(
        2 * np.pi * kvec[None, :] * x[:, None])


def draw_data(theta, N, kvec, T, rng, T0=0.0):
    """One realisation of eq:model."""
    t = rng.uniform(T0, T, N)
    x = rng.uniform(0.0, 1.0, N)
    Phi = design(t, x, kvec, T)
    return Phi, Phi @ theta + rng.standard_normal(N)


def exact_posterior(Phi, Y, s0sq):
    """Conjugate Gaussian posterior, eq:linpost. Ground truth."""
    prec = Phi.T @ Phi + np.diag(1.0 / s0sq)
    cov = np.linalg.inv(prec)
    return cov @ (Phi.T @ Y), cov


# ------------------------------------------------------------------- summary statistics
def summary_onestep(Phi, Y, kvec, T, N, use_T_correction=True):
    """One-step efficient-score summary, Definition 5.4, from bar theta_N = 0.

    bar e_j = T (I*I)^{-1} e_j, and <e_j, I*I e_j> = T iota_j by eq:modeinfo, so
    bar e_j = e_j / iota_j and

        S_j = bar theta_j + (1/(N iota_j)) sum_i Phi_ij (Y_i - (Phi bar theta)_i).

    Dropping the factor T, as the manuscript did before correction, replaces
    1/(N iota_j) by 1/(N T iota_j) and estimates (1/T)<e_j, theta_0> instead of
    <e_j, theta_0>. The two agree only at T = 1.
    """
    io = iota(kvec, T)
    scale = 1.0 / (N * io) if use_T_correction else 1.0 / (N * T * io)
    return scale * (Phi.T @ Y)


def summary_adjoint(Phi, Y):
    """Exactly sufficient statistic for the linear case, Lemma 5.1: the adjoint
    evolution driven by the data.

    NOT interchangeable with summary_onestep in gbc_posterior. The identity-skip head
    centres its draws at S_obs itself, so it requires a summary already on the scale of
    theta; Phi'Y is on the scale N iota_j theta_j. Preconditioning it to theta scale means
    multiplying by 1/(N iota_j), and that is exactly summary_onestep. This is the same point
    prop:linsuff makes in the manuscript: the sufficient summary enters the mean map with
    slope V_N, not with slope one, so the raw adjoint has to be preconditioned before a
    skip connection can consume it. There is therefore no adjoint-versus-one-step ablation
    to run: after the rescaling the two coincide.
    """
    return Phi.T @ Y


# ----------------------------------------------------------------------------- GBC
def gbc_posterior(kvec, T, N, M, s0sq, rng, S_obs, summary_fn, n_draw=4000):
    """Algorithm 1 with the identity-skip Gaussian-head generator of Definition 12.2.

    Steps 1 to 2: simulate M pairs from the prior and the model, compute each
    summary, whiten the residuals by D = diag(1/iota_j), and form the uncentred
    second-moment matrix hat C_M. The generator is closed form: no gradient
    training is involved, which is the point of the identity-skip parametrisation.
    Steps 3 to 4: evaluate at the observed summary and draw.
    """
    J = len(kvec)
    D_half = np.sqrt(1.0 / iota(kvec, T))              # D^{1/2}, D = diag(1/iota_j)
    W = np.empty((M, J))
    for m in range(M):
        th = rng.standard_normal(J) * np.sqrt(s0sq)     # theta^(m) ~ prior
        Phi_m, Y_m = draw_data(th, N, kvec, T, rng)     # Z^(m) ~ model
        S_m = summary_fn(Phi_m, Y_m)
        W[m] = (th - S_m) * np.sqrt(N) / D_half         # W = D^{-1/2} sqrt(N)(theta - S)
    C = (W.T @ W) / M                                   # hat C_M, uncentred by design
    # symmetric psd square root; C can be singular when M < J
    ev, V = np.linalg.eigh(0.5 * (C + C.T))
    C_half = V @ np.diag(np.sqrt(np.maximum(ev, 0.0))) @ V.T
    Z = rng.standard_normal((n_draw, J))
    draws = S_obs[None, :] + (Z @ (D_half[:, None] * C_half).T) / np.sqrt(N)
    return draws, C


# ------------------------------------------------------------------------- diagnostics
def w1_gauss(m1, s1, m2, s2):
    """Wasserstein-1 between two univariate Gaussians, by numerical integration of
    the quantile difference (no closed form for W1 unlike W2)."""
    tau = np.linspace(1e-4, 1 - 1e-4, 2001)
    from scipy.stats import norm
    z = norm.ppf(tau)
    return _trapz(np.abs((m1 + s1 * z) - (m2 + s2 * z)), tau)


def score(draws, mu_ex, cov_ex, kvec):
    """Per-mode agreement between the GBC draws and the exact posterior."""
    m_g, s_g = draws.mean(0), draws.std(0, ddof=1)
    s_e = np.sqrt(np.diag(cov_ex))
    w1 = np.array([w1_gauss(m_g[j], s_g[j], mu_ex[j], s_e[j]) for j in range(len(kvec))])
    lo, hi = np.percentile(draws, [2.5, 97.5], axis=0)
    cov95 = np.mean((mu_ex >= lo) & (mu_ex <= hi))      # does GBC cover the exact mean
    return dict(w1_mean=float(w1.mean()), w1_max=float(w1.max()),
                mean_abs_err=float(np.abs(m_g - mu_ex).max()),
                sd_ratio_med=float(np.median(s_g / s_e)),
                cov95=float(cov95))


# ------------------------------------------------------------------------------ pCN
def pcn(Phi, Y, s0sq, n_iter, rng, beta=0.08):
    """Preconditioned Crank-Nicolson, the dimension-robust benchmark sampler.
    Prior-reversible proposal, so the acceptance ratio is the likelihood ratio."""
    J = Phi.shape[1]
    th = rng.standard_normal(J) * np.sqrt(s0sq)
    r = Y - Phi @ th
    ll = -0.5 * r @ r
    keep, acc = np.empty((n_iter, J)), 0
    for i in range(n_iter):
        prop = np.sqrt(1 - beta**2) * th + beta * (rng.standard_normal(J) * np.sqrt(s0sq))
        rp = Y - Phi @ prop
        llp = -0.5 * rp @ rp
        if np.log(rng.uniform()) < llp - ll:
            th, ll, acc = prop, llp, acc + 1
        keep[i] = th
    return keep, acc / n_iter


# ------------------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--rep', type=int, required=True)
    ap.add_argument('--T', type=float, default=1.0)
    ap.add_argument('--N', type=int, default=4000)
    ap.add_argument('--quick', action='store_true')
    a = ap.parse_args()

    T, N = a.T, a.N
    rng = np.random.default_rng(a.rep * 31 + 7)
    Js = [4, 8] if a.quick else [4, 8, 16, 32]
    Ms = [64, 256] if a.quick else [64, 128, 256, 512, 1024, 2048, 4096]
    rows = []

    for J in Js:
        kvec = np.arange(1, J + 1)
        s0sq = RHO**2 * lam(kvec) ** (-ALPHA)
        theta0 = (1.0 / (1 + kvec**2)) * np.sign(np.sin(kvec))   # as in fig_heat_stokes
        Phi, Y = draw_data(theta0, N, kvec, T, rng)
        mu_ex, cov_ex = exact_posterior(Phi, Y, s0sq)

        # eq:gram check: Phi^T Phi should be diag(N iota_j) to O(sqrt(N))
        G = Phi.T @ Phi
        gram_rel = float(np.max(np.abs(np.diag(G) / (N * iota(kvec, T)) - 1)))
        offdiag = float(np.max(np.abs(G - np.diag(np.diag(G)))) / N)

        for use_T in ([True, False] if not np.isclose(T, 1.0) else [True]):
            S_obs = summary_onestep(Phi, Y, kvec, T, N, use_T)
            fn = lambda P, YY: summary_onestep(P, YY, kvec, T, N, use_T)
            for M in Ms:
                t0 = time.time()
                draws, C = gbc_posterior(kvec, T, N, M, s0sq, rng, S_obs, fn)
                sec = time.time() - t0
                r = score(draws, mu_ex, cov_ex, kvec)
                r.update(J=J, M=M, N=N, T=T, rep=a.rep, T_corrected=use_T,
                         summary='onestep', sec=sec, gram_rel=gram_rel,
                         gram_offdiag=offdiag, sqrtN_w1=float(np.sqrt(N) * r['w1_mean']))
                rows.append(r)
                print(f"J={J:3d} M={M:5d} T={T} Tfix={use_T}  "
                      f"W1={r['w1_mean']:.3e} sdratio={r['sd_ratio_med']:.3f} "
                      f"cov95={r['cov95']:.2f} {sec:.1f}s", flush=True)

        # An adjoint-versus-one-step ablation was reported here in an earlier revision.
        # It was not one: it called summary_onestep twice and merely relabelled the second
        # run. See the docstring of summary_adjoint for why no such ablation exists. The
        # block is removed rather than fixed, because preconditioning the adjoint to theta
        # scale reproduces summary_onestep identically.

    # ---- pCN cost comparison at the largest J
    J = Js[-1]
    kvec = np.arange(1, J + 1)
    s0sq = RHO**2 * lam(kvec) ** (-ALPHA)
    theta0 = (1.0 / (1 + kvec**2)) * np.sign(np.sin(kvec))
    Phi, Y = draw_data(theta0, N, kvec, T, rng)
    mu_ex, cov_ex = exact_posterior(Phi, Y, s0sq)
    n_it = 20000 if a.quick else 200000
    t0 = time.time()
    chain, acc = pcn(Phi, Y, s0sq, n_it, rng)
    pcn_sec = time.time() - t0
    burn = n_it // 5
    m_p, s_p = chain[burn:].mean(0), chain[burn:].std(0, ddof=1)
    s_e = np.sqrt(np.diag(cov_ex))
    w1_p = float(np.mean([w1_gauss(m_p[j], s_p[j], mu_ex[j], s_e[j]) for j in range(J)]))
    rows.append(dict(J=J, M=n_it, N=N, T=T, rep=a.rep, T_corrected=True, summary='pcn',
                     sec=pcn_sec, w1_mean=w1_p, w1_max=w1_p, mean_abs_err=float(np.abs(m_p - mu_ex).max()),
                     sd_ratio_med=float(np.median(s_p / s_e)), cov95=float('nan'),
                     gram_rel=float('nan'), gram_offdiag=float('nan'),
                     sqrtN_w1=float(np.sqrt(N) * w1_p)))
    print(f"pCN  J={J} iters={n_it} acc={acc:.3f} W1={w1_p:.3e} {pcn_sec:.1f}s", flush=True)

    os.makedirs('results', exist_ok=True)
    out = f'results/gbc_heat_T{T}_rep{a.rep}.json'
    with open(out, 'w') as f:
        json.dump(rows, f, indent=1)
    print("wrote", out)


if __name__ == '__main__':
    main()
