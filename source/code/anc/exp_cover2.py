"""Coverage over replicates, with the raw per-replicate indicators archived.

exp_study.py reported per-mode coverage rates only and discarded ``zst``, the
raw standardised errors, so the exact-versus-GBC comparison could not be
analysed as what it is: a *paired* comparison, both methods scored on the same
replicate and the same mode.  The unpaired binomial standard error
sqrt(.95*.05/reps) that resulted is the wrong yardstick, and it understates the
evidence by an order of magnitude.

Here every coverage indicator is written out, so McNemar's paired test can be
computed from the archived data rather than guessed at from marginal rates.

Usage:  python3 -u exp_cover2.py --rep <k> --out results/cover2_rep<k>.json
"""
import argparse
import json
import os

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


def gbc_generator(Phi, Y, s0sq, rng, M, c=2.0, chunk=256):
    """alg:loc with the cor:locG rescaling; returns the generator's analytic law."""
    N, J = Phi.shape
    Sig = np.linalg.inv(Phi.T @ Phi + np.diag(1.0 / s0sq))
    S_obs = Phi.T @ Y
    m0 = Sig @ S_obs
    L0 = c * np.linalg.cholesky(Sig + 1e-15 * np.eye(J))
    R = np.empty((M, J))
    for a in range(0, M, chunk):
        b = min(a + chunk, M)
        th = m0[None, :] + rng.standard_normal((b - a, J)) @ L0.T
        Yc = Phi @ th.T + rng.standard_normal((N, b - a))
        R[a:b] = th - (Phi.T @ Yc).T @ Sig.T
    Rc = R - R.mean(0)
    C = (Rc.T @ Rc) / max(M - 1, 1)
    p = np.diag(Sig @ np.diag(1.0 / s0sq))
    f = 1.0 / np.sqrt(np.maximum(1.0 - p + c * c * p * p, 1e-300))
    C = (f[:, None] * C) * f[None, :]
    w, Q = np.linalg.eigh(0.5 * (C + C.T))
    C = Q @ np.diag(np.maximum(w, 0.0)) @ Q.T
    return m0, C


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--rep', type=int, default=1)
    ap.add_argument('--reps_per_task', type=int, default=25)
    ap.add_argument('--N', type=int, default=50000)
    ap.add_argument('--J', type=int, default=8)
    ap.add_argument('--M', type=int, default=4000)
    ap.add_argument('--rho', type=float, default=124.0)
    ap.add_argument('--alpha', type=float, default=3.0)
    ap.add_argument('--c', type=float, default=2.0)
    ap.add_argument('--out', default='results/cover2.json')
    a = ap.parse_args()

    kvec = np.arange(1, a.J + 1)
    s0sq = a.rho ** 2 / lam(kvec) ** a.alpha
    ke = int((a.N * iota(kvec) >= 1.0 / s0sq).sum())
    # One prior draw, fixed across every replicate and every array task, so all 1000
    # replicates speak about the same theta_0. The seed is a constant, not a.rep.
    th0_typical = (np.random.default_rng(20260826).standard_normal(a.J) * np.sqrt(s0sq))
    # The deterministic truth of exp_gbc_heat.py: rougher than the prior's RKHS.
    th0_rough = (1.0 / (1 + kvec ** 2)) * np.sign(np.sin(kvec))
    TRUTH = {'fixed_typical': th0_typical, 'fixed_rough': th0_rough}

    out = dict(rep=a.rep, N=a.N, J=a.J, M=a.M, rho=a.rho, alpha=a.alpha,
               nu=NU, T=T, c=a.c, k_eff=ke, level=0.95,
               reps_per_task=a.reps_per_task,
               th0_typical=th0_typical.tolist(), th0_rough=th0_rough.tolist())

    for arm in ('prior', 'fixed_typical', 'fixed_rough'):
        cov_ex, cov_gb = [], []
        for r in range(a.reps_per_task):
            off = {'prior': 0, 'fixed_typical': 400000, 'fixed_rough': 800000}[arm]
            seed = 300000 + 1000 * a.rep + r + off
            rng = np.random.default_rng(seed)
            th0 = (rng.standard_normal(a.J) * np.sqrt(s0sq) if arm == 'prior'
                   else TRUTH[arm])
            t = rng.uniform(0, T, a.N)
            x = rng.uniform(0, 1, a.N)
            Phi = design(t, x, kvec)
            Y = Phi @ th0 + rng.standard_normal(a.N)

            Sig = np.linalg.inv(Phi.T @ Phi + np.diag(1.0 / s0sq))
            mu = Sig @ (Phi.T @ Y)
            sd = np.sqrt(np.diag(Sig))
            rr = np.random.default_rng(seed + 500000)
            mG, CG = gbc_generator(Phi, Y, s0sq, rr, a.M, c=a.c)
            sdG = np.sqrt(np.diag(CG))

            z_ex = (th0 - mu) / sd
            z_gb = (th0 - mG) / sdG
            assert np.all(np.isfinite(z_ex)) and np.all(np.isfinite(z_gb))
            cov_ex.append((np.abs(z_ex) <= 1.959963985).astype(int).tolist())
            cov_gb.append((np.abs(z_gb) <= 1.959963985).astype(int).tolist())
            print(f"  [{arm}] rep {a.rep}.{r}: exact {sum(cov_ex[-1])}/{a.J} "
                  f" gbc {sum(cov_gb[-1])}/{a.J}", flush=True)

        out[arm] = dict(cover_exact=cov_ex, cover_gbc=cov_gb)   # raw indicators, archived

    os.makedirs(os.path.dirname(a.out) or '.', exist_ok=True)
    json.dump(out, open(a.out, 'w'))
    print("wrote", a.out, flush=True)


if __name__ == '__main__':
    main()
