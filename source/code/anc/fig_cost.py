"""Error against cost for GBC and pCN, and per-mode coverage over replicates.

Reads results/study2_agg.json (from exp_study2.py via agg_study2.py) and, when present,
results/cover2_agg.json (from exp_cover2.py via agg_cover2.py); writes paper/fig_cost.pdf.

The left panel plots the error of the estimated posterior standard deviations, not of the
mean.  In this linear-Gaussian model prop:linsuff makes the mean map analytic, so the mean
error is exactly zero at every budget and plotting it shows only the sampling noise of
however many output draws were taken.  Plotting the mean would therefore show noise, not
accuracy, so the panel plots the standard-deviation error only.
"""
import json
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(__file__)
S = json.load(open(os.path.join(HERE, 'results/study2_agg.json')))
CP = os.path.join(HERE, 'results/cover2_agg.json')
cov = json.load(open(CP)) if os.path.exists(CP) else None
if cov is None:                      # fall back to the marginal-only study while it runs
    cov = json.load(open(os.path.join(HERE, 'results/study.json')))['coverage']
    cov = dict(cov, per_mode_exact=cov['exact_by_mode'], per_mode_gbc=cov['gbc_by_mode'],
               se_marginal=float(np.sqrt(0.95 * 0.05 / cov['reps'])), paired_all=None)

G, P, PM = S['gbc']['local'], S['pcn'], S['published_metric']
gs = np.array(G['solves'], float)
gm = np.array(G['sd_err_rel']['mean'], float)
ge = np.array(G['sd_err_rel']['se'], float)
ps = np.array(P['solves'], float)
pm = np.array(P['sd_err_rel']['mean'], float)
pe = np.array(P['sd_err_rel']['se'], float)
es = np.array(P['ess_min'], float)
RM = S['ratio_measured']['local']['sd_err_rel']

fig, ax = plt.subplots(1, 2, figsize=(6.5, 2.5))

# ---- the band of accuracy both methods actually reached; the ratio is read off inside it
ax[0].axhspan(RM['err_lo'], RM['err_hi'], color='C2', alpha=.13, lw=0, zorder=0,
              label=f"band both reached: {RM['ratio_min']:.0f}$\\times$ to "
                    f"{RM['ratio_max']:.0f}$\\times$ fewer solves")

ax[0].errorbar(gs, gm, yerr=ge, fmt='o-', color='C0', ms=4, lw=1.3, capsize=2,
               label=f"GBC (Algorithm 1), slope {G['sd_err_rel']['slope']:.2f}")
ax[0].errorbar(ps, pm, yerr=pe, fmt='s-', color='C3', ms=4, lw=1.3, capsize=2,
               label=f"pCN, slope {P['sd_err_rel']['slope']:.2f}")

# mixing behind each pCN point: the small budgets have not converged
for x, y, e in zip(ps, pm, es):
    ax[0].text(x, y * 0.70, f'ESS {e:.0f}', color='C3', fontsize=6,
               ha='center', va='top', alpha=.85)

ax[0].set_xscale('log'); ax[0].set_yscale('log')
ax[0].set_xlim(gs[0] * 0.35, ps[-1] * 2.5)
ax[0].set_xlabel('linearised solves', fontsize=8)
ax[0].set_ylabel('error of posterior sd (relative)', fontsize=8)
ax[0].set_title('Error against cost', fontsize=9)
ax[0].legend(fontsize=6.5, frameon=False, loc='lower left')
ax[0].tick_params(labelsize=7)
ax[0].grid(alpha=.3, which='both', lw=.4)

# ---- right panel: per-mode coverage
pe_m = np.asarray(cov['per_mode_exact'], float)
pg_m = np.asarray(cov['per_mode_gbc'], float)
k = np.arange(1, len(pe_m) + 1)
w = 0.38
ax[1].bar(k - w / 2, pe_m, w, label='exact posterior', color='C7')
ax[1].bar(k + w / 2, pg_m, w, label='GBC', color='C0')
se = float(cov['se_marginal'])
ax[1].axhspan(0.95 - 2 * se, 0.95 + 2 * se, color='k', alpha=.07, lw=0, zorder=0,
              label=f'nominal $\\pm2$ s.e. ({2 * se:.3f})')
ax[1].axhline(0.95, ls='--', color='k', lw=1)
ax[1].axvline(cov['k_eff'] + 0.5, ls=':', color='C2', lw=1.2)
ax[1].text(cov['k_eff'] + 0.62, 0.883, r'$k_{\rm eff}$', color='C2', fontsize=7.5, va='bottom')
ax[1].set_ylim(0.88, 1.0)
ax[1].set_xlabel('mode $|k|$', fontsize=8)
ax[1].set_ylabel(f"coverage over {cov['reps']} replicates", fontsize=8)
ax[1].set_title('Coverage of nominal 95% intervals', fontsize=9)
ax[1].set_xticks(k)
ax[1].legend(fontsize=6.5, frameon=False, loc='upper left', ncol=1)
ax[1].tick_params(labelsize=7)
ax[1].grid(alpha=.3, axis='y', lw=.4)

fig.tight_layout()
out = os.path.join(HERE, '../paper/fig_cost.pdf')
fig.savefig(out, bbox_inches='tight')
print('wrote', out)
