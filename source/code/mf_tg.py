"""Figure mf_tg: ratio of advective coupling to viscous decay for the linearized Navier Stokes equation about the Taylor Green vortex.

Part IV, chapter on examples, section on two dimensional Navier Stokes (label m:fig:tg).
Run from this folder: python3 mf_tg.py   (writes ../figures/mf_tg.pdf; no data file is read).

Provenance. Rebuilt from fig_heat_stokes.py of the code archive of the 92 page paper (archive copy: anc/fig_heat_stokes.py in this
folder), the block "Figure 3 (Taylor-Green coupling ratio)". The curves are those of the archive script: the ratio 2 pi A |k| / (nu lambda_k)
with lambda_k = 4 pi^2 |k|^2 (the unit torus, where the vortex is A exp(-8 pi^2 nu t) (sin 2 pi x1 cos 2 pi x2, -cos 2 pi x1 sin 2 pi x2)),
nu = 0.01, A = 0.1, 1, 5, |k| = 1, ..., 40, and the level one. On the 2 pi torus of the advection remark of the chapter, where
lambda_k = |k|^2, the same ratio is A / (nu |k|), larger by the factor 2 pi; the figure does not show that version.
What changed: size 3.45 in by 2.35 in (the original is 4.5 in wide and was printed at 0.55 of the text width, which halved its type)
with text at 7 to 8 pt, no title (the caption carries the content). The numbers are identical.
The script prints the crossover |k| = A / (2 pi nu) of each curve.
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

nu = 0.01


def lam(k2):
    return 4 * np.pi ** 2 * k2


blue, red, teal = "#1b4f9c", "#d1495b", "#00798c"
fig, ax = plt.subplots(figsize=(3.45, 2.35), constrained_layout=True)
kk = np.arange(1, 41)
for A, ls, col in [(0.1, "-", blue), (1.0, "--", red), (5.0, "-.", teal)]:
    ax.semilogy(kk, A * 2 * np.pi * kk / (nu * lam(kk ** 2)), ls, color=col, label=r"$A=%g$" % A)
    print("A = %g: ratio equals one at |k| = A/(2 pi nu) = %.2f" % (A, A / (2 * np.pi * nu)))
ax.axhline(1, color="k", lw=0.6)
ax.set_xlabel(r"$|k|$")
ax.set_ylabel(r"ratio $2\pi A|k|/(\nu\lambda_k)$")
ax.set_xlim(0, 41)
ax.legend(loc="upper right", frameon=False, handlelength=2.2)

os.makedirs(OUT, exist_ok=True)
fig.savefig(os.path.join(OUT, "mf_tg.pdf"))
