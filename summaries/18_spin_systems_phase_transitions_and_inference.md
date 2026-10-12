# Chapter 18. Spin Systems, Phase Transitions and Inference

<!-- cite:begin -->
From *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation* by Nick Polson and Vadim Sokolov (2026), chapter 18. Cite as Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1, https://doi.org/10.5281/zenodo.23327515. Book page: https://vsokolov.org/books/hilbert6/. Source: https://github.com/VadimSokolov/hilbert6.
<!-- cite:end -->

This chapter asks how statistical mechanics describes Bayesian inference and sampling. It proves the Peierls theorem (a low temperature phase transition of the two dimensional Ising model), the Lee Yang circle theorem on the zeros of the partition function (Asano's lemma proved, the rest sketched), the Nishimori identity and the Gibbs variational principle. It derives the mean field equation of the Curie Weiss model by the Hubbard Stratonovich transformation and Laplace's method, and reports Onsager's solution. Bayes optimal inference in the spiked Wigner model is a planted spin glass on the Nishimori line, and the replica symmetric formula for the mutual information, with the I MMSE relation, locates the phase transitions of the Bayes optimal error. Further topics are statistical versus computational thresholds (planted clique, approximate message passing), double descent of ridge regression, samplers from physics (Metropolis, Glauber, Swendsen Wang, slice and log concave sampling), variational inference, and belief propagation with the Bethe approximation.

## From the literature

Ising model (Lenz 1920; Ising 1925); Peierls argument (Peierls 1936); Lee Yang theorem (Lee and Yang 1952) and Asano's lemma (Asano 1970); Onsager's solution (Onsager 1944) and spontaneous magnetization (Yang 1952); Nishimori identity (Nishimori 1981); replica symmetric formula for the spiked Wigner model (Lelarge and Miolane 2019); I MMSE relation (Guo, Shamai and Verdú 2005); approximate message passing for planted clique (Deshpande and Montanari 2015); Metropolis process on planted clique (Jerrum 1992); ridgeless least squares risk (Hastie, Montanari, Rosset and Tibshirani 2022); Metropolis algorithm (Metropolis et al. 1953); Swendsen Wang algorithm (Swendsen and Wang 1987) as data augmentation (Edwards and Sokal 1988); slice sampling (Damien, Wakefield and Walker 1999); Gibbs variational principle (Donsker and Varadhan 1975); loopy belief propagation and the Bethe free energy (Yedidia, Freeman and Weiss 2005).

## New results

The theorems of this chapter are known results. The running text also reports work of the authors: the critical ridge penalty for Bayesian double descent (Polson and Sokolov 2025), the extension of random walk sampling to log concave densities (Applegate, Kannan and Polson 1990; Frieze, Kannan and Polson 1994), and the witch's hat example, on which local samplers appear to converge while missing a region of substantial mass (Polson 1992).

<!-- results:begin -->
No new results of this chapter are catalogued.
<!-- results:end -->

## Key terms

Ising model, Gibbs measure, phase transition, spontaneous magnetization, Peierls argument, Lee Yang theorem, Curie Weiss model, mean field, Hubbard Stratonovich, Nishimori line, Nishimori identity, spiked Wigner model, planted spin glass, replica symmetric formula, planted clique, statistical computational gap, approximate message passing, double descent, Swendsen Wang, Gibbs variational principle, variational inference, belief propagation, Bethe approximation
