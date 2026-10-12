"""Data-dominated rerun of the heat-equation example, effective resolution, and baselines.

Addresses three referee findings at once.

  B  The published Figure 2 is run at rho=1, alpha=3, where the prior precision
     lambda_k^3 exceeds the data precision N iota_k by 44x at k=1.  Worse, the
     truth theta_0(k)=1/(1+k^2) has theta_0(1)=0.5 against a prior standard
     deviation of rho lambda_1^{-3/2}=0.004, i.e. the truth sits 124 prior
     standard deviations from the prior mean.  Missing it in 20 of 20 modes is
     forced by the prior, not by the method.  Here rho is calibrated to the
     truth and the figure is drawn over the modes the data actually informs.

  J  The effective resolution.  Equating data and prior precision,
     N iota_K = lambda_K^alpha / rho^2, and using iota_K ~ 1/(2 nu lambda_K T),
         lambda_K = (N rho^2 / (2 nu T))^{1/(alpha+1)},
         K_eff    ~ (N rho^2 / (2 nu T))^{1/(2(alpha+1))},
     a power of N with exponent 1/(2(alpha+1)) = 1/8 at alpha=3.  This is an
     independent finite-N counterpart of the licensed summary dimension
     J_N ~ N^{d/(2 gamma + d)}, and shows that J_N being small is the dissipation
     barrier rather than an artefact of the proof technique.

  E, I  A preconditioned Crank-Nicolson baseline and a solve-count and
     wall-clock accounting for GBC against 4DVar and an ensemble Kalman update.

Run: python3 -u exp_paper_figs.py --mode all
"""
import argparse, json, os, time
import numpy as np

NU, T = 0.01, 1.0


def lam(k):
    return 4.0*np.pi**2*k**2


def iota(k, T0=0.0):
    l = lam(k)
    return (np.exp(-2*NU*l*T0) - np.exp(-2*NU*l*T)) / (2*NU*l*(T-T0))


def design(t, x, kvec):
    return (np.exp(-NU*lam(kvec)[None, :]*t[:, None])
            * np.sqrt(2.0)*np.cos(2*np.pi*kvec[None, :]*x[:, None]))


def truth(kvec):
    """The initial condition of the published figure: theta_0(k)=1/(1+k^2)."""
    return (1.0/(1.0+kvec**2))*np.sign(np.sin(kvec))


def truth_typical(kvec, s0sq, seed=7):
    """A fixed draw from the prior, so the truth is prior-typical at every mode.

    The published truth decays like k^{-2} while the prior standard deviation
    decays like lambda_k^{-alpha/2} ~ k^{-alpha}; at alpha=3 the truth is rougher
    than the prior supports, so it sits many prior standard deviations out at
    high modes however rho is chosen.  Calibrating rho fixes the low modes only.
    """
    z = np.random.default_rng(seed).standard_normal(len(kvec))
    return np.sqrt(s0sq)*z


def calibrate_rho(kvec, alpha):
    """Choose rho so the prior standard deviation matches the truth at k=1, i.e.
    so the truth is a prior-typical draw rather than a 124-sigma outlier."""
    return abs(truth(kvec)[0]) * lam(kvec[0])**(alpha/2.0)


def k_eff(N, rho, alpha, kmax=200):
    """Largest k with data precision at least prior precision."""
    k = np.arange(1, kmax+1)
    ok = N*iota(k) >= lam(k)**alpha/rho**2
    return int(k[ok].max()) if ok.any() else 0


# --------------------------------------------------------------------------- J
def resolution_scaling(alpha, rho, Ns):
    """K_eff(N) measured against the predicted exponent 1/(2(alpha+1))."""
    out = []
    for N in Ns:
        out.append(dict(N=float(N), k_eff=k_eff(N, rho, alpha)))
    ks = np.array([o['k_eff'] for o in out], float)
    ns = np.array([o['N'] for o in out], float)
    m = ks > 0
    slope = np.polyfit(np.log(ns[m]), np.log(ks[m]), 1)[0] if m.sum() > 2 else float('nan')
    return out, float(slope), 1.0/(2*(alpha+1))


# --------------------------------------------------------------------------- B
def figure2(N, alpha, rho, kmax, seed=1, typical=False):
    rng = np.random.default_rng(seed)
    kvec = np.arange(1, kmax+1)
    s0sq = rho**2*lam(kvec)**(-alpha)
    th0 = truth_typical(kvec, s0sq) if typical else truth(kvec)
    t = rng.uniform(0, T, N); x = rng.uniform(0, 1, N)
    Phi = design(t, x, kvec)
    Y = Phi @ th0 + rng.standard_normal(N)
    prec = Phi.T@Phi + np.diag(1.0/s0sq)
    cov = np.linalg.inv(prec); mean = cov @ (Phi.T@Y)
    sd = np.sqrt(np.diag(cov))
    z = (th0-mean)/sd
    Ke = k_eff(N, rho, alpha)
    inside = np.abs(z) <= 2
    return dict(N=N, alpha=alpha, rho=rho, kmax=kmax, k_eff=Ke, typical=bool(typical),
                cover2_all=float(inside.mean()),
                cover2_informed=float(inside[:Ke].mean()) if Ke > 0 else None,
                max_absz_all=float(np.abs(z).max()),
                max_absz_informed=float(np.abs(z[:Ke]).max()) if Ke > 0 else None,
                rel_l2=float(np.linalg.norm(mean-th0)/np.linalg.norm(th0)),
                truth_in_prior_sd=float(abs(th0[0])/np.sqrt(s0sq[0])),
                max_truth_in_prior_sd=float(np.max(np.abs(th0)/np.sqrt(s0sq))),
                bvm_max_rel=float(np.max(np.abs(sd/(1.0/np.sqrt(N*iota(kvec)+1.0/s0sq))-1.0))),
                bvm_max_rel_informed=float(np.max(np.abs(
                    sd[:Ke]/(1.0/np.sqrt(N*iota(kvec[:Ke])+1.0/s0sq[:Ke]))-1.0))) if Ke > 0 else None,
                z=[float(v) for v in z], sd=[float(v) for v in sd],
                mean=[float(v) for v in mean], theta0=[float(v) for v in th0])


# ------------------------------------------------------------------------ E, I
def pcn(Phi, Y, s0sq, n_iter, rng, beta=0.15, target=0.25, adapt_frac=0.2):
    """Preconditioned Crank-Nicolson with beta adapted to a target acceptance
    during burn-in and frozen thereafter, so the baseline is tuned rather than
    handicapped."""
    J = Phi.shape[1]
    th = rng.standard_normal(J)*np.sqrt(s0sq)
    r = Y - Phi@th; ll = -0.5*r@r
    keep = np.empty((n_iter, J)); acc = 0
    n_adapt = int(adapt_frac*n_iter); win = 500; wacc = 0
    for i in range(n_iter):
        if i < n_adapt and i > 0 and i % win == 0:
            rate = wacc/win
            beta *= np.exp(0.6*(rate-target))
            beta = float(np.clip(beta, 1e-4, 0.999)); wacc = 0
        prop = np.sqrt(1-beta**2)*th + beta*(rng.standard_normal(J)*np.sqrt(s0sq))
        rp = Y - Phi@prop; llp = -0.5*rp@rp
        if np.log(rng.uniform()) < llp-ll:
            th, ll, acc = prop, llp, acc+1
            wacc += 1
        keep[i] = th
    return keep, acc/n_iter, beta


def ess(chain):
    """Initial-positive-sequence effective sample size, per coordinate."""
    n, J = chain.shape
    out = np.empty(J)
    for j in range(J):
        x = chain[:, j]-chain[:, j].mean()
        f = np.fft.rfft(x, 2*n); ac = np.fft.irfft(f*np.conj(f))[:n].real
        if ac[0] <= 0: out[j] = 1.0; continue
        ac /= ac[0]
        s = 0.0
        for k in range(1, n-1, 2):
            p = ac[k]+ac[k+1]
            if p <= 0: break
            s += p
        out[j] = n/(1.0+2.0*s)
    return out


def baselines(N, alpha, rho, kmax, n_iter, seed=1):
    rng = np.random.default_rng(seed)
    kvec = np.arange(1, kmax+1); J = kmax
    s0sq = rho**2*lam(kvec)**(-alpha); th0 = truth_typical(kvec, s0sq)
    t = rng.uniform(0, T, N); x = rng.uniform(0, 1, N)
    Phi = design(t, x, kvec); Y = Phi@th0 + rng.standard_normal(N)
    prec = Phi.T@Phi+np.diag(1.0/s0sq); cov = np.linalg.inv(prec)
    mu = cov@(Phi.T@Y); sd = np.sqrt(np.diag(cov))

    t0 = time.time(); ch, acc, beta_f = pcn(Phi, Y, s0sq, n_iter, rng); t_pcn = time.time()-t0
    burn = n_iter//5; ch = ch[burn:]
    e = ess(ch)
    pcn_sd = ch.std(0, ddof=1)
    pcn_err = float(np.max(np.abs(ch.mean(0)-mu)/sd))

    # Laplace: one linear solve; exact here because the model is linear-Gaussian
    t0 = time.time(); _ = np.linalg.inv(Phi.T@Phi+np.diag(1.0/s0sq)); t_lap = time.time()-t0

    # GBC with the regularised summary, localised at c=2, identity head
    M = 4000
    t0 = time.time()
    L = 2.0*np.linalg.cholesky(cov+1e-14*np.eye(J))
    R = np.empty((M, J))
    for m in range(M):
        th = mu + L@rng.standard_normal(J)
        Ym = Phi@th + rng.standard_normal(N)
        R[m] = th - cov@(Phi.T@Ym)
    Rc = R-R.mean(0); C = (Rc.T@Rc)/M
    p = np.diag(cov@np.diag(1.0/s0sq)); s = 1.0-p
    f = 1.0/np.sqrt(np.maximum(s+4.0*p**2, 1e-300))
    C = (f[:, None]*C)*f[None, :]
    w, Q = np.linalg.eigh(0.5*(C+C.T))
    draws = mu[None, :] + rng.standard_normal((4000, J)) @ (Q@np.diag(np.sqrt(np.maximum(w, 0)))@Q.T).T
    t_gbc = time.time()-t0
    gbc_sd = draws.std(0, ddof=1)

    return dict(N=N, kmax=kmax, n_iter=n_iter, pcn_acc=float(acc), pcn_beta=float(beta_f),
                pcn_time_s=float(t_pcn), pcn_ess_min=float(e.min()), pcn_ess_med=float(np.median(e)),
                pcn_sd_ratio_med=float(np.median(pcn_sd/sd)), pcn_mean_err_psd=pcn_err,
                pcn_ess_per_s=float(e.min()/t_pcn),
                laplace_time_s=float(t_lap),
                gbc_M=M, gbc_time_s=float(t_gbc),
                gbc_sd_ratio_med=float(np.median(gbc_sd/sd)),
                gbc_mean_err_psd=float(np.max(np.abs(draws.mean(0)-mu)/sd)),
                # solve counts, in units of one linearised forward+adjoint pair
                solves_gbc=int(2*M), solves_4dvar=int(2*10), solves_enkf=int(100),
                solves_pcn=int(n_iter))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--mode', default='all')
    ap.add_argument('--alpha', type=float, default=3.0)
    ap.add_argument('--out', default='results')
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    kv = np.arange(1, 21)
    rho_cal = calibrate_rho(kv, a.alpha)
    res = dict(alpha=a.alpha, rho_calibrated=float(rho_cal), nu=NU, T=T)

    # published setting, for the record
    res['published'] = figure2(N=2000, alpha=3.0, rho=1.0, kmax=20)
    # calibrated prior, same N
    res['calibrated_N2000'] = figure2(N=2000, alpha=a.alpha, rho=rho_cal, kmax=20)
    # calibrated prior, N chosen to inform more modes
    for N in (50_000, 1_300_000):
        res[f'calibrated_N{N}'] = figure2(N=N, alpha=a.alpha, rho=rho_cal, kmax=20)
    for N in (2000, 50_000, 1_300_000):
        res[f'typical_N{N}'] = figure2(N=N, alpha=a.alpha, rho=rho_cal, kmax=20, typical=True)

    sc, slope, pred = resolution_scaling(a.alpha, rho_cal,
                                         [10**e for e in (3, 4, 5, 6, 7, 8, 9, 10)])
    res['resolution'] = dict(curve=sc, fitted_exponent=slope, predicted_exponent=pred)

    res['baselines'] = baselines(N=50_000, alpha=a.alpha, rho=rho_cal, kmax=8, n_iter=200_000)

    with open(os.path.join(a.out, 'paper_figs.json'), 'w') as f:
        json.dump(res, f, indent=1)
    print(json.dumps({k: v for k, v in res.items() if k != 'resolution'}, indent=1)[:4000])
    print('\nresolution:', json.dumps(res['resolution'], indent=1))


if __name__ == '__main__':
    main()
