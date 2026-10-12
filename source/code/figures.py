"""Figures for On Hilbert's 6th Problem (Polson and Sokolov).
Every figure is computed from scratch; run: python3 figures.py
Output: ../figures/*.pdf (grayscale friendly vector graphics)."""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

OUT = os.path.join(os.path.dirname(__file__), "..", "figures")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.family": "serif", "font.size": 9,
                     "axes.linewidth": 0.6, "lines.linewidth": 1.0,
                     "figure.figsize": (4.4, 2.9), "savefig.bbox": "tight", "pdf.fonttype": 42,
                     "axes.prop_cycle": matplotlib.cycler(color=["#1b4f9c", "#d1495b", "#edae49", "#00798c", "#66a182", "#7b2d8e"])})
rng = np.random.default_rng(1900)

def save(name):
    plt.savefig(os.path.join(OUT, name + ".pdf"), dpi=300)
    plt.close()

# 1. Henon Heiles surface of section (Poincare)
def hh(t, s):
    x, y, px, py = s
    return [px, py, -x - 2 * x * y, -y - x * x + y * y]

def section(E, y0, py0):
    rest = 2 * E - py0 ** 2 - y0 ** 2 + (2.0 / 3.0) * y0 ** 3
    if rest < 0:
        return None
    s0 = [0.0, y0, np.sqrt(rest), py0]
    ev = lambda t, s: s[0]
    ev.direction = 1
    sol = solve_ivp(hh, [0, 2500], s0, events=ev, rtol=1e-9, atol=1e-11)
    pts = sol.y_events[0]
    return pts[:, 1], pts[:, 3]

E = 1.0 / 8.0
fig, ax = plt.subplots(figsize=(4.0, 3.4))
hh_cmap = matplotlib.colors.LinearSegmentedColormap.from_list("viridis_dark", plt.cm.viridis(np.linspace(0, 0.88, 256)))   # print safe, ordered in grayscale, no pale yellow
for y0 in np.linspace(-0.25, 0.45, 15):
    out = section(E, y0, 0.0)
    if out is not None:
        ax.plot(out[0], out[1], ".", ms=2.2, mew=0, color=hh_cmap((y0 + 0.25) / 0.7), rasterized=True)
fig.colorbar(plt.cm.ScalarMappable(cmap=hh_cmap, norm=plt.Normalize(-0.25, 0.45)), ax=ax, label="initial $y$", fraction=0.045, pad=0.02)
ax.set_xlabel("$y$"); ax.set_ylabel("$p_y$")
ax.set_title("H\u00e9non Heiles section, $E=1/8$")
save("henon_heiles")

# 2. Exit time of Brownian motion from (-1,1) and the Polya Gamma series
def exit_times(n, dt=2e-4):
    T = np.zeros(n); x = np.zeros(n); alive = np.ones(n, bool); t = 0.0
    while alive.any():
        t += dt
        x[alive] += np.sqrt(dt) * rng.standard_normal(alive.sum())
        hit = alive & (np.abs(x) >= 1)
        T[hit] = t; alive &= ~hit
    return T

Tbm = exit_times(6000)
K = 200
k = np.arange(1, K + 1)
E_ = rng.exponential(size=(60000, K))
Tpg = (8.0 / (np.pi ** 2 * (2 * k - 1) ** 2) * E_).sum(axis=1)
# exact density via the eigenfunction series f(t) = sum_n (-1)^n (2n+1) (pi/2) exp(-(2n+1)^2 pi^2 t/8)
tt = np.linspace(0.01, 3.5, 400)
n = np.arange(0, 200)[:, None]
lam = (2 * n + 1) ** 2 * np.pi ** 2 / 8.0
dens = ((-1) ** n * (2 * n + 1) * np.pi / 2.0 * np.exp(-lam * tt)).sum(axis=0)
fig, ax = plt.subplots()
ax.hist(Tbm, bins=60, density=True, color="#9ecae1", edgecolor="#3182bd", lw=0.3, label="Euler paths")
ax.hist(Tpg, bins=120, density=True, histtype="step", color="#d1495b", lw=0.8, label="series of exponentials")
ax.plot(tt, dens, color="#1b1b1b", ls="--", lw=0.9, label="spectral density")
ax.set_xlim(0, 3.5); ax.set_xlabel("$T$"); ax.set_ylabel("density"); ax.legend(frameon=False)
save("exit_time")

# 3. Kac model relaxation
N = 20000
v = np.where(rng.random(N) < 0.5, -1.0, 1.0) * (1 + 0.1 * rng.standard_normal(N))
v /= np.sqrt(np.mean(v ** 2))
snap = {}
kurt = []
times = []
collisions_per_unit = N // 2
for step in range(0, 15 * collisions_per_unit + 1):
    if step % (collisions_per_unit // 10) == 0:
        times.append(step / collisions_per_unit)
        kurt.append(np.mean(v ** 4) / np.mean(v ** 2) ** 2)
    if step in (0, collisions_per_unit, 3 * collisions_per_unit, 12 * collisions_per_unit):
        snap[step / collisions_per_unit] = v.copy()
    i, j = rng.integers(0, N, 2)
    if i == j:
        continue
    th = rng.uniform(0, 2 * np.pi)
    vi, vj = v[i], v[j]
    v[i] = vi * np.cos(th) - vj * np.sin(th)
    v[j] = vi * np.sin(th) + vj * np.cos(th)
fig, axs = plt.subplots(1, 2, figsize=(5.2, 2.4))
grid = np.linspace(-3.5, 3.5, 200)
styles = ["#edae49", "#d1495b", "#7b2d8e", "#1b4f9c"]
for (t, vs), c in zip(sorted(snap.items()), styles):
    h, e = np.histogram(vs, bins=70, range=(-3.5, 3.5), density=True)
    axs[0].step(0.5 * (e[1:] + e[:-1]), h, color=c, lw=0.8, label=f"$t={t:g}$")
axs[0].plot(grid, np.exp(-grid ** 2 / 2) / np.sqrt(2 * np.pi), "k:", lw=1.0, label="Maxwellian")
axs[0].legend(frameon=False, fontsize=6); axs[0].set_xlabel("$v$")
axs[1].plot(times, kurt, color="#00798c", lw=1.2)
axs[1].axhline(3, color="0.5", ls=":")
axs[1].set_xlabel("time (collisions per particle)"); axs[1].set_ylabel("kurtosis")
fig.suptitle("Kac's model: relaxation to the Maxwellian", fontsize=9)
save("kac_model")

# 4. Kac ring recurrence
Nr, m = 500, 61
marked = np.zeros(Nr, bool); marked[rng.choice(Nr, m, replace=False)] = True
balls = np.ones(Nr)  # +1 white, -1 black
delta = []
for t in range(0, 2 * Nr + 50):
    delta.append(balls.mean())
    balls = np.where(marked, -balls, balls)
    balls = np.roll(balls, 1)
mu = m / Nr
fig, ax = plt.subplots()
ax.plot(delta, color="#1b4f9c", lw=0.8, label="ring of $N=500$ sites")
ax.plot((1 - 2 * mu) ** np.arange(len(delta)), color="#d1495b", ls="--", lw=0.9, label="Boltzmann's prediction $(1-2\\mu)^t$")
ax.set_xlabel("$t$"); ax.set_ylabel("(white $-$ black)/$N$")
ax.legend(frameon=False); ax.set_title("Kac's ring: decay, then recurrence at $t=2N$")
save("kac_ring")

# 5. Heat equation inverse problem on the solution manifold
L = np.pi; xs = np.linspace(0, L, 300); Kmodes = 40; kk = np.arange(1, Kmodes + 1)
phi = np.sqrt(2 / L) * np.sin(np.outer(kk, xs))
prior_sd = 1.0 / kk ** 1.5
theta_true = prior_sd * rng.standard_normal(Kmodes)
Tobs = 0.05; sigma = 0.002
decay = np.exp(-kk ** 2 * Tobs)
y = decay * theta_true + sigma * rng.standard_normal(Kmodes)
post_var = 1.0 / (decay ** 2 / sigma ** 2 + 1 / prior_sd ** 2)
post_mean = post_var * decay * y / sigma ** 2
draws = post_mean + np.sqrt(post_var) * rng.standard_normal((200, Kmodes))
fig, axs = plt.subplots(1, 2, figsize=(5.4, 2.4))
u0 = draws @ phi
axs[0].fill_between(xs, np.percentile(u0, 5, 0), np.percentile(u0, 95, 0), color="#c6dbef")
axs[0].plot(xs, theta_true @ phi, color="#d1495b", lw=1.2, label="true $u_0$")
axs[0].plot(xs, post_mean @ phi, color="#1b4f9c", ls="--", lw=1.1, label="posterior mean")
axs[0].set_title("initial condition", fontsize=8); axs[0].legend(frameon=False, fontsize=6)
axs[1].scatter(kk, np.sqrt(post_var) / prior_sd, c=kk, cmap="viridis", s=10); axs[1].set_yscale("log")
axs[1].set_xlabel("mode $k$"); axs[1].set_title("posterior sd / prior sd", fontsize=8)
save("heat_inverse")

# 6. Lee Yang zeros, 2D Ising on 4x4 torus
Lx = 4; Ns = Lx * Lx; beta = 0.6
idx = np.arange(Ns).reshape(Lx, Lx)
bonds = [(idx[i, j], idx[(i + 1) % Lx, j]) for i in range(Lx) for j in range(Lx)] + \
        [(idx[i, j], idx[i, (j + 1) % Lx]) for i in range(Lx) for j in range(Lx)]
coef = np.zeros(Ns + 1)
confs = ((np.arange(2 ** Ns)[:, None] >> np.arange(Ns)) & 1)
spins = 2 * confs - 1
bi = np.array(bonds)
energy = (spins[:, bi[:, 0]] * spins[:, bi[:, 1]]).sum(1)
nup = confs.sum(1)
w = np.exp(beta * (energy - energy.max()))
np.add.at(coef, nup, w)
roots = np.roots(coef[::-1])
fig, ax = plt.subplots(figsize=(3.2, 3.2))
th = np.linspace(0, 2 * np.pi, 400)
ax.plot(np.cos(th), np.sin(th), color="#9ecae1", lw=1.0)
ax.scatter(roots.real, roots.imag, color="#1b4f9c", s=22, edgecolor="k", lw=0.3, zorder=3)
ax.set_aspect("equal"); ax.set_xlabel("Re $z$"); ax.set_ylabel("Im $z$")
ax.set_title("Lee Yang zeros, Ising $4\\times4$ torus")
save("lee_yang")
print("max | |z|-1 | =", np.abs(np.abs(roots) - 1).max())

# 7. de Bruijn Newman heat flow of the Polya kernel
u = np.linspace(0, 1.4, 20001)
def Phi(u):
    s = np.zeros_like(u)
    for n in range(1, 31):
        s += (2 * np.pi ** 2 * n ** 4 * np.exp(9 * u) - 3 * np.pi * n ** 2 * np.exp(5 * u)) * np.exp(-np.pi * n ** 2 * np.exp(4 * u))
    return s
P = Phi(u)
xg = np.linspace(18, 56, 900)
fig, axs = plt.subplots(1, 2, figsize=(5.4, 2.4))
axs[0].plot(u, P, color="#7b2d8e"); axs[0].fill_between(u, P, color="#7b2d8e", alpha=0.15); axs[0].set_xlabel("$u$"); axs[0].set_ylabel("kernel"); axs[0].set_title("P\u00f3lya kernel $\\Phi(u)$", fontsize=8)
from scipy.optimize import brentq
for t, c, ls in [(-4.0, "#00798c", (0, (5, 2))), (0.0, "#1b1b1b", "-"), (4.0, "#d1495b", ":")]:
    integrand = np.exp(t * u ** 2) * P
    H = np.trapezoid(integrand[None, :] * np.cos(np.outer(xg, u)), u, axis=1)
    axs[1].plot(xg, H * np.exp(np.pi * xg / 8) * xg ** (-1.75), color=c, ls=ls, lw=1.1, label=f"$t={t:g}$")
    # the first three zeros of H_t: sign changes on the grid, refined by a root solve on the quadrature
    Hq = lambda x: np.trapezoid(integrand * np.cos(x * u), u)
    sc = np.where(np.sign(H[:-1]) != np.sign(H[1:]))[0]
    print("zeros of H_t at t =", t, [round(brentq(Hq, xg[i], xg[i + 1], xtol=1e-10), 2) for i in sc[:3]])
axs[1].axhline(0, color="0.7", lw=0.5)
axs[1].set_xlim(20, 56)
axs[1].set_xlabel("$x$"); axs[1].set_ylabel("normalized $H_t$"); axs[1].legend(frameon=False, fontsize=6)
axs[1].set_title("$x^{-7/4}e^{\\pi x/8} H_t(x)$", fontsize=8)
save("debruijn_newman")

# 8. Entropic transport (Schrodinger bridge, static) via Sinkhorn
xg = np.linspace(-4, 4, 160)
mu = np.exp(-(xg + 1.5) ** 2 / 0.3) + 0.6 * np.exp(-(xg - 1.0) ** 2 / 0.5); mu /= mu.sum()
nu = np.exp(-(xg - 0.5) ** 2 / 1.2); nu /= nu.sum()
C = (xg[:, None] - xg[None, :]) ** 2
fig, axs = plt.subplots(1, 3, figsize=(5.6, 2.0))
for ax, eps in zip(axs, [2.0, 0.3, 0.03]):
    Kmat = np.exp(-C / eps); a = np.ones_like(mu); b = np.ones_like(nu)
    for _ in range(3000):
        a = mu / (Kmat @ b); b = nu / (Kmat.T @ a)
    Pi = a[:, None] * Kmat * b[None, :]
    ax.imshow(Pi ** 0.5, origin="lower", extent=[-4, 4, -4, 4], cmap="magma", aspect="equal", interpolation="bilinear")
    ax.set_title(f"$\\varepsilon={eps:g}$", fontsize=8); ax.set_xticks([-4, 0, 4]); ax.set_yticks([-4, 0, 4] if ax is axs[0] else []); ax.tick_params(labelsize=6)
    ax.set_xlabel("$\\nu$", fontsize=7)
    if ax is axs[0]: ax.set_ylabel("$\\mu$", fontsize=7)
fig.suptitle("Entropic transport plans: Schr\u00f6dinger's problem as $\\varepsilon\\to0$", fontsize=9)
save("sinkhorn")

# 9. Kelly growth and Szilard bound
p = 0.6
f = np.linspace(0, 0.6, 400)
G = p * np.log(1 + f) + (1 - p) * np.log(1 - f)
fig, ax = plt.subplots()
ax.plot(f, G / np.log(2), color="#1b4f9c", lw=1.4)
fstar = 2 * p - 1
ax.axvline(fstar, color="0.5", ls=":", label="$f^*=2p-1$")
ax.axhline((np.log(2) + p * np.log(p) + (1 - p) * np.log(1 - p)) / np.log(2), color="0.5", ls="--", lw=0.8, label="$1-H(p)$")
ax.axvline(2 * fstar, color="0.5", ls="-.", lw=0.8, label="$2f^*$")
ax.axhline(0, color="k", lw=0.5)
ax.set_xlabel("fraction $f$ bet on the favored side"); ax.set_ylabel("growth (bits per bet)")
ax.set_title("Kelly: optimal growth $=1-H(p)$ bits, $p=0.6$")
ax.legend(fontsize=8)
save("kelly")
# numbers of the caption: the growth curve crosses zero just below 2f*, where it is slightly negative (no random draws)
kelly_growth = lambda x: (p * np.log(1 + x) + (1 - p) * np.log(1 - x)) / np.log(2)
print(f"kelly: maximum 1-H(p) = {kelly_growth(fstar):.4f} bits at f* = {fstar:.1f}, growth zero at f = {brentq(kelly_growth, fstar, 0.6, xtol=1e-12):.5f}, "
      f"growth at 2f* = {kelly_growth(2 * fstar):.5f} bits")
print("figures written to", os.path.abspath(OUT))

# 10. Burgers equation via Hopf Cole, several viscosities
def burgers_hopf_cole(nu, t, xs, u0int):
    # u(x,t) = -2 nu d/dx log phi, phi(x,t) = int exp(-(x-y)^2/(4 nu t) - U0(y)/(2 nu)) dy
    y = np.linspace(-np.pi, 3 * np.pi, 6000)
    U0 = u0int(y)
    out = []
    for x in xs:
        e = -(x - y) ** 2 / (4 * nu * t) - U0 / (2 * nu)
        m = e.max(); w = np.exp(e - m)
        out.append(np.sum((x - y) / t * w) / np.sum(w))
    return np.array(out)
u0int = lambda y: 1 - np.cos(y)          # U0' = sin y, so u0 = sin y
xs = np.unique(np.concatenate([np.linspace(0, 2 * np.pi, 400), np.pi + np.linspace(-0.15, 0.15, 1201)]))
fig, ax = plt.subplots()
ax.plot(xs, np.sin(xs), color="#6baed6", lw=1.3, ls="dashed", label="$u_0=\\sin x$")
for nu, c in [(0.2, "#edae49"), (0.05, "#d1495b"), (0.005, "#1b4f9c")]:
    ax.plot(xs, burgers_hopf_cole(nu, 1.5, xs, u0int), color=c, lw=1.2, label=f"$\\nu={nu:g}$, $t=1.5$")
ax.set_xlabel("$x$"); ax.set_ylabel("$u$"); ax.legend(frameon=False, fontsize=7)
ax.set_title("Burgers equation by the Hopf Cole transform")
save("burgers")

# 11. Two dimensional Navier Stokes vorticity, pseudospectral
Nn = 96; nu2 = 2e-3; dt = 2e-3
k1 = np.fft.fftfreq(Nn, 1.0 / Nn); KX, KY = np.meshgrid(k1, k1, indexing="ij")
K2 = KX ** 2 + KY ** 2; K2i = np.where(K2 == 0, 0, 1.0 / np.where(K2 == 0, 1, K2))
dealias = (np.abs(KX) < Nn / 3) & (np.abs(KY) < Nn / 3)
xg2 = np.linspace(0, 2 * np.pi, Nn, endpoint=False); Xg, Yg = np.meshgrid(xg2, xg2, indexing="ij")
w0 = np.zeros((Nn, Nn))
for _ in range(10):
    cx, cy = rng.uniform(0, 2 * np.pi, 2); s = rng.choice([-1, 1]) * rng.uniform(3, 6)
    dx = np.angle(np.exp(1j * (Xg - cx))); dy = np.angle(np.exp(1j * (Yg - cy)))
    w0 += s * np.exp(-(dx ** 2 + dy ** 2) / 0.12)
wh = np.fft.fft2(w0); wh[0, 0] = 0
def rhs(wh):
    psi = wh * K2i
    u = np.real(np.fft.ifft2(1j * KY * psi)); v = np.real(np.fft.ifft2(-1j * KX * psi))
    wx = np.real(np.fft.ifft2(1j * KX * wh)); wy = np.real(np.fft.ifft2(1j * KY * wh))
    return -np.fft.fft2(u * wx + v * wy) * dealias - nu2 * K2 * wh
snaps2 = {0.0: np.real(np.fft.ifft2(wh))}
spec2 = {0.0: wh.copy()}
t = 0.0
for step in range(1, 2501):
    k1_ = rhs(wh); k2_ = rhs(wh + 0.5 * dt * k1_); k3_ = rhs(wh + 0.5 * dt * k2_); k4_ = rhs(wh + dt * k3_)
    wh = wh + dt / 6 * (k1_ + 2 * k2_ + 2 * k3_ + k4_); t += dt
    if step in (750, 2500):
        snaps2[round(t, 2)] = np.real(np.fft.ifft2(wh))
        spec2[round(t, 2)] = wh.copy()
# energy E(k) and enstrophy Z(k) by shells m - 1/2 <= |k| < m + 1/2 (per unit area; Parseval: mean(w^2) = sum |c_k|^2, c_k = fft2/N^2)
shell = np.rint(np.sqrt(K2)).astype(int); kshell = np.arange(1, Nn // 3)
def shell_spectra(wh_):
    c2 = np.abs(wh_ / Nn ** 2) ** 2
    Ek = np.bincount(shell.ravel(), weights=(0.5 * c2 * K2i).ravel(), minlength=Nn)[kshell]
    Zk = np.bincount(shell.ravel(), weights=(0.5 * c2).ravel(), minlength=Nn)[kshell]
    return Ek, Zk
spec_k = {tt_: shell_spectra(wh_) for tt_, wh_ in spec2.items()}
vm = np.abs(w0).max()
print("ns2d: vm =", round(vm, 3))
for tt_, (Ek, Zk) in sorted(spec_k.items()):
    print(f"ns2d spectra t={tt_:g}: energy {Ek.sum():.4f} enstrophy {Zk.sum():.4f}; centroid of E {np.sum(kshell * Ek) / Ek.sum():.2f}, of Z {np.sum(kshell * Zk) / Zk.sum():.2f}; "
          f"E(k=1) {Ek[0]:.4f}; share of E at k<=3 {Ek[:3].sum() / Ek.sum():.3f}; share of Z at k>=10 {Zk[9:].sum() / Zk.sum():.2e}, at k>=16 {Zk[15:].sum() / Zk.sum():.2e}")
W_, H_ = 4.6, 4.05
fig = plt.figure(figsize=(W_, H_))
def axin(l, b, w, h):
    return fig.add_axes([l / W_, b / H_, w / W_, h / H_])
ms = 1.26
for i, (tt_, w) in enumerate(sorted(snaps2.items())):
    ax = axin(0.40 + i * (ms + 0.17), 2.52, ms, ms)
    im = ax.imshow(w.T, origin="lower", cmap="RdBu_r", vmin=-vm, vmax=vm, extent=[0, 2 * np.pi, 0, 2 * np.pi], interpolation="bicubic")
    ax.set_title(f"$t={tt_:g}$", fontsize=8, pad=3)
    ax.set_xticks([0, np.pi, 2 * np.pi]); ax.set_xticklabels(["0", r"$\pi$", r"$2\pi$"])
    ax.set_yticks([0, np.pi, 2 * np.pi]); ax.set_yticklabels(["0", r"$\pi$", r"$2\pi$"] if i == 0 else [])
    ax.tick_params(labelsize=7, length=2, width=0.5, pad=1.5)
cax = axin(0.40, 2.12, 3 * ms + 0.34, 0.08)
cb = fig.colorbar(im, cax=cax, orientation="horizontal")
cb.set_ticks([-vm, 0, vm]); cb.set_ticklabels([f"\u2212{vm:.1f}", "0", f"{vm:.1f}"])
cb.set_label("vorticity", fontsize=7.5, labelpad=2); cb.ax.tick_params(labelsize=7, length=2, width=0.5, pad=1.5)
sty = {0.0: ("#1b4f9c", "-"), 1.5: ("#d1495b", "--"), 5.0: ("#00798c", ":")}
for j, (idx, ttl, yl) in enumerate([(0, "energy spectrum", "$E(k)$"), (1, "enstrophy spectrum", "$Z(k)$")]):
    ax = axin(0.68 if j == 0 else 2.86, 0.48, 1.53 if j == 0 else 1.64, 1.10)
    for tt_ in sorted(spec_k):
        ax.plot(kshell, spec_k[tt_][idx], color=sty[tt_][0], ls=sty[tt_][1], lw=1.1 if tt_ != 5.0 else 1.4, label=f"$t={tt_:g}$")
    ax.set_xscale("log"); ax.set_yscale("log")
    ax.set_xticks([1, 2, 5, 10, 20]); ax.set_xticklabels(["1", "2", "5", "10", "20"]); ax.minorticks_off()
    ax.set_ylim(10 ** np.floor(np.log10(spec_k[5.0][idx].min())), None)
    ax.set_xlabel("wavenumber $k$", fontsize=7.5, labelpad=1); ax.set_ylabel(yl, fontsize=7.5, labelpad=1)
    ax.set_title(ttl, fontsize=8, pad=3); ax.tick_params(labelsize=7, length=2, width=0.5, pad=1.5)
    if j == 0:
        ax.legend(frameon=False, fontsize=6.5, loc="lower left", handlelength=1.8, borderpad=0.2, labelspacing=0.25)
fig.suptitle("Two dimensional Navier Stokes: vorticity and spectra", fontsize=8.5, y=0.99, va="bottom")
save("ns2d")
print("extra figures done")
