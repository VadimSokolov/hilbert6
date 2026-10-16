# Chapter 12. Navier Stokes as Inference on the Solution Manifold

<!-- cite:begin -->
From *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation* by Nick Polson and Vadim Sokolov (2026), chapter 12. Cite as Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1, https://doi.org/10.5281/zenodo.23407620. Book page: https://vsokolov.org/books/hilbert6/. Source: https://github.com/VadimSokolov/hilbert6.
<!-- cite:end -->

This chapter treats the Navier Stokes equations as a Bayesian inverse problem on the solution manifold: from noisy, incomplete observations of the velocity or vorticity, infer the initial condition and push the posterior through the solution map. The linear case, the backward heat equation with Gaussian priors, is solved exactly, with logarithmic posterior contraction and a Bernstein von Mises theorem for linear functionals with fast decaying coefficients. The nonlinear theory of Nickl and coauthors is presented, including gradient stability and polynomial time Langevin sampling from a warm start, proved by Nickl and Wang for a Schrödinger equation. The chapter deduces a gradient stability bound for the initial condition of the two dimensional Navier Stokes equations when time zero is observed, and lists the other steps for Navier Stokes as open. It shows that a generator trained on simulations (generative Bayesian computation) inherits the Bernstein von Mises theorem when accurate at the posterior scale. It also reviews Hellinger well posedness and preconditioned Crank Nicolson sampling, with computed posteriors for the Fisher Kolmogorov and vorticity equations.

## From the literature

Global solutions in two dimensions (Leray, Ladyzhenskaya, Lions); backward uniqueness (Bardos and Tartar 1973); well posedness of the posterior (Stuart 2010; Dashti and Stuart 2017); the Cameron Martin formula and Feldman Hájek dichotomy (proved in Bogachev 1998); contraction and credible sets for the heat equation (Knapik, van der Vaart and van Zanten 2013); Bernstein von Mises theorems (Castillo and Nickl 2013; Nickl 2024; Konen and Nickl 2026); nonlinear inverse problems (Nickl 2023); posterior consistency for Navier Stokes (Nickl and Titi 2024); gradient stability and polynomial time Langevin sampling (Nickl and Wang 2024; Bohr and Nickl 2024; Castre and Nickl 2026; Durmus and Moulines 2019); preconditioned Crank Nicolson (Cotter, Roberts, Stuart and White 2013); the Fisher Kolmogorov equation (Fisher 1937; Kolmogorov, Petrovsky and Piskunov 1937); the ensemble Kalman filter (Evensen 1994).

## New results

The theorems of Nickl and Wang, of Cameron Martin, Feldman and Hájek, and of Stuart are results of other authors, quoted without proof or with a sketch, and are not listed.

<!-- results:begin -->
- [Gradient stability for the initial condition of two dimensional Navier Stokes, with time zero observed](../RESULTS.md#gradient_stability_initial_condition_ns2d) (Proposition 12.8, page 153; proved): Using estimates of Konen and Nickl, the map from the first D Stokes coefficients of the initial velocity of the two dimensional Navier Stokes equations on the torus to the solution observed over space and over a time window that starts at zero is gradient stable on a Sobolev ball, with a constant of order D to the power minus one half. New in this book.
- [Bernstein von Mises for generators](../RESULTS.md#bernstein_von_mises_for_generators) (Proposition 12.10, page 157; proved): If the posterior of a functional satisfies a Bernstein von Mises theorem at the square root n scale and a generator is close to the posterior in the bounded Lipschitz metric after both are centered and rescaled by the square root of n, then the generated law satisfies the same Bernstein von Mises theorem. New in this book.
<!-- results:end -->

## Key terms

Bayesian inverse problem, Navier Stokes, solution manifold, data assimilation, backward heat equation, posterior contraction, Bernstein von Mises, gradient stability, unadjusted Langevin algorithm, polynomial time sampling, Cameron Martin space, Hellinger distance, preconditioned Crank Nicolson, pCN, Hamiltonian Monte Carlo, generative Bayesian computation, Fisher Kolmogorov equation, Fisher KPP, vorticity equation, 4DVar, ensemble Kalman filter.
