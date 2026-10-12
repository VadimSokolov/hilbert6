"""Figure mf_heat: information per mode and trajectory uncertainty for the heat (Stokes) equation.

Part IV, chapter on examples, section on the heat equation (labels m:fig:heat, m:eq:iota, m:tab:iota).
Run from this folder: python3 mf_heat.py   (writes ../figures/mf_heat.pdf; no data file is read).

Provenance. Rebuilt from fig_heat_stokes.py of the code archive of the 92 page paper (archive copy: anc/fig_heat_stokes.py in this
folder), first figure of that script. Formulas, parameters and curves are those of the archive script:
  * left panel: iota_k(T0) = (exp(-2 nu lam T0) - exp(-2 nu lam T)) / (2 nu lam (T - T0)) with lam = 4 pi^2 |k|^2, nu = 0.01, T = 1,
    T0 = 0, 0.05, 0.2, 0.5, |k| = 1, ..., 40; a triangle marks the mode where a curve falls below 1e-24 and leaves the frame;
  * right panel: sqrt( sum_{0 < |k| <= K_max} exp(-2 nu lam_k t) / (N iota_k(0)) ) for N = 10^4 and K_max = 16, 32, 64, 128,
    the sum running over the integer wavevectors k in the plane with 0 < |k| <= K_max, t from 1e-5 to 1.
What changed: size 4.6 in by 2.15 in with text at 7 to 8 pt (the original is 9 in wide and would be scaled by one half), no titles
(the caption carries the content), the line styles and colors of the book. The numbers are identical. The script prints the values
that the caption of the chapter states.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "figures")
plt.rcParams.update({"font.family": "serif", "mathtext.fontset": "stix", "font.size": 8,
                     "axes.linewidth": 0.6, "lines.linewidth": 1.0, "xtick.labelsize": 7, "ytick.labelsize": 7,
                     "legend.fontsize": 7, "axes.labelsize": 8, "pdf.fonttype": 42})

nu, T = 0.01, 1.0
blue, red, teal, purple = "#1b4f9c", "#d1495b", "#00798c", "#7b2d8e"


def lam(k2):
    return 4 * np.pi ** 2 * k2


def iota(k2, T0):
    l = lam(k2)
    return (np.exp(-2 * nu * l * T0) - np.exp(-2 * nu * l * T)) / (2 * nu * l * (T - T0))


fig, (ax0, ax1) = plt.subplots(1, 2, figsize=(4.6, 2.15), constrained_layout=True)

# left panel: information per mode
ks = np.arange(1, 41)
YFLOOR = 1e-24
for T0, ls, col in [(0, "-", blue), (0.05, "--", red), (0.2, "-.", teal), (0.5, ":", purple)]:
    y = iota(ks ** 2, T0)
    ax0.semilogy(ks, y, ls, color=col, label=r"$T_0=%g$" % T0)
    below = np.where(y < YFLOOR)[0]
    if len(below):
        ax0.plot([ks[below[0]]], [YFLOOR * 3], "v", ms=3.5, color=col, clip_on=False)
        print("T0 = %g: iota_k falls below 1e-24 at |k| = %d" % (T0, ks[below[0]]))
ax0.set_ylim(YFLOOR, 3.0)
ax0.set_yticks(10.0 ** np.arange(0, -25, -6))
ax0.set_xlabel(r"$|k|$")
ax0.set_ylabel(r"information $\iota_k(T_0)$")
ax0.legend(loc="upper right", frameon=False, handlelength=2.2)

# right panel: posterior standard deviation of the state against t, for four truncations
ts = np.logspace(-5, 0, 240)
Nn = 10 ** 4
curves = {}
for K, ls, col in [(16, ":", purple), (32, "-.", teal), (64, "--", red), (128, "-", blue)]:
    kx, ky = np.meshgrid(np.arange(-K, K + 1), np.arange(-K, K + 1))
    k2 = (kx ** 2 + ky ** 2).ravel()
    k2 = k2[(k2 > 0) & (k2 <= K * K)]
    sd = np.array([np.sqrt(np.sum(np.exp(-2 * nu * lam(k2) * t) / (Nn * iota(k2, 0)))) for t in ts])
    curves[K] = sd
    ax1.loglog(ts, sd, ls, color=col, label=r"$K_{\max}=%d$" % K)
ax1.set_xlabel(r"$t$")
ax1.set_ylabel(r"posterior s.d. of $u_\theta(t,x)$")
ax1.legend(loc="lower left", frameon=False, title=r"$N=10^4$", title_fontsize=7, handlelength=2.2)

os.makedirs(OUT, exist_ok=True)
fig.savefig(os.path.join(OUT, "mf_heat.pdf"))

print("values at t = 1e-5:", {K: round(float(c[0]), 3) for K, c in curves.items()})
print("ratios of consecutive plateaus:", [round(float(curves[2 * K][0] / curves[K][0]), 3) for K in (16, 32, 64)])
for K in (16, 32, 64):
    rel = curves[K] / curves[128]
    bad = np.where(np.abs(rel - 1) > 0.01)[0]
    print("K_max = %d agrees with K_max = 128 to within 1 percent for t >= %.4f" % (K, ts[bad.max() + 1]))
print("value at t = 1 (all truncations): %.4f" % curves[128][-1])
print("Table of the chapter, iota_k(0), iota_k(0.05), iota_k(0.2), 1/iota_k(0):")
for k in (1, 2, 4, 8, 16, 32):
    print(k, "%.3e %.3e %.3e %.3g" % (iota(k * k, 0), iota(k * k, 0.05), iota(k * k, 0.2), 1 / iota(k * k, 0)))
