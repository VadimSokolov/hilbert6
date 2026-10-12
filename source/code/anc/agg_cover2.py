"""Aggregate exp_cover2 replicates and run the comparison as the PAIRED test it is.

Both methods are scored on the same replicate and the same mode, so the exact-versus-GBC
difference is a paired comparison.  The unpaired binomial standard error sqrt(.95*.05/reps)
that the published text quoted is the wrong yardstick: it is the error of one marginal
coverage estimate, not of the difference between two coverages measured on shared data.

McNemar: let b be the number of (replicate, mode) pairs the exact posterior covers and GBC
misses, c the number GBC covers and exact misses.  The difference in coverage is (b-c)/n and
its standard error under the null is sqrt(b+c)/n.

Usage:  python3 agg_cover2.py results/cover2_rep*.json --out results/cover2_agg.json
"""
import argparse
import glob
import json

import numpy as np


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('files', nargs='*')
    ap.add_argument('--out', default='results/cover2_agg.json')
    a = ap.parse_args()

    files = a.files or sorted(glob.glob('results/cover2_rep*.json'))
    if not files:
        raise SystemExit('no cover2 replicate files found')
    runs = [json.load(open(f)) for f in files]

    for k in ('N', 'J', 'M', 'rho', 'alpha', 'c', 'k_eff', 'level'):
        vals = {r[k] for r in runs}
        if len(vals) != 1:
            raise SystemExit(f'replicates disagree on {k}: {vals}')
    h = runs[0]

    ARMS = [a for a in ('prior', 'fixed_typical', 'fixed_rough') if a in h]
    if not ARMS:
        raise SystemExit('no truth arms found; these are pre-three-arm replicate files')
    ke = h['k_eff']

    def mcnemar(Ei, Gi, reps):
        b = int(((Ei == 1) & (Gi == 0)).sum())   # exact covers, gbc misses
        c = int(((Ei == 0) & (Gi == 1)).sum())   # gbc covers, exact misses
        n = Ei.size
        diff = (b - c) / n
        se = np.sqrt(b + c) / n if (b + c) > 0 else 0.0
        z = diff / se if se > 0 else 0.0
        return dict(b=b, c=c, n=int(n), discordant=b + c, diff=float(diff),
                    se_paired=float(se), z=float(z),
                    se_unpaired=float(np.sqrt(0.95 * 0.05 / reps)))

    out = dict(N=h['N'], J=h['J'], M=h['M'], rho=h['rho'], alpha=h['alpha'], nu=h['nu'],
               T=h['T'], c=h['c'], k_eff=ke, level=h['level'], n_tasks=len(runs),
               arms=ARMS, th0_typical=h.get('th0_typical'), th0_rough=h.get('th0_rough'))

    for arm in ARMS:
        E = np.concatenate([np.asarray(r[arm]['cover_exact'], int) for r in runs])
        G = np.concatenate([np.asarray(r[arm]['cover_gbc'], int) for r in runs])
        reps, J = E.shape
        d = dict(reps=reps,
                 exact_all=float(E.mean()), gbc_all=float(G.mean()),
                 exact_informed=float(E[:, :ke].mean()),
                 gbc_informed=float(G[:, :ke].mean()),
                 per_mode_exact=E.mean(0).tolist(), per_mode_gbc=G.mean(0).tolist(),
                 se_marginal=float(np.sqrt(0.95 * 0.05 / reps)),
                 paired_all=mcnemar(E, G, reps),
                 paired_informed=mcnemar(E[:, :ke], G[:, :ke], reps))
        out[arm] = d

    # the figure and the generated prose read the prior arm, which is the published design
    out.update({k: out['prior'][k] for k in
                ('reps', 'exact_all', 'gbc_all', 'exact_informed', 'gbc_informed',
                 'per_mode_exact', 'per_mode_gbc', 'se_marginal',
                 'paired_all', 'paired_informed')})
    out['J'] = h['J']
    json.dump(out, open(a.out, 'w'), indent=1)

    print(f"{len(runs)} tasks, arms: {', '.join(ARMS)}")
    for arm in ARMS:
        d = out[arm]
        t = d['paired_all']
        print(f"\n[{arm}]  {d['reps']} replicates x {out['J']} modes = {t['n']} pairs")
        print(f"  exact  all {d['exact_all']:.4f}   informed {d['exact_informed']:.4f}")
        print(f"  gbc    all {d['gbc_all']:.4f}   informed {d['gbc_informed']:.4f}")
        print(f"  paired b={t['b']} c={t['c']} discordant={t['discordant']} of {t['n']}: "
              f"diff {t['diff']:+.5f}, SE {t['se_paired']:.5f}, z = {t['z']:+.2f} "
              f"(unpaired SE would be {t['se_unpaired']:.5f})")
    print("\nwrote", a.out)


if __name__ == '__main__':
    main()
