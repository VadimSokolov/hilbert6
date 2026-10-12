"""The two further regimes of the Navier Stokes experiment, with the corrected generator.

Copy of anc/ns/crossover.py statement by statement up to the scoring of the identity
head (same seeds, same order of random draws, so the recorded crossover2.json and
crossover3.json are reproduced), then, on the SAME training draws and the SAME
resampling indices:
  (a) the identity head with the residuals centered at their sample mean
      (Theorem locbias (ii));
  (b) centered and rescaled by (s_j + c^2 p_j^2)^(-1/2) in the eigenbasis of
      P = Sigma_N Sigma_0^{-1} (Theorem locbias (iii)), which is the generator of
      Algorithm loc and of the row "spread rescaled" of the main table;
  (c) the Monte Carlo standard error of the reference chain, by the estimator of
      mcmc_error.py (autocorrelation summed up to the first lag below 0.05);
  (d) the eigenvalues of P (prior fractions) and the proxy max|theta_0|/nu;
  (e) the resampling noise of the scores: 20 further resampling seeds for the
      generators and 20 further Laplace samples.
Usage: python regimes.py amplitude|posterior   -> regimes_<regime>.json
"""
import sys, json, time
REGIME = sys.argv[1] if len(sys.argv) > 1 else 'posterior'
SIGMA, SCALE = {'amplitude': (0.45, 2.0), 'posterior': (1.30, 3.0)}[REGIME]
import numpy as np
from ns_solver import NS2D, MODES, theta_to_w0h
from scipy.stats import skew, kurtosis
D = len(MODES); lam = np.array([4*np.pi**2*(kx**2+ky**2) for kx, ky in MODES], float)
NU, T, NSTEPS, N = 0.005, 1.0, 100, 25
ns = NS2D(n=24, nu=NU, T=T, nsteps=NSTEPS); prior_sd = SCALE*(lam/lam[0])**(-1.0)
r = np.random.default_rng(404)
th0 = r.normal(size=D)*prior_sd
it = r.integers(0, NSTEPS+1, N); ix = r.integers(0, ns.n, N); iy = r.integers(0, ns.n, N)
def G(th):
    s, _ = ns.solve(theta_to_w0h(th, ns)); U = np.empty((len(s), ns.n, ns.n)); V = np.empty_like(U)
    for i, wh in enumerate(s): U[i], V[i] = ns.velocity(wh)
    return np.concatenate([U[it, ix, iy], V[it, ix, iy]])
G0 = G(th0); Y = G0 + SIGMA*r.normal(size=2*N)
res = {'regime': REGIME, 'SIGMA': SIGMA, 'SCALE': SCALE, 'signal_sd': float(np.std(G0)),
       'max_abs_theta0_over_nu': float(np.abs(th0).max()/NU)}
print(REGIME, "signal sd %.3f noise %.2f  max|th0|/nu %.1f" % (np.std(G0), SIGMA, np.abs(th0).max()/NU), flush=True)
def jac(th, eps=1e-4):
    b = G(th); Jm = np.empty((len(b), D))
    for j in range(D):
        tp = th.copy(); tp[j] += eps; Jm[:, j] = (G(tp)-b)/eps
    return b, Jm
th = np.zeros(D)
for _ in range(12):
    g, Jm = jac(th); H = Jm.T@Jm/SIGMA**2 + np.diag(1/prior_sd**2)
    th = th + np.linalg.solve(H, Jm.T@(Y-g)/SIGMA**2 - th/prior_sd**2)
th_map = th; g_map, Jm = jac(th_map); H = Jm.T@Jm/SIGMA**2 + np.diag(1/prior_sd**2); Cov = np.linalg.inv(H)
Lc = np.linalg.cholesky(Cov)
t0 = time.time()
def mcmc(nit, burn, seed):
    q = np.random.default_rng(seed)
    ll = lambda t: -0.5*np.sum((Y-G(t))**2)/SIGMA**2 - 0.5*np.sum((t/prior_sd)**2)
    t = th_map.copy(); lp = ll(t); s = 1.0; acc = 0; out = []
    for i in range(nit):
        p = t + s*(Lc@q.normal(size=D)); lpp = ll(p)
        if np.log(q.uniform()) < lpp-lp: t, lp = p, lpp; acc += 1
        if i % 200 == 199: s *= np.exp(acc/200-0.30); acc = 0
        if i >= burn: out.append(t.copy())
    return np.array(out)
post = mcmc(4000, 1000, 77)
print("mcmc %.0fs skew %.4f exkurt %.4f" % (time.time()-t0, np.abs(skew(post, axis=0)).mean(), np.abs(kurtosis(post, axis=0)).mean()), flush=True)
def w1(a, b):
    q = np.linspace(0.005, 0.995, 199); return np.mean(np.abs(np.quantile(a, q)-np.quantile(b, q)))
def score(s): return float(np.mean([w1(s[:, j], post[:, j])/np.std(post[:, j]) for j in range(D)]))
lap = th_map + (Lc@r.normal(size=(D, 8000))).T
res.update({'laplace': score(lap), 'skew': float(np.abs(skew(post, axis=0)).mean()),
            'exkurt': float(np.abs(kurtosis(post, axis=0)).mean())})
print("Laplace %.4f" % res['laplace'], flush=True)
Fi = np.linalg.inv(Jm.T@Jm/SIGMA**2 + np.diag(1/prior_sd**2))
summ = lambda Yv: th_map + Fi@(Jm.T@(Yv-g_map)/SIGMA**2 - th_map/prior_sd**2)
s_obs = summ(Y); M = 1200
def acf(x):
    x = x - x.mean(); m = len(x); f = np.fft.rfft(x, 2*m); a = np.fft.irfft(f*np.conj(f))[:m].real; return a/a[0]
def iact_cut(rr, thresh=0.05):
    k = int(np.argmax(rr[1:] < thresh)) + 1; return 1.0 + 2.0*rr[1:k].sum()
iact = [iact_cut(acf(post[:, j])) for j in range(D)]
se = [float(np.sqrt(t/len(post))) for t in iact]
res.update({'mc_se_over_psd': se, 'mc_se_mean': float(np.mean(se)), 'iact_mean': float(np.mean(iact)),
            'n_chain': int(len(post))})
P = Cov@np.diag(1/prior_sd**2); ev, V = np.linalg.eig(P); ev = ev.real; V = V.real
res['P_eigenvalues'] = [float(x) for x in np.sort(ev)]
c = 2.0
TH = th_map + c*(Lc@r.normal(size=(D, M))).T
GG = np.array([G(TH[m]) for m in range(M)])
S = np.array([summ(GG[m] + SIGMA*r.normal(size=2*N)) for m in range(M)])
infl = np.sqrt((1-ev) + c**2*ev**2); Dfl = V@np.diag(1/infl)@np.linalg.inv(V)
for lin in [False, True]:
    if lin:
        X = np.hstack([np.ones((M, 1)), S]); B = np.linalg.lstsq(X, TH, rcond=None)[0]
        R = TH - X@B; ctr = np.r_[1, s_obs]@B
    else:
        R = TH - S; ctr = s_obs
    C = np.cov(R.T); L = np.linalg.cholesky(C + 1e-10*np.eye(D)); W = np.linalg.solve(L, R.T).T
    idx = r.integers(0, M, 8000)
    res[f'gbc_c{c}_{"lin" if lin else "id"}'] = score(ctr + (L@W[idx].T).T)
    if not lin:
        Rb = R[idx]
        res['check_LW_equals_R'] = float(np.max(np.abs((L@W[idx].T).T - Rb)))
        mu = R.mean(0)
        res['id_centered'] = score(s_obs + (Rb - mu))
        res['id_centered_rescaled'] = score(s_obs + (Dfl@(Rb - mu).T).T)
        res['id_analytic_centered_rescaled'] = score(s_obs + (Dfl@(Rb - P@th_map).T).T)
        noise = {'uncorrected': [], 'centered': [], 'centered_rescaled': [], 'laplace': []}
        for sd in range(2000, 2020):
            q = np.random.default_rng(sd); ii = q.integers(0, M, 8000)
            noise['uncorrected'].append(score(s_obs + R[ii]))
            noise['centered'].append(score(s_obs + (R[ii] - mu)))
            noise['centered_rescaled'].append(score(s_obs + (Dfl@(R[ii] - mu).T).T))
            noise['laplace'].append(score(th_map + (Lc@q.normal(size=(D, 8000))).T))
        for k, v in noise.items():
            res['resample_'+k+'_mean'] = float(np.mean(v)); res['resample_'+k+'_sd'] = float(np.std(v, ddof=1))
    print("c=%.1f %s  %.4f" % (c, 'lin' if lin else 'id', res[f'gbc_c{c}_{"lin" if lin else "id"}']), flush=True)
print(json.dumps(res, indent=1))
json.dump(res, open('regimes_%s.json' % REGIME, 'w'), indent=1)
