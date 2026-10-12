"""Aggregate exp_study2 replicates: honest error-against-cost curves for GBC and pCN.

The published curve scored GBC's mean against the exact posterior mean while the code set
that mean to the exact one by direct inversion, so its expectation was exactly zero and the
measurement could only see output sampling noise.  It therefore showed a floor where none
exists.  Here the mean is not handed to the method: the 'scale' arm estimates only the D x D
covariance from M simulations, 'local' adds the cor:locG rescaling, 'learned' regresses theta
on the summary, and the metrics are analytic (no draw noise at all).

published_metric reproduces the old measurement so the artifact can be shown side by side.

Usage:  python3 agg_study2.py --out results/study2_agg.json
"""
import argparse
import glob
import json

import numpy as np

METRICS = ('sd_err_rel', 'cov_rel_fro', 'w2_psd', 'mean_err_psd')


def exactly_zero(Y):
    """True when the metric vanishes identically, not merely to numerical tolerance.

    In the linear-Gaussian model prop:linsuff makes the mean map analytic, so the mean error
    is exactly zero at every simulation budget: there is nothing to fit a rate to.  The
    published curve measured this same quantity from finite draws and saw the Monte Carlo
    noise of that sampling instead, which is the whole of the reported floor.
    """
    return bool((Y == 0.0).all())


def slope_with_se(x, Y):
    """log-log slope of the replicate-mean curve, with an SE from a replicate bootstrap.

    Y is (reps, budgets).  The SE is over replicates, refitting the slope on each, so it
    reflects how much the fitted rate itself moves from one data set to another.
    """
    lx = np.log(x)
    per = np.array([np.polyfit(lx, np.log(y), 1)[0] for y in Y])
    fit = np.polyfit(lx, np.log(Y.mean(0)), 1)
    return float(fit[0]), float(fit[1]), float(per.std(ddof=1) / np.sqrt(len(per)))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('files', nargs='*')
    ap.add_argument('--out', default='results/study2_agg.json')
    a = ap.parse_args()

    files = a.files or sorted(glob.glob('results/study2_rep*.json'))
    if not files:
        raise SystemExit('no study2 replicate files found')
    R = [json.load(open(f)) for f in files]
    h = R[0]
    out = dict(N=h['N'], J=h['J'], nu=h['nu'], T=h['T'], rho=h['rho'], alpha=h['alpha'],
               c=h['c'], k_eff=h['k_eff'], reps=len(R))

    # ---- GBC arms
    out['gbc'] = {}
    for arm in R[0]['gbc']:
        rows = [r['gbc'][arm] for r in R]
        M = np.array([x['M'] for x in rows[0]], float)
        solves = np.array([x['solves'] for x in rows[0]], float)
        arm_out = dict(M=M.tolist(), solves=solves.tolist())
        for met in METRICS:
            Y = np.array([[x[met] for x in row] for row in rows], float)
            if exactly_zero(Y):
                arm_out[met] = dict(mean=Y.mean(0).tolist(), se=[0.0] * Y.shape[1],
                                    slope=None, intercept=None, slope_se=None,
                                    exact_zero=True, n_measurements=int(Y.size))
                continue
            sl, ic, se = slope_with_se(solves, Y)
            arm_out[met] = dict(mean=Y.mean(0).tolist(),
                                se=(Y.std(0, ddof=1) / np.sqrt(len(R))).tolist(),
                                slope=sl, intercept=ic, slope_se=se, exact_zero=False)
        out['gbc'][arm] = arm_out

    # ---- the published metric, to display the artifact
    rows = [r['published_metric'] for r in R]
    solves = np.array([x['solves'] for x in rows[0]], float)
    Y = np.array([[x['mean_err_psd'] for x in row] for row in rows], float)
    sl, ic, se = slope_with_se(solves, Y)
    out['published_metric'] = dict(solves=solves.tolist(), mean=Y.mean(0).tolist(),
                                   se=(Y.std(0, ddof=1) / np.sqrt(len(R))).tolist(),
                                   slope=sl, intercept=ic, slope_se=se)

    # ---- pCN
    rows = [r['pcn'] for r in R]
    ps = np.array([x['solves'] for x in rows[0]], float)
    pcn = dict(solves=ps.tolist(),
               iters=[x['iters'] for x in rows[0]],
               ess_min=np.array([[x['ess_min'] for x in row] for row in rows],
                                float).mean(0).tolist(),
               seconds=np.array([[x['seconds'] for x in row] for row in rows],
                                float).mean(0).tolist())
    # The two smallest pCN budgets have a minimum effective sample size of 4 and 5, so their
    # error measures how far the chain has failed to move, not a Monte Carlo error. Fitting a
    # rate through them flattens the slope and inflates the ratio at the accurate end. Both
    # fits are reported; the ratio below uses the converged one.
    ESS_CUT = 7.0
    ess = np.array(pcn['ess_min'], float)
    conv = ess >= ESS_CUT
    pcn['ess_cut'] = ESS_CUT
    pcn['n_converged'] = int(conv.sum())
    for met in METRICS:
        Y = np.array([[x[met] for x in row] for row in rows], float)
        sl, ic, se = slope_with_se(ps, Y)
        slc, icc, sec = slope_with_se(ps[conv], Y[:, conv])
        pcn[met] = dict(mean=Y.mean(0).tolist(),
                        se=(Y.std(0, ddof=1) / np.sqrt(len(R))).tolist(),
                        slope_all=sl, intercept_all=ic, slope_se_all=se,
                        slope=slc, intercept=icc, slope_se=sec)
    out['pcn'] = pcn

    # ---- the ratio where BOTH curves were actually measured.
    # Matching pCN to GBC's error at GBC's largest budget requires extrapolating pCN far
    # beyond any run performed, which is not evidence.  The two error ranges do overlap, so
    # the ratio can be read off inside the measured range of both, with no extrapolation.
    ratio_measured = {}
    for arm, ao in out['gbc'].items():
        r_arm = {}
        for met in ('sd_err_rel', 'cov_rel_fro'):
            ge = np.array(ao[met]['mean'], float)
            pe = np.array(pcn[met]['mean'], float)
            lo, hi = max(ge.min(), pe.min()), min(ge.max(), pe.max())
            if lo >= hi:
                r_arm[met] = dict(overlap=False)
                continue
            tgt = float(np.sqrt(lo * hi))            # geometric midpoint of the overlap
            ng = float(np.exp((np.log(tgt) - ao[met]['intercept']) / ao[met]['slope']))
            npc = float(np.exp((np.log(tgt) - pcn[met]['intercept']) / pcn[met]['slope']))
            def at(e):
                return (np.exp((np.log(e) - pcn[met]['intercept']) / pcn[met]['slope'])
                        / np.exp((np.log(e) - ao[met]['intercept']) / ao[met]['slope']))
            # named for the ratio, not for which end of the error band produced it
            r_lo, r_hi = sorted((float(at(hi)), float(at(lo))))
            r_arm[met] = dict(overlap=True, err_lo=float(lo), err_hi=float(hi), target=tgt,
                              gbc_solves=ng, pcn_solves=npc, ratio=npc / ng,
                              ratio_min=r_lo, ratio_max=r_hi)
        ratio_measured[arm] = r_arm
    out['ratio_measured'] = ratio_measured

    # ---- crossover on the honest metric: where pCN reaches GBC's error at its best budget
    cross = {}
    for arm, ao in out['gbc'].items():
        c_arm = {}
        for met in ('sd_err_rel', 'cov_rel_fro'):
            target = ao[met]['mean'][-1]                    # GBC at its largest budget
            sl, ic = pcn[met]['slope'], pcn[met]['intercept']
            need = float(np.exp((np.log(target) - ic) / sl))
            c_arm[met] = dict(gbc_error=float(target),
                              gbc_solves=float(ao['solves'][-1]),
                              pcn_solves_needed=need,
                              ratio=need / float(ao['solves'][-1]),
                              extrapolation=need / float(ps[-1]))
        cross[arm] = c_arm
    out['crossover'] = cross

    json.dump(out, open(a.out, 'w'), indent=1)

    print(f"{len(R)} replicates, N={h['N']}, J={h['J']}, k_eff={h['k_eff']}")
    print(f"{'curve':>26} {'slope':>18}   error at largest budget")
    pm = out['published_metric']
    print(f"{'published (mean vs exact)':>26} "
          f"{pm['slope']:+.3f} +/- {pm['slope_se']:.3f}   {pm['mean'][-1]:.4f}")
    for arm, ao in out['gbc'].items():
        for met in ('sd_err_rel', 'cov_rel_fro', 'mean_err_psd'):
            d = ao[met]
            if d.get('exact_zero'):
                print(f"{'gbc ' + arm + ' ' + met:>26} "
                      f"{'exactly 0':>18}   in all {d['n_measurements']} measurements")
            else:
                print(f"{'gbc ' + arm + ' ' + met:>26} "
                      f"{d['slope']:+.3f} +/- {d['slope_se']:.3f}   {d['mean'][-1]:.4f}")
    for met in ('sd_err_rel', 'cov_rel_fro'):
        d = pcn[met]
        print(f"{'pcn ' + met:>26} {d['slope']:+.3f} +/- {d['slope_se']:.3f}   "
              f"{d['mean'][-1]:.4f}")
    print("\nratio inside the measured range of BOTH curves (no extrapolation):")
    for arm, r in ratio_measured.items():
        for met, v in r.items():
            if not v['overlap']:
                print(f"  {arm:>8} {met:>12}: no overlap")
                continue
            print(f"  {arm:>8} {met:>12}: {v['ratio']:7.0f}x at error {v['target']:.4f}"
                  f"   ({v['ratio_min']:.0f}x to {v['ratio_max']:.0f}x across the overlap"
                  f" {v['err_hi']:.4f} to {v['err_lo']:.4f})")
    print("\ncrossover (pCN solves to match GBC at its largest budget, EXTRAPOLATED):")
    for arm, c in cross.items():
        for met, v in c.items():
            print(f"  {arm:>8} {met:>12}: {v['ratio']:8.1f}x GBC, "
                  f"{v['extrapolation']:6.1f}x beyond the largest pCN run")
    print("\nwrote", a.out)


if __name__ == '__main__':
    main()
