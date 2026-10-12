"""Corrected error-against-cost study for the heat equation.

Replaces exp_study.py, whose measurement had two defects that made its headline
number meaningless:

  (D1) the scored quantity was ``max_j |draws.mean(0) - mu|/sd_j`` where the
       draws were centred at ``mu`` by construction.  Its expectation is exactly
       zero, so the metric could only ever measure output sampling noise.  The
       centring itself is not a coding error: Proposition prop:linsuff says that
       in the linear model the mean map is affine with slope exactly one and only
       the D x D scale is estimated from M simulations.  What is wrong is
       scoring that structurally exact mean and calling the result GBC's error.
  (D2) ``n_draw`` was fixed at 4000 while the budget M swept a factor of 128, and
       it never entered the cost axis, so the reported "approximation floor" was
       the 1/sqrt(n_draw) noise of that fixed draw count.

Here every generator is scored analytically, as the Gaussian it is, against the
exact posterior.  No output draw count enters, so M is the only budget parameter
and the non-degenerate quantity, the covariance, is what is measured.

Three arms are run.  The first two are the paper's own algorithm, and differ
only in the training proposal, which is the ablation isolating localisation.
The third assumes nothing in closed form and is the honest test of the general
method on this problem.

  scale    alg:gbc with prop:linsuff's identity-plus-scale head: the affine mean
           map is exact, the scale is estimated from M prior-drawn pairs
  local    alg:loc: the same head, trained on N(thetabar_N, c^2 Sigma_N) pairs,
           with the centring and rescaling of cor:locG
  learned  nothing assumed: the full affine map from summary to parameter is
           estimated from the M pairs by least squares

The as-published metric is recorded alongside, so the diagnosis is shown rather
than asserted.

Usage:  python3 -u exp_study2.py --rep <k> --out results/study2_rep<k>.json
"""
import argparse
import json
import os
import time

import numpy as np

NU = 0.01
T = 1.0


def lam(k):
    return 4.0 * np.pi ** 2 * k ** 2


def iota(k):
    l = lam(k)
    return (1.0 - np.exp(-2 * NU * l * T)) / (2 * NU * l * T)


def design(t, x, kvec):
    return (np.exp(-NU * lam(kvec)[None, :] * t[:, None])
            * np.sqrt(2.0) * np.cos(2 * np.pi * kvec[None, :] * x[:, None]))


def k_eff(N, s0sq, kvec):
    return int((N * iota(kvec) >= 1.0 / s0sq).sum())


# ----------------------------------------------------------------------------
# GBC: simulate training pairs, learn the affine map, return its analytic law
# ----------------------------------------------------------------------------

def gbc_learn(Phi, Y, s0sq, rng, M, arm, c=2.0, chunk=256):
    """Run Algorithm 1 and return the generator's analytic law (mean, covariance).

    arm is one of 'scale', 'local', 'learned'; see the module docstring.  In every
    arm the M training pairs are produced by an actual forward solve and adjoint
    solve, so the 2M solve count on the cost axis is real.
    """
    N, J = Phi.shape
    G = Phi.T @ Phi
    S_obs = Phi.T @ Y                     # the adjoint statistic, lem:adjoint
    Sig = np.linalg.inv(G + np.diag(1.0 / s0sq))   # posterior covariance, eq:linpost

    if arm == 'local':
        # alg:loc step 1: propose in a ball of radius c about the preliminary fit
        m0 = Sig @ S_obs
        L0 = c * np.linalg.cholesky(Sig + 1e-15 * np.eye(J))
    else:
        m0 = np.zeros(J)
        L0 = np.diag(np.sqrt(s0sq))

    Th = np.empty((M, J))
    Sm = np.empty((M, J))
    for a in range(0, M, chunk):
        b = min(a + chunk, M)
        th = m0[None, :] + rng.standard_normal((b - a, J)) @ L0.T
        Yc = Phi @ th.T + rng.standard_normal((N, b - a))   # forward solve + noise
        Th[a:b] = th
        Sm[a:b] = (Phi.T @ Yc).T                            # adjoint solve
    assert np.all(np.isfinite(Sm)), "non-finite summary in the training set"

    if arm == 'learned':
        # nothing assumed: estimate the whole affine map from the pairs
        X = np.hstack([np.ones((M, 1)), Sm])
        coef, *_ = np.linalg.lstsq(X, Th, rcond=None)
        resid = Th - X @ coef
        C = (resid.T @ resid) / max(M - J - 1, 1)
        mean_G = coef[0] + coef[1:].T @ S_obs
        return mean_G, C

    # 'scale' and 'local': prop:linsuff's identity-plus-scale head.  The affine
    # mean map is exact with slope one, so only the scale is estimated.  The
    # residual is R = theta - Sigma_N S, whose law is Theorem thm:locbias.
    R = Th - Sm @ Sig.T
    Rc = R - R.mean(0)
    C = (Rc.T @ Rc) / max(M - 1, 1)
    if arm == 'local':
        # cor:locG: centre and rescale, without which the head reports
        # sqrt(s_j + c^2 p_j^2) times the correct standard deviation
        p = np.diag(Sig @ np.diag(1.0 / s0sq))
        f = 1.0 / np.sqrt(np.maximum(1.0 - p + c * c * p * p, 1e-300))
        C = (f[:, None] * C) * f[None, :]
    w, Q = np.linalg.eigh(0.5 * (C + C.T))
    C = Q @ np.diag(np.maximum(w, 0.0)) @ Q.T
    return Sig @ S_obs, C


def as_published(Phi, Y, s0sq, rng, M, c=2.0, n_draw=4000):
    """The original measurement, kept so the diagnosis can be shown, not asserted."""
    J = Phi.shape[1]
    cov = np.linalg.inv(Phi.T @ Phi + np.diag(1.0 / s0sq))
    mu = cov @ (Phi.T @ Y)
    L = c * np.linalg.cholesky(cov + 1e-15 * np.eye(J))
    R = np.empty((M, J))
    for m in range(M):
        th = mu + L @ rng.standard_normal(J)
        Ym = Phi @ th + rng.standard_normal(Phi.shape[0])
        R[m] = th - cov @ (Phi.T @ Ym)
    Rc = R - R.mean(0)
    C = (Rc.T @ Rc) / M
    p = np.diag(cov @ np.diag(1.0 / s0sq))
    s = 1.0 - p
    f = 1.0 / np.sqrt(np.maximum(s + c * c * p * p, 1e-300))
    C = (f[:, None] * C) * f[None, :]
    w, Q = np.linalg.eigh(0.5 * (C + C.T))
    H = Q @ np.diag(np.sqrt(np.maximum(w, 0.0))) @ Q.T
    d = mu[None, :] + rng.standard_normal((n_draw, J)) @ H.T
    sd = np.sqrt(np.diag(cov))
    return float(np.max(np.abs(d.mean(0) - mu) / sd))


# ----------------------------------------------------------------------------
# pCN, unchanged from exp_study.py so the baseline is the same one
# ----------------------------------------------------------------------------

def pcn(Phi, Y, s0sq, n_iter, rng, beta=0.1, target=0.25, adapt_frac=0.2):
    J = Phi.shape[1]
    th = rng.standard_normal(J) * np.sqrt(s0sq)
    r = Y - Phi @ th
    ll = -0.5 * r @ r
    keep = np.empty((n_iter, J))
    acc = 0
    n_ad = int(adapt_frac * n_iter)
    win = 500
    wa = 0
    for i in range(n_iter):
        if i < n_ad and i > 0 and i % win == 0:
            beta = float(np.clip(beta * np.exp(0.6 * (wa / win - target)), 1e-4, .999))
            wa = 0
        prop = np.sqrt(1 - beta ** 2) * th + beta * (rng.standard_normal(J) * np.sqrt(s0sq))
        rp = Y - Phi @ prop
        llp = -0.5 * rp @ rp
        if np.log(rng.uniform()) < llp - ll:
            th, ll, acc, wa = prop, llp, acc + 1, wa + 1
        keep[i] = th
    return keep, acc / n_iter, beta


def ess1(x):
    n = len(x)
    x = x - x.mean()
    f = np.fft.rfft(x, 2 * n)
    ac = np.fft.irfft(f * np.conj(f))[:n].real
    if ac[0] <= 0:
        return 1.0
    ac /= ac[0]
    s = 0.0
    for k in range(1, n - 1, 2):
        p = ac[k] + ac[k + 1]
        if p <= 0:
            break
        s += p
    return n / (1.0 + 2.0 * s)


# ----------------------------------------------------------------------------
# scoring: both laws are Gaussian, so score them as such
# ----------------------------------------------------------------------------

def w2_gauss(m1, C1, m2, C2):
    """Squared 2-Wasserstein between two Gaussians."""
    w, Q = np.linalg.eigh(0.5 * (C2 + C2.T))
    w = np.maximum(w, 0.0)
    R = Q @ np.diag(np.sqrt(w)) @ Q.T
    M = R @ C1 @ R
    wm, _ = np.linalg.eigh(0.5 * (M + M.T))
    cross = float(np.sum(np.sqrt(np.maximum(wm, 0.0))))
    return float(np.sum((m1 - m2) ** 2) + np.trace(C1) + np.trace(C2) - 2 * cross)


def score(mean_G, C_G, mu, cov, sd):
    # mean_err_psd and sd_err_rel are worst-mode maxima, not averages, despite the key
    # names; the table column and the prose in make_experiments_tex.py both say "max".
    return dict(
        mean_err_psd=float(np.max(np.abs(mean_G - mu) / sd)),
        sd_err_rel=float(np.max(np.abs(np.sqrt(np.diag(C_G)) / sd - 1.0))),
        cov_rel_fro=float(np.linalg.norm(C_G - cov) / np.linalg.norm(cov)),
        w2_psd=float(np.sqrt(max(w2_gauss(mean_G, C_G, mu, cov), 0.0)) / np.mean(sd)),
    )


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--rep', type=int, default=1)
    ap.add_argument('--N', type=int, default=50000)
    ap.add_argument('--J', type=int, default=8)
    ap.add_argument('--rho', type=float, default=124.0)
    ap.add_argument('--alpha', type=float, default=3.0)
    ap.add_argument('--c', type=float, default=2.0)
    ap.add_argument('--out', default='results/study2.json')
    a = ap.parse_args()

    rng = np.random.default_rng(90000 + a.rep)
    kvec = np.arange(1, a.J + 1)
    s0sq = a.rho ** 2 / lam(kvec) ** a.alpha
    assert np.all(s0sq > 0), "prior variances must be positive"

    th0 = rng.standard_normal(a.J) * np.sqrt(s0sq)      # prior-typical truth
    t = rng.uniform(0, T, a.N)
    x = rng.uniform(0, 1, a.N)
    Phi = design(t, x, kvec)
    Y = Phi @ th0 + rng.standard_normal(a.N)

    cov = np.linalg.inv(Phi.T @ Phi + np.diag(1.0 / s0sq))
    mu = cov @ (Phi.T @ Y)
    sd = np.sqrt(np.diag(cov))
    ke = k_eff(a.N, s0sq, kvec)
    print(f"rep {a.rep}: N={a.N} J={a.J} rho={a.rho} k_eff={ke}", flush=True)

    Ms = (250, 500, 1000, 2000, 4000, 8000, 16000, 32000)
    curves = {}
    for arm in ('scale', 'local', 'learned'):
        rows = []
        for M in Ms:
            rr = np.random.default_rng(500000 + 1000 * a.rep + M
                                       + {'scale': 0, 'local': 7, 'learned': 13}[arm])
            t0 = time.time()
            mG, CG = gbc_learn(Phi, Y, s0sq, rr, M, arm, c=a.c)
            el = time.time() - t0
            r = score(mG, CG, mu, cov, sd)
            r.update(M=M, solves=2 * M, seconds=el, arm=arm)
            rows.append(r)
            print(f"  {arm:7s} M={M:6d} mean_err={r['mean_err_psd']:.5f} "
                  f"sd_err={r['sd_err_rel']:.5f} W2={r['w2_psd']:.5f} {el:.1f}s", flush=True)
        curves[arm] = rows

    # the original metric, for the diagnosis
    pub = []
    for M in Ms:
        rr = np.random.default_rng(5000 + M)
        pub.append(dict(M=M, solves=2 * M,
                        mean_err_psd=as_published(Phi, Y, s0sq, rr, M, c=a.c)))
        print(f"  published M={M:6d} err={pub[-1]['mean_err_psd']:.5f}", flush=True)

    pcn_rows = []
    for it in (5_000, 20_000, 80_000, 320_000, 1_280_000):
        rr = np.random.default_rng(700000 + 1000 * a.rep + it)
        t0 = time.time()
        ch, acc, bt = pcn(Phi, Y, s0sq, it, rr)
        el = time.time() - t0
        ch = ch[it // 5:]
        e = float(min(ess1(ch[:, j]) for j in range(a.J)))
        mC = ch.mean(0)
        CC = np.cov(ch.T)
        r = score(mC, CC, mu, cov, sd)
        r.update(iters=it, solves=it, seconds=el, acc=float(acc), beta=float(bt), ess_min=e)
        pcn_rows.append(r)
        print(f"  pcn   it={it:9d} mean_err={r['mean_err_psd']:.5f} "
              f"sd_err={r['sd_err_rel']:.5f} W2={r['w2_psd']:.5f} ess={e:.0f} {el:.1f}s",
              flush=True)

    out = dict(rep=a.rep, N=a.N, J=a.J, rho=a.rho, alpha=a.alpha, nu=NU, T=T, c=a.c,
               k_eff=ke, gbc=curves, published_metric=pub, pcn=pcn_rows)
    os.makedirs(os.path.dirname(a.out) or '.', exist_ok=True)
    json.dump(out, open(a.out, 'w'), indent=1)
    print("wrote", a.out, flush=True)


if __name__ == '__main__':
    main()
