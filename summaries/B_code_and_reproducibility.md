# Appendix B. Code and Reproducibility

<!-- cite:begin -->
From *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation* by Nick Polson and Vadim Sokolov (2026), appendix B. Cite as Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1, https://doi.org/10.5281/zenodo.23327515. Book page: https://vsokolov.org/books/hilbert6/. Source: https://github.com/VadimSokolov/hilbert6.
<!-- cite:end -->

Each of the book's 32 figures is drawn by a Python script in the folder `code`: 28 compute their data, 3 replot recorded experiment results and one, the Lanford window, is a schematic. Ten tables have numbers that a script computes or reads. `figures.py` and `figures_color.py` draw 20 figures; `figures_pf.py`, `figures_pl.py` and `figures_msw.py` the filter figures of Chapter 20; `fk_posterior.py` (whose generator study needs PyTorch) and `ns2d_posterior.py` (which needs JAX) the posterior figures and tables of Chapter 12; `yor_catalogue.py` the table of Yor identity checks; six `mf_` scripts the Part IV figures, with `mf_gain.py` and `mf_gap.py` for two tables. The Part IV experiments are in `code/anc`, a copy of the ancillary files of the authors' manifold paper (scripts, recorded results, SLURM files). The figure and table scripts need Python 3, NumPy, SciPy and Matplotlib (NumPy 2.0 or later for three), fix any random seeds, overwrite the shipped figures unless run in a copy, and take under a second to 19 minutes on an Apple M2 laptop. The replicate studies take hours, so the book reads their recorded results; the authors reran them on a cluster, and the Navier Stokes experiment scripts in a copy of the folder, and matched the recorded results to a relative difference of at most $3\times10^{-10}$, except wall clock times and four entries (up to $6\times10^{-8}$). The chaotic Hénon Heiles and standard map figures can differ in detail on another machine, but not in structure. Some files in `code/anc` are outdated or absent. Three `pdflatex` runs rebuild the book.

## From the literature

None.

## New results

<!-- results:begin -->
No new results of this appendix are catalogued.
<!-- results:end -->

## Key terms

reproducibility, code, Python scripts, figure scripts, `figures.py`, `figures_color.py`, `fk_posterior.py`, `ns2d_posterior.py`, `yor_catalogue.py`, `hh_checks.py`, `code/anc`, `code/ns_checks`, ancillary files, recorded results, JSON, SLURM, fixed random seeds, replicate studies, GBC (generative Bayesian computation), pCN (preconditioned Crank Nicolson), NumPy, SciPy, Matplotlib, JAX, PyTorch, wall clock time, Hénon Heiles, standard map, rebuilding the book, pdflatex
