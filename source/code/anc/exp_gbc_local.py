"""Localised versus prior training for GBC on the heat equation.

Tests Theorem 10.2 (thm:locbias), Proposition 10.3 (prop:radius) and
Algorithm 10.4 (alg:loc) on the one problem where the exact posterior is
available in closed form, so every claim is scored against ground truth
rather than against another approximation.

Three questions, each with a sharp prediction from the manuscript.

  Q1  eq:varR.  Under a proposal q_c = N(bar theta, c^2 Sigma_N) the residual
      R = theta - S has mean P bar theta and variance c^2 P Sigma_N P' +
      Sigma_N F Sigma_N, equal to Sigma_{N,j}(s_j + c^2 p_j^2) in the basis
      diagonalising P.  This is exact linear algebra and is checked as such.

  Q2  thm:locbias(i).  Under the true prior the identity head is EXACT, so
      prior training should give sd ratio 1 on the heat equation.  Any large
      departure must come from the summary, not from the training design.

  Q3  The summary.  def:summary uses S_j = (1/(N iota_j)) (Phi'Y)_j, which
      omits the prior precision and is the MLE; lem:exact uses
      S = Sigma_N Phi'Y, the posterior mean.  They differ exactly in the
      prior-dominated modes that Figure 2 is made of.

Conventions follow the manuscript: design uniform on [0,T] x Omega of measure
T, adjoint w.r.t. unnormalised L^2, noise variance 1.

Run: python3 -u exp_gbc_local.py --rep 1 [--J 12] [--N 4000] [--M 1200]
"""
import argparse, json, os, time
import numpy as np

NU, ALPHA, RHO = 0.01, 3.0, 1.0


def lam(k):
    return 4.0 * np.pi**2 * k**2


def iota(k, T, T0=0.0):
    l = lam(k)
    return (np.exp(-2*NU*l*T0) - np.exp(-2*NU*l*T)) / (2*NU*l*(T-T0))


def design(t, x, kvec):
    return (np.exp(-NU*lam(kvec)[None, :]*t[:, None])
            * np.sqrt(2.0)*np.cos(2*np.pi*kvec[None, :]*x[:, None]))


def prior_var(kvec, rho=None):
    return (RHO if rho is None else rho)**2 * lam(kvec)**(-ALPHA)


# ------------------------------------------------------------------ exact objects
def posterior(Phi, Y, s0sq):
    """Conjugate Gaussian posterior; ground truth. varsigma = 1."""
    F = Phi.T @ Phi
    Sig = np.linalg.inv(F + np.diag(1.0/s0sq))
    return Sig @ (Phi.T @ Y), Sig, F


def p_basis(Sig, s0sq):
    """Eigen-decomposition of P = Sigma_N Sigma_0^{-1}, returned in the
    symmetrised form A = Sigma_0^{-1/2} Sigma_N Sigma_0^{-1/2} so the basis is
    orthonormal.  p_j are the prior fractions, s_j = 1 - p_j the data fractions."""
    d = np.sqrt(s0sq)
    A = (Sig / d[:, None]) / d[None, :]
    p, U = np.linalg.eigh(A)
    p = np.clip(p, 0.0, 1.0)
    V = d[:, None] * U                      # columns are P-eigenvectors
    return p, 1.0 - p, V, U


# ---------------------------------------------------------------------- summaries
def summary_onestep(Phi, Y, kvec, T, N, s0sq=None):
    """def:summary, evaluated at bar theta = 0: S_j = (Phi'Y)_j/(N iota_j)."""
    return (Phi.T @ Y) / (N * iota(kvec, T))


def summary_exact(Phi, Y, kvec, T, N, s0sq=None):
    """lem:exact: S = Sigma_N Phi'Y, the exact posterior mean."""
    Sig = np.linalg.inv(Phi.T @ Phi + np.diag(1.0/s0sq))
    return Sig @ (Phi.T @ Y)


SUMMARIES = {'onestep': summary_onestep, 'exact': summary_exact}


# ----------------------------------------------------------------------- Q1: eq:varR
def check_varR(Sig, F, s0sq, c):
    """Exact check of eq:varR.  Both sides are closed form, so this is linear
    algebra, not Monte Carlo.

    With D0 = Sigma_0^{1/2} and A = D0^{-1} Sigma_N D0^{-1} = U diag(p) U',
    P = Sigma_N Sigma_0^{-1} = D0 A D0^{-1} and

        c^2 P Sigma_N P' = D0 A^3 D0,   Sigma_N F Sigma_N = D0 (A - A^2) D0,

    so Var(R) = D0 (c^2 A^3 + A - A^2) D0, whose entries in the U basis are
    p_j (s_j + c^2 p_j^2), against Sigma_N -> p_j in the same coordinates.
    """
    D0 = np.sqrt(s0sq)
    P = Sig @ np.diag(1.0/s0sq)
    V = c**2 * P @ Sig @ P.T + Sig @ F @ Sig            # left-hand side, exact
    A = (Sig / D0[:, None]) / D0[None, :]
    p, U = np.linalg.eigh(A)
    p = np.clip(p, 0.0, 1.0); s = 1.0 - p
    Vt = U.T @ ((V / D0[:, None]) / D0[None, :]) @ U     # conjugate and rotate
    lhs = np.diag(Vt)
    rhs = p * (s + c**2 * p**2)
    off = np.max(np.abs(Vt - np.diag(lhs)))              # is it actually diagonal?
    return (float(np.max(np.abs(lhs - rhs) / np.maximum(np.abs(rhs), 1e-300))),
            float(off / max(np.max(np.abs(lhs)), 1e-300)))


# ------------------------------------------------------------------------- the GBC
def gbc(Phi_obs, Y_obs, kvec, T, N, M, s0sq, rng, summary, c=None,
        centre=True, rescale=False, n_draw=4000):
    """Algorithm 1, with Step 1 replaced by alg:loc when c is not None.

    c=None      draw theta^(m) from the true prior N(0, Sigma_0)
    c=float     draw theta^(m) from q_c = N(bar theta_N, c^2 Sigma_N)

    The head is the identity head: the GBC posterior is S_obs plus the fitted
    law of the residuals.  `centre` removes the residual mean (alg:loc);
    `rescale` divides the sd by sqrt(s_j + c^2 p_j^2) in the P-eigenbasis,
    the analytic correction alg:loc prescribes.
    """
    J = len(kvec)
    mu, Sig, F = posterior(Phi_obs, Y_obs, s0sq)
    S_obs = summary(Phi_obs, Y_obs, kvec, T, N, s0sq)
    if c is None:
        centre_th, L = np.zeros(J), np.diag(np.sqrt(s0sq))
    else:
        centre_th = mu
        w, Q = np.linalg.eigh(Sig)
        L = c * (Q @ np.diag(np.sqrt(np.maximum(w, 0.0))) @ Q.T)
    R = np.empty((M, J))
    for m in range(M):
        th = centre_th + L @ rng.standard_normal(J)
        Y_m = Phi_obs @ th + rng.standard_normal(N)          # fixed design
        R[m] = th - summary(Phi_obs, Y_m, kvec, T, N, s0sq)
    Rf = R - R.mean(0) if centre else R
    C = (Rf.T @ Rf) / M
    if rescale and c is not None:
        p, s, V, U = p_basis(Sig, s0sq)
        f = 1.0/np.sqrt(np.maximum(s + c**2*p**2, 1e-300))
        D0 = np.sqrt(s0sq)
        Mm = (D0[:, None] * (U @ np.diag(f) @ U.T)) / D0[None, :]
        C = Mm @ C @ Mm.T
        C = 0.5*(C + C.T)
    w, Q = np.linalg.eigh(0.5*(C + C.T))
    Ch = Q @ np.diag(np.sqrt(np.maximum(w, 0.0))) @ Q.T
    draws = S_obs[None, :] + rng.standard_normal((n_draw, J)) @ Ch.T
    return draws, mu, Sig


def score(draws, mu, Sig):
    m_g, s_g = draws.mean(0), draws.std(0, ddof=1)
    s_e = np.sqrt(np.diag(Sig))
    lo, hi = np.percentile(draws, [2.5, 97.5], axis=0)
    # W2 per mode between N(m_g,s_g) and N(mu,s_e), in units of posterior sd
    w2 = np.sqrt((m_g-mu)**2 + (s_g-s_e)**2) / s_e
    return dict(sd_ratio_med=float(np.median(s_g/s_e)),
                sd_ratio_min=float(np.min(s_g/s_e)),
                sd_ratio_max=float(np.max(s_g/s_e)),
                mean_err_psd=float(np.max(np.abs(m_g-mu)/s_e)),
                w2_psd_mean=float(w2.mean()), w2_psd_max=float(w2.max()),
                cov95=float(np.mean((mu >= lo) & (mu <= hi))))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--rep', type=int, default=1)
    ap.add_argument('--J', type=int, default=12)
    ap.add_argument('--N', type=int, default=4000)
    ap.add_argument('--M', type=int, default=1200)
    ap.add_argument('--T', type=float, default=1.0)
    ap.add_argument('--rho', type=float, default=1.0)
    ap.add_argument('--out', default='results')
    a = ap.parse_args()
    rng = np.random.default_rng(20260826 + 1000*a.rep)
    kvec = np.arange(1, a.J+1)
    s0sq = prior_var(kvec, a.rho)
    theta0 = rng.standard_normal(a.J)*np.sqrt(s0sq)
    t = rng.uniform(0.0, a.T, a.N); x = rng.uniform(0.0, 1.0, a.N)
    Phi = design(t, x, kvec)
    Y = Phi @ theta0 + rng.standard_normal(a.N)
    mu, Sig, F = posterior(Phi, Y, s0sq)
    p, s, V, U = p_basis(Sig, s0sq)

    rows = []
    # Q1: eq:varR, exact
    for c in [0.5, 1.0, 2.0, 3.0, 5.0]:
        re_, off_ = check_varR(Sig, F, s0sq, c)
        rows.append(dict(kind='varR', c=c, rel_err=re_, offdiag=off_))
    # Q2/Q3: prior vs localised, both summaries
    for sname, sfn in SUMMARIES.items():
        d, mu_, Sig_ = gbc(Phi, Y, kvec, a.T, a.N, a.M, s0sq, rng, sfn, c=None)
        rows.append(dict(kind='gbc', summary=sname, train='prior', c=None,
                         rescale=False, **score(d, mu_, Sig_)))
        for c in [0.25, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 6.0, 8.0]:
            for rs in (False, True):
                d, mu_, Sig_ = gbc(Phi, Y, kvec, a.T, a.N, a.M, s0sq, rng, sfn,
                                   c=c, rescale=rs)
                rows.append(dict(kind='gbc', summary=sname, train='local', c=c,
                                 rescale=rs, **score(d, mu_, Sig_)))
    os.makedirs(a.out, exist_ok=True)
    meta = dict(rep=a.rep, J=a.J, N=a.N, M=a.M, T=a.T, rho=a.rho, nu=NU, alpha=ALPHA,
                p_frac=[float(v) for v in p], s_frac=[float(v) for v in s],
                post_sd=[float(v) for v in np.sqrt(np.diag(Sig))],
                prior_sd=[float(v) for v in np.sqrt(s0sq)])
    with open(os.path.join(a.out, f'local_rep{a.rep}.json'), 'w') as f:
        json.dump(dict(meta=meta, rows=rows), f, indent=1)
    for r in rows:
        print(json.dumps(r))


if __name__ == '__main__':
    main()
