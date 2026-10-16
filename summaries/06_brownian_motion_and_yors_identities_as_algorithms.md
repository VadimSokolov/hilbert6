# Chapter 6. Brownian Motion and Yor's Identities as Algorithms

<!-- cite:begin -->
From *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation* by Nick Polson and Vadim Sokolov (2026), chapter 6. Cite as Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1, https://doi.org/10.5281/zenodo.23407620. Book page: https://vsokolov.org/books/hilbert6/. Source: https://github.com/VadimSokolov/hilbert6.
<!-- cite:end -->

How can Yor's identities in law for Brownian functionals be turned into exact simulation algorithms? Following the authors' paper Yor's Identities as Algorithms, an identity in law between a Brownian functional and independent Gamma, normal, exponential or uniform variables is read as a sampler with no discretization, Markov chain or rejection step. The chapter builds Brownian motion by the Lévy Ciesielski series of Haar and Schauder functions and describes the Smoluchowski Kramers high friction limit of the Langevin equation. It treats squared Bessel processes and their additivity, Lamperti's time change, and Dufresne's identity for the perpetuity of geometric Brownian motion, sampled by one Gamma variable. It tabulates eight identities, seven of them as samplers, and checks four algorithms (perpetuity, Bougerol, maximum, first passage time with drift) against exact distribution functions and Euler schemes by Kolmogorov Smirnov distance. The exit time from $(-1,1)$ is an infinite sum of exponentials, four times a Pólya Gamma $PG(1,0)$ variable, sampled exactly only up to truncation. Also covered: the reflection principle, arcsine laws, Girsanov's theorem, local time, Ray Knight theorems, the Biane Pitman Yor identity for the Riemann $\xi$ function (quoted without proof), Dyson Brownian motion.

## From the literature

The Lévy Ciesielski series; Einstein (1905), Smoluchowski (1906), Perrin (1908, 1909), Langevin (1908) and Wiener (1923) on Brownian motion; the Smoluchowski Kramers limit; Brownian motion of a tagged hard sphere (Bodineau, Gallagher and Saint Raymond 2016); additivity of squared Bessel processes (Shiga and Watanabe); Lamperti (1972); Dufresne (1990); Pitman (1975); Bougerol (1983) and Alili, Dufresne and Yor (1997); Michael, Schucany and Haas (1976); Ciesielski and Taylor (1962) and Kent (1980) on the exit time; Kotani and Watanabe (1982) on Krein strings; Biane, Pitman and Yor (2001) on the Riemann $\xi$ function; Dyson (1962) and Biane (2009); the reflection principle (Bachelier 1900); Lévy's arcsine laws; Girsanov (1960); the Ray Knight theorems (Revuz and Yor 1999).

## New results

The theorems of this chapter are credited in the text to their authors; the algorithms and numerical checks are not catalogued as results. One row of the table of identities is credited to the authors' paper on Yor's identities (Polson and Sokolov 2026) together with Carvalho, Polson and Scott (2010): the squared horseshoe scale $\lambda^2$, a ratio of two independent Gamma(1/2) variables, is a generalized gamma convolution with Thorin mass 1/2 and Laplace transform $e^s\operatorname{erfc}\sqrt s$.

<!-- results:begin -->
No new results of this chapter are catalogued.
<!-- results:end -->

## Key terms

Brownian motion, Wiener process, Lévy Ciesielski construction, Einstein relation, Langevin equation, Bessel process, Lamperti representation, geometric Brownian motion, perpetuity, Dufresne identity, Bougerol identity, Yor identities, exact simulation, reflection principle, first passage time, exit time, Pólya Gamma, Girsanov theorem, local time, Ray Knight theorem, arcsine law, Riemann xi function, Dyson Brownian motion, Levy
