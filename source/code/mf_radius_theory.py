"""Figure mf_radius_theory: the decomposition of the localization error against measurement.

Chapter on generators, Section on the radius: Navier Stokes problem of Polson and Sokolov, D = 6, M = 1200.
Run from this folder: python3 mf_radius_theory.py   (writes ../figures/mf_radius_theory.pdf).

Provenance. The original plotting script of the 92 page paper (fig_radius_theory.py) is not in its code archive, so this script
rebuilds the figure from the recorded numbers and reproduces every number of the original figure:
  * measured points: results/ns/radius.json of the archive (the keys c<c>_id, c<c>_lin and laplace), copied below because this
    script must run from this folder without the archive;
  * prior fractions p_j of the Navier Stokes run, as printed in the text of the chapter;
  * curves: E(c)^2 = beta(c)^2 + a_v / c^v + b c^4 with v = 0 (identity head) and v = 2 (affine head); beta(c) is computed from
    the prior fractions with no free parameter, and (a_v, b) are fitted separately for each head by least squares on the absolute
    residuals E(c) - measured, over the seven radii.
Check against the text: the fitted optimum of the affine head c* = (a_2 / (2 b))^(1/6) is 2.44 and the root mean square residual of the
affine head is 0.044; both are printed when the script runs. The curves of the original figure were also read off its vector
paths: the two fitted curves agree with the curves computed here to better than 1e-4 in log10, and the dotted bias curve, which
here uses the prior fractions as printed to three decimals, agrees with the original to within 0.7 percent.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import least_squares

OUT = os.path.join(os.path.dirname(__file__), "..", "figures")
os.makedirs(OUT, exist_ok=True)
plt.rcParams.update({"font.family": "serif", "mathtext.fontset": "stix", "font.size": 8,
                     "axes.linewidth": 0.6, "lines.linewidth": 1.0, "xtick.labelsize": 7, "ytick.labelsize": 7,
                     "legend.fontsize": 7, "axes.labelsize": 8, "savefig.bbox": "tight", "pdf.fonttype": 42})

p = np.array([0.002, 0.002, 0.020, 0.023, 0.140, 0.173])
radii = np.array([0.5, 1.0, 2.0, 3.0, 5.0, 8.0, 14.0])
meas_id = np.array([0.1652371933685557, 0.16761917962619047, 0.15987202724401584, 0.17723622304791373,
                    0.2893065681353137, 0.7382074354778773, 2.688751301061291])
meas_aff = np.array([0.43491761136105517, 0.24010236994218648, 0.16259011278313282, 0.16946799812035018,
                     0.2747962610529283, 0.6372105239080881, 2.2369798346408842])
laplace = 0.08151298239226033


def beta(c):
    """Relative error in posterior standard deviations, beta(c) = mean_j |sqrt(s_j + c^2 p_j^2) - 1| with s_j = 1 - p_j."""
    c = np.atleast_1d(np.asarray(c, dtype=float))
    return np.array([np.mean(np.abs(np.sqrt(1 - p + ci ** 2 * p ** 2) - 1)) for ci in c])


def theory(c, a, b, v):
    c = np.atleast_1d(np.asarray(c, dtype=float))
    return np.sqrt(beta(c) ** 2 + a / c ** v + b * c ** 4)


def fit(meas, v):
    best = None
    for a0 in (1e-3, 1e-2, 5e-2, 1e-1):
        for b0 in (1e-5, 1e-4, 1e-3):
            r = least_squares(lambda th: theory(radii, *np.exp(th), v) - meas, np.log([a0, b0]))
            if best is None or r.cost < best.cost:
                best = r
    a, b = np.exp(best.x)
    return a, b, float(np.sqrt(np.mean(best.fun ** 2)))


a0, b0, rms0 = fit(meas_id, 0)
a2, b2, rms2 = fit(meas_aff, 2)
print("identity head: a_0 = %.5g, b = %.5g, rms residual %.4f" % (a0, b0, rms0))
print("affine head:   a_2 = %.5g, b = %.5g, rms residual %.4f" % (a2, b2, rms2))
print("affine optimum c* = (a_2/(2b))^(1/6) = %.3f" % ((a2 / (2 * b2)) ** (1 / 6)))
print("beta(c) for c = 0.5, 1, 2, 2.44, 3: ", np.round(beta([0.5, 1, 2, 2.44, 3]), 4))

grid = np.geomspace(0.4, 16, 400)
blue, red = "#1b4f9c", "#d1495b"
fig, ax = plt.subplots(figsize=(4.4, 2.9))
ax.plot(radii, meas_id, "o", color=blue, ms=3.6, label="identity head, measured")
ax.plot(grid, theory(grid, a0, b0, 0), "-", color=blue, label="identity head, decomposition")
ax.plot(radii, meas_aff, "s", color=red, ms=3.4, label="affine head, measured")
ax.plot(grid, theory(grid, a2, b2, 2), "--", color=red, label="affine head, decomposition")
ax.plot(grid, beta(grid), ":", color="0.45", lw=1.4, label=r"localization bias $\beta(c)$")
ax.axhline(laplace, color="k", lw=0.9, label="Laplace approximation")
ax.set_xscale("log")
ax.set_yscale("log")
ax.set_xlim(0.33, 19)
ax.set_ylim(0.01, 4.0)
ax.set_xlabel(r"localization radius $c$")
ax.set_ylabel(r"$\mathcal{W}_1$ / posterior s.d.")
ax.legend(loc="upper left", ncol=1, frameon=False, handlelength=2.0, labelspacing=0.3, borderaxespad=0.3)
fig.savefig(os.path.join(OUT, "mf_radius_theory.pdf"), dpi=300)
plt.close(fig)
