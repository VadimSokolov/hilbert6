"""Figure 2: the finite-N check for the heat equation, before and after calibration.

Driven entirely by results/paper_figs.json so the figure cannot disagree with
Section "Experiments".  Writes paper/fig_heat_gbc.pdf.
"""
import json
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(HERE, 'results/paper_figs.json')))
pub, cal = d['published'], d['calibrated_N2000']
k = np.arange(1, pub['kmax'] + 1)

fig, ax = plt.subplots(1, 3, figsize=(13.2, 3.5))

for a, b, ttl in ((ax[0], pub, r'Uncalibrated prior, $\rho=1$'),
                  (ax[1], cal, rf"Calibrated, $\rho={d['rho_calibrated']:.0f}$")):
    th0 = np.array(b['theta0'])
    m = np.array(b['mean'])
    sd = np.array(b['sd'])
    a.plot(k, th0, 'ko', ms=3.5, label=r'truth $\theta_0$', zorder=3)
    a.errorbar(k, m, yerr=2 * sd, fmt='r.', ms=3.5, elinewidth=1,
               label=r'posterior mean $\pm2$ s.d.', zorder=2)
    if b['k_eff'] > 0:
        a.axvline(b['k_eff'] + 0.5, ls=':', color='C2', lw=1.2)
        a.text(b['k_eff'] + 0.7, a.get_ylim()[1] * 0.78, r'$k_{\rm eff}$', color='C2', fontsize=8)
    if b['k_eff'] > 0:
        # k_eff is small, so report counts: a ratio out of two or three intervals
        # is not a coverage probability, and the replicate study is what supports one
        ni = int(round(b['cover2_informed'] * b['k_eff']))
        na = int(round(b['cover2_all'] * b['kmax']))
        sub = (rf"$k_{{\rm eff}}={b['k_eff']}$: {ni} of {b['k_eff']} informed modes covered"
               rf" ({na} of {b['kmax']} overall)")
    else:
        na = int(round(b['cover2_all'] * b['kmax']))
        sub = rf"$k_{{\rm eff}}=0$: no mode is data-dominated, {na} of {b['kmax']} modes covered"
    a.set_title(ttl + "\n" + sub, fontsize=8.5)
    a.set_xlabel(r'mode $k$')
    a.legend(fontsize=8, frameon=False)
    a.grid(alpha=.3, lw=.4)
ax[0].set_ylabel(r'$\theta_k$')

ax[2].semilogy(k, pub['sd'], 'o', ms=3.5, color='C7', label=r'exact s.d., $\rho=1$')
ax[2].semilogy(k, cal['sd'], 'o', ms=3.5, color='C3', label=rf"exact s.d., $\rho={d['rho_calibrated']:.0f}$")
NU, T, al = d['nu'], d['T'], d['alpha']
lam = 4 * np.pi ** 2 * k ** 2
iota = (1 - np.exp(-2 * NU * lam * T)) / (2 * NU * lam * T)
for rho, c, lab in ((1.0, 'C7', None), (d['rho_calibrated'], 'C3', None)):
    ax[2].semilogy(k, 1 / np.sqrt(cal['N'] * iota + lam ** al / rho ** 2), '-', color=c, lw=1)
ax[2].axvline(cal['k_eff'] + 0.5, ls=':', color='C2', lw=1.2)
ax[2].set_xlabel(r'mode $k$')
ax[2].set_ylabel('posterior s.d.')
ax[2].set_title(r'Exact s.d. against $(N\iota_k+\rho^{-2}\lambda_k^\alpha)^{-1/2}$' + '\n(lines: prediction)', fontsize=9)
ax[2].legend(fontsize=8, frameon=False)
ax[2].grid(alpha=.3, which='both', lw=.4)

fig.tight_layout()
out = os.path.join(HERE, '../paper/fig_heat_gbc.pdf')
fig.savefig(out, bbox_inches='tight')
print('wrote', out)
print(f"published : k_eff={pub['k_eff']}, coverage={pub['cover2_all']:.2f}, max|z|={pub['max_absz_all']:.1f}")
print(f"calibrated: k_eff={cal['k_eff']}, coverage(informed)={cal['cover2_informed']:.2f}, max|z| informed={cal['max_absz_informed']:.2f}")
