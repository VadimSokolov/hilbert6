"""Figure mf_heat_gbc: the finite N check for the heat equation on T^1, before and after calibration of the prior scale.

Part IV, chapter on examples, section on the heat equation (label m:fig:heatgbc).
Run from this folder: python3 mf_heat_gbc.py   (reads anc/results/paper_figs.json, writes ../figures/mf_heat_gbc.pdf).

Provenance. Rebuilt from fig_heat_gbc.py of the code archive of the 92 page paper (archive copy: anc/fig_heat_gbc.py in this folder).
The data are the recorded run results/paper_figs.json of that archive (copy: anc/results/paper_figs.json); nothing is recomputed except
the closed form prediction (N iota_k + rho^-2 lambda_k^alpha)^(-1/2) with iota_k = (1 - exp(-2 nu lambda_k T)) / (2 nu lambda_k T),
lambda_k = 4 pi^2 k^2, as in the archive script. The same two settings are drawn (published: rho = 1; calibrated_N2000: rho = 124.03).
What changed: the three panels of the original (13.2 in by 3.5 in, scaled by about one third in a 4.6 in column) are arranged as two
panels on top and one wide panel below at 4.6 in by 3.75 in, with text at 7 to 8 pt, panel letters instead of the words left, center and right,
the titles of panels (a) and (b) set over three lines, and the title of the third panel (the prediction formula) moved to the caption with a legend entry
"prediction (lines)". The numbers are identical.
The script prints the values that the caption of the chapter states.
"""
import json
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "figures")
plt.rcParams.update({"font.family": "serif", "mathtext.fontset": "stix", "font.size": 7.5,
                     "axes.linewidth": 0.6, "lines.linewidth": 1.0, "xtick.labelsize": 7, "ytick.labelsize": 7,
                     "legend.fontsize": 7, "axes.labelsize": 7.5, "axes.titlesize": 7.5, "pdf.fonttype": 42})

d = json.load(open(os.path.join(HERE, "anc", "results", "paper_figs.json")))
pub, cal = d["published"], d["calibrated_N2000"]
k = np.arange(1, pub["kmax"] + 1)
rho_cal = d["rho_calibrated"]

fig = plt.figure(figsize=(4.6, 3.75), constrained_layout=True)
gs = fig.add_gridspec(2, 2, height_ratios=[1.0, 0.78])
axa = fig.add_subplot(gs[0, 0])
axb = fig.add_subplot(gs[0, 1], sharey=axa)
axc = fig.add_subplot(gs[1, :])

for ax, b, ttl, letter in ((axa, pub, r"Uncalibrated prior, $\rho=1$", "(a)"),
                           (axb, cal, rf"Calibrated, $\rho={rho_cal:.0f}$", "(b)")):
    th0 = np.array(b["theta0"])
    m = np.array(b["mean"])
    sd = np.array(b["sd"])
    ax.plot(k, th0, "ko", ms=2.6, label=r"truth $\theta_0$", zorder=3)
    ax.errorbar(k, m, yerr=2 * sd, fmt="r.", ms=2.6, elinewidth=0.8, capsize=0,
                label=r"posterior mean $\pm2$ s.d.", zorder=2)
    if b["k_eff"] > 0:
        ax.axvline(b["k_eff"] + 0.5, ls=":", color="C2", lw=1.0)
        ax.text(b["k_eff"] + 0.9, 0.30, r"$k_{\rm eff}$", color="C2", fontsize=7)
        ni = int(round(b["cover2_informed"] * b["k_eff"]))
        na = int(round(b["cover2_all"] * b["kmax"]))
        sub = (rf"$k_{{\rm eff}}={b['k_eff']}$: {ni} of {b['k_eff']} informed" + "\n"
               + rf"modes covered ({na} of {b['kmax']} overall)")
    else:
        na = int(round(b["cover2_all"] * b["kmax"]))
        sub = rf"$k_{{\rm eff}}=0$: no mode is data dominated," + "\n" + rf"{na} of {b['kmax']} modes covered"
    ax.set_title(ttl + "\n" + sub, fontsize=7, loc="left", pad=3)
    ax.set_xlabel(r"mode $k$")
    ax.set_xticks([1, 5, 10, 15, 20])
    ax.legend(loc="upper right", frameon=False, handletextpad=0.3, borderaxespad=0.2)
    ax.grid(alpha=0.3, lw=0.4)
    ax.text(0.02, 0.02, letter, transform=ax.transAxes, fontsize=8, va="bottom", ha="left")
axa.set_ylabel(r"$\theta_k$")

axc.semilogy(k, pub["sd"], "o", ms=2.6, color="C7", label=r"exact s.d., $\rho=1$")
axc.semilogy(k, cal["sd"], "o", ms=2.6, color="C3", label=rf"exact s.d., $\rho={rho_cal:.0f}$")
NU, T, al = d["nu"], d["T"], d["alpha"]
lam = 4 * np.pi ** 2 * k ** 2
iota = (1 - np.exp(-2 * NU * lam * T)) / (2 * NU * lam * T)
for rho, c in ((1.0, "C7"), (rho_cal, "C3")):
    axc.semilogy(k, 1 / np.sqrt(cal["N"] * iota + lam ** al / rho ** 2), "-", color=c, lw=0.9)
axc.plot([], [], "-", color="k", lw=0.9, label="prediction (lines)")
axc.axvline(cal["k_eff"] + 0.5, ls=":", color="C2", lw=1.0)
axc.set_xlabel(r"mode $k$")
axc.set_xticks([1, 5, 10, 15, 20])
axc.set_ylabel("posterior s.d.")
axc.set_ylim(top=0.2)
axc.legend(loc="upper right", frameon=False, handletextpad=0.4, borderaxespad=0.3)
axc.grid(alpha=0.3, which="major", lw=0.4)
axc.text(0.02, 0.04, "(c)", transform=axc.transAxes, fontsize=8, va="bottom", ha="left")

os.makedirs(OUT, exist_ok=True)
fig.savefig(os.path.join(OUT, "mf_heat_gbc.pdf"))

print("published : k_eff=%d, coverage(all)=%.2f, max|z|=%.1f, max truth in prior s.d.=%.1f, BvM max rel=%.3g"
      % (pub["k_eff"], pub["cover2_all"], pub["max_absz_all"], pub["max_truth_in_prior_sd"], pub["bvm_max_rel"]))
print("calibrated: rho=%.2f, k_eff=%d, coverage(informed)=%.2f, coverage(all)=%.2f, max|z| informed=%.2f, BvM max rel=%.3g"
      % (rho_cal, cal["k_eff"], cal["cover2_informed"], cal["cover2_all"], cal["max_absz_informed"], cal["bvm_max_rel"]))
