"""Colour figures for the ergodic theory, types and Lanford window material."""
import os, numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from scipy.special import gammaln
OUT = os.path.join(os.path.dirname(__file__), "..", "figures")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.family": "serif", "font.size": 9, "savefig.bbox": "tight", "pdf.fonttype": 42})
rng = np.random.default_rng(2026)
def save(n): plt.savefig(os.path.join(OUT, n + ".pdf"), dpi=300); plt.close()

# 1. Arnold cat map on a colour image: mixing and recurrence on a 101 x 101 grid
N = 101
yy, xx = np.mgrid[0:N, 0:N] / N
r = np.sqrt((xx - 0.5) ** 2 + (yy - 0.5) ** 2)
img = plt.cm.turbo((np.sin(14 * r) * 0.5 + 0.5) * (r < 0.45) + 0.0 * (r >= 0.45))[:, :, :3]
img[r >= 0.45] = np.array([0.06, 0.1, 0.18])
img[(np.abs(xx - 0.5) < 0.03) & (r < 0.45)] = [1, 1, 1]
I, J = np.mgrid[0:N, 0:N]
def cat(a):
    out = np.empty_like(a); out[(2 * I + J) % N, (I + J) % N] = a[I, J]; return out
# period
b = cat(img); per = 1
while not np.allclose(b, img): b = cat(b); per += 1
shots = {0: img}; b = img.copy()
for n in range(1, per + 1):
    b = cat(b)
    if n in (1, 2, 5, per // 2, per): shots[n] = b.copy()
fig, axs = plt.subplots(1, 6, figsize=(6.4, 1.35))
for ax, (n, im) in zip(axs, sorted(shots.items())):
    ax.imshow(im, interpolation="nearest"); ax.set_xticks([]); ax.set_yticks([]); ax.set_title(f"$n={n}$", fontsize=7)
fig.suptitle(f"Arnold's cat map on a ${N}\\times{N}$ grid: mixing, then exact recurrence at $n={per}$", fontsize=8, y=1.06)
save("cat_map"); print("cat period", per)

# 2. Birkhoff averages
n = np.arange(1, 100001)
alpha = (np.sqrt(5) - 1) / 2
x = (0.1 + n * alpha) % 1
rot = np.cumsum(np.cos(2 * np.pi * x)) / n
# In floating point x -> 2x mod 1 sends a start drawn by rng (a multiple of 2^-53) to 0 in at most 53 steps, so the orbit is computed exactly as the shift of the
# binary digits of a random start x_0 = 0.b_1 b_2 ... with fair coin flips b_j: x_k = 0.b_{k+1} b_{k+2} ... (52 digits).
# The first n.size digits come from rng, which keeps the random stream of the later figures unchanged.
bits = np.concatenate([rng.random(n.size) < 0.5, np.random.default_rng(7).random(52) < 0.5]).astype(float)
xs = np.lib.stride_tricks.sliding_window_view(bits, 52)[1:n.size + 1] @ 2.0 ** -np.arange(1, 53)
dbl = np.cumsum(np.cos(2 * np.pi * xs)) / n
z = rng.random(); comp = np.where(z < 0.5, 0.25, 0.75)
fig, ax = plt.subplots(figsize=(4.6, 2.8))
ax.loglog(n, np.abs(rot), color="#1b4f9c", lw=0.8, label="irrational rotation (uniquely ergodic)")
ax.loglog(n, np.abs(dbl), color="#d1495b", lw=0.8, label="doubling map (mixing)")
ax.loglog(n, 1 / n, color="#1b4f9c", ls=":", lw=0.8); ax.loglog(n, 1 / np.sqrt(n), color="#d1495b", ls=":", lw=0.8)
ax.set_xlabel("$n$"); ax.set_ylabel(r"$|A_n f - \int f|$, $f=\cos 2\pi x$"); ax.legend(frameon=False, fontsize=7)
ax.set_title("Birkhoff averages: rates $1/n$ and $1/\\sqrt{n}$", fontsize=9)
save("birkhoff")

# 3. Chirikov standard map
K = 0.971635
fig, ax = plt.subplots(figsize=(4.4, 4.4)); ax.set_facecolor("#0f1b2d")
cm = plt.cm.turbo
for k in range(90):
    p, q = rng.random() * 2 * np.pi, rng.random() * 2 * np.pi
    P = np.empty(900); Q = np.empty(900)
    for i in range(900):
        p = (p + K * np.sin(q)) % (2 * np.pi); q = (q + p) % (2 * np.pi); P[i] = p; Q[i] = q
    ax.plot(Q, P, ",", color=cm(k / 90), alpha=0.9)
ax.set_xlim(0, 2 * np.pi); ax.set_ylim(0, 2 * np.pi); ax.set_xticks([]); ax.set_yticks([])
ax.set_title(f"Standard map, $K={K:.4f}$: KAM tori, islands and chaos", fontsize=9)
save("standard_map")

# 4. Logistic map: bifurcation colored by Lyapunov exponent
rs = np.linspace(2.8, 4.0, 1600); xk = np.full(rs.size, 0.3); lyap = np.zeros(rs.size)
for _ in range(600): xk = rs * xk * (1 - xk)
pts_r, pts_x, pts_c = [], [], []
for i in range(400):
    xk = rs * xk * (1 - xk); lyap += np.log(np.abs(rs * (1 - 2 * xk)) + 1e-12)
    if i >= 250: pts_r.append(rs); pts_x.append(xk.copy())
lyap /= 400
fig, axs = plt.subplots(2, 1, figsize=(4.8, 4.2), sharex=True, gridspec_kw={"height_ratios": [2.2, 1]})
R = np.concatenate(pts_r); X = np.concatenate(pts_x); C = np.tile(lyap, len(pts_r))
sc = axs[0].scatter(R, X, c=np.clip(C, -0.8, 0.7), cmap="plasma", s=0.25, lw=0, rasterized=True)
axs[0].set_ylabel("$x$"); axs[0].set_title("Logistic map: attractor colored by Lyapunov exponent", fontsize=9)
fig.colorbar(sc, ax=axs, label="$\\chi(r)$", pad=0.02, fraction=0.05)
axs[1].plot(rs, lyap, color="#1b1b1b", lw=0.5); axs[1].axhline(0, color="#d1495b", lw=0.7)
axs[1].fill_between(rs, lyap, 0, where=lyap > 0, color="#d1495b", alpha=0.35)
axs[1].set_ylim(-1.5, 0.8); axs[1].set_xlabel("$r$"); axs[1].set_ylabel("$\\chi(r)$")
save("logistic")

# 5. Types on the simplex with KL contours and an I projection
P = np.array([0.2, 0.3, 0.5]); f = np.array([0.0, 1.0, 2.0]); a = 0.6
def bary(q): return q[..., 1] + 0.5 * q[..., 2], (np.sqrt(3) / 2) * q[..., 2]
g = 300; t1, t2 = np.meshgrid(np.linspace(0, 1, g), np.linspace(0, 1, g))
mask = t1 + t2 <= 1; Q = np.stack([1 - t1 - t2, t1, t2], -1)
with np.errstate(divide="ignore", invalid="ignore"):
    KL = np.where(Q > 0, Q * np.log(Q / P), 0).sum(-1)
KL[~mask] = np.nan
X, Y = bary(Q)
fig, ax = plt.subplots(figsize=(4.4, 3.9))
cs = ax.contourf(X, Y, KL, levels=np.linspace(0, 1.6, 17), cmap="viridis_r", rasterized=True)
plt.colorbar(cs, ax=ax, fraction=0.04, pad=0.02, label=r"$\mathrm{KL}(Q\,\|\,P)$")
nn = 12
for i in range(nn + 1):
    for j in range(nn + 1 - i):
        q = np.array([nn - i - j, i, j]) / nn; xb, yb = bary(q)
        ax.plot(xb, yb, "o", ms=2.2, color="white", mec="#1b1b1b", mew=0.3)
# constraint line E_Q f = a : q1 + 2 q2 = a
qs = []
for q2 in np.linspace(0, a / 2, 200):
    q1 = a - 2 * q2; q0 = 1 - q1 - q2
    if q0 >= 0 and q1 >= 0: qs.append([q0, q1, q2])
qs = np.array(qs); xb, yb = bary(qs); ax.plot(xb, yb, color="#d1495b", lw=1.6, label=r"$\{Q:\ \mathbb{E}_Q f=a\}$")
from scipy.optimize import brentq
lam = brentq(lambda l: (P * np.exp(l * f) * f).sum() / (P * np.exp(l * f)).sum() - a, -20, 20)
Ps = P * np.exp(lam * f); Ps /= Ps.sum(); xs_, ys_ = bary(Ps)
ax.plot(xs_, ys_, "*", ms=12, color="#edae49", mec="k", label=r"I projection $P^*$")
xp, yp = bary(P); ax.plot(xp, yp, "s", ms=6, color="#d1495b", mec="k", label="$P$")
ax.plot([0, 1, 0.5, 0], [0, 0, np.sqrt(3) / 2, 0], color="k", lw=0.8)
for lab_, cx_, cy_ in [("0", 0.0, -0.05), ("1", 1.0, -0.05), ("2", 0.5, np.sqrt(3) / 2 + 0.05)]: ax.text(cx_, cy_, lab_, ha="center", va="center", fontsize=8)
ax.set_aspect("equal"); ax.axis("off"); ax.legend(frameon=False, fontsize=7, loc="upper right")
ax.set_title("Types of length $12$ on a three letter alphabet", fontsize=9, pad=12)
save("types_simplex"); print("Pstar", Ps, lam)

# 6. Moment conditioning for exponential samples
a = 2.0; x = np.linspace(0, 10, 600)
fig, axs = plt.subplots(1, 2, figsize=(6.0, 2.5))
cols = ["#edae49", "#d1495b", "#7b2d8e", "#1b4f9c"]
for nn_, c in zip([3, 5, 10, 50], cols):
    d = np.where(x < nn_ * a, (nn_ - 1) / (nn_ * a) * np.clip(1 - x / (nn_ * a), 0, None) ** (nn_ - 2), 0)
    axs[0].plot(x, d, color=c, lw=1.2, label=f"$n={nn_}$")
axs[0].plot(x, np.exp(-x / a) / a, color="k", ls="--", lw=1, label="tilt $e^{-x/a}/a$")
axs[0].set_xlabel("$x_1$"); axs[0].legend(frameon=False, fontsize=6.5); axs[0].set_title("law of $X_1$ given $\\bar X_n=a$", fontsize=8)
ns = np.unique(np.logspace(0.5, 3.3, 30).astype(int)); tvs = []
xx_ = np.linspace(0, 80, 200001)
for nn_ in ns:
    d = np.where(xx_ < nn_ * a, (nn_ - 1) / (nn_ * a) * np.clip(1 - xx_ / (nn_ * a), 0, None) ** (nn_ - 2), 0)
    tvs.append(0.5 * np.trapezoid(np.abs(d - np.exp(-xx_ / a) / a), xx_))
axs[1].loglog(ns, tvs, "o", ms=3, color="#00798c"); axs[1].loglog(ns, 0.5 * np.array(tvs)[-1] * ns[-1] / ns * 2, color="#d1495b", lw=0.8, label="slope $-1$")
axs[1].set_xlabel("$n$"); axs[1].set_title("total variation to the tilt", fontsize=8); axs[1].legend(frameon=False, fontsize=7)
save("conditioning"); print("TV n*tv", ns[-1] * tvs[-1])

# 7. Maxwell Poincare Borel: (v1, v2) for uniform points on sphere radius sqrt(n)
fig, axs = plt.subplots(1, 3, figsize=(6.0, 2.1), constrained_layout=True)
thc = np.linspace(0, 2 * np.pi, 200)
for ax, nn_ in zip(axs, [3, 6, 60]):
    Z = rng.standard_normal((200000, nn_)); V = np.sqrt(nn_) * Z / np.linalg.norm(Z, axis=1, keepdims=True)
    hh = ax.hist2d(V[:, 0], V[:, 1], bins=120, range=[[-3.2, 3.2], [-3.2, 3.2]], cmap="inferno", density=True, vmin=0, vmax=0.2, rasterized=True)
    for rr in (1, 2, 3): ax.plot(rr * np.cos(thc), rr * np.sin(thc), color="white", lw=0.4, ls=":")
    ax.set_title(f"$n={nn_}$", fontsize=8); ax.set_xticks([-3, 0, 3]); ax.set_yticks([-3, 0, 3]); ax.tick_params(labelsize=6); ax.set_aspect("equal")
cb = fig.colorbar(hh[3], ax=axs, fraction=0.025, pad=0.02); cb.set_label("density", fontsize=7); cb.ax.tick_params(labelsize=6)
fig.suptitle("Two velocity components of a uniform point on $S^{n-1}(\\sqrt{n})$", fontsize=8)
save("sphere_maxwell")

# 8. Lanford window: Duhamel majorant
tt = np.linspace(0, 1.6, 400)
fig, axs = plt.subplots(1, 2, figsize=(6.0, 2.5))
for kmax, c in zip([2, 5, 10, 40], cols):
    S = sum((tt) ** k for k in range(kmax + 1)); axs[0].plot(tt, S, color=c, lw=1.1, label=f"$k\\leq{kmax}$")
tin = tt[tt < 1]; axs[0].plot(tin, 1 / (1 - tin), "k--", lw=0.8, label="$1/(1-t/T^*)$")
axs[0].axvspan(0, 1, color="#66a182", alpha=0.18); axs[0].set_ylim(0, 30); axs[0].set_xlabel("$t/T^*$")
axs[0].set_title("Duhamel majorant $\\sum_k (t/T^*)^k$", fontsize=8); axs[0].legend(frameon=False, fontsize=6.5)
axs[0].text(0.08, 26.5, "Lanford window", color="#2b6e4f", fontsize=7)
ks = np.arange(0, 31)
for r_, c in zip([0.5, 0.9, 1.1], ["#1b4f9c", "#7b2d8e", "#d1495b"]):
    axs[1].semilogy(ks, r_ ** ks, "o-", ms=2.5, lw=0.8, color=c, label=f"$t={r_}\\,T^*$")
axs[1].set_xlabel("number of collisions $k$ in the tree"); axs[1].set_ylabel("bound on $k$th term")
axs[1].set_title("$k$th term of the majorant", fontsize=8); axs[1].legend(frameon=False, fontsize=6.5)
save("lanford_window")

# 9. Universal coding regret: Laplace and Jeffreys mixtures
nsr = np.arange(2, 2001)
def regret(nv, a0):
    # worst case over k of log of max likelihood / mixture probability (nats), Beta(a0,a0) mixture
    out = []
    for n_ in nv:
        k = np.arange(0, n_ + 1)
        with np.errstate(divide="ignore", invalid="ignore"):
            ml = np.where(k > 0, k * np.log(k / n_), 0) + np.where(k < n_, (n_ - k) * np.log((n_ - k) / n_), 0)
        mix = gammaln(k + a0) + gammaln(n_ - k + a0) - gammaln(n_ + 2 * a0) - 2 * gammaln(a0) + gammaln(2 * a0)
        out.append(np.max(ml - mix))
    return np.array(out)
fig, ax = plt.subplots(figsize=(4.6, 2.7))
ax.semilogx(nsr, regret(nsr, 1.0) / np.log(2), color="#d1495b", lw=1.2, label="Laplace, uniform prior")
ax.semilogx(nsr, regret(nsr, 0.5) / np.log(2), color="#1b4f9c", lw=1.2, label="Jeffreys, Beta$(1/2,1/2)$")
ax.semilogx(nsr, 0.5 * np.log2(nsr) + 0.5 * np.log2(np.pi / 2), color="k", ls="--", lw=0.9, label="asymptotic minimax $\\frac{1}{2}\\log_2(\\pi n/2)$")
ax.semilogx(nsr, np.log2(nsr + 1), color="#edae49", ls=":", lw=2.2, label="$\\log_2(n+1)$", zorder=0)
ax.set_xlabel("$n$"); ax.set_ylabel("worst case regret (bits)"); ax.legend(frameon=False, fontsize=6.5)
ax.set_title("Bayes mixtures as universal codes", fontsize=9)
save("regret")
print("done")
