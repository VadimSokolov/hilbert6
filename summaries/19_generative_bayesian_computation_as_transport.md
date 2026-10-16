# Chapter 19. Generative Bayesian Computation as Transport

<!-- cite:begin -->
From *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation* by Nick Polson and Vadim Sokolov (2026), chapter 19. Cite as Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1, https://doi.org/10.5281/zenodo.23407620. Book page: https://vsokolov.org/books/hilbert6/. Source: https://github.com/VadimSokolov/hilbert6.
<!-- cite:end -->

This chapter asks how Bayes' rule can be computed as a map instead of a density. Generative Bayesian computation (GBC) seeks a function $H$ such that $H(y,U)$, with $U$ a fixed reference noise, has the posterior law for every $y$, learns $H$ from simulated pairs of parameters and data, and samples the posterior for a new $y$ by one evaluation. The chapter proves noise outsourcing (for real valued parameters, the general case by a Borel isomorphism), the check loss characterization of quantiles, that the perturbed observation ensemble Kalman update transports prior draws to posterior draws in the linear Gaussian model, Tweedie's formula, and the static reduction of the Schrödinger problem to entropic optimal transport. It quotes Brenier's theorem without proof. It connects GBC with diffusion models and score matching, Schrödinger bridges and Sinkhorn's algorithm (geometric convergence through Hilbert's projective metric), the Föllmer process, bootstraps and martingale posteriors, and approximate Bayesian computation (ABC) and its limits. A last section proposes quantile GBC for reinforcement learning with verifiable rewards.

## From the literature

Transfer theorem behind noise outsourcing (Kallenberg 2002); Knothe Rosenblatt map (Rosenblatt 1952; Knothe 1957); Brenier's theorem (Brenier 1991) and McCann's extension (McCann 1995); perturbed observation ensemble Kalman filter (Evensen 1994; Burgers, van Leeuwen and Evensen 1998); time reversal of diffusions (Anderson 1982); Tweedie's formula as popularized by Efron (2011); Schrödinger's problem (Schrödinger 1931); Sinkhorn's algorithm (Sinkhorn 1964), its convergence for the continuous problem (Fortet 1940), geometric convergence by Birkhoff's contraction (Birkhoff 1957; Franklin and Lorenz 1989); small noise limit of entropic plans (Mikami 2004; Léonard 2012); Föllmer process (Föllmer 1985; Lehec 2013); stochastic interpolants (Albergo and Vanden Eijnden 2023); flow matching (Lipman et al. 2023); martingale posteriors (Fong, Holmes and Walker 2023); approximate Bayesian computation (Tavaré et al. 1997).

## New results

Generative Bayesian computation is the authors' method (Polson and Sokolov 2025, Generative AI for Bayesian computation; Polson, Ruggeri and Sokolov 2024, Generative Bayesian computation for maximum expected utility), and the chapter presents none of its numbered results as new.

<!-- results:begin -->
No new results of this chapter are catalogued.
<!-- results:end -->

## Key terms

generative Bayesian computation, GBC, noise outsourcing, quantile map, check loss, pinball loss, Knothe Rosenblatt map, optimal transport, ensemble Kalman filter, Tweedie's formula, empirical Bayes, score matching, diffusion models, Schrödinger bridge, entropic optimal transport, Sinkhorn algorithm, iterative proportional fitting, Hilbert projective metric, Föllmer process, stochastic interpolants, flow matching, martingale posterior, approximate Bayesian computation, ABC, verifiable rewards
