# Chapter 7. Scale Mixtures, Thorin Measures and Shot Noise

<!-- cite:begin -->
From *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation* by Nick Polson and Vadim Sokolov (2026), chapter 7. Cite as Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1, https://doi.org/10.5281/zenodo.23327515. Book page: https://vsokolov.org/books/hilbert6/. Source: https://github.com/VadimSokolov/hilbert6.
<!-- cite:end -->

When is a heavy tailed law a scale mixture of Gaussians, and what does the mixing law give as an algorithm? The chapter treats scale mixtures of normals, infinite divisibility, the Lévy Khintchine formula and subordination of Brownian motion. It defines generalized Gamma convolutions (GGC) through Thorin measures, quotes Bondesson's theorem that hyperbolically completely monotone (HCM) laws are GGCs, and defines Pólya Gamma variables $PG(b,c)$, with $PG(1,0)$ a quarter of the Brownian exit time from $(-1,1)$. It proves the Polson, Scott and Windle identity that writes the logistic likelihood as a Gaussian scale mixture, giving a two block Gibbs sampler for Bayesian logistic regression. It proves Campbell's theorem for Poisson processes, deduces that shot noise is infinitely divisible, and proves Bondesson's shot noise representation of a GGC with zero drift and a Thorin measure of finite total mass, a sampling algorithm. It also covers the Lee Yang property (Newman's theorem, quoted without proof), the Matérn covariance as a Gamma mixture, the horseshoe prior, and the Gamma and Dirichlet processes.

## From the literature

Andrews and Mallows (1974) on normal scale mixtures; the Lévy Khintchine formula; Thorin (1977) on generalized Gamma convolutions; Bondesson (1992) on GGCs and HCM laws, and his shot noise representation of GGCs; Bosch and Simon (2016) on stable laws; Campbell (1909), Schottky (1918) and Rice (1944) on shot noise; Newman (1974) on the Lee Yang property; Khinchin (1938) on unimodal laws; Whittle (1954, 1963) and Lindgren, Rue and Lindström (2011) on Matérn fields; Carvalho, Polson and Scott (2010) on the horseshoe prior; Ferguson (1973), Blackwell and MacQueen (1973), Sethuraman (1994) and Regazzini, Lijoi and Prünster (2003) on the Dirichlet process; Pitman and Yor (1997, 2003); James, Roynette and Yor (2008).

## New results

The catalogued results were first stated in papers of the first author: the Pólya Gamma identity in Polson, Scott and Windle (2013) and the horseshoe density bounds in Carvalho, Polson and Scott (2010); the other theorems are credited in the text to their sources.

<!-- results:begin -->
- [Pólya Gamma integral identity for the logistic likelihood](../RESULTS.md#polya_gamma_logistic_identity) (Theorem 7.5, page 85; proved): The logistic likelihood equals an exponential factor times an average, over a Pólya Gamma variable, of Gaussian kernels in the linear predictor, and given the linear predictor that variable again has a Pólya Gamma law. First stated in Polson, Scott and Windle (2013), Bayesian inference for logistic models using Pólya Gamma latent variables, Journal of the American Statistical Association 108, 1339 to 1349.
- [Horseshoe density bounds](../RESULTS.md#horseshoe_density_bounds) (Theorem 7.9, page 89; proved): The marginal density of the horseshoe prior lies between two explicit multiples of logarithms, so it has a logarithmic pole at zero and tails of order theta to the power minus two. First stated in Carvalho, Polson and Scott (2010), The horseshoe estimator for sparse signals, Biometrika 97, 465 to 480.
<!-- results:end -->

## Key terms

scale mixture of normals, Gaussian scale mixture, Andrews Mallows theorem, completely monotone, Lévy Khintchine formula, infinite divisibility, subordinator, generalized Gamma convolution, GGC, Thorin measure, HCM, Pólya Gamma, Polya Gamma, logistic regression, Gibbs sampler, Campbell theorem, shot noise, Lee Yang property, Matérn covariance, horseshoe prior, Dirichlet process, Levy, Matern
