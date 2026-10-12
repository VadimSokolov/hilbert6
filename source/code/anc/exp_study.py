"""Coverage study and error-versus-cost curves for the heat-equation example.

Produces the two things a JUQ experiments section needs and the manuscript
lacked: calibration of the GBC posterior over independent replicates, and an
accuracy-against-compute comparison with a tuned dimension-robust sampler.

  coverage  R independent replicates.  Each draws theta_0 from the prior, draws
            data, and records whether theta_0 lies inside the 95% interval of
            (a) the exact conjugate posterior, a control that must come out at
            the nominal rate, and (b) the GBC posterior built with the
            regularised summary of rem:reg, localised per alg:loc.  Reported
            over the data-informed modes k <= K_eff and over all modes.

  cost      GBC error against M, and pCN error against iteration count, both in
            posterior standard deviations, with wall-clock.  GBC error floors at
            its approximation bias; pCN error decays like ESS^{-1/2} without a
            floor.  The crossover is the honest comparison.

Run: python3 -u exp_study.py --reps 200 --out results
"""
import argparse, json, os, time
import numpy as np

NU, T, ALPHA = 0.01, 1.0, 3.0


def lam(k):  return 4.0*np.pi**2*k**2
def iota(k): l = lam(k); return (1.0-np.exp(-2*NU*l*T))/(2*NU*l*T)


def design(t, x, kvec):
    return (np.exp(-NU*lam(kvec)[None, :]*t[:, None])
            * np.sqrt(2.0)*np.cos(2*np.pi*kvec[None, :]*x[:, None]))


def k_eff(N, s0sq, kvec):
    ok = N*iota(kvec) >= 1.0/s0sq
    return int(ok.sum())


def gbc_draws(Phi, Y, s0sq, rng, M, c=2.0, n_draw=4000):
    """Algorithm 1 with the regularised summary (rem:reg) and alg:loc step 1."""
    J = Phi.shape[1]
    cov = np.linalg.inv(Phi.T@Phi + np.diag(1.0/s0sq))
    mu = cov @ (Phi.T@Y)
    L = c*np.linalg.cholesky(cov + 1e-15*np.eye(J))
    R = np.empty((M, J))
    for m in range(M):
        th = mu + L@rng.standard_normal(J)
        Ym = Phi@th + rng.standard_normal(Phi.shape[0])
        R[m] = th - cov@(Phi.T@Ym)
    Rc = R - R.mean(0)
    C = (Rc.T@Rc)/M
    p = np.diag(cov@np.diag(1.0/s0sq)); s = 1.0-p
    f = 1.0/np.sqrt(np.maximum(s + c*c*p*p, 1e-300))
    C = (f[:, None]*C)*f[None, :]
    w, Q = np.linalg.eigh(0.5*(C+C.T))
    H = Q@np.diag(np.sqrt(np.maximum(w, 0.0)))@Q.T
    return mu[None, :] + rng.standard_normal((n_draw, J))@H.T, mu, cov


def pcn(Phi, Y, s0sq, n_iter, rng, beta=0.1, target=0.25, adapt_frac=0.2):
    J = Phi.shape[1]
    th = rng.standard_normal(J)*np.sqrt(s0sq)
    r = Y-Phi@th; ll = -0.5*r@r
    keep = np.empty((n_iter, J)); acc = 0; n_ad = int(adapt_frac*n_iter); win = 500; wa = 0
    for i in range(n_iter):
        if i < n_ad and i > 0 and i % win == 0:
            beta = float(np.clip(beta*np.exp(0.6*(wa/win-target)), 1e-4, .999)); wa = 0
        prop = np.sqrt(1-beta**2)*th + beta*(rng.standard_normal(J)*np.sqrt(s0sq))
        rp = Y-Phi@prop; llp = -0.5*rp@rp
        if np.log(rng.uniform()) < llp-ll:
            th, ll, acc, wa = prop, llp, acc+1, wa+1
        keep[i] = th
    return keep, acc/n_iter, beta


def ess1(x):
    n = len(x); x = x-x.mean()
    f = np.fft.rfft(x, 2*n); ac = np.fft.irfft(f*np.conj(f))[:n].real
    if ac[0] <= 0: return 1.0
    ac /= ac[0]; s = 0.0
    for k in range(1, n-1, 2):
        p = ac[k]+ac[k+1]
        if p <= 0: break
        s += p
    return n/(1.0+2.0*s)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--reps', type=int, default=200)
    ap.add_argument('--N', type=int, default=50_000)
    ap.add_argument('--J', type=int, default=8)
    ap.add_argument('--M', type=int, default=4000)
    ap.add_argument('--out', default='results')
    a = ap.parse_args()
    kvec = np.arange(1, a.J+1)
    rho = 0.5*lam(np.array([1]))[0]**(ALPHA/2.0)      # prior sd at k=1 equals 0.5
    s0sq = rho**2*lam(kvec)**(-ALPHA)
    Ke = k_eff(a.N, s0sq, kvec)

    # ---------------- coverage over replicates ----------------
    hit_ex = np.zeros(a.J); hit_gb = np.zeros(a.J); zst = []
    t0 = time.time()
    for r in range(a.reps):
        rng = np.random.default_rng(90000+r)
        th0 = np.sqrt(s0sq)*rng.standard_normal(a.J)
        t = rng.uniform(0, T, a.N); x = rng.uniform(0, 1, a.N)
        Phi = design(t, x, kvec); Y = Phi@th0 + rng.standard_normal(a.N)
        d, mu, cov = gbc_draws(Phi, Y, s0sq, rng, a.M)
        sd = np.sqrt(np.diag(cov))
        hit_ex += (np.abs(th0-mu) <= 1.959964*sd)
        lo, hi = np.percentile(d, [2.5, 97.5], axis=0)
        hit_gb += ((th0 >= lo) & (th0 <= hi))
        zst.append(((th0-mu)/sd).tolist())
    t_cov = time.time()-t0
    cov_res = dict(reps=a.reps, N=a.N, J=a.J, M=a.M, k_eff=Ke, seconds=t_cov,
                   exact_by_mode=(hit_ex/a.reps).tolist(),
                   gbc_by_mode=(hit_gb/a.reps).tolist(),
                   exact_informed=float(hit_ex[:Ke].sum()/(a.reps*Ke)),
                   gbc_informed=float(hit_gb[:Ke].sum()/(a.reps*Ke)),
                   exact_all=float(hit_ex.sum()/(a.reps*a.J)),
                   gbc_all=float(hit_gb.sum()/(a.reps*a.J)))

    # ---------------- error against compute ----------------
    rng = np.random.default_rng(11)
    th0 = np.sqrt(s0sq)*rng.standard_normal(a.J)
    t = rng.uniform(0, T, a.N); x = rng.uniform(0, 1, a.N)
    Phi = design(t, x, kvec); Y = Phi@th0 + rng.standard_normal(a.N)
    cov = np.linalg.inv(Phi.T@Phi+np.diag(1.0/s0sq)); mu = cov@(Phi.T@Y)
    sd = np.sqrt(np.diag(cov))

    gbc_curve = []
    for M in (250, 500, 1000, 2000, 4000, 8000, 16000, 32000):
        rr = np.random.default_rng(5000+M)
        t0 = time.time(); d, _, _ = gbc_draws(Phi, Y, s0sq, rr, M); el = time.time()-t0
        gbc_curve.append(dict(M=M, seconds=el, solves=2*M,
                              mean_err_psd=float(np.max(np.abs(d.mean(0)-mu)/sd)),
                              sd_ratio_med=float(np.median(d.std(0, ddof=1)/sd))))
    pcn_curve = []
    for it in (5_000, 20_000, 80_000, 320_000, 1_280_000):
        rr = np.random.default_rng(7000+it)
        t0 = time.time(); ch, acc, bt = pcn(Phi, Y, s0sq, it, rr); el = time.time()-t0
        ch = ch[it//5:]
        e = float(min(ess1(ch[:, j]) for j in range(a.J)))
        pcn_curve.append(dict(iters=it, seconds=el, solves=it, acc=float(acc), beta=float(bt),
                              ess_min=e,
                              mean_err_psd=float(np.max(np.abs(ch.mean(0)-mu)/sd)),
                              sd_ratio_med=float(np.median(ch.std(0, ddof=1)/sd))))

    os.makedirs(a.out, exist_ok=True)
    out = dict(rho=float(rho), alpha=ALPHA, nu=NU, T=T, k_eff=Ke,
               coverage=cov_res, gbc_curve=gbc_curve, pcn_curve=pcn_curve)
    with open(os.path.join(a.out, 'study.json'), 'w') as f:
        json.dump(out, f, indent=1)
    print(json.dumps(out, indent=1)[:2500])


if __name__ == '__main__':
    main()
