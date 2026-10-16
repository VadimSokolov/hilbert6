# Appendix A. Lévy Processes, Thorin Measures and Related Classes

<!-- cite:begin -->
From *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation* by Nick Polson and Vadim Sokolov (2026), appendix A. Cite as Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1, https://doi.org/10.5281/zenodo.23407620. Book page: https://vsokolov.org/books/hilbert6/. Source: https://github.com/VadimSokolov/hilbert6.
<!-- cite:end -->

This appendix collects the definitions and standard results on infinite divisibility that the book uses, with references for the proofs. It defines Lévy processes, their characteristic exponent through the Lévy Khintchine formula, and the Lévy Itô decomposition into drift, Brownian motion and an independent Poisson jump part with Lévy measure $\nu$. It defines Bernstein, completely monotone, Stieltjes and complete Bernstein functions, and generalized Gamma convolutions (GGC): laws on $[0,\infty)$ with Laplace exponent $\phi(\lambda)=a\lambda+\int\log(1+\lambda/y)\,U(\mathrm{d}y)$, drift $a\ge0$ and Thorin measure $U$, which Stieltjes inversion of $\phi'$ recovers (the formula behind the computational strategy of Chapter 22). It states that the class of GGCs is closed under convolution and weak limits, that every GGC is self decomposable and unimodal, and that hyperbolically completely monotone (HCM) laws are GGCs. It then treats normal scale mixtures by Brownian subordination and extended generalized Gamma convolutions (EGGC), a class that contains the GGCs and the Student $t$, symmetric hyperbolic and logistic laws, and finally the Lee Yang measures of Newman (Section 7.7). The results are presented as standard, with chapter or section numbers of the references.

## From the literature

- The Lévy Khintchine formula, the Lévy Itô decomposition, the characterization of self decomposable laws by their Lévy measure and the characteristic exponent of a Brownian subordinated process (Sato 1999).
- Bernstein, Stieltjes and complete Bernstein functions, and Bernstein's theorem on completely monotone functions (Schilling, Song and Vondraček 2012).
- Generalized Gamma convolutions and Thorin measures (Thorin 1977), and hyperbolically completely monotone laws, with proofs of their closure properties in Bondesson (1992); the lognormal law is a GGC (Thorin 1977).
- Every self decomposable law is unimodal (Yamazato 1978).
- Positive stable laws of index at most one half are HCM (Bosch and Simon 2016).
- Extended generalized Gamma convolutions (Thorin 1978; Bondesson 1992).
- The Lee Yang class of even measures (Newman 1974).

## New results

<!-- results:begin -->
No new results of this appendix are catalogued.
<!-- results:end -->

## Key terms

Lévy process, infinitely divisible law, Lévy Khintchine formula, Lévy Itô decomposition, Lévy measure, Poisson point process, subordinator, Brownian subordination, Laplace exponent, Bernstein function, complete Bernstein function, Stieltjes function, completely monotone function, generalized Gamma convolution, GGC, Thorin measure, Stieltjes inversion, self decomposable law, unimodal law, hyperbolically completely monotone, HCM, generalized inverse Gaussian, normal scale mixture, extended generalized Gamma convolution, EGGC, Student t law, hyperbolic law, logistic law, Pólya Gamma law, Lee Yang measure, Newman class
