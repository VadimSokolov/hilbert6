"""Particle filter Monte Carlo error compounding, local level model with exact Kalman reference."""
import os, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
OUT = os.path.join(os.path.dirname(__file__), "..", "figures")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.family": "serif", "font.size": 9, "savefig.bbox": "tight", "pdf.fonttype": 42})
rng = np.random.default_rng(1993)
q, r, T = 0.1, 1.0, 200
x = np.cumsum(np.sqrt(q) * rng.standard_normal(T)); y = x + np.sqrt(r) * rng.standard_normal(T)
# exact Kalman log likelihood path
m, P, ll = 0.0, 1.0, np.zeros(T)
for t in range(T):
    Pp = P + q; S = Pp + r; ll[t] = (ll[t-1] if t else 0) - 0.5 * (np.log(2*np.pi*S) + (y[t]-m)**2 / S)
    K = Pp / S; m = m + K * (y[t] - m); P = (1 - K) * Pp
def pf(N, resample=True):
    xs = rng.standard_normal(N); logw = np.zeros(N); llh = np.zeros(T); ess = np.zeros(T); anc = np.arange(N); nd = np.zeros(T)
    lz = 0.0
    for t in range(T):
        xs = xs + np.sqrt(q) * rng.standard_normal(N)
        lw_inc = -0.5 * (np.log(2*np.pi*r) + (y[t]-xs)**2 / r)
        lwp = logw + lw_inc; mx = lwp.max()
        lz += mx + np.log(np.exp(lwp - mx).sum()) - (np.log(np.exp(logw - logw.max()).sum()) + logw.max())
        logw = lwp; w = np.exp(logw - logw.max()); w /= w.sum()
        ess[t] = 1 / np.sum(w**2); llh[t] = lz
        if resample:
            idx = rng.choice(N, N, p=w); xs = xs[idx]; anc = anc[idx]; logw = np.zeros(N)
        nd[t] = np.unique(anc).size
    return llh, ess, nd
fig, axs = plt.subplots(1, 3, figsize=(6.6, 2.3))
_, ess_nr, _ = pf(1000, resample=False); _, ess_r, nd = pf(1000, resample=True)
axs[0].semilogy(ess_nr, color="#d1495b", lw=1.1, label="no resampling")
axs[0].semilogy(ess_r, color="#1b4f9c", lw=0.8, label="bootstrap")
axs[0].set_xlabel("$t$"); axs[0].set_title("effective sample size, $N=1000$", fontsize=8); axs[0].legend(frameon=False, fontsize=6.5)
for N, c in [(100, "#edae49"), (1000, "#00798c")]:
    runs = np.array([pf(N)[0] for _ in range(60)])
    v = np.var(runs - ll, axis=0)
    print("N =", N, "least squares slope of Var(log p_N) against t:", np.polyfit(np.arange(T), v, 1)[0])
    axs[1].plot(v, color=c, lw=1.2, label=f"$N={N}$")
axs[1].set_xlabel("$t$"); axs[1].set_title(r"$\mathrm{Var}(\log\hat p_N(y_{1:t}))$", fontsize=8); axs[1].legend(frameon=False, fontsize=6.5)
axs[2].semilogy(nd, color="#7b2d8e", lw=1.2)
axs[2].set_xlabel("$t$"); axs[2].set_title("distinct time zero ancestors", fontsize=8)
save = lambda n: (plt.savefig(os.path.join(OUT, n + ".pdf")), plt.close())
save("pf_errors")
print("done", ess_nr[-1], nd[-1])
print("ESS without resampling at t = 10, 20, 30, 200:", np.round(ess_nr[[9, 19, 29, 199]], 1), "; minimum ESS with resampling:", round(ess_r.min(), 1), "; distinct ancestors at t = 1, 10, 50, 200:", nd[[0, 9, 49, 199]])
