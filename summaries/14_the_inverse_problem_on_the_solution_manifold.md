# Chapter 14. The Inverse Problem on the Solution Manifold

<!-- cite:begin -->
From *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation* by Nick Polson and Vadim Sokolov (2026), chapter 14. Cite as Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1, https://doi.org/10.5281/zenodo.23327515. Book page: https://vsokolov.org/books/hilbert6/. Source: https://github.com/VadimSokolov/hilbert6.
<!-- cite:end -->

Chapter 14 opens Part IV with the Bayesian inverse problem for the initial condition $\theta$ of an evolution equation, observed through noisy values of the solution at $N$ random space time points, with a Gaussian process prior on $\theta$. It summarizes the framework of Nickl and coauthors for nonlinear parabolic equations (heat, reaction diffusion, two dimensional Navier Stokes): Bernstein von Mises theorems for the posterior in a weak norm and in the supremum norm on forward trajectories, exact coverage of credible bands and local asymptotic minimax efficiency. It then introduces the solution manifold $\mathcal M=\{u_\theta\}$: posterior draws of the field solve the equation exactly, the Gaussian limit lives on the tangent space, and prediction beyond the observation window needs no extrapolation model. For the heat equation a closed form comparison with an unconstrained space time Gaussian process prior, with the Gram matrix of the design replaced by its limit, shows the posterior standard deviation shrinking in time. The chapter states the generative Bayesian computation (GBC) algorithm and compares GBC with function space MCMC, ensemble Kalman inversion, Laplace approximation, transport maps and simulation based inference. It proves that the Gaussian limit is nondegenerate for the reaction diffusion class of Nickl's trajectory theorem ($\partial_tu-\Delta u=f(u)$, $f$ smooth with compact support, torus of dimension at most three).

## From the literature

Bernstein von Mises theorems for the posterior of the initial condition of nonlinear parabolic equations, in a weak norm and in supremum norm on forward trajectories (Nickl 2024). For two dimensional Navier Stokes: these theorems, exact coverage of credible bands, the Fredholm decomposition of the information operator and local asymptotic minimax efficiency of the posterior mean (Konen and Nickl 2026, with Konen 2026). Inverse logarithmic contraction rates (Nickl and Titi 2024). Polynomial time Langevin computation of posteriors (Nickl and Wang 2024). Gaussian process regression under linear equations (Raissi, Perdikaris and Karniadakis 2017; Albert and Rath 2020). For a nonlinear forward map, the large ensemble limit of ensemble Kalman inversion is a linear Bayes estimator, not the posterior (Ernst, Sprungk and Starkloff 2015).

## New results

The new results are a nondegeneracy lemma and the manifold gain for the heat equation.

<!-- results:begin -->
- [Nondegeneracy of the Gaussian limit of the posterior trajectory for reaction diffusion equations](../RESULTS.md#the_limit_law_is_nondegenerate) (Lemma 14.3, page 189; proved): For the reaction diffusion equation, the Gaussian limit law of the posterior forward trajectory in the supremum norm is nondegenerate: its reproducing kernel Hilbert space is nontrivial and the distribution function of its supremum norm is continuous and strictly increasing, which is the property that the argument for exact asymptotic coverage of credible bands uses. New in this book.
- [Manifold gain for the heat equation: prior on the initial condition against a space time Gaussian process prior](../RESULTS.md#manifold_gain_for_the_heat_equation) (Proposition 14.5, page 193; proved): For the heat equation with Gaussian priors and the design Gram matrix replaced by its limit, the posterior standard deviation of the field under a prior on the initial condition decreases in time, while under a space time Gaussian process prior of comparable regularity it does not depend on time or place, and the ratio of the two at time $t$ is at least $e^{\nu\lambda_1 t}$ times its value at time zero; the effective numbers of parameters of the two models are also given in order. New in this book.
<!-- results:end -->

## Key terms

inverse problem, initial condition, data assimilation, solution manifold, tangent space, manifold gain, Bernstein von Mises theorem, nonlinear parabolic equation, reaction diffusion, heat equation, Navier Stokes, Gaussian process prior, information operator, Fredholm decomposition, credible band, exact coverage, local asymptotic minimax, reproducing kernel Hilbert space, adjoint equation, generative Bayesian computation, GBC, simulation based inference, function space MCMC, ensemble Kalman inversion
