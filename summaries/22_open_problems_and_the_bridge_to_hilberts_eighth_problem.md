# Chapter 22. Open Problems and the Bridge to Hilbert's Eighth Problem

<!-- cite:begin -->
From *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation* by Nick Polson and Vadim Sokolov (2026), chapter 22. Cite as Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1, https://doi.org/10.5281/zenodo.23327515. Book page: https://vsokolov.org/books/hilbert6/. Source: https://github.com/VadimSokolov/hilbert6.
<!-- cite:end -->

This chapter links Hilbert's sixth and eighth problems through the heat equation and closes with open problems. The Riemann hypothesis (RH) is expressed through the backward heat flow: the de Bruijn Newman constant $\Lambda$ is defined from the Gaussian deformation $H_t$ of the Pólya kernel of the Riemann $\Xi$ function, $H_t$ solves the backward heat equation, and RH holds if and only if $\Lambda\leq0$. The chapter proves the Pólya de Bruijn theorem that the backward heat semigroup preserves real zeros of even entire functions of order less than 2, quotes $0\leq\Lambda\leq0.2$ without proof, and shows that RH is equivalent to the Lee Yang property of the Pólya law. It reads the de Bruijn flow as exponential tilting and conditioning on the second moment, and relates RH to the Biane Pitman Yor Brownian excursion identity and to generalized Gamma convolutions. The link with the inferential sixth problem is an analogy and not an equivalence. No proof of RH is claimed.

## From the literature

Riemann (1859): $\Xi$ as a cosine transform, roots very probably real. Pólya (1926): the explicit kernel of $\Xi$. Pólya (1927) and de Bruijn (1950): the backward heat semigroup preserves real zeros. de Bruijn (1950): the Gaussian family $H_t$ and $\Lambda\leq\frac12$. Newman (1976): $\Lambda>-\infty$, the conjecture $\Lambda\geq0$ and the Lee Yang reformulation of RH, after Lee and Yang (1952) and Newman (1974). Rodgers and Tao (2020): $\Lambda\geq0$. Polymath (2019): $\Lambda\leq0.22$. Platt and Trudgian (2021): $\Lambda\leq0.2$. Csordas, Smith and Varga (1994): rigorous zero dynamics. Biane, Pitman and Yor (2001): $2\xi(s)$ as a Brownian excursion moment. Kent (1980): hitting time expansions. Csiszár (1984): conditional limit theorem. Behind the open problems: Villani (2003), Carlen, Carvalho, Le Roux, Loss and Villani (2010, the fourth moment question), Einav (2011) and Gao, Wang and Xia (2026, preprint) on Kac walk entropy production; Konen and Nickl (2026) on Navier Stokes; Deng, Hani and Ma (2024, 2025, preprints).

## New results

The theorems and proposition of this chapter are known results; the catalogued items are three open problems posed by the authors.

<!-- results:begin -->
- [Open problem: exact samplers for Brownian functionals from Kent's eigenvalue expansion](../RESULTS.md#open_problem_yor_exact_samplers) (Open Problem 4, page 445; open): A program: find a class of regular diffusions whose hitting time remainder after the first terms of Kent's exponential series can be sampled exactly at finite expected cost, prove the sampler exact, and use it to build a library of exact samplers for Brownian functionals. New in this book.
- [Open problem: uniform entropy production bound for the Kac walk on conditioned products of normal scale mixtures](../RESULTS.md#open_problem_kac_entropy_production_ggc_mixtures) (Open Problem 8, page 446; open): Decide whether the entropy production of the Kac walk is bounded below by a fixed multiple of the relative entropy, with a constant that does not depend on the number of particles, for conditioned product densities built from bounded normal scale mixtures with generalized Gamma convolution mixing law, unit variance and fourth moment at most $M$; the constant may depend on $M$. New in this book.
- [Open problem: posterior contraction and Bernstein von Mises theorems for the initial vorticity of two dimensional Navier Stokes from fixed sensors](../RESULTS.md#open_problem_ns_posterior_fixed_sensors) (Open Problem 10, page 447; open): Determine the posterior contraction rate for the initial vorticity of the two dimensional Navier Stokes equations from noisy observations at a fixed array of sensors and times, identify the functionals of the initial vorticity that admit a Bernstein von Mises theorem, and ask whether the posterior can be computed in polynomial time. New in this book.
<!-- results:end -->

## Key terms

Hilbert's sixth problem, Hilbert's eighth problem, Riemann hypothesis, RH, Riemann xi function, de Bruijn Newman constant, backward heat equation, Pólya kernel, Polya kernel, Lee Yang property, ferromagnetic random variables, Pólya law, Biane Pitman Yor identity, Brownian excursion, generalized Gamma convolution, GGC, Thorin measure, exact sampling, Kac walk, entropy production, Navier Stokes, Bernstein von Mises, posterior contraction
