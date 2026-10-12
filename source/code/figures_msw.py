"""Markov switching filter via a particle representation with latent regime z."""
import os, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
OUT = os.path.join(os.path.dirname(__file__), "..", "figures")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.family": "serif", "font.size": 9, "savefig.bbox": "tight", "pdf.fonttype": 42})
rng = np.random.default_rng(7)
dt, T = 0.05, 600
mu = np.array([1.0, -1.0]); sig = np.array([0.6, 1.6]); Qrate = np.array([[-0.15, 0.15], [0.25, -0.25]])
Pz = np.eye(2) + Qrate * dt
z = np.zeros(T, int); x = np.zeros(T); y = np.zeros(T)
for t in range(1, T):
    z[t] = rng.choice(2, p=Pz[z[t-1]])
    x[t] = x[t-1] + mu[z[t]] * dt + sig[z[t]] * np.sqrt(dt) * rng.standard_normal()
    y[t] = x[t] + 0.3 * rng.standard_normal()
N = 4000
X = np.zeros(N); Z = rng.choice(2, N); pz = np.zeros(T); Xs = []
for t in range(1, T):
    u = rng.random(N); Z = np.where(u < Pz[Z, 1 - Z], 1 - Z, Z)          # each particle carries its own regime chain
    X = X + mu[Z] * dt + sig[Z] * np.sqrt(dt) * rng.standard_normal(N)   # regime dependent motion
    lw = -0.5 * (y[t] - X) ** 2 / 0.09; w = np.exp(lw - lw.max()); w /= w.sum()   # weights A_i
    pz[t] = w[Z == 1].sum()                                              # V_t(R x {1}) / V_t(1)
    idx = rng.choice(N, N, p=w); X, Z = X[idx], Z[idx]; Xs.append(X.copy())
tt = np.arange(T) * dt
fig, axs = plt.subplots(2, 1, figsize=(6.0, 3.8), sharex=True, gridspec_kw={"height_ratios": [1.6, 1]})
grid = np.linspace(x.min() - 1.5, x.max() + 1.5, 160)
H = np.array([np.histogram(v, bins=grid, density=True)[0] for v in Xs]).T
axs[0].imshow(np.sqrt(H), origin="lower", aspect="auto", extent=[tt[1], tt[-1], grid[0], grid[-1]], cmap="viridis")
axs[0].plot(tt, x, color="#ff6b6b", lw=0.8, label="true state")
axs[0].set_title(r"filtering law of $x_t$ from particles carrying $(X_i, Z_i)$", fontsize=8.5); axs[0].legend(frameon=False, fontsize=6.5, labelcolor="white")
axs[1].fill_between(tt, 0, z, step="mid", color="#edae49", alpha=0.45, label="true regime $z_t=1$")
axs[1].plot(tt, pz, color="#7b2d8e", lw=1.1, label=r"$P(z_t=1\mid y_{1:t})$")
axs[1].set_ylim(-0.05, 1.05); axs[1].set_xlabel("time"); axs[1].legend(frameon=False, fontsize=6.5, loc="upper left")
plt.savefig(os.path.join(OUT, "markov_switching.pdf"), dpi=300); plt.close()
acc = np.mean((pz[1:] > 0.5) == (z[1:] == 1)); print("regime classification accuracy", acc)
print("switch times", (np.where(np.diff(z) != 0)[0] + 1) * dt, "; misclassified steps", int(np.sum((pz[1:] > 0.5) != (z[1:] == 1))), "of", T - 1)
for s_ in np.where(np.diff(z) != 0)[0] + 1:
    k_ = s_
    while k_ < T - 1 and (pz[k_] > 0.5) != (z[k_] == 1): k_ += 1
    print("switch at time", round(s_ * dt, 2), ": the filter agrees with the new regime after", k_ - s_, "steps =", round((k_ - s_) * dt, 2), "time units")
