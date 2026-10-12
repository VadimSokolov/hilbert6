"""Particle learning with conditional sufficient statistics, local level model with unknown variances."""
import os, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
OUT = os.path.join(os.path.dirname(__file__), "..", "figures")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.family": "serif", "font.size": 9, "savefig.bbox": "tight", "pdf.fonttype": 42})
rng = np.random.default_rng(2010)
q0, r0, T, N = 0.25, 1.0, 400, 5000
x = np.cumsum(np.sqrt(q0) * rng.standard_normal(T)); y = x + np.sqrt(r0) * rng.standard_normal(T)
a0, b0 = 3.0, 1.0   # inverse Gamma priors for q and r: IG(a0, b0) with mean 0.5
def pl():
    xs = rng.standard_normal(N) * 2.0
    q = 1 / rng.gamma(a0, 1 / b0, N); r = 1 / rng.gamma(a0, 1 / b0, N)
    ssq = np.zeros(N); ssr = np.zeros(N)
    Qs, Rs, Xs = [], [], []
    for t in range(T):
        # resample with predictive weights p(y_t | x_{t-1}, q, r) = N(x_{t-1}, q + r)
        lw = -0.5 * np.log(q + r) - 0.5 * (y[t] - xs) ** 2 / (q + r)
        w = np.exp(lw - lw.max()); w /= w.sum()
        idx = rng.choice(N, N, p=w)
        xs, q, r, ssq, ssr = xs[idx], q[idx], r[idx], ssq[idx], ssr[idx]
        # propagate from p(x_t | x_{t-1}, y_t, q, r)
        v = 1 / (1 / q + 1 / r); mn = v * (xs / q + y[t] / r)
        xn = mn + np.sqrt(v) * rng.standard_normal(N)
        # update conditional sufficient statistics and redraw parameters
        ssq += (xn - xs) ** 2; ssr += (y[t] - xn) ** 2; xs = xn
        q = 1 / rng.gamma(a0 + (t + 1) / 2, 1 / (b0 + ssq / 2))
        r = 1 / rng.gamma(a0 + (t + 1) / 2, 1 / (b0 + ssr / 2))
        Qs.append(np.percentile(q, [5, 50, 95])); Rs.append(np.percentile(r, [5, 50, 95])); Xs.append(xs.copy())
    return np.array(Qs), np.array(Rs), Xs
def naive():
    xs = rng.standard_normal(N) * 2.0
    q = 1 / rng.gamma(a0, 1 / b0, N); r = 1 / rng.gamma(a0, 1 / b0, N); nd = []; Qs = []
    for t in range(T):
        xs = xs + np.sqrt(q) * rng.standard_normal(N)
        lw = -0.5 * np.log(r) - 0.5 * (y[t] - xs) ** 2 / r
        w = np.exp(lw - lw.max()); w /= w.sum(); idx = rng.choice(N, N, p=w)
        xs, q, r = xs[idx], q[idx], r[idx]; nd.append(np.unique(q).size); Qs.append(np.percentile(q, [5, 50, 95]))
    return np.array(nd), np.array(Qs)
Qs, Rs, Xs = pl(); nd, Qn = naive()
tt = np.arange(1, T + 1)
fig = plt.figure(figsize=(6.6, 4.4))
ax0 = fig.add_axes([0.07, 0.62, 0.88, 0.33])
grid = np.linspace(x.min() - 3, x.max() + 3, 220)
H = np.array([np.histogram(Xs[t], bins=grid, density=True)[0] for t in range(T)]).T
ax0.imshow(np.sqrt(H), origin="lower", aspect="auto", extent=[1, T, grid[0], grid[-1]], cmap="magma")
ax0.plot(tt, x, color="#5ff2ff", lw=0.7, label="true state $x_t$")
ax0.plot(tt, y, ".", ms=1.2, color="white", alpha=0.6, label="data $y_t$")
ax0.set_title(r"one forward pass: the particle marginals are the filtering laws $p(x_t\mid y_{1:t})$", fontsize=8.5)
ax0.legend(frameon=False, fontsize=6.5, loc="upper left", labelcolor="white"); ax0.set_xlabel("$t$")
ax1 = fig.add_axes([0.07, 0.08, 0.27, 0.34]); ax2 = fig.add_axes([0.40, 0.08, 0.27, 0.34]); ax3 = fig.add_axes([0.73, 0.08, 0.22, 0.34])
for ax, S, tr, c, lab in [(ax1, Qs, q0, "#d1495b", "$q$"), (ax2, Rs, r0, "#1b4f9c", "$r$")]:
    ax.fill_between(tt, S[:, 0], S[:, 2], color=c, alpha=0.25); ax.plot(tt, S[:, 1], color=c, lw=1.1)
    ax.axhline(tr, color="k", ls="--", lw=0.8); ax.set_title(f"particle learning: {lab}", fontsize=8); ax.set_xlabel("$t$"); ax.set_ylim(0, 1.6)
ax1.fill_between(tt, Qn[:, 0], Qn[:, 2], color="#edae49", alpha=0.35); ax1.plot(tt, Qn[:, 1], color="#edae49", lw=0.9)
ax3.semilogy(tt, nd, color="#edae49", lw=1.2); ax3.set_title("naive filter: distinct $q$", fontsize=8); ax3.set_xlabel("$t$")
plt.savefig(os.path.join(OUT, "particle_learning.pdf"), dpi=300); plt.close()
print("final PL q", Qs[-1], "r", Rs[-1], "naive distinct", nd[-1], Qn[-1])
