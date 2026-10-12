#!/bin/bash
# Reproduces every Navier-Stokes number in the paper.  ~45 min on one core.
# Each script writes its JSON into ../results/ns/, which is the only thing
# make_experiments_tex.py reads.
set -e
python3 full.py                  # reference chain + training pools -> cache.npz   (~5 min)
python3 variants.py              # architecture sweep, Table 5 upper panel         (~1 min)
python3 variants2.py             # importance-weighted variants                    (~1 min)
python3 radius.py                # radius sweep                                    (~4 min)
python3 radius_iw.py             # importance weighting back to the prior          (~3 min)
python3 spectrum.py              # 6-mode per-mode information                     (~1 min)
python3 spectrum_hi.py           # extended mode set, information vs T0            (~1 min)
python3 advection_ratio.py       # advection/dissipation ratio of the tangent op   (~1 min)
python3 mcmc_error.py            # Monte Carlo error of the reference itself       (<1 min)
python3 crossover.py amplitude   # crossover regime 1: raise the amplitude         (~3 min)
python3 crossover.py posterior   # crossover regime 2: widen the posterior         (~3 min)
python3 relin.py                 # one-step vs re-linearised summary               (~4 min)
python3 relin2.py                # error flat in M                                 (~8 min)
python3 hetero.py                # residual spread homogeneous -> hetero_cache.npz (~5 min)
python3 centring.py              # residual centring, Theorem 10.2(ii)             (<1 min)
python3 correct_centre.py        # spread rescaling, Theorem 10.2(iii)             (~1 min)
python3 make_fig2.py             # fig_ns_study.pdf (companion study only)
