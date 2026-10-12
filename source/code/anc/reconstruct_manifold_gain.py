"""Reproduce paper/manifold_gain.json, which has no generating script.

manifold_gain.json feeds Table tab:gain in the supplement and the introduction's claim that the
constrained model has 20 effective parameters against the unconstrained model's 172, with
credible bands 1.7 times tighter at the initial time and 7.3 times tighter at the end of the
window.  No script in the repository produces it and the JSON records neither N nor the
calibration constants, so this file establishes the provenance from the caption alone.

Settings from the caption of tab:gain: 2D heat equation, N = 2000, nu = 0.01, T = 1, alpha = 3,
priors matched to a pointwise prior standard deviation of 2.2 (constrained) and 2.5
(unconstrained).

RESULT
------
Both arms reproduce.  The one convention the caption does not state, and the one that had to be
recovered, is that the spatial constant mode is excluded from the unconstrained arm's product
basis.  Including the (0, 0, m) column, which is the natural first reading of "a GP on the
space-time field", puts sd_unc at 0.3545 against the recorded 0.3774, a 6 percent gap; excluding
it puts sd_unc at 0.3769, a 0.14 percent gap, and leaves Jeff_u at 172 exactly.  The residual
0.14 percent is the caption rounding its calibration constant: solving for the pointwise prior sd
that reproduces sd_unc exactly gives 2.5079, which the caption reports as 2.5.

The constrained arm reproduces Jeff_c = 20 exactly at the caption's 2.2, and its five band
entries to within 0.7 percent, with t = 0 exact to 0.016 percent.  The residual is a shape
difference in the time weighting at intermediate t, not a scale error, and no single calibration
constant removes it.

Every claim the paper makes in prose reproduces: 20 effective parameters against 172, 1.7 times
tighter at the initial time, 4.4 at t = 0.5, and 7.3 at t = 1.  One table cell sits on a rounding
boundary: t = 0.2 gives 2.74 here, which rounds to 2.7, against the recorded 2.76 printed as 2.8.
That cell is reported below rather than tuned away.

Usage:  python3 reconstruct_manifold_gain.py
"""
import json
import os

import numpy as np

NU, T, ALPHA, N = 0.01, 1.0, 3.0, 2000
SD_TARGET_C, SD_TARGET_U = 2.2, 2.5
KCUT2 = 40                    # |k|^2 <= 40, the constrained arm's spatial truncation (D = 128)
KBOX, MMAX = 48, 120          # unconstrained product basis, large enough to be converged
TIMES = (0.0, 0.05, 0.2, 0.5, 1.0)


def calibrate(eigs, target_sd):
    """rho such that the pointwise prior sd sqrt(sum rho^2 mu^-alpha) equals target_sd."""
    return target_sd / np.sqrt((eigs ** (-ALPHA)).sum())


def constrained(target=SD_TARGET_C):
    K = int(np.sqrt(KCUT2)) + 1
    k2 = np.array([a * a + b * b for a in range(-K, K + 1) for b in range(-K, K + 1)
                   if 0 < a * a + b * b <= KCUT2], float)
    lam = 4.0 * np.pi ** 2 * k2
    iota = (1.0 - np.exp(-2 * NU * lam * T)) / (2 * NU * lam * T)
    rho = calibrate(lam, target)
    prior_prec = lam ** ALPHA / rho ** 2
    prec = N * iota + prior_prec
    return dict(D=int(k2.size), rho=float(rho),
                Jeff_c=int((N * iota >= prior_prec).sum()),
                sd_c={f"{t}": float(np.sqrt((np.exp(-2 * NU * lam * t) / prec).sum()))
                      for t in TIMES})


def unconstrained(target=SD_TARGET_U, keep_spatial_constant=False):
    """GP on the space-time field: mu = lambda_k + omega_m^2, omega_m = 2 pi m / T.

    keep_spatial_constant includes the (0, 0, m) column.  It is the natural first reading and it
    is not the one that generated the recorded numbers; the flag exists so the 6 percent gap it
    produces can be reproduced rather than asserted.
    """
    lo = 0 if keep_spatial_constant else 1
    k2 = np.array([a * a + b * b for a in range(-KBOX, KBOX + 1) for b in range(-KBOX, KBOX + 1)
                   if a * a + b * b >= lo], float)
    om = 2.0 * np.pi * np.arange(-MMAX, MMAX + 1) / T
    mu = (4.0 * np.pi ** 2 * k2[:, None] + om[None, :] ** 2).ravel()
    mu = mu[mu > 0]
    rho = calibrate(mu, target)
    prior_prec = mu ** ALPHA / rho ** 2
    return dict(rho=float(rho), Jeff_u=int((N >= prior_prec).sum()),
                sd_unc=float(np.sqrt((1.0 / (N + prior_prec)).sum())))


def solve_target(ref_sd, lo=2.0, hi=3.5):
    """The pointwise prior sd that reproduces the recorded sd_unc exactly."""
    for _ in range(60):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if unconstrained(mid)['sd_unc'] < ref_sd else (lo, mid)
    return (lo + hi) / 2


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ref = json.load(open(os.path.join(here, '..', 'paper', 'manifold_gain.json')))
    C, U = constrained(), unconstrained()
    Uin = unconstrained(keep_spatial_constant=True)

    print(f"constrained: D={C['D']} modes at |k|^2<={KCUT2}, rho={C['rho']:.3f}")
    print(f"  Jeff_c   {C['Jeff_c']:>10}   recorded {ref['Jeff_c']:>10}   "
          f"{'MATCH' if C['Jeff_c'] == ref['Jeff_c'] else 'MISMATCH'}")
    for t in TIMES:
        got, want = C['sd_c'][f"{t}"], ref['sd_c'][f"{t}"]
        print(f"  sd(t={t:<4}) {got:10.6f}   recorded {want:10.6f}   {(got-want)/want*100:+7.3f}%")

    print(f"\nunconstrained: {(2*KBOX+1)**2-1} spatial x {2*MMAX+1} temporal, rho={U['rho']:.4f}")
    print(f"  Jeff_u   {U['Jeff_u']:>10}   recorded {ref['Jeff_u']:>10}   "
          f"{'MATCH' if U['Jeff_u'] == ref['Jeff_u'] else 'MISMATCH'}")
    print(f"  sd_unc   {U['sd_unc']:10.6f}   recorded {ref['sd_unc']:10.6f}   "
          f"{(U['sd_unc']-ref['sd_unc'])/ref['sd_unc']*100:+7.3f}%")
    print(f"  with the (0,0,m) column kept, for comparison: {Uin['sd_unc']:.6f}  "
          f"({(Uin['sd_unc']-ref['sd_unc'])/ref['sd_unc']*100:+.3f}%), Jeff_u={Uin['Jeff_u']}")
    print(f"  pointwise prior sd that reproduces sd_unc exactly: {solve_target(ref['sd_unc']):.4f}"
          f"   (caption reports {SD_TARGET_U})")

    print("\nratio row of tab:gain, which is what the paper claims:")
    print(f"{'t':>6} {'reconstructed':>15} {'recorded':>12} {'printed':>9}")
    for t in TIMES:
        r = U['sd_unc'] / C['sd_c'][f"{t}"]
        w = ref['sd_unc'] / ref['sd_c'][f"{t}"]
        flag = '' if round(r, 1) == round(w, 1) else '   <-- rounds differently'
        print(f"{t:>6} {r:>15.3f} {w:>12.3f} {round(w, 1):>9}{flag}")


if __name__ == '__main__':
    main()
