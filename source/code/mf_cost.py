"""Figure mf_cost: error against cost for GBC and pCN, and per mode coverage over replicates, heat equation.

Part IV, chapter on examples, section on the experiments (label m:fig:cost).
Run from this folder: python3 mf_cost.py   (reads anc/results/study2_agg.json, anc/results/cover2_agg.json and the twenty recorded replicate files
anc/results/cover2_rep1.json to cover2_rep20.json, writes ../figures/mf_cost.pdf).

Provenance. Rebuilt from fig_cost.py of the code archive of the 92 page paper (archive copy: anc/fig_cost.py in this folder). The data are the
recorded aggregates of that archive (copies: anc/results/study2_agg.json from exp_study2.py and agg_study2.py, and anc/results/cover2_agg.json from
exp_cover2.py and agg_cover2.py); nothing that is drawn is recomputed. As in the archive script, the left panel (here the upper panel) plots the GBC series
study2_agg.json["gbc"]["local"] and the pCN series study2_agg.json["pcn"], and the right panel (here the lower panel) plots the prior drawn arm
of cover2_agg.json, which is the arm the archive script reads at its top level.
What changed: (1) the two panels are stacked, at 4.6 in by 4.2 in with text at 7 to 7.5 pt; the original is 6.4 in by 2.4 in, which a 4.6 in column
would scale to type of about 5 pt; (2) the legend of the original called the GBC series "Algorithm 1", but the series is the localized generator
(Algorithm alg:loc of the paper, radius c = 2, with the centering and rescaling of its Corollary locG; see gbc_learn(arm="local") in anc/exp_study2.py), so
the legend now says plain "GBC" and the caption of the chapter names the variant (Algorithm alg:loc, c = 2); (3) the label of the plotted quantity says
what it is, the worst mode relative error of the posterior standard deviation (sd_err_rel is a maximum over the retained modes, not an average, as
anc/README.txt says), averaged over the 40 replicates; (4) the k_eff label, which the original drew on top of a bar at the foot of the right panel, is
moved to the top; the legend of the right panel states that the shaded band is the nominal level plus or minus two binomial standard errors; (5) the
ordinate label of the right panel names the arm, which the original did not; (6) the upper limit of the upper panel is raised to 1 so that the label
of the first pCN point stays inside the frame. The numbers drawn are identical. The script prints the values that the caption of the chapter states.

(7) The paired test of the coverage study is recomputed with the replicate as the unit. agg_cover2.py applies McNemar's test to the 2400
(replicate, mode) pairs of an arm as if they were independent, but the eight modes of a replicate are computed from the same data; the replicates
are independent. For replicate r let x_r be the number of modes that the exact posterior covers and GBC misses minus the number that GBC covers and
the exact posterior misses. The script reads the per replicate coverage indicators of the twenty recorded task files, checks that they reproduce
the coverages and the discordant counts of cover2_agg.json, and prints for each arm the clustered McNemar statistic z = sum x_r / sqrt(sum x_r^2)
(Durkalski, Palesch, Lipsitz and Rust, Statistics in Medicine 22 (2003) 2417 to 2428, for clusters of equal size), the exact two sided p value of
the sign flip test over the replicates (the 2^m sign patterns of the m nonzero x_r, equally likely when the two methods are exchangeable within a
replicate; with at most one discordant pair per replicate this is McNemar's exact test), the standard error sqrt(sum x_r^2)/2400 of the coverage
difference and, for comparison, the binomial standard error sqrt(0.95 x 0.05/300) of the coverage of one mode and the standard error of the
difference of the all mode coverages of two methods run on independent data, sqrt((var e_r + var g_r)/300), where e_r and g_r are the fractions of
the modes of replicate r that the two methods cover. The pooled statistic of agg_cover2.py is printed alongside for the record.
"""
import glob
import itertools
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

S = json.load(open(os.path.join(HERE, "anc", "results", "study2_agg.json")))
C = json.load(open(os.path.join(HERE, "anc", "results", "cover2_agg.json")))
G, P = S["gbc"]["local"], S["pcn"]
gs, gm, ge = (np.array(G["solves"], float), np.array(G["sd_err_rel"]["mean"], float), np.array(G["sd_err_rel"]["se"], float))
ps, pm, pe = (np.array(P["solves"], float), np.array(P["sd_err_rel"]["mean"], float), np.array(P["sd_err_rel"]["se"], float))
es = np.array(P["ess_min"], float)
RM = S["ratio_measured"]["local"]["sd_err_rel"]
arm = C["prior"]
blue, red, grey, green = "#1b4f9c", "#d1495b", "0.55", "#2a8f5a"

fig, (ax0, ax1) = plt.subplots(2, 1, figsize=(4.6, 4.2), constrained_layout=True,
                               gridspec_kw={"height_ratios": [1.0, 0.95]})

# upper panel: error of the estimated posterior standard deviations against the number of linearized solves
ax0.axhspan(RM["err_lo"], RM["err_hi"], color="C2", alpha=0.15, lw=0, zorder=0)
ax0.errorbar(gs, gm, yerr=ge, fmt="o-", color=blue, ms=3, lw=1.0, capsize=1.5, elinewidth=0.7,
             label=r"GBC, slope $%.2f$" % G["sd_err_rel"]["slope"])
ax0.errorbar(ps, pm, yerr=pe, fmt="s-", color=red, ms=3, lw=1.0, capsize=1.5, elinewidth=0.7,
             label=r"pCN, slope $%.2f$" % P["sd_err_rel"]["slope"])
for x, y, e in zip(ps, pm, es):      # mixing behind each pCN point: the small budgets have not converged
    ax0.annotate("ESS %.0f" % e, (x, y), textcoords="offset points", xytext=(4, 4), fontsize=7, color=red,
                 ha="left", va="bottom")
ax0.set_xscale("log")
ax0.set_yscale("log")
ax0.set_xlim(300, 8e6)
ax0.set_ylim(top=1.0)
ax0.set_xlabel("linearized solves")
ax0.set_ylabel("worst mode relative error\nof posterior sd")
ax0.grid(alpha=0.3, which="major", lw=0.4)
ax0.legend(loc="lower left", frameon=False, handlelength=1.8)
ax0.text(2.6e3, np.sqrt(RM["err_lo"] * RM["err_hi"]), "band both methods reached", fontsize=7, color="0.2", va="center")

# lower panel: per mode coverage of nominal 95% intervals, prior drawn arm, exact posterior against GBC
k = np.arange(1, len(arm["per_mode_exact"]) + 1)
w = 0.38
ax1.bar(k - w / 2, arm["per_mode_exact"], w, color=grey, label="exact posterior")
ax1.bar(k + w / 2, arm["per_mode_gbc"], w, color=blue, label="GBC")
se = arm["se_marginal"]
ax1.axhspan(0.95 - 2 * se, 0.95 + 2 * se, color="k", alpha=0.07, lw=0, zorder=0, label=r"nominal level $\pm2$ s.e.")
ax1.axhline(0.95, ls="--", color="k", lw=0.8)
ax1.axvline(C["k_eff"] + 0.5, ls=":", color=green, lw=1.1, zorder=1)
ax1.set_ylim(0.88, 1.03)
ax1.set_yticks([0.88, 0.90, 0.92, 0.94, 0.96, 0.98, 1.00])
ax1.set_xlabel("mode $|k|$")
ax1.set_ylabel("coverage of 95%% intervals\n(prior drawn truth, %d replicates)" % arm["reps"])
ax1.set_xticks(k)
ax1.grid(alpha=0.3, axis="y", lw=0.4)
ax1.legend(loc="upper center", frameon=True, framealpha=1.0, edgecolor="none", ncol=3, handlelength=1.2,
           columnspacing=1.2, borderpad=0.2)
ax1.annotate(r"$k_{\rm eff}$", (C["k_eff"] + 0.5, 0.972), textcoords="offset points", xytext=(3, 0), fontsize=7.5,
             color=green, va="center")

os.makedirs(OUT, exist_ok=True)
fig.savefig(os.path.join(OUT, "mf_cost.pdf"))



def clustered_test(E, G, level=0.95):
    """Exact posterior (E) against GBC (G), coverage indicators with replicates in rows and modes in columns; the replicate is the unit."""
    R, J = E.shape
    b_r = ((E == 1) & (G == 0)).sum(1)            # modes the exact posterior covers and GBC misses, per replicate
    c_r = ((E == 0) & (G == 1)).sum(1)            # modes GBC covers and the exact posterior misses, per replicate
    x = b_r - c_r
    s, ss, n = int(x.sum()), int((x ** 2).sum()), R * J
    nz = np.abs(x[x != 0])
    if len(nz):                                   # exact sign flip test: all 2^m sign patterns of the m nonzero x_r
        tot = np.array([np.dot(sg, nz) for sg in itertools.product((-1, 1), repeat=len(nz))])
        p = float(np.mean(np.abs(tot) >= abs(s)))
    else:
        p = 1.0
    e, g = E.mean(1), G.mean(1)
    b, c = int(b_r.sum()), int(c_r.sum())
    return dict(b=b, c=c, n=n, reps=R, reps_disc=int(((b_r + c_r) > 0).sum()), reps_nonzero=int(len(nz)), sum_x=s, sum_x2=ss,
                diff=s / n, se=np.sqrt(ss) / n, z=s / np.sqrt(ss) if ss else 0.0, p=p,
                se_sandwich=float(np.std(x / J, ddof=1) / np.sqrt(R)),
                se_one_mode=float(np.sqrt(level * (1 - level) / R)),
                se_unpaired=float(np.sqrt((e.var(ddof=1) + g.var(ddof=1)) / R)),
                z_pooled=(b - c) / np.sqrt(b + c) if b + c else 0.0)


files = sorted(glob.glob(os.path.join(HERE, "anc", "results", "cover2_rep*.json")),
               key=lambda f: int(os.path.basename(f)[len("cover2_rep"):-len(".json")]))
runs = [json.load(open(f)) for f in files]
if len(runs) != C["n_tasks"]:
    raise SystemExit("expected %d replicate files, found %d" % (C["n_tasks"], len(runs)))
T = {}
for name in C["arms"]:
    E = np.concatenate([np.asarray(r[name]["cover_exact"], int) for r in runs])
    Gc = np.concatenate([np.asarray(r[name]["cover_gbc"], int) for r in runs])
    T[name] = t = clustered_test(E, Gc, C["level"])
    a = C[name]
    ok = (E.shape == (a["reps"], C["J"]) and abs(E.mean() - a["exact_all"]) < 1e-12 and abs(Gc.mean() - a["gbc_all"]) < 1e-12
          and abs(E[:, :C["k_eff"]].mean() - a["exact_informed"]) < 1e-12 and abs(Gc[:, :C["k_eff"]].mean() - a["gbc_informed"]) < 1e-12
          and (t["b"], t["c"]) == (a["paired_all"]["b"], a["paired_all"]["c"]))
    if not ok:
        raise SystemExit("the replicate files do not reproduce cover2_agg.json for the arm %s" % name)

# the values that the captions and the text state
RF = S["ratio_measured"]["local"]["cov_rel_fro"]
A = T["prior"]
print("GBC M = %d to %d, pCN solves %.1e to %.1e, replicates %d" % (G["M"][0], G["M"][-1], ps[0], ps[-1], S["reps"]))
print("fitted slopes: GBC %.3f, pCN %.3f (converged budgets only)" % (G["sd_err_rel"]["slope"], P["sd_err_rel"]["slope"]))
print("band both reached: %.4f down to %.4f; pCN needs %.0f to %.0f times as many solves" % (RM["err_hi"], RM["err_lo"], RM["ratio_min"], RM["ratio_max"]))
print("relative Frobenius error of the covariance: band both reached %.4f down to %.4f; pCN needs %.0f to %.0f times as many solves" %
      (RF["err_hi"], RF["err_lo"], RF["ratio_min"], RF["ratio_max"]))
print("coverage: %d replicates, k_eff %d; prior drawn arm: %d pairs against %d out of %d, in %d replicates, difference %.4f, z %.2f" %
      (A["reps"], C["k_eff"], A["b"], A["c"], A["n"], A["reps_disc"], abs(A["diff"]), abs(A["z"])))
print("paired test with the replicate as the unit (the replicate files reproduce cover2_agg.json):")
for name in C["arms"]:
    t, a = T[name], C[name]
    print("  arm %-14s coverage all %.3f/%.3f, informed %.3f/%.3f; b/c = %d/%d of %d, in %d replicates, %d with x_r nonzero; sum x_r %+d, sum x_r^2 %d"
          % (name, a["exact_all"], a["gbc_all"], a["exact_informed"], a["gbc_informed"], t["b"], t["c"], t["n"], t["reps_disc"],
             t["reps_nonzero"], t["sum_x"], t["sum_x2"]))
    print("      difference %+.5f, se %.5f (sandwich %.5f), z = %+.2f, exact two sided p = %.4f; pooled z of agg_cover2.py %+.2f"
          % (t["diff"], t["se"], t["se_sandwich"], t["z"], t["p"], t["z_pooled"]))
    print("      se of one mode's coverage %.5f, ratio %.1f; se of the all mode difference on independent data %.5f, ratio %.1f"
          % (t["se_one_mode"], t["se_one_mode"] / t["se"], t["se_unpaired"], t["se_unpaired"] / t["se"]))
big = max(T, key=lambda k: abs(T[k]["z"]))
print("largest |z| %.2f (arm %s, exact p %.3f); largest coverage difference %.4f; ratios to one mode's se %.1f to %.1f, to the unpaired se %.1f to %.1f" %
      (abs(T[big]["z"]), big, T[big]["p"], max(abs(t["diff"]) for t in T.values()),
       min(t["se_one_mode"] / t["se"] for t in T.values()), max(t["se_one_mode"] / t["se"] for t in T.values()),
       min(t["se_unpaired"] / t["se"] for t in T.values()), max(t["se_unpaired"] / t["se"] for t in T.values())))
