"""Figure mf_nls: information blocks Theta_p(T) of the cubic NLS linearized about a plane wave (Bogoliubov system).

Chapter on examples, section on nondissipative equations: Proposition on the information operator about a plane wave.
Run from this folder: python3 mf_nls.py   (writes ../figures/mf_nls.pdf).

Provenance. This is the script fig_nls_bogoliubov.py of the 92 page paper (code archive of the paper), with the numerical core
unchanged and the plotting rebuilt for a figure of 4.6 in width with text at 6.5 to 8 pt: no title, serif text, a legend that does not
cover the curves, a logarithmic wave number axis, and the smaller eigenvalue of every block drawn as a pale curve of the same style
(as in the original, where the pale curve was not mentioned in the caption).
The numbers are those of the original. Two changes of labels only:
  * the horizontal axis of the left panel is the wave number |k| (an integer) with p = 2 pi k, so that |p|^2 = lambda_p = 4 pi^2 |k|^2
    is the eigenvalue of -Delta; the original printed this axis as |p|, which was the integer k;
  * the right panel states its parameters: kappa a^2 = -0.6 lambda_1, and |p|^2/(2|kappa|a^2) = 0.2, 0.5, 0.9 (values of |p|^2 inside
    the unstable band; none of them is an eigenvalue of the unit torus, whose only unstable mode |k| = 1 has the ratio 0.83).
The caption of the chapter quotes the numbers printed by the last lines of this script.
"""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "figures")
plt.rcParams.update({"font.family": "serif", "mathtext.fontset": "stix", "font.size": 8, "axes.linewidth": 0.6,
                     "lines.linewidth": 1.0, "xtick.labelsize": 7, "ytick.labelsize": 7, "legend.fontsize": 6.5,
                     "legend.title_fontsize": 6.5, "axes.labelsize": 8, "savefig.bbox": "tight", "pdf.fonttype": 42})

tr = np.trapezoid


def info(p2, ka2, T=1.0, n=4000):
    """Theta_p(T) = int_0^T M_p(t)^T M_p(t) dt for the 2x2 Bogoliubov propagator.
    p2 = |p|^2 = lambda_p (the eigenvalue of -Delta at the mode), ka2 = kappa a^2 (defocusing > 0, focusing < 0)."""
    w2 = p2 * (p2 + 2 * ka2)
    ts = np.linspace(0, T, n)
    if w2 > 0:
        w = np.sqrt(w2); c = np.cos(w * ts); s = np.sin(w * ts); r = w / p2
        M = np.array([[c, (1 / r) * s], [-r * s, c]])
    else:
        g = np.sqrt(-w2); c = np.cosh(g * ts); s = np.sinh(g * ts); r = g / p2
        M = np.array([[c, (1 / r) * s], [r * s, c]])
    I = np.zeros((2, 2))
    for i in range(2):
        for j in range(2):
            I[i, j] = tr(np.sum(M[:, i, :] * M[:, j, :], axis=0), ts)
    return I


ks = np.arange(1, 41)
lam = lambda k: 4 * np.pi ** 2 * k ** 2   # eigenvalue of -Delta on the unit torus at wave number |k|

fig, ax = plt.subplots(1, 2, figsize=(4.6, 2.15), gridspec_kw={"wspace": 0.42})
cases = [(0.0, "k-", "free"), (20.0, "b--", r"defocusing, $\kappa a^2=20$"), (-20.0, "r-.", r"focusing, $\kappa a^2=-20$")]
for ka2, ls, lab in cases:
    ev = np.array([np.linalg.eigvalsh(info(lam(k), ka2)) for k in ks])
    ax[0].semilogy(ks, ev[:, 1], ls, marker="o", ms=1.8, markevery=list(range(6)), label=lab)
    ax[0].semilogy(ks, ev[:, 0], ls, marker="o", ms=1.8, markevery=list(range(6)), alpha=0.35)
ax[0].set_xscale("log")
ax[0].set_xticks([1, 2, 4, 8, 16, 32])
ax[0].set_xticklabels(["1", "2", "4", "8", "16", "32"])
ax[0].set_xlim(0.9, 45)
ax[0].set_xlabel(r"wave number $|k|$")
ax[0].set_ylabel(r"eigenvalues of $\Theta_p(T)$, $T=1$")
ax[0].legend(loc="upper right", frameon=False, handlelength=2.2)

Ts = np.linspace(0.05, 3, 60)
ka2 = -0.6 * lam(1)
for frac, ls in [(0.2, "-"), (0.5, "--"), (0.9, "-.")]:
    p2 = frac * 2 * abs(ka2)
    ax[1].semilogy(Ts, [np.linalg.eigvalsh(info(p2, ka2, T=t))[1] for t in Ts], ls, label="%.1f" % frac)
ax[1].plot(Ts, Ts, "k:", label=r"$T$ (free)")
ax[1].set_xlabel(r"$T$")
ax[1].set_ylabel("largest eigenvalue of $\\Theta_p(T)$")
ax[1].legend(loc="upper left", frameon=False, title=r"$|p|^2/(2|\kappa|a^2)$", handlelength=2.2)
ax[1].set_ylim(1e-1, 1e64)
ax[1].set_yticks([1e0, 1e15, 1e30, 1e45, 1e60])
for a in ax:
    a.tick_params(length=2.5, width=0.5)
    a.spines["top"].set_visible(False)
    a.spines["right"].set_visible(False)
os.makedirs(OUT, exist_ok=True)
fig.savefig(os.path.join(OUT, "mf_nls.pdf"))

# numbers quoted in the caption of the chapter
print("free case: Theta_p(T) = T Id; at T = 1:", np.round(info(lam(3), 0.0), 6).tolist())
for k in [1, 2, 4, 8, 16]:
    print("|k| =", k, "defocusing", np.round(np.linalg.eigvalsh(info(lam(k), 20.0)), 4),
          "focusing", np.round(np.linalg.eigvalsh(info(lam(k), -20.0)), 4))
print("focusing band: lambda_1 = %.4f < 2|kappa|a^2 = 40" % lam(1))
