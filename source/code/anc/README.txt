Code and recorded results for

  Bayesian Estimation on the Solution Manifold of a PDE:
  Generative Computation and Adjoint Sufficient Statistics
  N. G. Polson and V. Sokolov

This is a snapshot of the code that produced every number and figure in the article, together
with the JSON files each run wrote.  Python 3 with numpy, scipy and matplotlib; no other
dependencies.  All seeds are fixed in the drivers.

WHAT PRODUCES WHAT
------------------
Main paper.
  Table 3 (finite-N check)        exp_paper_figs.py    -> results/paper_figs.json
  Table 4 (cost and accuracy)     exp_paper_figs.py    -> results/paper_figs.json
  Table 5 (Navier-Stokes)         ns/*.py              -> results/ns/*.json
  Figure 1 (GBC on the heat eq.)  fig_heat_gbc.py
  Figure 2 (error vs cost;        exp_study2.py        -> results/study2_rep*.json
            per-mode coverage)    agg_study2.py        -> results/study2_agg.json
                                  exp_cover2.py        -> results/cover2_rep*.json
                                  agg_cover2.py        -> results/cover2_agg.json
                                  fig_cost.py          -> ../paper/fig_cost.pdf
  Section 13 text                 make_experiments_tex.py reads the JSON above and writes the
                                  Experiments section, so that section cannot drift from the runs
                                  behind it.  paper/check_numbers.py fails the build on drift.

Supplement.
  Coverage table, three arms      exp_cover2.py, agg_cover2.py (as above)
  Heat information figure         fig_heat_stokes.py
  Radius figure                   exp_gbc_local.py, fig_radius_theory.py
  Advection/dissipation ratio     ns/advection_ratio.py -> results/ns/advection.json

The Navier-Stokes run, code/ns/.
  ns_solver.py       pseudo-spectral 2D solver, vorticity form, on the 2pi-torus.  It decays
                     mode k at nu*|k|^2: lambda_k = |k|^2, NOT 4*pi^2*|k|^2.  Anything that
                     compares against a Stokes prediction must use the same convention.
  variants.py        architecture sweep, prior vs localised training  -> variants.json
  centring.py        residual centring, Theorem 10.2(ii)             -> centring.json
  correct_centre.py  spread rescaling, Theorem 10.2(iii)             -> correct_centre.json
  relin.py, relin2.py  re-linearised summary, the c^4 term           -> relin*.json
  radius.py, radius_iw.py  radius sweep and importance weighting     -> radius*.json
  crossover.py       the two further regimes; takes 'amplitude' or 'posterior'
                     -> crossover2.json, crossover3.json
  spectrum.py, spectrum_hi.py   per-mode information                 -> spectrum*.json
  mcmc_error.py      Monte Carlo error of the Metropolis reference   -> mcmc_error.json
                     Reads cache.npz.  Reports two autocorrelation-time estimators;
                     the paper uses the smaller, which is the conservative one for the
                     claim it supports.  See the docstring.
  advection_ratio.py off-diagonal vs diagonal of the tangent operator -> advection.json
  run_all.sh         runs the above in order; about 40 minutes on one core.

REPRODUCING
-----------
The two replicate studies were run as SLURM array jobs; each task takes a --rep index and writes
one JSON.  To reproduce serially:

  for r in $(seq 1 40); do python3 exp_study2.py --rep $r; done
  python3 agg_study2.py results/study2_rep*.json --out results/study2_agg.json

  for r in $(seq 1 20); do python3 exp_cover2.py --rep $r; done
  python3 agg_cover2.py results/cover2_rep*.json --out results/cover2_agg.json

  python3 fig_cost.py
  python3 make_experiments_tex.py --results results/paper_figs.json --study results/study.json \
      --study2 results/study2_agg.json --out ../paper/experiments_generated.tex

The recorded JSON is included, so the figures and the Experiments section can be regenerated
without rerunning the studies.

reconstruct_manifold_gain.py re-derives the manifold-gain table from the settings given in its
caption, and reports plainly which entries reproduce and which do not: the one table cell at
t = 0.2 rounds to 2.7 here against the recorded 2.76 printed as 2.8.

A NOTE ON TWO METRIC NAMES
--------------------------
In the JSON, mean_err_psd and sd_err_rel are worst-mode maxima, not averages, despite the key
names.  The article's table column reads "Max err." and its prose reads "worst-mode error"
accordingly.  See the comment at the definition in exp_study2.py.

A CORRECTION TO THE COMPANION NUMERICAL STUDY
---------------------------------------------
An earlier version of the companion study read spectrum_hi.json as showing that advective
transfer defeats the viscous barrier.  It did not.  That reading compared the measurement
against a Stokes prediction computed with lambda_k = 4*pi^2*|k|^2, the eigenvalue of the
Laplacian on the unit torus, while ns_solver.py works on the 2pi-torus and decays mode k at
nu*|k|^2.  The factor of 4*pi^2 was the whole of the claimed effect.  Corrected, the measurement
agrees with the Stokes prediction to within Monte Carlo error, and over that mode set
2*nu*lambda_k*T <= 0.41, so no barrier was engaged.  The finding is withdrawn.  Nothing in the
article or its supplement ever depended on it.
