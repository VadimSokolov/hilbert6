"""Baseline for the skewness numbers of the two crossover regimes: same code as anc/ns/crossover.py up to the reference chain, run at the
baseline constants (SCALE 1.5, SIGMA 0.45) for the N=25, 100-step setting, for the regime seed 404 / chain seed 77 and for other chain seeds."""
import sys, json, time
sys.path.insert(0, '.')
SCALE = float(sys.argv[1]); SIGMA = float(sys.argv[2]); tag = sys.argv[3]
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
print(tag, "signal sd %.2f noise %.2f" % (np.std(G0), SIGMA), flush=True)
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
def acf(x):
    x = x - x.mean(); m = len(x); f = np.fft.rfft(x, 2*m); a = np.fft.irfft(f*np.conj(f))[:m].real; return a/a[0]
def iact(x):
    a = acf(x); k = np.argmax(a < 0.05) if np.any(a < 0.05) else len(a)//2
    return 1+2*np.sum(a[1:max(k, 1)])
out = {}
for seed in (77, 78, 79):
    t0 = time.time(); post = mcmc(4000, 1000, seed)
    sk = np.abs(skew(post, axis=0)).mean(); ek = np.abs(kurtosis(post, axis=0)).mean()
    ia = np.mean([iact(post[:, j]) for j in range(D)])
    # skewness of a Gaussian chain with the same IACT, for the noise level
    out[seed] = dict(skew=float(sk), exkurt=float(ek), iact=float(ia), ess=float(len(post)/ia))
    print(tag, "seed %d  %.0fs  mean|skew| %.4f  mean|exkurt| %.4f  iact %.1f  ESS %.0f" % (seed, time.time()-t0, sk, ek, ia, len(post)/ia), flush=True)
json.dump(out, open('cross_base_%s.json' % tag, 'w'), indent=1)
