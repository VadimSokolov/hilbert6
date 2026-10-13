# On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation

By Nick Polson and [Vadim Sokolov](https://orcid.org/0000-0002-6618-2965).

Independently published, 2026. Edition 1, version 1.0.0. DOI [10.5281/zenodo.23327515](https://doi.org/10.5281/zenodo.23327515). All versions: [10.5281/zenodo.23327514](https://doi.org/10.5281/zenodo.23327514).

- The book as a PDF: [hilbert6.pdf](https://github.com/VadimSokolov/hilbert6/releases/download/v1.0.0/hilbert6.pdf) (548 pages, 6.3 MB)
- LaTeX source, code and bibliography: [github.com/VadimSokolov/hilbert6](https://github.com/VadimSokolov/hilbert6/tree/v1.0.0)
- Archived copy: [Zenodo](https://zenodo.org/records/23327515)
- This page in Markdown: [index.html.md](https://vsokolov.org/books/hilbert6/index.html.md)
- [How to cite](#how-to-cite)

## Description

In 1900 David Hilbert asked for a mathematical treatment of the axioms of physics, beginning with probability and mechanics, and for the limiting processes that lead from the atomistic view to the laws of motion of continua. This book follows that program, with Henri Poincaré as a central figure: Kolmogorov's axioms, de Finetti's theorem and Sanov's large deviation theorem; ergodic theory and the method of types; Brownian motion, entropy and Nelson's stochastic mechanics; kinetic theory, Lanford's theorem and the passage from the Boltzmann equation to the Navier Stokes equations.

It then adds the inverse passage, from observed fluids back to the states that produced them. Part IV treats the inverse problem of a partial differential equation as Bayesian estimation on its solution manifold. For linear equations the adjoint evolution of the data is a sufficient statistic; for nonlinear equations it is asymptotically sufficient under a uniform Bernstein von Mises statement that the book states and leaves open. The cost of generative computation depends on the dimension that the data can resolve, and examples and experiments cover the heat, Navier Stokes and Schrödinger equations.

The last part treats inference itself as statistical mechanics: spin systems and Lee Yang zeros, Schrödinger bridges and generative Bayesian computation, gates as approximate nonlinear filters, and the thermodynamics of information. A final chapter lists open problems and builds a bridge to Hilbert's eighth problem through the de Bruijn Newman heat flow. Every chapter closes with exercises, and the Python code behind the computed figures and tables is in the repository.

## Main new results

- [Adjoint representation of the sufficient statistic](#adjoint_representation_of_the_sufficient_statistic) (Lemma 15.1, page 206): For a linear evolution equation that is diagonal in a fixed basis, the data statistic that is sufficient for the initial state is the coefficient vector of the time zero value of the solution of the backward adjoint equation driven by the data as point sources.
- [Exact sufficiency, linear case](#exact_sufficiency_linear_case) (Proposition 15.2, page 207): In the linear model with a Gaussian prior the adjoint statistic is sufficient, the posterior given it is the full data posterior, and the conditional quantile map is exactly affine with slope equal to the posterior covariance.
- [Equivalence of the one step efficient score summary with the efficient centering](#equivalence_with_the_efficient_centering) (Proposition 15.5, page 210): Under explicit regularity, rate and Lipschitz conditions, the cross fitted one step efficient score summary agrees with the efficient centering of Nickl's Bernstein von Mises theorem to order smaller than the root N scale in a negative Sobolev norm, so it is a computable center of the Gaussian limit of the posterior.
- [Jiang Wong under a uniform Bernstein von Mises assumption: the posterior mean summary is asymptotically sufficient](#jiang_wong_under_bernstein_von_mises) (Theorem 15.38, page 256): If a Bernstein von Mises theorem holds uniformly over prior typical truths, then conditioning on the posterior mean alone, or on any summary root N equivalent to it, loses nothing at the root N scale: the recentered posterior given the summary and the recentered posterior given all of the data have the same Gaussian limit in Wasserstein distance. Status: conditional on The uniform Bernstein von Mises assumption (Assumption U, clauses (U1) to (U4)) for the posterior mean, and for the one step statistic the same assumption for that statistic; the book does not prove it (Open Question 17.18, Uniformity)..
- [Effective dimension under dissipation](#effective_dimension_under_dissipation) (Theorem 15.46, page 267): For the heat and Stokes equations on the torus with a power law prior, the number of modes in which the data at least halve the prior variance grows like a power of the sample size divided by viscosity times observation time, so dissipation lowers the effective dimension; for a nonlinear forward map, under a uniform Bernstein von Mises hypothesis and assumptions on the training residuals and the summary, a generator need only learn the posterior scale on those modes (in the linear model it needs no training), and the cost of using the prior spread beyond them is bounded explicitly. Status: conditional on Part (ii) for a nonlinear forward map assumes the hypotheses of the book's Theorem 16.10 (Bernstein von Mises for the identity skip quantile generator), among them the uniform Bernstein von Mises assumption (Assumption U, open: Open Question 17.18), the whitened training residual assumption (U2') (the whitened training residuals $\mathcal{D}^{-1/2}\sqrt N(\theta^{(m)}-\hat S^{(m)}_N)$, $\mathcal{D}=\operatorname{diag}(1/\iota_j)$, split, conditionally i.i.d. given the data, into a part whose projections on unit vectors have sub Gaussian norms given the data bounded in probability uniformly over the unit vectors and whose conditional second moment matrix tends in operator norm to the whitened limit covariance $\mathrm{Id}+\Xi$, and a remainder whose conditional mean square norm tends to zero, all in $P^N_{\theta_0}$ probability; the book proves it for training parameters drawn from a proposal localized at the preliminary estimate, under the other hypotheses, and it fails in general for a nonlinear forward map when they are drawn from the prior) and the error bounds $\|\hat S_N-\theta_0\|_{L^2}=o_P(\tilde\delta_N(0))$, with $\tilde\delta_N(0)$ the posterior contraction rate in $L^2$, and $\|\hat S_N-\theta_0\|_{H^{\bar\gamma}}=o_P(1)$, $\bar\gamma\ge2$, on the summary, which the book leaves open for a nonlinear forward map other than reaction diffusion when the preliminary estimates have only the rates of the summary's definition; parts (i) and (iii) and the linear case of part (ii) assume nothing unproved..
- [Transfer of Bernstein von Mises guarantees to the GBC posterior (BvM for GBC)](#bvm_for_gbc) (Theorem 16.2, page 275): If the posterior produced by a generative Bayesian computation (GBC) generator is closer to the exact posterior than the root N scale in Wasserstein distance and concentrates on the localization set with bounded moments, then it inherits the Bernstein von Mises limit of the exact posterior for the initial condition and, for the reaction diffusion and two dimensional Navier Stokes equations, for the trajectory, with exact asymptotic coverage of its credible bands and, for Navier Stokes, attainment of the local asymptotic minimax bound for bounded losses; nothing is assumed about how the generator was trained.
- [No uniform guarantee: minimax lower bound for conditional quantile generators over monotone Hölder classes](#no_uniform_guarantee_for_quantile_generators) (Theorem 16.15, page 290): Any generator, trained on M simulated pairs, that must be accurate at a fixed interior summary value for every conditional law in a monotone Hölder class of conditional quantile maps of smoothness beta on a J dimensional summary has, for some map in the class, Wasserstein error at least a constant free of J times (C M) to the power minus beta over (2 beta plus J) with probability at least 1/8, where C bounds the design density, so root N accuracy uniformly over the class requires at least N to the power 1 plus J over (2 beta) simulations divided by C, more than any polynomial once J grows; reading this as the accuracy condition of the transfer theorem uses the uniform Bernstein von Mises assumption.

## How to cite

Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1, https://doi.org/10.5281/zenodo.23327515.

```bibtex
@book{polsonsokolov2026hilbert6,
  author = {Polson, Nick and Sokolov, Vadim},
  title = {{On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation}},
  year = {2026},
  publisher = {Independently published},
  doi = {10.5281/zenodo.23327515},
  url = {https://vsokolov.org/books/hilbert6/}
}
```

To credit a result, cite the book with the number of the result, for example Polson and Sokolov (2026), Lemma 15.1.

## Chapters

<a id="ch-1"></a>

### Chapter 1. Hilbert's Sixth Problem

Pages 3 to 12.

This chapter states Hilbert's sixth problem (Paris, 1900), the mathematical treatment of the axioms of physics, and the passage from atomistic mechanics to the laws of continua. It separates three readings. The axiomatic reading asks for axioms of probability and of physical theories in the style of Hilbert's Grundlagen der Geometrie. The derivational reading asks for a rigorous derivation of the Boltzmann equation from Newtonian hard sphere dynamics in the Boltzmann Grad scaling, and then of the compressible Euler and incompressible Navier Stokes Fourier equations; the chapter reports Lanford's short time theorem, the Bardos Golse Levermore and Golse Saint Raymond hydrodynamic limits, and the long time results of Deng, Hani and Ma. The inferential reading asks for the initial state of a dynamical system, with its uncertainty, from noisy observations. For it the chapter proves Proposition 1.1: for a Polish state space and a Borel measurable trajectory map into continuous paths, the posterior pushed forward to path space puts probability one on the solution manifold, which is universally measurable, and posterior expectations of Borel path functionals that are nonnegative or integrable are averages of exact solutions. Examples include an ideal gas with an inverse gamma posterior and Perrin's Avogadro number.

#### From the literature

Hilbert's problem list (Hilbert 1900); the Hilbert expansion (Hilbert 1912); Hilbert, von Neumann and Nordheim on quantum mechanics (1928) and von Neumann (1932); Kolmogorov's axioms (Kolmogorov 1933); the hard sphere flow (Alexander 1975); Lanford's theorem (Lanford 1975); the Navier Stokes limit of the Boltzmann equation (Bardos, Golse and Levermore 1991, 1993; Golse and Saint Raymond 2004, 2009); the long time derivation from hard spheres of the Boltzmann, Euler and Navier Stokes Fourier equations (Deng, Hani and Ma 2024, 2025); Bachelier's model of prices (Bachelier 1900); the Gaussian velocity law (Maxwell 1860; Boltzmann 1872, 1877) and the characterization of the Gaussian by independence of $X+Y$ and $X-Y$ (Kac 1939; Bernstein, independently); Gödel's incompleteness theorems (Gödel 1931).

#### New results

The text calls Proposition 1.1 elementary.

- [Posterior on the solution manifold](#posterior_on_the_solution_manifold) (Proposition 1.1, page 7; proved): For a dynamical system on a Polish space whose trajectory map is Borel measurable, the posterior over initial states given noisy observations, pushed forward along the flow, puts probability one on the set of exact trajectories (the solution manifold), so posterior averages of path functionals are averages of exact solutions. New in this book.

#### Key terms

Hilbert's sixth problem, Hilbert's 6th problem, axiomatization of physics, Boltzmann equation, hard sphere gas, Boltzmann Grad limit, Lanford theorem, hydrodynamic limit, Navier Stokes Fourier, Bayesian inverse problem, solution manifold, universally measurable set, Polish space, method of mean values, Bachelier, Avogadro number, inverse gamma prior

<a id="ch-2"></a>

### Chapter 2. Poincaré: Recurrence, Chance and the Crisis of Physics

Pages 13 to 26.

This chapter asks how recurrence, chance and irreversibility fit together in Poincaré's work, and proves the theorems behind it. It proves the Poincaré recurrence theorem for measure preserving maps; Kac's lemma, that the mean return time to a set of positive measure under an ergodic map is the reciprocal of its measure, with an estimate of return times for a mole of gas; a bound with an explicit constant for Poincaré's method of arbitrary functions (the fractional part of $tX$ for a density of bounded variation, the roulette argument); the Gaussian Poincaré inequality, by the Ornstein Uhlenbeck semigroup, with exponential convergence to equilibrium; convergence of random walks on finite groups by Fourier analysis, from Poincaré's card shuffling; and the Maxwell, Poincaré and Borel lemma on the first coordinates of a uniform point on a high dimensional sphere. The historical sections cover the three body problem, the surface of section and the Hénon Heiles system, the probability of causes and the Dreyfus affair, Poincaré's report on Bachelier, his 1912 argument that Planck's law requires quanta, his 1906 coarse and fine entropy, Gauss's derivation of the normal law, and Perelman's entropy and the Poincaré conjecture.

#### From the literature

The Poincaré recurrence theorem (Poincaré 1890; Carathéodory 1919) and Zermelo's objection to the H theorem (Zermelo 1896); Kac's lemma (Kac 1947); the method of arbitrary functions (Poincaré 1899, 1912; Borel 1909; Fréchet 1921; Hopf 1934; Engel 1992); the Kolmogorov Arnold Moser theorem (Kolmogorov 1954; Arnold 1963; Moser 1962); the Gaussian Poincaré inequality (Nash 1958; Chernoff 1981); the upper bound lemma for random walks on groups (Diaconis and Shahshahani 1981); the Maxwell, Poincaré and Borel lemma (Borel 1914; Diaconis and Freedman 1987); Poincaré's quantum paper (Poincaré 1912) and the report on the Bertillon analysis (Darboux, Appell and Poincaré 1904); Gauss's derivation of the normal law (Gauss 1809; Teicher 1961); Ricci flow (Hamilton 1982) and Perelman's entropy (Perelman 2002, 2003).

#### New results

No new results of this chapter are catalogued.

#### Key terms

Poincaré recurrence theorem, Poincare recurrence, Kac lemma, return time, Zermelo objection, H theorem, method of arbitrary functions, roulette, Poincaré inequality, spectral gap, Ornstein Uhlenbeck semigroup, random walk on a finite group, card shuffling, Maxwell Poincaré Borel lemma, three body problem, homoclinic tangle, surface of section, Hénon Heiles, Henon Heiles, KAM theorem, Dreyfus affair, Planck's law, coarse grained entropy, Poincaré conjecture, Ricci flow

<a id="ch-3"></a>

### Chapter 3. Axioms of Probability and Large Deviations

Pages 27 to 38.

This chapter asks what the axioms of probability are and how they connect with large deviations and statistical mechanics. It covers Kolmogorov's axioms (probability space, the Kolmogorov extension theorem, conditional expectation), de Finetti's coherence (Dutch book) theorem, exchangeability with the de Finetti, Hewitt and Savage representation and the Diaconis and Freedman bounds for finite sequences, and molecular chaos as a de Finetti statement, with Sznitman's characterization of chaos. It proves Sanov's theorem for a finite alphabet by the method of types and Gibbs conditioning for a finite alphabet, the equivalence of ensembles behind Jaynes's maximum entropy principle, and derives the Maxwellian by conditioning on the energy with the Maxwell, Poincaré and Borel lemma. It compares the Cox and Savage axiomatizations and algorithmic randomness (Kolmogorov complexity, Martin Löf tests, the Solomonoff universal prior). It proves the binary de Finetti theorem through the Hausdorff moment problem, with Laplace's rule of succession, sketches Doob's posterior consistency theorem, quotes the Bernstein von Mises theorem, and relates Sanov's theorem to Cramér's theorem, exponential tilting, Legendre duality and Varadhan's lemma.

#### From the literature

Kolmogorov's axioms and extension theorem (Kolmogorov 1933); de Finetti's coherence and exchangeability theorems (de Finetti 1937) and the Hewitt and Savage extension (1955); finite exchangeable sequences (Diaconis and Freedman 1980); the characterization of chaos (Sznitman 1991); Boltzmann's counting argument (Boltzmann 1877); Sanov's theorem (Sanov 1957; Dembo and Zeitouni 1998); Gibbs conditioning (Van Campenhout and Cover 1981; Csiszár 1984); the maximum entropy principle (Jaynes 1957); Cox's theorem (Cox 1946) and Halpern's counterexample (Halpern 1999); Savage's axioms (Savage 1954); Kolmogorov complexity (Kolmogorov 1965), Martin Löf randomness (Martin Löf 1966), the Levin Schnorr criterion (Levin 1973; Schnorr 1973) and the universal prior (Solomonoff 1964; Zvonkin and Levin 1970); Doob's consistency theorem (Doob 1949); the Bernstein von Mises theorem (van der Vaart 1998).

#### New results

The chapter's theorems are attributed in the text to the authors listed above.

No new results of this chapter are catalogued.

#### Key terms

Kolmogorov axioms, probability space, Kolmogorov extension theorem, conditional expectation, de Finetti theorem, exchangeability, Dutch book, coherence, molecular chaos, propagation of chaos, Sanov theorem, large deviation principle, relative entropy, Kullback Leibler divergence, method of types, Gibbs conditioning, equivalence of ensembles, maximum entropy, Maxwellian, Cox theorem, Kolmogorov complexity, algorithmic randomness, Solomonoff prior, Doob consistency, Bernstein von Mises, Cramér theorem, Varadhan lemma, rule of succession

<a id="ch-4"></a>

### Chapter 4. Ergodic Theory: From Boltzmann's Hypothesis to Entropy

Pages 39 to 52.

This chapter asks whether Boltzmann's ergodic hypothesis, that time averages equal averages over the energy surface, can justify equilibrium measures in statistical mechanics, and what replaces it when it fails. It develops measure preserving systems, ergodicity, mixing and the Koopman operator, and proves von Neumann's mean ergodic theorem, the maximal ergodic lemma, Birkhoff's pointwise ergodic theorem, Weyl's equidistribution theorem, mixing of the Arnold cat map, and the arcsine invariant density, Lyapunov exponent and Kolmogorov Sinai entropy $\log 2$ of the logistic map at $r=4$. The Kolmogorov Sinai generator theorem, the Shannon McMillan Breiman theorem and Ornstein's isomorphism theorem are quoted without proof. KAM theory and the Chirikov standard map illustrate the failure of ergodicity for typical Hamiltonian systems with few degrees of freedom, and Khinchin's concentration argument shows that, for noninteracting particles, infinite time averages of sum functions are close to phase averages for most initial conditions without ergodicity. The chapter relates the ergodic decomposition to de Finetti's theorem and ends with spectral gaps, the Kipnis Varadhan central limit theorem and Markov chain Monte Carlo.

#### From the literature

The ergodic hypothesis (Boltzmann 1871) and its failure read literally (Rosenthal 1913, Plancherel 1913); the mean ergodic theorem (von Neumann 1932); the maximal ergodic lemma (Hopf 1937, proof of Garsia 1965); the pointwise ergodic theorem (Birkhoff 1931); equidistribution of irrational rotations (Weyl 1916); weak mixing (Koopman and von Neumann 1932); the cat map (Arnold and Avez 1968); Kolmogorov Sinai entropy (Kolmogorov 1958, 1959, Sinai 1959); the Shannon McMillan Breiman theorem (Shannon 1948, McMillan 1953, Breiman 1957); the isomorphism theorem for Bernoulli shifts (Ornstein 1970); the logistic map at $r=4$ as a random number generator (Ulam and von Neumann 1947); KAM theory (Kolmogorov 1954, Arnold 1963, Moser 1962); Khinchin's concentration argument (Khinchin 1949); the central limit theorem for reversible Markov chains (Kipnis and Varadhan 1986).

#### New results

The chapter presents results of the literature, and the book claims none of its theorems as new.

No new results of this chapter are catalogued.

#### Key terms

ergodic theory, ergodic hypothesis, ergodicity, measure preserving system, Koopman operator, mean ergodic theorem, Birkhoff ergodic theorem, Weyl equidistribution, unique ergodicity, mixing, weak mixing, Arnold cat map, Kolmogorov Sinai entropy, metric entropy, Shannon McMillan Breiman theorem, asymptotic equipartition, Ornstein isomorphism theorem, Bernoulli shift, logistic map, Lyapunov exponent, KAM theory, standard map, Khinchin, ergodic decomposition, de Finetti theorem, spectral gap, Kipnis Varadhan central limit theorem, MCMC

<a id="ch-5"></a>

### Chapter 5. The Method of Types and Moment Conditioning

Pages 53 to 66.

This chapter asks why conditioning a large system of independent particles on macroscopic moments produces the exponential families, Gibbs distributions and Maxwellians of statistical mechanics, and how fast. It uses the method of types: sequences over a finite alphabet are counted by their empirical distribution (type), which turns Boltzmann's count $\log W=nH$ into exact nonasymptotic bounds. It proves the type counting bounds, Csiszár's Pythagorean inequality for the I projection onto a closed convex set of laws, with the exponential tilt form for linear families, the conditional limit theorem, and Stein's lemma by types. It computes the conditional law exactly for exponential and Poisson samples, shows that conditioning independent Gaussian velocity vectors on their mean and kinetic energy gives the Maxwellian, and treats Bayes mixtures as universal codes with minimax regret. It also covers Chernoff information and types for Markov chains. A closing section reads Boltzmann's $H$ theorem through types and says that this reading is not a theorem.

#### From the literature

Boltzmann's count of microstates (Boltzmann 1877); Sanov's theorem (Sanov 1957); the method of types (Csiszár and Körner 2011, Cover and Thomas 2006); the I projection, Pythagorean inequality and exponential form (Csiszár 1975); the conditional limit theorem (Van Campenhout and Cover 1981, Csiszár 1984); finite exchangeable sequences and sampling bounds (Diaconis and Freedman 1980, 1987); the maximum entropy principle (Jaynes 1957); iterative proportional fitting and Sinkhorn's algorithm (Deming and Stephan 1940, Sinkhorn 1964); Laplace's rule of succession (Laplace 1814); universal coding (Krichevsky and Trofimov 1981, Shtarkov 1987, Xie and Barron 2000); Stein's lemma (Chernoff 1956) and Chernoff information (Chernoff 1952); types for Markov chains (Whittle 1955; Davisson, Longo and Sgarro 1981; Csiszár, Cover and Choi 1987) and the Donsker Varadhan rate function (Donsker and Varadhan 1975).

#### New results

The chapter presents results of the literature and exact computations, and the book claims none of them as new.

No new results of this chapter are catalogued.

#### Key terms

method of types, type class, empirical distribution, Sanov theorem, large deviations, relative entropy, Kullback Leibler divergence, I projection, information projection, Pythagorean identity, exponential tilt, exponential family, maximum entropy principle, Gibbs conditioning, conditional limit theorem, equivalence of ensembles, Maxwellian, moment conditioning, microcanonical ensemble, finite de Finetti theorem, Laplace rule of succession, Bayes mixture, universal code, minimax regret, Krichevsky Trofimov, Shtarkov, Jeffreys prior, minimum description length, Stein lemma, Chernoff information, hypothesis testing, Markov types, iterative proportional fitting, Sinkhorn algorithm

<a id="ch-6"></a>

### Chapter 6. Brownian Motion and Yor's Identities as Algorithms

Pages 69 to 82.

How can Yor's identities in law for Brownian functionals be turned into exact simulation algorithms? Following the authors' paper Yor's Identities as Algorithms, an identity in law between a Brownian functional and independent Gamma, normal, exponential or uniform variables is read as a sampler with no discretization, Markov chain or rejection step. The chapter builds Brownian motion by the Lévy Ciesielski series of Haar and Schauder functions and describes the Smoluchowski Kramers high friction limit of the Langevin equation. It treats squared Bessel processes and their additivity, Lamperti's time change, and Dufresne's identity for the perpetuity of geometric Brownian motion, sampled by one Gamma variable. It tabulates eight identities, seven of them as samplers, and checks four algorithms (perpetuity, Bougerol, maximum, first passage time with drift) against exact distribution functions and Euler schemes by Kolmogorov Smirnov distance. The exit time from $(-1,1)$ is an infinite sum of exponentials, four times a Pólya Gamma $PG(1,0)$ variable, sampled exactly only up to truncation. Also covered: the reflection principle, arcsine laws, Girsanov's theorem, local time, Ray Knight theorems, the Biane Pitman Yor identity for the Riemann $\xi$ function (quoted without proof), Dyson Brownian motion.

#### From the literature

The Lévy Ciesielski series; Einstein (1905), Smoluchowski (1906), Perrin (1908, 1909), Langevin (1908) and Wiener (1923) on Brownian motion; the Smoluchowski Kramers limit; Brownian motion of a tagged hard sphere (Bodineau, Gallagher and Saint Raymond 2016); additivity of squared Bessel processes (Shiga and Watanabe); Lamperti (1972); Dufresne (1990); Pitman (1975); Bougerol (1983) and Alili, Dufresne and Yor (1997); Michael, Schucany and Haas (1976); Ciesielski and Taylor (1962) and Kent (1980) on the exit time; Kotani and Watanabe (1982) on Krein strings; Biane, Pitman and Yor (2001) on the Riemann $\xi$ function; Dyson (1962) and Biane (2009); the reflection principle (Bachelier 1900); Lévy's arcsine laws; Girsanov (1960); the Ray Knight theorems (Revuz and Yor 1999).

#### New results

The theorems of this chapter are credited in the text to their authors; the algorithms and numerical checks are not catalogued as results. One row of the table of identities is credited to the authors' paper on Yor's identities (Polson and Sokolov 2026) together with Carvalho, Polson and Scott (2010): the squared horseshoe scale $\lambda^2$, a ratio of two independent Gamma(1/2) variables, is a generalized gamma convolution with Thorin mass 1/2 and Laplace transform $e^s\operatorname{erfc}\sqrt s$.

No new results of this chapter are catalogued.

#### Key terms

Brownian motion, Wiener process, Lévy Ciesielski construction, Einstein relation, Langevin equation, Bessel process, Lamperti representation, geometric Brownian motion, perpetuity, Dufresne identity, Bougerol identity, Yor identities, exact simulation, reflection principle, first passage time, exit time, Pólya Gamma, Girsanov theorem, local time, Ray Knight theorem, arcsine law, Riemann xi function, Dyson Brownian motion, Levy

<a id="ch-7"></a>

### Chapter 7. Scale Mixtures, Thorin Measures and Shot Noise

Pages 83 to 92.

When is a heavy tailed law a scale mixture of Gaussians, and what does the mixing law give as an algorithm? The chapter treats scale mixtures of normals, infinite divisibility, the Lévy Khintchine formula and subordination of Brownian motion. It defines generalized Gamma convolutions (GGC) through Thorin measures, quotes Bondesson's theorem that hyperbolically completely monotone (HCM) laws are GGCs, and defines Pólya Gamma variables $PG(b,c)$, with $PG(1,0)$ a quarter of the Brownian exit time from $(-1,1)$. It proves the Polson, Scott and Windle identity that writes the logistic likelihood as a Gaussian scale mixture, giving a two block Gibbs sampler for Bayesian logistic regression. It proves Campbell's theorem for Poisson processes, deduces that shot noise is infinitely divisible, and proves Bondesson's shot noise representation of a GGC with zero drift and a Thorin measure of finite total mass, a sampling algorithm. It also covers the Lee Yang property (Newman's theorem, quoted without proof), the Matérn covariance as a Gamma mixture, the horseshoe prior, and the Gamma and Dirichlet processes.

#### From the literature

Andrews and Mallows (1974) on normal scale mixtures; the Lévy Khintchine formula; Thorin (1977) on generalized Gamma convolutions; Bondesson (1992) on GGCs and HCM laws, and his shot noise representation of GGCs; Bosch and Simon (2016) on stable laws; Campbell (1909), Schottky (1918) and Rice (1944) on shot noise; Newman (1974) on the Lee Yang property; Khinchin (1938) on unimodal laws; Whittle (1954, 1963) and Lindgren, Rue and Lindström (2011) on Matérn fields; Carvalho, Polson and Scott (2010) on the horseshoe prior; Ferguson (1973), Blackwell and MacQueen (1973), Sethuraman (1994) and Regazzini, Lijoi and Prünster (2003) on the Dirichlet process; Pitman and Yor (1997, 2003); James, Roynette and Yor (2008).

#### New results

The catalogued result is an identity from Polson, Scott and Windle (2013), a paper of the first author; the other theorems are credited in the text to their sources.

- [Pólya Gamma integral identity for the logistic likelihood](#polya_gamma_logistic_identity) (Theorem 7.5, page 85; proved): The logistic likelihood equals an exponential factor times an average, over a Pólya Gamma variable, of Gaussian kernels in the linear predictor, and given the linear predictor that variable again has a Pólya Gamma law. First stated in Polson, Scott and Windle (2013), Bayesian inference for logistic models using Pólya Gamma latent variables, Journal of the American Statistical Association 108, 1339 to 1349.

#### Key terms

scale mixture of normals, Gaussian scale mixture, Andrews Mallows theorem, completely monotone, Lévy Khintchine formula, infinite divisibility, subordinator, generalized Gamma convolution, GGC, Thorin measure, HCM, Pólya Gamma, Polya Gamma, logistic regression, Gibbs sampler, Campbell theorem, shot noise, Lee Yang property, Matérn covariance, horseshoe prior, Dirichlet process, Levy, Matern

<a id="ch-8"></a>

### Chapter 8. Entropy, Perelman and the Uncertainty Principle

Pages 93 to 104.

This chapter relates entropy, Fisher information and the heat flow, and applies the relation to Perelman's entropy, the uncertainty principle and Bayesian computation. It proves de Bruijn's identity, the Cramér Rao bound, Stam's inequality, the Gaussian and Euclidean forms of Gross's logarithmic Sobolev inequality with their equivalence, and McKean's formula for the second derivative of entropy. On flat space it proves, by Bochner's identity, that Perelman's entropy, a scale invariant combination of entropy and Fisher information, is nonincreasing along the heat equation from a density of finite variance and tends to zero as $\tau\to\infty$, so it is nonnegative, and that this nonnegativity is equivalent to the Euclidean log Sobolev inequality. A probabilistic proof for scale mixtures, from the authors' paper with Zantedeschi (2026), is described. Further sections derive Heisenberg's inequality from Fisher information, quote the Jordan Kinderlehrer Otto theorem without proof, and cover Herbst's concentration argument, the I MMSE identity and transport inequalities.

#### From the literature

Boltzmann's H functional (1872), Shannon entropy (1948), Fisher information (Fisher 1925). De Bruijn's identity (in Stam 1959, integrated form Barron 1986), Stam's inequality (Stam 1959, Blachman 1965), the entropy power inequality (Shannon 1948, Stam 1959). The log Sobolev inequality (Gross 1975), derived from Stam's inequality (Carlen 1991), and exponential decay of relative entropy (Bakry and Émery 1985). McKean's identity (McKean 1966). Perelman's entropy formula (Perelman 2002) and its linear heat equation analogue (Ni 2004). The entropic uncertainty principle (conjectured by Hirschman 1957, proved by Beckner 1975 and by Białynicki Birula and Mycielski 1975). The Jordan Kinderlehrer Otto theorem (1998), displacement convexity (McCann 1997), the HWI inequality (Otto and Villani 2000), Talagrand's inequality (1996), Ricci curvature as entropy convexity (von Renesse and Sturm 2005, Lott and Villani 2009). Herbst's argument (Ledoux 2001). The I MMSE identity (Guo, Shamai and Verdú 2005).

#### New results

No new results of this chapter are catalogued.

#### Key terms

differential entropy, Boltzmann H functional, Shannon entropy, Fisher information, de Bruijn identity, Stam inequality, Cramér Rao bound, Cramer Rao, entropy power inequality, logarithmic Sobolev inequality, Bakry Émery criterion, Bochner identity, Perelman entropy, Ricci flow, scale mixture, subordinated Brownian motion, Heisenberg uncertainty principle, entropic uncertainty principle, JKO scheme, Wasserstein gradient flow, Fokker Planck equation, HWI inequality, Talagrand inequality, Herbst argument, I MMSE, mutual information, Langevin sampling

<a id="ch-9"></a>

### Chapter 9. Quantum Mechanics: von Neumann, Nelson and Wick

Pages 105 to 114.

This chapter asks in what sense quantum mechanics is a probability theory and how it connects back to Brownian motion. It states the von Neumann axioms, explains that noncommuting observables have no joint distribution, quotes Gleason's theorem without proof, and derives the CHSH form of Bell's inequality, stating Fine's converse and Tsirelson's bound. It writes the Schrödinger equation in Madelung form, where the average of Bohm's quantum potential is a multiple of the Fisher information, and derives Nelson's theorem: for smooth positive $\rho$ and smooth $S$, a diffusion with diffusion constant $\hbar/2m$, density $\rho(\cdot,t)$ at time $t$ and forward drift determined by $\rho$ and $S$ obeys the stochastic Newton law if and only if $\psi=\sqrt\rho\,e^{iS/\hbar}$ solves the Schrödinger equation, after $S$ is changed by a function of time alone. It treats the harmonic oscillator as an Ornstein Uhlenbeck process and discusses the theory's difficulties. In imaginary time (Wick rotation) it gives a proof sketch of the Feynman Kac formula and states the Donsker Varadhan formula for the ground state energy. Further sections cover Euclidean quantum field theory, the Schrödinger bridge problem, quantum relative entropy and Bayesian updating, and diffusion Monte Carlo.

#### From the literature

Axiomatization of quantum mechanics (Hilbert, von Neumann and Nordheim 1928; von Neumann 1927, 1930, 1932). Gleason's theorem (1957). Bell's theorem (1964), the CHSH inequality (Clauser, Horne, Shimony and Holt 1969), Fine (1982), Tsirelson's bound (1980), Bell tests (Aspect, Dalibard and Roger 1982; Hensen et al., Giustina et al. and Shalm et al. 2015). Madelung's equations (1927). Nelson's stochastic mechanics (1966), existence of the diffusion (Carlen 1984), Wallstrom's objection (1994). The Feynman Kac formula (Kac 1949). Osterwalder and Schrader reconstruction (1973, corrected 1975). The Schrödinger problem (Schrödinger 1931, Fortet 1940, Beurling 1960, Jamison 1975, Föllmer 1988). Klein's inequality (1931), monotonicity of quantum relative entropy (Lindblad 1975, Uhlmann 1977), Lüders' rule (1951), quantum sufficiency (Petz 1986, 1988), propagation of chaos (Del Moral 2004).

#### New results

No new results of this chapter are catalogued.

#### Key terms

quantum mechanics axioms, density operator, density matrix, Born rule, Gleason's theorem, quantum probability, Bell's theorem, CHSH inequality, Tsirelson bound, Madelung equations, quantum potential, Nelson stochastic mechanics, osmotic velocity, Wallstrom objection, Ornstein Uhlenbeck process, Feynman Kac formula, Wick rotation, imaginary time, Donsker Varadhan, Osterwalder Schrader, Euclidean quantum field theory, Schrödinger bridge, von Neumann entropy, quantum relative entropy, Lüders rule, Petz recovery, quantum state tomography, diffusion Monte Carlo

<a id="ch-10"></a>

### Chapter 10. Kinetic Theory: Boltzmann, Kac and Propagation of Chaos

Pages 117 to 132.

When does molecular chaos, independence between particles, propagate in time, and how does the irreversible Boltzmann equation arise from reversible particle dynamics? The chapter proves the weak form of the collision operator, the collision invariants for continuous functions and Boltzmann's H theorem for smooth positive rapidly decaying spatially homogeneous solutions. For hard spheres in the Boltzmann Grad scaling it writes the BBGKY hierarchy, states Lanford's theorem on a short time interval, the Lanford window, with a sketch of the proof, proves the abstract Cauchy Kovalevskaya lemma behind the window, and quotes without proof the long time theorem of Deng, Hani and Ma. It quotes Kac's propagation of chaos theorem without proof, proves a coupling bound of order $N^{-1/2}$ for McKean Vlasov mean field diffusions with Lipschitz interaction and initial data of finite second moment, and analyzes Kac's ring, an exactly solvable model of the arrow of time. Shorter sections cover the Lorentz gas, the Vlasov equation, Grad's moment method and ergodic theory.

#### From the literature

- H theorem (Boltzmann 1872); Cercignani's conjecture, its failure in general (Bobylev and Cercignani 1999) and a weaker bound (Villani 2003)
- Lanford's theorem for hard spheres (Lanford 1975); complete proofs (Cercignani, Illner and Pulvirenti 1994; Gallagher, Saint Raymond and Texier 2014)
- Long time derivation from hard spheres (Deng, Hani and Ma 2024)
- Kac model and propagation of chaos (Kac 1956); Kac's ring (Kac 1959)
- Kac's program (Janvresse 2001; Carlen, Carvalho and Loss 2003; Villani 2003; Mischler and Mouhot 2013; Gao, Wang and Xia 2026, preprint)
- McKean Vlasov coupling (Sznitman 1991)
- Lorentz gas, random and periodic scatterers (Gallavotti 1969; Spohn 1978; Boldrighini, Bunimovich and Sinai 1983; Golse 2008; Marklof and Strömbergsson 2011)
- Vlasov mean field limit (Braun and Hepp 1977; Dobrushin 1979); Landau damping (Mouhot and Villani 2011)
- Moment closures (Grad 1949; Levermore 1996)
- Boltzmann Sinai ergodic hypothesis for hard ball systems on tori (Simányi 2003, 2004, 2009, 2013)

#### New results

No new results of this chapter are catalogued.

#### Key terms

Boltzmann equation, H theorem, collision invariants, molecular chaos, Stosszahlansatz, propagation of chaos, BBGKY hierarchy, Boltzmann Grad limit, hard spheres, Lanford theorem, Lanford window, Cauchy Kovalevskaya, Cauchy Kowalevski, Kac model, Kac ring, McKean Vlasov, mean field limit, Wasserstein distance, Loschmidt paradox, Zermelo recurrence, arrow of time, Lorentz gas, Vlasov equation, moment closure

<a id="ch-11"></a>

### Chapter 11. From Boltzmann to Navier Stokes

Pages 133 to 142.

Can the equations of fluid dynamics be derived from the Boltzmann equation and from particle systems, the second limit in Hilbert's sixth problem? The chapter presents the Hilbert and Chapman Enskog expansions, the compressible Euler limit through the truncated Hilbert expansion (Caflisch's theorem in one space dimension, quoted without proof), and the linearized collision operator (Hilbert, Grad), for which it shows nonnegativity, identifies the kernel through the collision invariants, and quotes compactness and the spectral gap. It gives the formal derivation of the incompressible Navier Stokes Fourier system from the Bardos, Golse and Levermore scaling, with viscosity and heat conductivity as Green Kubo type coefficients, and surveys the acoustic, Stokes Fourier and incompressible Euler regimes. It proves the hydrodynamic limit of the symmetric simple exclusion process to the heat equation, computes the BGK transport coefficients (Prandtl number one), and reports the derivation of fluid equations from hard sphere dynamics on the torus by Deng, Hani and Ma, with three limitations of the derivation.

#### From the literature

- Hilbert expansion and linearized collision operator (Hilbert 1912; Grad 1963); Chapman Enskog expansion (Chapman 1916; Enskog 1917); the BGK model (Bhatnagar, Gross and Krook 1954)
- Euler limit from the Hilbert expansion (Caflisch 1980; Guo, Jang and Jiang 2009)
- Incompressible Navier Stokes Fourier limit: formal (Bardos, Golse and Levermore 1991), rigorous for renormalized solutions (Golse and Saint Raymond 2004, 2009; Levermore and Masmoudi 2010)
- Acoustic and Stokes Fourier limits (Golse and Levermore 2002); incompressible Euler limit (Saint Raymond 2003)
- Hydrodynamic limits of particle systems (Guo, Papanicolaou and Varadhan 1988; Yau 1991); large deviations (Kipnis, Olla and Varadhan 1989; Bertini, De Sole, Gabrielli, Jona Lasinio and Landim 2015)
- Fluid equations from hard spheres on the torus (Deng, Hani and Ma 2025), who state that it resolves Hilbert's sixth problem as it pertains to deriving fluid equations from Newton's laws through Boltzmann's kinetic theory, as long as the fluid solutions are smooth

#### New results

No new results of this chapter are catalogued.

#### Key terms

Hilbert expansion, Chapman Enskog expansion, Knudsen number, hydrodynamic limit, fluid dynamic limit, compressible Euler equations, incompressible Navier Stokes Fourier system, linearized Boltzmann operator, Fredholm alternative, Bardos Golse Levermore, Green Kubo, transport coefficients, Prandtl number, BGK model, symmetric simple exclusion process, heat equation, macroscopic fluctuation theory, Hilbert sixth problem

<a id="ch-12"></a>

### Chapter 12. Navier Stokes as Inference on the Solution Manifold

Pages 143 to 170.

This chapter treats the Navier Stokes equations as a Bayesian inverse problem on the solution manifold: from noisy, incomplete observations of the velocity or vorticity, infer the initial condition and push the posterior through the solution map. The linear case, the backward heat equation with Gaussian priors, is solved exactly, with logarithmic posterior contraction and a Bernstein von Mises theorem for linear functionals with fast decaying coefficients. The nonlinear theory of Nickl and coauthors is presented, including gradient stability and polynomial time Langevin sampling from a warm start, proved by Nickl and Wang for a Schrödinger equation. The chapter deduces a gradient stability bound for the initial condition of the two dimensional Navier Stokes equations when time zero is observed, and lists the other steps for Navier Stokes as open. It shows that a generator trained on simulations (generative Bayesian computation) inherits the Bernstein von Mises theorem when accurate at the posterior scale. It also reviews Hellinger well posedness and preconditioned Crank Nicolson sampling, with computed posteriors for the Fisher Kolmogorov and vorticity equations.

#### From the literature

Global solutions in two dimensions (Leray, Ladyzhenskaya, Lions); backward uniqueness (Bardos and Tartar 1973); well posedness of the posterior (Stuart 2010; Dashti and Stuart 2017); the Cameron Martin formula and Feldman Hájek dichotomy (proved in Bogachev 1998); contraction and credible sets for the heat equation (Knapik, van der Vaart and van Zanten 2013); Bernstein von Mises theorems (Castillo and Nickl 2013; Nickl 2024; Konen and Nickl 2026); nonlinear inverse problems (Nickl 2023); posterior consistency for Navier Stokes (Nickl and Titi 2024); gradient stability and polynomial time Langevin sampling (Nickl and Wang 2024; Bohr and Nickl 2024; Castre and Nickl 2026; Durmus and Moulines 2019); preconditioned Crank Nicolson (Cotter, Roberts, Stuart and White 2013); the Fisher Kolmogorov equation (Fisher 1937; Kolmogorov, Petrovsky and Piskunov 1937); the ensemble Kalman filter (Evensen 1994).

#### New results

The theorems of Nickl and Wang, of Cameron Martin, Feldman and Hájek, and of Stuart are results of other authors, quoted without proof or with a sketch, and are not listed.

- [Gradient stability for the initial condition of two dimensional Navier Stokes, with time zero observed](#gradient_stability_initial_condition_ns2d) (Proposition 12.8, page 153; proved): Using estimates of Konen and Nickl, the map from the first D Stokes coefficients of the initial velocity of the two dimensional Navier Stokes equations on the torus to the solution observed over space and over a time window that starts at zero is gradient stable on a Sobolev ball, with a constant of order D to the power minus one half. New in this book.
- [Bernstein von Mises for generators](#bernstein_von_mises_for_generators) (Proposition 12.10, page 157; proved): If the posterior of a functional satisfies a Bernstein von Mises theorem at the square root n scale and a generator is close to the posterior in the bounded Lipschitz metric after both are centered and rescaled by the square root of n, then the generated law satisfies the same Bernstein von Mises theorem. New in this book.

#### Key terms

Bayesian inverse problem, Navier Stokes, solution manifold, data assimilation, backward heat equation, posterior contraction, Bernstein von Mises, gradient stability, unadjusted Langevin algorithm, polynomial time sampling, Cameron Martin space, Hellinger distance, preconditioned Crank Nicolson, pCN, Hamiltonian Monte Carlo, generative Bayesian computation, Fisher Kolmogorov equation, Fisher KPP, vorticity equation, 4DVar, ensemble Kalman filter.

<a id="ch-13"></a>

### Chapter 13. The Boundary of the Manifold: Blowup, Turbulence and Steady Flows

Pages 171 to 182.

This chapter studies the boundary of the solution manifold of the Navier Stokes equations: finite time blowup, turbulence and steady flows. It reviews Leray weak solutions and the regularity problem, hypodissipative equations and Matérn fields, Kolmogorov's 1941 and 1962 turbulence theories (the $k^{-5/3}$ spectrum, the four fifths law, intermittency), Onsager's conjecture, Burgers' equation, and Bayesian flow MRI. The one result it proves is statistical: in a linear model for the reciprocal of the vorticity supremum norm, with Gaussian errors of known variance and a flat prior, the posterior probability of no blowup is an explicit normal probability, and the Fieller confidence set for the blowup time (Fieller 1954) is bounded exactly when the slope is significantly nonzero. Sparse priors for forcing and a posterior for the hypodissipation exponent are only proposed. Regularity for smooth data in $\mathbb{R}^3$ without boundary remains open.

#### From the literature

Leray weak solutions (Leray 1934); no nontrivial Leray self similar profiles in $L^q$ for $q\ge3$ (Nečas, Růžička and Šverák 1996; Tsai 1998); no blowup of unforced solutions bounded in $L^\infty_tL^3_x$ (Escauriaza, Seregin and Šverák 2003); partial regularity (Caffarelli, Kohn and Nirenberg 1982); the Beale Kato Majda criterion (1984); blowup for an averaged equation (Tao 2016); nonuniqueness of weak solutions (Buckmaster and Vicol 2019) and of forced Leray solutions (Albritton, Brué and Colombo 2022); Euler blowup (Elgindi 2021 for $C^{1,\alpha}$ velocities; Chen and Hou 2022, 2025 with a boundary); forced blowup for Euler, porous media and hypodissipative equations (Córdoba and Martínez Zoroa 2023, 2024; Córdoba, Martínez Zoroa and Zheng 2026); global regularity for dissipation exponent at least 5/4 (Lions 1969; logarithmic improvement in Tao 2009); Kolmogorov 1941, 1962 and Obukhov 1962; four fifths laws under hypotheses (Duchon and Robert 2000; Eyink 2003; Bedrossian and coauthors 2019); Onsager's conjecture (Onsager 1949; Constantin, E and Titi 1994; Isett 2018); Hopf Cole transform (Hopf 1950; Cole 1951) and Burgers turbulence (Sinai 1992); Bayesian flow MRI (Kontogiannis and coauthors 2025); Fieller set (Fieller 1954).

#### New results

The theorem on Onsager's conjecture (Constantin, E and Titi; Isett) is quoted without proof and is not listed.

No new results of this chapter are catalogued.

#### Key terms

finite time blowup, singularity, regularity problem, Leray solutions, Beale Kato Majda criterion, partial regularity, convex integration, nonuniqueness, hypodissipative Navier Stokes, Matérn field, K41, K62, four fifths law, intermittency, anomalous dissipation, Onsager conjecture, Burgers equation, Hopf Cole transform, flow MRI, Fieller interval, Fieller's theorem, blowup time posterior, self similar blowup, type I blowup, magnetic resonance velocimetry.

<a id="ch-14"></a>

### Chapter 14. The Inverse Problem on the Solution Manifold

Pages 185 to 204.

Chapter 14 opens Part IV with the Bayesian inverse problem for the initial condition $\theta$ of an evolution equation, observed through noisy values of the solution at $N$ random space time points, with a Gaussian process prior on $\theta$. It summarizes the framework of Nickl and coauthors for nonlinear parabolic equations (heat, reaction diffusion, two dimensional Navier Stokes): Bernstein von Mises theorems for the posterior in a weak norm and in the supremum norm on forward trajectories, exact coverage of credible bands and local asymptotic minimax efficiency. It then introduces the solution manifold $\mathcal M=\{u_\theta\}$: posterior draws of the field solve the equation exactly, the Gaussian limit lives on the tangent space, and prediction beyond the observation window needs no extrapolation model. For the heat equation a closed form comparison with an unconstrained space time Gaussian process prior, with the Gram matrix of the design replaced by its limit, shows the posterior standard deviation shrinking in time. The chapter states the generative Bayesian computation (GBC) algorithm and compares GBC with function space MCMC, ensemble Kalman inversion, Laplace approximation, transport maps and simulation based inference. It proves that the Gaussian limit is nondegenerate for the reaction diffusion class of Nickl's trajectory theorem ($\partial_tu-\Delta u=f(u)$, $f$ smooth with compact support, torus of dimension at most three).

#### From the literature

Bernstein von Mises theorems for the posterior of the initial condition of nonlinear parabolic equations, in a weak norm and in supremum norm on forward trajectories (Nickl 2024). For two dimensional Navier Stokes: these theorems, exact coverage of credible bands, the Fredholm decomposition of the information operator and local asymptotic minimax efficiency of the posterior mean (Konen and Nickl 2026, with Konen 2026). Inverse logarithmic contraction rates (Nickl and Titi 2024). Polynomial time Langevin computation of posteriors (Nickl and Wang 2024). Gaussian process regression under linear equations (Raissi, Perdikaris and Karniadakis 2017; Albert and Rath 2020). For a nonlinear forward map, the large ensemble limit of ensemble Kalman inversion is a linear Bayes estimator, not the posterior (Ernst, Sprungk and Starkloff 2015).

#### New results

The new results are a nondegeneracy lemma and the manifold gain for the heat equation.

- [Nondegeneracy of the Gaussian limit of the posterior trajectory for reaction diffusion equations](#the_limit_law_is_nondegenerate) (Lemma 14.3, page 189; proved): For the reaction diffusion equation, the Gaussian limit law of the posterior forward trajectory in the supremum norm is nondegenerate: its reproducing kernel Hilbert space is nontrivial and the distribution function of its supremum norm is continuous and strictly increasing, which is the property that the argument for exact asymptotic coverage of credible bands uses. New in this book.
- [Manifold gain for the heat equation: prior on the initial condition against a space time Gaussian process prior](#manifold_gain_for_the_heat_equation) (Proposition 14.5, page 193; proved): For the heat equation with Gaussian priors and the design Gram matrix replaced by its limit, the posterior standard deviation of the field under a prior on the initial condition decreases in time, while under a space time Gaussian process prior of comparable regularity it does not depend on time or place, and the ratio of the two at time $t$ is at least $e^{\nu\lambda_1 t}$ times its value at time zero; the effective numbers of parameters of the two models are also given in order. New in this book.

#### Key terms

inverse problem, initial condition, data assimilation, solution manifold, tangent space, manifold gain, Bernstein von Mises theorem, nonlinear parabolic equation, reaction diffusion, heat equation, Navier Stokes, Gaussian process prior, information operator, Fredholm decomposition, credible band, exact coverage, local asymptotic minimax, reproducing kernel Hilbert space, adjoint equation, generative Bayesian computation, GBC, simulation based inference, function space MCMC, ensemble Kalman inversion

<a id="ch-15"></a>

### Chapter 15. Adjoint Sufficient Statistics

Pages 205 to 272.

Which statistic of the data should generative or approximate Bayesian computation (GBC, ABC) condition on when the unknown is the initial condition of a dissipative partial differential equation observed with noise? For linear equations such as heat and Stokes, the adjoint statistic $\Phi^\top Y$, the time zero value of the backward adjoint equation driven by the data, is exactly sufficient together with the design. For nonlinear forward maps (reaction diffusion, two dimensional Navier Stokes) the chapter defines a cross fitted one step efficient score summary, proves it, under rate conditions on its preliminary estimates, root N equivalent to the efficient centering of Nickl's Bernstein von Mises theorem, and bounds its error in Sobolev norms. It gives Lindley information gain identities, a Kullback Leibler form of the Bernstein von Mises theorem and an entropic van Trees bound, identifies the adjoint statistic with partial least squares (PLS) in the linear Gaussian model, and shows that the posterior mean summary is asymptotically sufficient under a uniform Bernstein von Mises hypothesis, which the book leaves open. Rao Blackwell and transport entropy bounds bracket the sufficiency gap of a linear summary in the linear Gaussian model, dissipation lowers the effective dimension of the heat and Stokes posteriors, and a generator trained on the raw data, accurate uniformly over a Hölder class, needs a number of simulations growing faster than any exponential in $N$.

#### From the literature

Bernstein von Mises theorems for time evolution equations (Nickl 2024) and for the two dimensional Navier Stokes equations (Konen and Nickl 2026); the expected information gain (Lindley 1956) and information as expected utility for diffusions (Polson and Roberts 1993); the posterior mean as a summary (Fearnhead and Prangle 2012; Jiang, Wu, Zheng and Wong 2017); agreement of ABC selection criteria (Hoffmann and Onnela 2026); the single index theorem (Brillinger 1983; Li and Duan 1989); deep partial least squares (Polson, Sokolov and Xu 2021); the transport entropy inequality (Talagrand 1996); likelihood informed subspaces (Cui et al. 2014) and optimal low rank posterior approximations (Spantini et al. 2015); the 4DVar adjoint (Le Dimet and Talagrand 1986); cross fitting (Chernozhukov et al. 2018).

#### New results

The catalogued results are the authors' own; some first appeared in their unpublished working paper on the solution manifold.

- [Adjoint representation of the sufficient statistic](#adjoint_representation_of_the_sufficient_statistic) (Lemma 15.1, page 206; proved): For a linear evolution equation that is diagonal in a fixed basis, the data statistic that is sufficient for the initial state is the coefficient vector of the time zero value of the solution of the backward adjoint equation driven by the data as point sources. New in this book.
- [Exact sufficiency, linear case](#exact_sufficiency_linear_case) (Proposition 15.2, page 207; proved): In the linear model with a Gaussian prior the adjoint statistic is sufficient, the posterior given it is the full data posterior, and the conditional quantile map is exactly affine with slope equal to the posterior covariance. New in this book.
- [Equivalence of the one step efficient score summary with the efficient centering](#equivalence_with_the_efficient_centering) (Proposition 15.5, page 210; proved): Under explicit regularity, rate and Lipschitz conditions, the cross fitted one step efficient score summary agrees with the efficient centering of Nickl's Bernstein von Mises theorem to order smaller than the root N scale in a negative Sobolev norm, so it is a computable center of the Gaussian limit of the posterior. New in this book.
- [The one step summary in Sobolev norms](#the_summary_in_sobolev_norms) (Proposition 15.6, page 213; proved): Under bounds on the linearizations and a rate for the preliminary estimates in a negative Sobolev norm, the error of the one step summary is bounded at an explicit polynomial rate in every Sobolev norm from index minus one to gamma, a rate that tends to zero for indices below gamma minus one, which gives the L2 and high Sobolev bounds that the generator theorem assumes of the summary. New in this book.
- [Preliminary estimates with the rate in $H^{-1}$](#preliminary_estimates_rate_in_h_minus_one) (Lemma 15.7, page 215; proved): A preliminary estimate bounded in a high Sobolev norm whose forward image converges at the rate delta N in L2 also converges at that rate in H minus one, interpolation then gives the whole family of Sobolev rates the summary needs, and the posterior mean computed on half the sample satisfies them. New in this book.
- [Sobolev rates of the one step summary under the efficient centering hypotheses](#summary_sobolev_rate_under_centering_hypotheses) (Corollary 15.9, page 217; proved): Under the hypotheses of the equivalence of the one step summary with the efficient centering, the summary has the same Sobolev rates as the earlier proposition, plus a term of smaller order than the root N scale multiplied by a power of N that grows with s and k, so that this term need not be small relative to the root N scale. New in this book.
- [The information operator of the reaction diffusion class](#the_information_operator_of_the_reaction_diffusion_class) (Lemma 15.11, page 219; proved): For the reaction diffusion class, the information operator differs from the heat equation one by a correction that gains regularity, the linearization has a quadratic remainder, and the summary weights depend on the linearization point in a Lipschitz way, all uniformly on Sobolev balls. New in this book.
- [The one step summary in Sobolev norms: reaction diffusion](#the_summary_in_sobolev_norms_reaction_diffusion) (Proposition 15.12, page 219; proved): For the reaction diffusion class the one step summary has the L2 and high Sobolev norm bounds that the generator theorem assumes, for every admissible choice of the preliminary estimates. New in this book.
- [The regularized summary on $J_N$ modes: heat and Stokes](#the_regularized_summary_on_modes_heat_and_stokes) (Proposition 15.13, page 220; proved): For the heat and Stokes equations the regularized summary on J N modes, which is the truncated posterior mean, is root N equivalent to Nickl's efficient centering in a negative Sobolev norm whatever the pilot estimate, and its posterior has the Gaussian Bernstein von Mises limit. New in this book.
- [The regularized summary under a fixed prior, and the untruncated posteriors](#regularized_summary_fixed_prior_untruncated_posteriors) (Proposition 15.14, page 225; proved): For the heat and Stokes equations the root N equivalence of the regularized summary with the efficient centering also holds under a fixed Gaussian prior and, under the rescaled prior, for the untruncated posterior, and under the fixed prior for its untruncated posterior when the prior exponent exceeds the dimension; when the true initial condition meets the hypotheses for both priors, the regularized summaries under the two priors are root N equivalent, and so are the untruncated posterior means when that exponent exceeds the dimension. New in this book.
- [The regularized summary on $J_N$ modes: reaction diffusion](#the_regularized_summary_on_modes_reaction_diffusion) (Proposition 15.16, page 228; proved): For the reaction diffusion class the cross fitted regularized summary on J N modes is root N equivalent in a negative Sobolev norm to the efficient centering, to the posterior mean and, under the hypotheses of the equivalence result, to the one step summary. New in this book.
- [Expected utility form of the Bernstein von Mises limit](#expected_utility_form_of_the_bernstein_von_mises_limit) (Proposition 15.18, page 231; proved): For the heat and Stokes equations the information gain from the data about the first J modes is given exactly by explicit formulas in the per mode ratios of data information to prior precision, its prior predictive expectation is Lindley's expected information gain, and under the rescaled prior only a vanishing fraction of the retained modes is strongly informative. New in this book.
- [Exact identities for the information gain under any forward map](#exact_identities_for_any_forward_map) (Lemma 15.21, page 233; proved): For any measurable forward map and a Gaussian product prior, the realized information gain is the Kullback Leibler divergence of the Gaussian approximation of the posterior from the prior plus a nonnegative non Gaussianity term, and, when the forward map has a finite prior second moment in supremum norm, the expected gain is the mutual information, which equals half the expected log determinant of the prior covariance times the posterior precision plus the expected non Gaussianity term. New in this book.
- [Kullback Leibler form of the Bernstein von Mises theorem](#kullback_leibler_form_of_the_bernstein_von_mises_theorem) (Theorem 15.22, page 234; proved): Under the conditions of Nickl's Bernstein von Mises theorem, the posterior is close in Kullback Leibler divergence, in probability, to the Gaussian posterior of the model linearized at the truth. New in this book.
- [Realized information gain of the posterior with the efficient information at the truth](#realized_information_gain_with_efficient_information) (Corollary 15.23, page 236; proved): Under the hypotheses of the Kullback Leibler form of the Bernstein von Mises theorem, the non Gaussianity term of the information gain tends to zero uniformly in the number of modes, and for a fixed number of modes the realized gain is given up to o(1) in probability by the Gaussian formula with the efficient information at the truth. New in this book.
- [Kullback Leibler form of the Bernstein von Mises theorem for the Navier Stokes equations](#kullback_leibler_bernstein_von_mises_navier_stokes) (Proposition 15.24, page 236; proved): The Kullback Leibler form of the Bernstein von Mises theorem and its corollary on the realized information gain also hold for the two dimensional Navier Stokes equations with the prior of Konen and Nickl and smoothness exponent above twelve. New in this book.
- [Entropic van Trees bound](#entropic_van_trees_bound) (Proposition 15.25, page 238; proved): For a forward map that is continuously differentiable in a fixed number of modes, the expected information gain is bounded above by a log determinant of the prior averaged Fisher information, and, under the rescaled prior with exponent above the dimension and continuity, polynomial growth and invertibility conditions on the Fisher information at the center, by the same expression with the Fisher information at the center of the prior, up to o(1). New in this book.
- [Reaction diffusion: the expected gain is set at the center of the prior](#reaction_diffusion_expected_gain_at_prior_center) (Proposition 15.26, page 239; proved): For reaction diffusion equations with a fixed number of modes the expected information gain is bounded, up to o(1), by the gain computed with the information at the center of the prior, with equality when the reaction term vanishes near zero, and not by the information at the true initial condition, and for some such equations the information at the truth overstates the gain by an amount that does not vanish. New in this book.
- [Quadratic variation and the sufficient statistic](#quadratic_variation_and_the_sufficient_statistic) (Proposition 15.28, page 243; proved): With unknown noise variance the adjoint statistic together with the squared norm of the data is sufficient, and for an observed diffusion path the diffusion coefficient is identified by quadratic variation while the adjoint evolution driven by the data remains the sufficient statistic for the initial state. New in this book.
- [The one step summary under four ABC criteria: Bayes risk optimal up to o(1), all four attained in the J mode Gaussian projection](#one_step_summary_under_four_abc_criteria) (Proposition 15.29, page 244; conditional on The uniform Bernstein von Mises statement (Assumption U of the chapter), applied both to the one step summary and to the posterior mean: sets of parameters of prior probability tending to one on which the Wasserstein distance between the posterior of the rescaled, recentered parameter and the Gaussian limit tends to zero uniformly in the truth, with uniform integrability of these discrepancies, Lipschitz dependence of the limit on the truth, first moment bounds on the limits, concentration of the posterior given the summary around the summary, and smallness of the discrepancy conditional on the summary at the true parameter; the book does not prove it (Open Question Uniformity). Also the uniform moment bound (MB) of order two plus a positive power on the rescaled posterior radius under the prior predictive law, which the book proves only for the linear Gaussian model and assumes for nonlinear forward maps.): Under the uniform Bernstein von Mises assumption and a moment bound, the full data bound four approximate Bayesian computation criteria (expected posterior entropy, Fisher information determinant, Bayes risk, information gain) over J dimensional statistics, the one step summary attains the Bayes risk optimum up to o(1), and it attains all four exactly in the J mode Gaussian projection. The agreement of these criteria in the large sample limit, for independent identically distributed data and a finite dimensional parameter, is due to Hoffmann and Onnela (2026). New in this book.
- [The adjoint statistic is the PLS projection](#the_adjoint_statistic_is_the_pls_projection) (Proposition 15.32, page 252; proved): In the linear model with a Gaussian prior the partial least squares scores computed from the raw data are exactly the coordinates of the sufficient adjoint statistic, so one PLS component per parameter coordinate suffices. New in this book.
- [Deep PLS structure of the GBC summary](#deep_pls_structure_of_the_gbc_summary) (Proposition 15.34, page 253; conditional on Part (ii) for the posterior given the scores alone assumes the uniform Bernstein von Mises statement (Assumption U), which the book does not prove (Open Question Uniformity), in addition to the hypotheses of the equivalence of the one step summary with the efficient centering.): For a nonlinear forward map the first stage of the one step summary is a PLS step with directions given by the linearized forward map, and under the stated hypotheses, including the open uniform Bernstein von Mises assumption for the posterior given the scores, the map from the scores to the posterior is asymptotically the identity plus a scale. New in this book.
- [Jiang Wong under a uniform Bernstein von Mises assumption: the posterior mean summary is asymptotically sufficient](#jiang_wong_under_bernstein_von_mises) (Theorem 15.38, page 256; conditional on The uniform Bernstein von Mises assumption (Assumption U, clauses (U1) to (U4)) for the posterior mean, and for the one step statistic the same assumption for that statistic; the book does not prove it (Open Question 17.18, Uniformity).): If a Bernstein von Mises theorem holds uniformly over prior typical truths, then conditioning on the posterior mean alone, or on any summary root N equivalent to it, loses nothing at the root N scale: the recentered posterior given the summary and the recentered posterior given all of the data have the same Gaussian limit in Wasserstein distance. New in this book.
- [GBC with the posterior mean summary](#gbc_with_the_posterior_mean_summary) (Corollary 15.40, page 258; conditional on The convergence at the root N scale assumes the uniform Bernstein von Mises assumption (Assumption U, clauses (U1) to (U4), stated clause by clause in the entry jiang_wong_under_bernstein_von_mises) for the posterior mean, which the book does not prove (Open Question 17.18, Uniformity); the two identities at finite N are unconditional.): The target of generative Bayesian computation that conditions only on the posterior mean has, at every sample size, the exact posterior mean and the averaged posterior covariance, and under a uniform Bernstein von Mises theorem it is within $o(N^{-1/2})$ of the posterior in Wasserstein distance. New in this book.
- [Sufficiency gap in the linear Gaussian model: Rao Blackwell lower bound and transport entropy upper bound](#sufficiency_gap) (Theorem 15.41, page 258; proved): For any linear summary in the linear Gaussian model, the Wasserstein distance between the posterior given the summary and the posterior given all of the data is bracketed, on average over the data, by two quantities computable before any simulation, one from the difference of the posterior covariances and one from the mutual information deficit, and both vanish exactly when the summary is Bayes sufficient, as the adjoint statistic is. New in this book.
- [Sufficiency gap beyond the linear model](#sufficiency_gap_beyond_the_linear_model) (Proposition 15.42, page 260; proved): If the posteriors given all of the data and given a summary are each within $o(N^{-1/2})$, in Wasserstein distance and on average under a coupling, of the corresponding posteriors of one linear Gaussian model, then the root N sufficiency gap of the summary is bracketed by the Rao Blackwell and transport entropy bounds of that Gaussian model; for the heat and Stokes equations and a truncated adjoint statistic the bounds are explicit. New in this book.
- [The Gaussian comparison models admitted by the first hypothesis of the nonlinear sufficiency gap bounds](#sufficiency_gap_admissible_gaussian_models) (Proposition 15.43, page 261; conditional on Clauses (U1) and (U2) of the uniform Bernstein von Mises assumption (Assumption U, stated clause by clause in the entry jiang_wong_under_bernstein_von_mises) for some summary, and for part (ii) clause (U3) as well; the book does not prove them (Open Question 17.18, Uniformity).): Under a uniform Bernstein von Mises theorem, a linear Gaussian model can match the full data posterior at the root N scale only if its posterior covariance matches the Bernstein von Mises covariance on average over the prior; for a nonlinear forward map this forces a constant limit covariance under a fixed prior, and the inverse information at the prior mean rather than at the truth under the rescaled prior. New in this book.
- [A sufficient condition for the nonlinear sufficiency gap hypotheses in terms of the centering](#sufficiency_gap_hypotheses_from_centering_clt) (Lemma 15.44, page 263; conditional on Clauses (U1) to (U3) of the uniform Bernstein von Mises assumption (Assumption U, stated clause by clause in the entry jiang_wong_under_bernstein_von_mises) for the centering $S_N$, with the prior mean 0 in every localization set; the book does not prove them (Open Question 17.18, Uniformity).): Under a uniform Bernstein von Mises theorem and a prior that contracts to zero, both hypotheses of the nonlinear sufficiency gap bounds follow, for a Gaussian model whose posterior covariance matches the limit at the prior mean, from a central limit statement for the conditional law of the centering given the summary. New in this book.
- [A two coordinate model in which the sufficiency gap hypotheses depend on the summary](#two_coordinate_model_sufficiency_gap_depends_on_summary) (Proposition 15.45, page 264; counterexample, proved): In a model with two parameters, a quadratic forward map and a prior contracting to zero, the Gaussian model at the prior mean matches the full data posterior at the root N scale while the Gaussian model at the truth need not, when the prior scale $s_N$ satisfies $\sqrt Ns_N^2\to\infty$, the posterior given the first coordinate of the adjoint statistic at the prior mean stays at a root N distance tending to infinity from every Gaussian posterior given a linear statistic, and the first coordinate of the maximum likelihood estimator satisfies both hypotheses of the nonlinear sufficiency gap bounds. New in this book.
- [Effective dimension under dissipation](#effective_dimension_under_dissipation) (Theorem 15.46, page 267; conditional on Part (ii) for a nonlinear forward map assumes the hypotheses of the book's Theorem 16.10 (Bernstein von Mises for the identity skip quantile generator), among them the uniform Bernstein von Mises assumption (Assumption U, open: Open Question 17.18), the whitened training residual assumption (U2') (the whitened training residuals $\mathcal{D}^{-1/2}\sqrt N(\theta^{(m)}-\hat S^{(m)}_N)$, $\mathcal{D}=\operatorname{diag}(1/\iota_j)$, split, conditionally i.i.d. given the data, into a part whose projections on unit vectors have sub Gaussian norms given the data bounded in probability uniformly over the unit vectors and whose conditional second moment matrix tends in operator norm to the whitened limit covariance $\mathrm{Id}+\Xi$, and a remainder whose conditional mean square norm tends to zero, all in $P^N_{\theta_0}$ probability; the book proves it for training parameters drawn from a proposal localized at the preliminary estimate, under the other hypotheses, and it fails in general for a nonlinear forward map when they are drawn from the prior) and the error bounds $\|\hat S_N-\theta_0\|_{L^2}=o_P(\tilde\delta_N(0))$, with $\tilde\delta_N(0)$ the posterior contraction rate in $L^2$, and $\|\hat S_N-\theta_0\|_{H^{\bar\gamma}}=o_P(1)$, $\bar\gamma\ge2$, on the summary, which the book leaves open for a nonlinear forward map other than reaction diffusion when the preliminary estimates have only the rates of the summary's definition; parts (i) and (iii) and the linear case of part (ii) assume nothing unproved.): For the heat and Stokes equations on the torus with a power law prior, the number of modes in which the data at least halve the prior variance grows like a power of the sample size divided by viscosity times observation time, so dissipation lowers the effective dimension; for a nonlinear forward map, under a uniform Bernstein von Mises hypothesis and assumptions on the training residuals and the summary, a generator need only learn the posterior scale on those modes (in the linear model it needs no training), and the cost of using the prior spread beyond them is bounded explicitly. New in this book.
- [Sufficiency versus the raw data: simulation cost of a generator trained without a summary](#sufficiency_versus_the_raw_data) (Theorem 15.47, page 269; conditional on The second claim (the hybrid generator trained on the sufficient statistic) assumes the hypotheses of part (ii) of the effective dimension theorem, which include those of the book's Theorem 16.10: the uniform Bernstein von Mises assumption (Assumption U, open: Open Question 17.18), the whitened training residual assumption (U2') (the whitened training residuals $\mathcal{D}^{-1/2}\sqrt N(\theta^{(m)}-\hat S^{(m)}_N)$, $\mathcal{D}=\operatorname{diag}(1/\iota_j)$, split, conditionally i.i.d. given the data, into a part whose projections on unit vectors have sub Gaussian norms given the data bounded in probability uniformly over the unit vectors and whose conditional second moment matrix tends in operator norm to the whitened limit covariance $\mathrm{Id}+\Xi$, and a remainder whose conditional mean square norm tends to zero, all in $P^N_{\theta_0}$ probability; the book proves it for training parameters drawn from a proposal localized at the preliminary estimate, under the other hypotheses, and it fails in general for a nonlinear forward map when they are drawn from the prior) and the error bounds $\|\hat S_N-\theta_0\|_{L^2}=o_P(\tilde\delta_N(0))$, with $\tilde\delta_N(0)$ the posterior contraction rate in $L^2$, and $\|\hat S_N-\theta_0\|_{H^{\bar\gamma}}=o_P(1)$, $\bar\gamma\ge2$, on the summary, which the book leaves open for a nonlinear forward map other than reaction diffusion when the preliminary estimates have only the rates of the summary's definition. The first claim, the lower bound on the number of simulations, is unconditional.): A generator trained on the raw observations and required to be accurate uniformly over a Hölder class of conditional quantile maps needs a number of simulations that grows faster than any exponential in the sample size, while the hybrid generator trained on the sufficient adjoint statistic needs only a number of simulations that grows faster than the effective dimension, conditionally on a uniform Bernstein von Mises hypothesis and assumptions on the training residuals and the summary. New in this book.

#### Key terms

adjoint sufficient statistic, 4DVar, Bayes sufficiency, one step estimator, cross fitting, Bernstein von Mises theorem, BvM, generative Bayesian computation, GBC, approximate Bayesian computation, ABC summary statistics, partial least squares, PLS, deep PLS, expected information gain, van Trees inequality, sufficiency gap, effective dimension, likelihood informed subspace, heat equation, Stokes equation, Navier Stokes, reaction diffusion, PDE inverse problem

<a id="ch-16"></a>

### Chapter 16. Transfer, Generators and Localized Training

Pages 273 to 330.

How accurate must a generative Bayesian computation (GBC) generator be for its output to inherit the Bernstein von Mises (BvM) theorem of the exact posterior in a nonlinear PDE inverse problem, and how should its training pairs be drawn? In Nickl's framework for reaction diffusion equations and the Konen Nickl theory for two dimensional Navier Stokes, the transfer theorem shows that Wasserstein accuracy $o(N^{-1/2})$ and concentration on the localization set pass the Gaussian limit, exact credible band coverage and, for Navier Stokes, local asymptotic minimax efficiency for bounded losses to the GBC posterior. An identity skip quantile generator with a closed form Gaussian head is that accurate once $J/M\to0$ (summary dimension $J$, simulations $M$), conditionally on a uniform BvM assumption, a whitened residual assumption and a summary error bound. A minimax lower bound over monotone Hölder classes of conditional quantile maps shows that uniform accuracy needs at least of order $N^{1+J/(2\beta)}$ simulations, and local quantile estimators attain the exponent $\beta/(2\beta+J)$ (for $\beta>2$ with bounded densities). Under Nickl's conditions on $L^\infty$ balls, unverified for any forward map, a sparse deep ReLU network prior gives contraction in $H^{-1}$. For localized training it derives the exact residual law in the linear Gaussian model, a center and rescale rule, and proves the whitened residual assumption under a localized proposal.

#### From the literature

- BvM theorems for time evolution equations (Nickl 2024) and for two dimensional Navier Stokes, with coverage and a local asymptotic minimax bound (Konen and Nickl 2026; Konen 2026); contraction for nonlinear inverse problems (Nickl 2023).
- Convolution and minimax theorems (van der Vaart and Wellner 2023), Le Cam's lemmas (van der Vaart 1998), Gaussian coverage (Giné and Nickl 2016).
- Covariance estimation (Vershynin 2018), empirical Wasserstein bounds (Bobkov and Ledoux 2019), Assouad's lemma (Tsybakov 2009), VC major empirical processes (Baraud 2016), Glaeser's inequality (Glaeser 1963), ReLU quantile regression rates (Padilla, Tansey and Chen 2022).
- Sparse deep ReLU network posteriors (Polson and Ročková 2018; Wang and Ročková 2020), misspecification (Kleijn and van der Vaart 2006), deep Gaussian process priors (Finocchio and Schmidt Hieber 2023; Abraham and Deo 2023), Langevin algorithms (Nickl and Wang 2024).

#### New results

- [Transfer of Bernstein von Mises guarantees to the GBC posterior (BvM for GBC)](#bvm_for_gbc) (Theorem 16.2, page 275; proved): If the posterior produced by a generative Bayesian computation (GBC) generator is closer to the exact posterior than the root N scale in Wasserstein distance and concentrates on the localization set with bounded moments, then it inherits the Bernstein von Mises limit of the exact posterior for the initial condition and, for the reaction diffusion and two dimensional Navier Stokes equations, for the trajectory, with exact asymptotic coverage of its credible bands and, for Navier Stokes, attainment of the local asymptotic minimax bound for bounded losses; nothing is assumed about how the generator was trained. New in this book.
- [Solve then simulate equals simulate the limit: tangent linear forward simulation of GBC draws](#solve_then_simulate_equals_simulate_the_limit) (Corollary 16.4, page 280; conditional on Only the plug in bound of the second part is conditional: its proof uses the set $\Theta_N$ and the Lipschitz clause (U3) of the uniform Bernstein von Mises assumption (Assumption U, stated clause by clause in the entry jiang_wong_under_bernstein_von_mises), which the book does not prove; the first part, and the rate for the GBC mean in the Sobolev norm of Condition 2D, whose proof uses only the transfer theorem and the moment clause of (G2), need only the hypotheses of the transfer theorem.): Pushing GBC draws through the nonlinear solver and pushing the Bernstein von Mises limit through the tangent linear equation give asymptotically the same law of the scaled trajectory error, and, under a uniform Bernstein von Mises assumption and a Lipschitz linearization, the forward simulations may be replaced by tangent linear solves at the GBC mean at a cost bounded by a term tending to zero plus a constant times the distance of that mean to the truth in a Sobolev norm, which tends to zero at an explicit rate. New in this book.
- [Bernstein von Mises for the identity skip Gaussian head quantile generator, conditional on the uniform hypothesis](#bernstein_von_mises_for_the_identity_skip_quantile_generator) (Theorem 16.10, page 285; conditional on Assumption U (uniform Bernstein von Mises) for the one step summary, clause (U4) included, which the book states as open (Open Question Uniformity); Assumption (U2') on the whitened training residuals, which the book proves for localized training proposals (catalog entry whitened_residual_assumption_under_a_localized_proposal) and which fails in general for training parameters drawn from the prior when the forward map is nonlinear; and the bounds on the error of the summary (smaller order than the localization rate in L2 and tending to zero in the Sobolev norm of the localization ball), which the same open question asks for.): A generator that adds to the one step summary a Gaussian whose covariance is the whitened sample second moment of the simulated residuals, computed in closed form, satisfies the accuracy conditions of the transfer theorem, and so inherits its Bernstein von Mises conclusions, as soon as the number of simulations grows faster than the summary dimension, conditionally on a uniform Bernstein von Mises assumption, an assumption on the whitened training residuals and a bound on the error of the summary. New in this book.
- [No uniform guarantee: minimax lower bound for conditional quantile generators over monotone Hölder classes](#no_uniform_guarantee_for_quantile_generators) (Theorem 16.15, page 290; proved): Any generator, trained on M simulated pairs, that must be accurate at a fixed interior summary value for every conditional law in a monotone Hölder class of conditional quantile maps of smoothness beta on a J dimensional summary has, for some map in the class, Wasserstein error at least a constant free of J times (C M) to the power minus beta over (2 beta plus J) with probability at least 1/8, where C bounds the design density, so root N accuracy uniformly over the class requires at least N to the power 1 plus J over (2 beta) simulations divided by C, more than any polynomial once J grows; reading this as the accuracy condition of the transfer theorem uses the uniform Bernstein von Mises assumption. New in this book.
- [The minimax exponent for conditional quantile generators is attained for Hölder smoothness at most one (histogram generator)](#quantile_generator_exponent_attained_for_beta_at_most_one) (Proposition 16.16, page 293; proved): For Hölder smoothness at most one, the generator that reports the empirical law of the simulated parameters whose summaries fall in the same cube of a grid of side M to the power minus 1 over (2 beta plus J) has Wasserstein risk at most a constant times J to the power beta over 2 times M to the power minus beta over (2 beta plus J), uniformly over the class and the summary value, so the summary dimension J, and not J plus one, governs the rate. New in this book.
- [The minimax exponent for conditional quantile generators is attained for smoothness between one and two by jittered local linear quantile regression](#quantile_generator_exponent_attained_for_beta_between_one_and_two) (Proposition 16.19, page 295; proved): For Hölder smoothness between one and two, local linear quantile regression on a Euclidean window around an interior summary value, applied level by level to responses with a small uniform jitter and clipped to [minus 1, 1], has Wasserstein risk at most a constant times M to the power minus beta over (2 beta plus J) uniformly over the monotone Hölder class, matching the lower bound exponent even though the conditional laws may have atoms. New in this book.
- [A local linear quantile fit is nearly monotone in its error (deterministic lemma for monotone Hölder quantile maps)](#a_quantile_fit_is_nearly_monotone_in_its_error) (Lemma 16.21, page 296; proved): For a monotone Hölder conditional quantile map of smoothness between one and two, the excess level of an affine fit at a rescaled design point near an interior summary value has the sign of the fit's error, is ordered like that error, and is bounded below by two thirds of it, all up to a term of order h to the power beta. New in this book.
- [Moment conditions force a small local linear quantile fit](#moment_conditions_force_a_small_fit) (Lemma 16.22, page 298; proved): If the excess level of an affine quantile fit has small mean and small first moments under a bounded design density on the unit ball, as the first order conditions of local linear quantile regression give, then, at every level whose distance to 0 and to 1 exceeds a multiple of the moment bound, the fit is uniformly close to the first order Taylor polynomial of the true conditional quantile, with explicit constants. New in this book.
- [The minimax exponent for conditional quantile generators is attained for smoothness above two when the conditional densities are bounded](#quantile_generator_exponent_attained_for_beta_above_two_with_bounded_densities) (Proposition 16.25, page 302; proved): For Hölder smoothness above two and conditional quantile maps whose slope in the level is bounded below, so that the conditional laws have bounded densities and no atoms, local polynomial quantile regression on a window around an interior summary value has Wasserstein risk at most a constant times M to the power minus beta over (2 beta plus J), which makes beta over (2 beta plus J) the minimax exponent at an interior point for every beta above one when the lower bound on the slope is at most 1/8. New in this book.
- [A local polynomial quantile fit is uniformly small when the conditional densities are bounded](#a_polynomial_quantile_fit_when_the_densities_are_bounded) (Lemma 16.26, page 303; proved): When the conditional quantile maps have slope in the level bounded below, a polynomial fit whose excess level has small moments up to its degree under a design density bounded below on the unit ball is, at every level whose distance to 0 and to 1 exceeds a multiple of the moment bound, uniformly close to the Taylor polynomial of the true conditional quantile, with explicit constants depending on the degree and the dimension. New in this book.
- [No two point lower bound gives a smaller exponent for conditional quantile generators](#no_two_point_bound_gives_a_smaller_exponent) (Proposition 16.27, page 304; proved): For any two conditional quantile maps in the monotone Hölder class, the squared Hellinger distance between the laws of one training pair is at least a constant times the Wasserstein separation of their conditional laws at the summary value raised to the power 2 plus J over beta, so no two point lower bound can give an exponent smaller than beta over (2 beta plus J). New in this book.
- [Posterior contraction for the initial condition of a PDE under a sparse deep ReLU network (Polson Ročková) prior](#contraction_under_a_network_prior) (Theorem 16.28, page 306; proved): If the forward map satisfies Conditions 2A, 2B and 2E of Nickl on sup norm balls, a strengthening that the book says has not been checked for any forward map, then under the Polson Ročková spike and slab prior on sparse deep ReLU networks for the initial condition of a time evolution equation the posterior contracts around a truth of Hölder smoothness alpha, between d/2 plus 1 and the input dimension p of the networks, at the rate N to the power minus alpha over (2 alpha plus p), up to a logarithmic factor, for the forward map in L2 and for the initial condition in the negative Sobolev norm of order one, adaptively in the smoothness; an L2 rate follows only when the sieve's sup norm plus Lipschitz bound is small enough, and the book's proof is a sketch. New in this book.
- [Exactness of the one step summary in the linear Gaussian model](#exactness_of_the_one_step_summary) (Lemma 16.32, page 310; proved): In the linear Gaussian model the regularized one step summary, evaluated at any linearization point, equals the posterior mean exactly, so it does not depend on the point at which it is computed and training under a proposal other than the prior does not change its target. New in this book.
- [Residual law under a localized training proposal: prior fraction mean and variance inflation](#residual_law_under_a_localized_proposal) (Theorem 16.33, page 310; proved): In the linear Gaussian model, when training parameters are drawn from a Gaussian proposal centered at a preliminary estimate with covariance c squared times the posterior covariance, the residual of the exact summary has mean equal to the prior shrinkage of the proposal center, independent of c, and, when the prior covariance commutes with the information, per eigendirection of the prior fraction operator, variance equal to the posterior variance times s plus c squared p squared, which gives the exact bias of uncentered heads and the standard deviation error of unrescaled heads. New in this book.
- [The localized GBC design (center and rescale) meets the accuracy conditions (G1) and (G2) in the linear Gaussian model](#localized_design_meets_gbc_accuracy_conditions) (Corollary 16.37, page 315; proved): In the linear Gaussian model with a prior that commutes with the information, the localized GBC algorithm, which draws training parameters around a preliminary estimate, centers the residuals and rescales them by the exact factor of the prior fraction, reproduces the exact posterior in population at every radius and center, and, when the posterior variance of each mode is at most of the order of its Laplace eigenvalue over N, as for the heat and Stokes equations, with M simulations on J modes is within order N to the power minus one half times the square root of J over M (plus J over M) of it in Wasserstein distance, so the transfer theorem applies when J over M tends to zero. New in this book.
- [Gram matrix of the whitened weights of the one step training summary](#the_gram_matrix_of_the_whitened_weights) (Lemma 16.41, page 319; proved): The Gram matrix of the whitened weights of the one step training summary equals the compression of the inverse whitened information plus an explicit positive Schur complement term, so it dominates that compression, which is bounded below by the inverse norm of the information, and differs from it by at most the squared norm of the tail of the compact correction divided by the cube of the lower bound. New in this book.
- [No sub Gaussian envelope uniform in the dimension for the whole whitened training residual with fresh designs](#no_sub_gaussian_envelope_for_the_whole_residual) (Proposition 16.42, page 319; proved): When each simulated data set has its own random design, no law of the training parameters gives the whole whitened residual of the one step training summary a sub Gaussian norm bounded uniformly in the summary dimension: the squared sub Gaussian norm is at least twice the envelope of the whitened weights, which grows at least linearly in the dimension when the whitened information operator is bounded, and for the heat and Stokes equations grows like the J th Laplace eigenvalue in the last coordinate. New in this book.
- [The whitened training residual assumption (U2') holds under a localized training proposal](#whitened_residual_assumption_under_a_localized_proposal) (Theorem 16.43, page 320; proved): For training parameters drawn from a Gaussian proposal localized at a preliminary estimate with covariance of the posterior scale, and the one step training summary linearized there once, the whitened training residuals split into a part with sub Gaussian norm bounded uniformly in the dimension and second moment converging to the whitened inverse information, plus a remainder whose second moment tends to zero, for the heat and Stokes equations and, under three conditions on the linearization, for a nonlinear forward map. New in this book.
- [Linearization conditions (I1) to (I4) for the reaction diffusion class](#the_linearization_of_the_reaction_diffusion_class) (Lemma 16.44, page 324; proved): For Nickl's reaction diffusion class with a smooth truth, the linearized solution map satisfies the four conditions on the linearization used to prove the whitened residual assumption under localized training (coercive whitened information with compact correction, Lipschitz dependence on the linearization point, sup norm bounds and a quadratic remainder), with an information bound depending only on the sup norm of the derivative of the reaction term and the time horizon. New in this book.
- [Linearization conditions (I1) to (I4) for the two dimensional Navier Stokes equations](#the_linearization_of_the_navier_stokes_equations) (Lemma 16.45, page 325; proved): For the two dimensional periodic Navier Stokes equations with forcing in the first divergence free Sobolev space and initial condition in the second, the linearized solution map satisfies the Lipschitz, sup norm and quadratic remainder conditions on the linearization with Sobolev index two, and for smooth forcing and truth every hypothesis on the forward map of the theorem on whitened residuals under localized training holds, with the conditions of Konen and Nickl in place of Nickl's Condition 2. New in this book.
- [Centered and rescaled training residuals for a nonlinear forward map with a reused design](#centered_and_rescaled_residuals_for_a_nonlinear_forward_map) (Proposition 16.47, page 327; proved): For a nonlinear forward map, when the simulated data sets reuse the observed design and the regularized one step summary is formed at a preliminary estimate, the centered and rescaled whitened residuals of the localized GBC algorithm satisfy the analogue of the whitened residual assumption with the identity as limit covariance, and with J over M tending to zero the algorithm's head, centered at the observed summary, is within smaller order than the root N scale of the Gaussian with that center and the regularized posterior covariance. New in this book.

#### Key terms

generative Bayesian computation, GBC, Bernstein von Mises theorem, BvM, transfer theorem, Wasserstein distance, simulation based inference, quantile generator, identity skip connection, minimax lower bound, Hölder class, local polynomial quantile regression, spike and slab prior, posterior contraction, localized training, whitened residuals, credible bands, local asymptotic minimax, Navier Stokes, reaction diffusion, nonlinear inverse problem, data assimilation

<a id="ch-17"></a>

### Chapter 17. Heat, Navier Stokes and Schrödinger: Examples and Experiments

Pages 331 to 384.

This chapter tests the book's generative Bayesian computation (GBC) for the initial condition of an evolution equation (data assimilation) on three examples: the heat equation, two dimensional Navier Stokes about the Taylor Green vortex, and the Schrödinger equation (linear, and cubic nonlinear, NLS). For the heat equation it computes the information per Fourier mode (the dissipation barrier, or viscous curse) and proves a matrix Bernstein concentration bound for the Gram matrix of a uniform random design with the finite sample Bernstein von Mises error. Experiments compare GBC with exact posteriors, the Laplace approximation, pCN and Metropolis references. Without dissipation it computes the Bogoliubov information blocks of cubic NLS about a plane wave (modulational instability), proves linearized stability (defocusing) and stability of the NLS solution map (for bounded solutions), and proves a Bernstein von Mises transfer theorem for the linear Schrödinger equation; no Bernstein von Mises theorem is proved for cubic NLS. It links GBC to Longstaff Schwartz least squares Monte Carlo and to Storvik sufficient statistic filtering, and lists open problems.

#### From the literature

Used as black boxes: the Bernstein von Mises theorems for time evolution equations (Nickl 2024) and for two dimensional Navier Stokes data assimilation (Konen and Nickl 2026). Also used: the inverse logarithmic lower bound (Nickl and Titi 2024), the local curvature condition for Langevin sampling (Nickl and Wang 2024), the matrix Bernstein inequality (Tropp 2015), the Taylor Green vortex (Taylor and Green 1937), the functional Bernstein von Mises theorem in Gaussian white noise (Castillo and Nickl 2013), Sobolev norm growth for NLS on two dimensional manifolds (Planchon, Tzvetkov and Visciglia 2017), the pCN sampler (Cotter, Roberts, Stuart and White 2013), the wave kinetic equation from cubic NLS (Deng and Hani 2023), Navier Stokes Fourier from hard spheres (Deng, Hani and Ma 2025) and gradient stability for McKean Vlasov (Castre and Nickl 2026). Connections: least squares Monte Carlo (Longstaff and Schwartz 2001; Clément, Lamberton and Protter 2002), Storvik's filter (Storvik 2002), jump diffusion filtering (Johannes, Polson and Stroud 2009) and Bayesian calibration (Kennedy and O'Hagan 2001; Higdon and coauthors 2004, 2008).

#### New results

Origin is the book for all entries below; the Notes record which also appear in the authors' unpublished paper on Bayesian estimation on the solution manifold.

- [Gram matrix concentration and the finite N Bernstein von Mises error for the heat equation](#gram_concentration_and_the_finite_bernstein_von_mises_error) (Proposition 17.1, page 332; proved): For the heat equation observed at N uniform random points with D retained modes (eigenfunctions bounded by the square root of 2) and N at least D log D, the normalized Gram matrix of the design is within 12 times the square root of D log D over N of its limit with probability at least 1 minus 1/D, which bounds the finite N error of the Bernstein von Mises covariance. New in this book.
- [Information operator of the cubic nonlinear Schrödinger equation about a plane wave (Bogoliubov blocks)](#information_operator_of_nls_about_a_plane_wave) (Proposition 17.5, page 356; proved): Linearized about a constant background, the information operator of the cubic nonlinear Schrödinger equation is block diagonal over Fourier modes with explicit 2 by 2 blocks given by the Bogoliubov dispersion relation, equal in the defocusing case to T times the identity plus a compact perturbation that decays like one over the squared wave number and exponentially amplified along one direction in the focusing band. New in this book.
- [Determinant, trace and smallest eigenvalue of the Bogoliubov information block](#bogoliubov_block_determinant_trace_and_smallest_eigenvalue) (Lemma 17.6, page 359; proved): The determinant of each 2 by 2 Bogoliubov information block is at least T squared because the linearized flow preserves area, which gives explicit lower bounds on its smallest eigenvalue, uniform in the mode in the defocusing case, while in the focusing band the largest eigenvalue grows exponentially and the smallest tends to a finite limit. New in this book.
- [Linearized stability and the analogue of Condition 2F for the defocusing NLS plane wave](#linearized_stability_and_condition_2f_analogue_for_the_defocusing_plane_wave) (Corollary 17.7, page 362; proved): For the defocusing cubic nonlinear Schrödinger equation linearized at a constant background, the information operator is bounded above and below on L2 and on every Sobolev space with explicit constants uniform in the mode, which gives a linearized stability estimate and bounds, uniformly in the mode and in the time horizon, the covariance of the Gaussian measure that would be the Bernstein von Mises limit; no such theorem is proved for cubic NLS. New in this book.
- [Stability of the cubic NLS solution map](#stability_of_the_cubic_nls_solution_map) (Proposition 17.8, page 364; proved): For solutions of the cubic nonlinear Schrödinger equation that stay bounded in the supremum norm, the L2 distance of two solutions is bounded above and below by exponential factors times the distance of the initial data, which gives a stability estimate for the solution map on balls of H1 in one dimension and of H2 in two dimensions, with a smallness condition in the focusing two dimensional case. New in this book.
- [Linear Schrödinger transfer: exact posterior and Bernstein von Mises theorem](#linear_schrodinger_transfer) (Proposition 17.10, page 366; proved): For the linear Schrödinger equation with a truncated Gaussian prior, the posterior is exactly Gaussian with the adjoint summary sufficient, and when the number of modes grows suitably the posterior and the posterior mean (for a smooth enough truth) satisfy a Bernstein von Mises theorem in negative Sobolev spaces with complex white noise as the limit, for the initial condition and for the state at every time but not in the supremum norm. New in this book.
- [The transfer theorem for the linear Schrödinger equation](#the_transfer_theorem_for_the_linear_schrodinger_equation) (Corollary 17.11, page 370; proved): If a GBC posterior approximates the exact posterior in Wasserstein distance on a negative Sobolev space with an error of smaller order than one over the square root of N, then for the linear Schrödinger equation it has the Gaussian limits for the parameter and for the state at every time, for Hadamard differentiable functionals, for credible balls, and efficiency of linear functionals. New in this book.
- [Beyond the plane wave: information operator of cubic NLS about a multimode background](#beyond_the_plane_wave) (Open Question 17.12, page 371; open): Open question: extend the exact information operator of cubic NLS from a constant background to a multimode background by separating a part supported on the four wave resonant manifold, decide when it is uniformly invertible, and prove a Bernstein von Mises theorem for a fixed time horizon in the focusing case. New in this book.
- [LSM is GBC for optimal stopping; GBC is LSM for the inverse problem (Longstaff Schwartz dictionary)](#lsm_gbc_dictionary_for_optimal_stopping_and_the_inverse_problem) (Proposition 17.13, page 372; proved): Longstaff Schwartz least squares regression for American options and the regression step of GBC are the same construction under a dictionary between paths and prior draws, state and summary, payoff and parameter, and continuation value and posterior mean, so that a linear basis is exact for the linear Gaussian model. New in this book.
- [Two limit convergence of the regression summary (least squares Monte Carlo and GBC)](#two_limit_convergence_of_the_regression_summary) (Theorem 17.14, page 373; conditional on Only the identification of the limit in case (c), the one step summary, is conditional: it rests on the book's theorem on the Jiang Wong posterior mean summary under Bernstein von Mises, which assumes Assumption U (a Bernstein von Mises statement for the posterior, uniform over a set of parameters of prior probability tending to one and small also conditionally on the observed summary), which the book does not prove and lists as an open question, and on the hypotheses of the book's proposition equating the one step summary with Nickl's efficient centering. The limits in the number of simulations and of basis functions, and cases (a) and (b), are proved without it.): The least squares regression of the parameter on a basis of the summary converges to the posterior mean given the summary as the number of simulations and then the number of basis functions grow, and jointly for a bounded basis; that limit is the exact posterior mean for the posterior mean summary and for the linear adjoint statistic, but only up to an error of smaller order than one over the square root of N for the one step summary, where it also depends on an unproved uniformity assumption. New in this book.
- [The adjoint statistic is a Storvik statistic](#the_adjoint_statistic_is_a_storvik_statistic) (Proposition 17.15, page 376; proved): In the linear model the adjoint statistic and the Gram matrix of the first n observations are updated recursively, the Gram matrix by a rank one update, so sequential parameter learning in the style of Storvik is exact, with particles drawn independently from the Gaussian posterior and carrying no weights. New in this book.
- [Uniformity: the uniform Bernstein von Mises assumption and related open hypotheses](#uniformity) (Open Question 17.18, page 380; open): Open question: prove the uniform Bernstein von Mises assumption (Assumption U) on which the book's conditional theorems rest. The book's question also lists six related hypotheses it leaves unproved: the training residual assumption for fresh designs, the error bound of the one step summary for other nonlinear forward maps, a weaker regularity requirement than $\alpha>12$ for Navier Stokes, the condition of the sufficiency gap proposition for nonlinear forward maps, the expected information gain outside the reaction diffusion class, and whether the exponent of the theorem that no uniform guarantee holds is attained for $\beta>2$. New in this book.

#### Key terms

heat equation, dissipation barrier, viscous curse, information per mode, Gram matrix concentration, matrix Bernstein inequality, Bernstein von Mises (BvM), generative Bayesian computation (GBC), adjoint sufficient statistic, Navier Stokes, Taylor Green vortex, Stokes limit, Schrödinger (Schrodinger) equation, nonlinear Schrödinger (NLS), plane wave, Bogoliubov blocks, Bogoliubov dispersion relation, modulational (Benjamin Feir) instability, defocusing, focusing, Longstaff Schwartz, least squares Monte Carlo, Storvik filter, Jiang Wong summary, posterior mean summary, negative Sobolev space, Wasserstein distance, Laplace approximation, pCN

<a id="ch-18"></a>

### Chapter 18. Spin Systems, Phase Transitions and Inference

Pages 387 to 396.

This chapter asks how statistical mechanics describes Bayesian inference and sampling. It proves the Peierls theorem (a low temperature phase transition of the two dimensional Ising model), the Lee Yang circle theorem on the zeros of the partition function (Asano's lemma proved, the rest sketched), the Nishimori identity and the Gibbs variational principle. It derives the mean field equation of the Curie Weiss model by the Hubbard Stratonovich transformation and Laplace's method, and reports Onsager's solution. Bayes optimal inference in the spiked Wigner model is a planted spin glass on the Nishimori line, and the replica symmetric formula for the mutual information, with the I MMSE relation, locates the phase transitions of the Bayes optimal error. Further topics are statistical versus computational thresholds (planted clique, approximate message passing), double descent of ridge regression, samplers from physics (Metropolis, Glauber, Swendsen Wang, slice and log concave sampling), variational inference, and belief propagation with the Bethe approximation.

#### From the literature

Ising model (Lenz 1920; Ising 1925); Peierls argument (Peierls 1936); Lee Yang theorem (Lee and Yang 1952) and Asano's lemma (Asano 1970); Onsager's solution (Onsager 1944) and spontaneous magnetization (Yang 1952); Nishimori identity (Nishimori 1981); replica symmetric formula for the spiked Wigner model (Lelarge and Miolane 2019); I MMSE relation (Guo, Shamai and Verdú 2005); approximate message passing for planted clique (Deshpande and Montanari 2015); Metropolis process on planted clique (Jerrum 1992); ridgeless least squares risk (Hastie, Montanari, Rosset and Tibshirani 2022); Metropolis algorithm (Metropolis et al. 1953); Swendsen Wang algorithm (Swendsen and Wang 1987) as data augmentation (Edwards and Sokal 1988); slice sampling (Damien, Wakefield and Walker 1999); Gibbs variational principle (Donsker and Varadhan 1975); loopy belief propagation and the Bethe free energy (Yedidia, Freeman and Weiss 2005).

#### New results

The theorems of this chapter are known results. The running text also reports work of the authors: the critical ridge penalty for Bayesian double descent (Polson and Sokolov 2025), the extension of random walk sampling to log concave densities (Applegate, Kannan and Polson 1990; Frieze, Kannan and Polson 1994), and the witch's hat example, on which local samplers appear to converge while missing a region of substantial mass (Polson 1992).

No new results of this chapter are catalogued.

#### Key terms

Ising model, Gibbs measure, phase transition, spontaneous magnetization, Peierls argument, Lee Yang theorem, Curie Weiss model, mean field, Hubbard Stratonovich, Nishimori line, Nishimori identity, spiked Wigner model, planted spin glass, replica symmetric formula, planted clique, statistical computational gap, approximate message passing, double descent, Swendsen Wang, Gibbs variational principle, variational inference, belief propagation, Bethe approximation

<a id="ch-19"></a>

### Chapter 19. Generative Bayesian Computation as Transport

Pages 397 to 406.

This chapter asks how Bayes' rule can be computed as a map instead of a density. Generative Bayesian computation (GBC) seeks a function $H$ such that $H(y,U)$, with $U$ a fixed reference noise, has the posterior law for every $y$, learns $H$ from simulated pairs of parameters and data, and samples the posterior for a new $y$ by one evaluation. The chapter proves noise outsourcing (for real valued parameters, the general case by a Borel isomorphism), the check loss characterization of quantiles, that the perturbed observation ensemble Kalman update transports prior draws to posterior draws in the linear Gaussian model, Tweedie's formula, and the static reduction of the Schrödinger problem to entropic optimal transport. It quotes Brenier's theorem without proof. It connects GBC with diffusion models and score matching, Schrödinger bridges and Sinkhorn's algorithm (geometric convergence through Hilbert's projective metric), the Föllmer process, bootstraps and martingale posteriors, and approximate Bayesian computation (ABC) and its limits. A last section proposes quantile GBC for reinforcement learning with verifiable rewards.

#### From the literature

Transfer theorem behind noise outsourcing (Kallenberg 2002); Knothe Rosenblatt map (Rosenblatt 1952; Knothe 1957); Brenier's theorem (Brenier 1991) and McCann's extension (McCann 1995); perturbed observation ensemble Kalman filter (Evensen 1994; Burgers, van Leeuwen and Evensen 1998); time reversal of diffusions (Anderson 1982); Tweedie's formula as popularized by Efron (2011); Schrödinger's problem (Schrödinger 1931); Sinkhorn's algorithm (Sinkhorn 1964), its convergence for the continuous problem (Fortet 1940), geometric convergence by Birkhoff's contraction (Birkhoff 1957; Franklin and Lorenz 1989); small noise limit of entropic plans (Mikami 2004; Léonard 2012); Föllmer process (Föllmer 1985; Lehec 2013); stochastic interpolants (Albergo and Vanden Eijnden 2023); flow matching (Lipman et al. 2023); martingale posteriors (Fong, Holmes and Walker 2023); approximate Bayesian computation (Tavaré et al. 1997).

#### New results

Generative Bayesian computation is the authors' method (Polson and Sokolov 2025, Generative AI for Bayesian computation; Polson, Ruggeri and Sokolov 2024, Generative Bayesian computation for maximum expected utility), and the chapter presents none of its numbered results as new.

No new results of this chapter are catalogued.

#### Key terms

generative Bayesian computation, GBC, noise outsourcing, quantile map, check loss, pinball loss, Knothe Rosenblatt map, optimal transport, ensemble Kalman filter, Tweedie's formula, empirical Bayes, score matching, diffusion models, Schrödinger bridge, entropic optimal transport, Sinkhorn algorithm, iterative proportional fitting, Hilbert projective metric, Föllmer process, stochastic interpolants, flow matching, martingale posterior, approximate Bayesian computation, ABC, verifiable rewards

<a id="ch-20"></a>

### Chapter 20. Filters, Gates and Local Rules

Pages 407 to 428.

A filter computes the posterior of a hidden state from the observations so far and updates it recursively. The chapter asks which recursive and local update rules compute or approximate the Bayes filter. It covers the Kalman, Kalman Bucy, Zakai and Wonham filters, the local level model, and the score function filter, a Gaussian summary corrected by the score of the predictive density. For a Gaussian prior and scale mixture of normals noise it proves that the gain is a posterior average of Kalman gains that does not increase with the size of the innovation, and it reads LSTM gates as approximate Bayes filters under conditions. It treats particle filters (sequential Monte Carlo): weight degeneracy, error bounds, path degeneracy, particle learning and a Markov switching Zakai equation. It proves that the stationary subthreshold potential of a shot noise neuron with exponential amplitudes is a generalized Gamma convolution whose Thorin measure is the law of the amplitude rates weighted by the time constants, or is infinite almost surely. It also treats local learning rules (Hebb, Oja), stochastic approximation and the energy budget of the brain.

#### From the literature

Kalman filter (Kalman 1960); Kalman Bucy filter (Kalman and Bucy 1961); Zakai equation (Zakai 1969); Wonham filter (Wonham 1964); exponential smoothing as the optimal local level filter (Muth 1960); the particle filter (Gordon, Salmond and Smith 1993); the score function update (Masreliez 1975, West 1981); the shot noise model of the neuron (Stein 1965); the LSTM (Hochreiter and Schmidhuber 1997); ARCH (Engle 1982) and GARCH (Bollerslev 1986); Hebb's rule (Hebb 1949) and Oja's rule (Oja 1982); stochastic approximation (Robbins and Monro 1951); the Pitman Koopman Darmois theorem (Darmois 1935, Pitman 1936, Koopman 1936); importance weight variance growth (Kong, Liu and Wong 1994); particle filter error bounds (Del Moral 1998, Crisan and Doucet 2002, Del Moral and Guionnet 2001, Cérou, Del Moral and Guyader 2011); particle learning (Carvalho, Johannes, Lopes and Polson 2010); the Kurtz Xiong representation (Kurtz and Xiong 1999).

#### New results

The common time constant case of the shot noise theorem is in the authors' paper on shot noise processes (Polson and Sokolov 2026).

- [Gain of the score function filter under scale mixture noise](#the_gain_of_the_score_function_filter) (Proposition 20.8, page 421; proved): For a Gaussian prior and observation noise that is a scale mixture of normals, the posterior mean is a weighted average of the prior mean and the observation, and the weight (the gain) is a posterior average of Kalman gains that lies strictly between 0 and 1 and does not increase as the observation moves away from the prior mean. New in this book.
- [Gamma law and Thorin measure of the shot noise neuron](#gamma_law_of_the_shot_noise_neuron) (Theorem 20.9, page 423; proved): In the subthreshold regime (no firing threshold or reset), a leaky integrate and fire neuron driven by Poisson input, where each spike has its own random time constant and an exponentially distributed amplitude with its own random rate, has a stationary potential that is a generalized Gamma convolution whose Thorin measure is the law of the amplitude rates weighted by the input rate and the time constants, or it is infinite almost surely when that measure is not a Thorin measure. New in this book.

#### Key terms

filtering, state space model, hidden Markov model, Kalman filter, Zakai equation, Wonham filter, local level model, score function filter, Tweedie formula, LSTM, GARCH, scale mixture of normals, particle filter, sequential Monte Carlo, weight degeneracy, path degeneracy, particle learning, propagation of chaos, Kurtz Xiong, Markov switching, shot noise neuron, generalized Gamma convolution, Thorin measure, Oja rule, stochastic approximation

<a id="ch-21"></a>

### Chapter 21. Kolmogorov, Cybernetics and the Thermodynamics of Information

Pages 429 to 438.

The chapter asks what Hilbert's sixth problem means for inference regarded as a physical process, starting from Kolmogorov's view of machines that learn and Wiener's cybernetics. It presents Kolmogorov's superposition theorem (the Kolmogorov Arnold representation, Hilbert's thirteenth problem) without proof, algorithmic information (Kolmogorov complexity, the universal prior, minimum description length), and Maxwell's demon with the Szilard engine and Landauer's principle. It proves a Landauer bound in information theoretic form: for a memory with finitely many states of equal energy and a heat bath that start independent, the bath in its Gibbs state, and evolve under reversible dynamics, the expected energy gained by the bath is at least $k_BT\log2$ per bit of entropy lost by the memory. It proves Kelly's theorem on optimal growth and proportional betting, a recursive self learning bound from the data processing inequality (without a verifier the information about the target never exceeds its initial value, and a verifier channel of capacity $C$ bits per round adds at most $C$ per round), Jarzynski's equality, and a lower bound on the heat dissipated in resetting a memory that stores reconstructions at a given average distortion. Crooks' theorem and the Sagawa Ueda inequality are quoted without proof.

#### From the literature

Kolmogorov's superposition theorem (Kolmogorov 1957) and Arnold's theorem on functions of three variables (Arnold 1957); Kolmogorov complexity (Kolmogorov 1965); minimum description length and stochastic complexity (Rissanen 1978, 1996); the Szilard engine (Szilard 1929); Landauer's principle (Landauer 1961) and its experimental confirmation (Bérut and coauthors 2012); reversible measurement (Bennett 1982); Kelly's theorem (Kelly 1956); Jarzynski's equality (Jarzynski 1997; for Markov dynamics, Jarzynski 1997 and Crooks 2000); Crooks' fluctuation theorem (Crooks 1999); annealed importance sampling (Neal 2001); the generalized second law with feedback (Sagawa and Ueda 2010); rate distortion theory and the data processing inequality, as treated by Cover and Thomas (2006); the algorithms of Blahut (1972) and Arimoto (1972).

#### New results

No new results of this chapter are catalogued.

#### Key terms

Kolmogorov Arnold representation theorem, Kolmogorov superposition theorem, Hilbert's thirteenth problem, Kolmogorov complexity, algorithmic information, universal prior, minimum description length, stochastic complexity, Maxwell's demon, Szilard engine, Landauer principle, Landauer bound, Kelly criterion, data processing inequality, recursive self learning, cybernetics, Jarzynski equality, Crooks theorem, Sagawa Ueda, rate distortion, Blahut Arimoto algorithm

<a id="ch-22"></a>

### Chapter 22. Open Problems and the Bridge to Hilbert's Eighth Problem

Pages 439 to 450.

This chapter links Hilbert's sixth and eighth problems through the heat equation and closes with open problems. The Riemann hypothesis (RH) is expressed through the backward heat flow: the de Bruijn Newman constant $\Lambda$ is defined from the Gaussian deformation $H_t$ of the Pólya kernel of the Riemann $\Xi$ function, $H_t$ solves the backward heat equation, and RH holds if and only if $\Lambda\leq0$. The chapter proves the Pólya de Bruijn theorem that the backward heat semigroup preserves real zeros of even entire functions of order less than 2, quotes $0\leq\Lambda\leq0.2$ without proof, and shows that RH is equivalent to the Lee Yang property of the Pólya law. It reads the de Bruijn flow as exponential tilting and conditioning on the second moment, and relates RH to the Biane Pitman Yor Brownian excursion identity and to generalized Gamma convolutions. The link with the inferential sixth problem is an analogy and not an equivalence. No proof of RH is claimed.

#### From the literature

Riemann (1859): $\Xi$ as a cosine transform, roots very probably real. Pólya (1926): the explicit kernel of $\Xi$. Pólya (1927) and de Bruijn (1950): the backward heat semigroup preserves real zeros. de Bruijn (1950): the Gaussian family $H_t$ and $\Lambda\leq\frac12$. Newman (1976): $\Lambda>-\infty$, the conjecture $\Lambda\geq0$ and the Lee Yang reformulation of RH, after Lee and Yang (1952) and Newman (1974). Rodgers and Tao (2020): $\Lambda\geq0$. Polymath (2019): $\Lambda\leq0.22$. Platt and Trudgian (2021): $\Lambda\leq0.2$. Csordas, Smith and Varga (1994): rigorous zero dynamics. Biane, Pitman and Yor (2001): $2\xi(s)$ as a Brownian excursion moment. Kent (1980): hitting time expansions. Csiszár (1984): conditional limit theorem. Behind the open problems: Villani (2003), Carlen, Carvalho, Le Roux, Loss and Villani (2010, the fourth moment question), Einav (2011) and Gao, Wang and Xia (2026, preprint) on Kac walk entropy production; Konen and Nickl (2026) on Navier Stokes; Deng, Hani and Ma (2024, 2025, preprints).

#### New results

The theorems and proposition of this chapter are known results; the catalogued items are three open problems posed by the authors.

- [Open problem: exact samplers for Brownian functionals from Kent's eigenvalue expansion](#open_problem_yor_exact_samplers) (Open Problem 4, page 445; open): A program: find a class of regular diffusions whose hitting time remainder after the first terms of Kent's exponential series can be sampled exactly at finite expected cost, prove the sampler exact, and use it to build a library of exact samplers for Brownian functionals. New in this book.
- [Open problem: uniform entropy production bound for the Kac walk on conditioned products of normal scale mixtures](#open_problem_kac_entropy_production_ggc_mixtures) (Open Problem 8, page 446; open): Decide whether the entropy production of the Kac walk is bounded below by a fixed multiple of the relative entropy, with a constant that does not depend on the number of particles, for conditioned product densities built from bounded normal scale mixtures with generalized Gamma convolution mixing law, unit variance and fourth moment at most $M$; the constant may depend on $M$. New in this book.
- [Open problem: posterior contraction and Bernstein von Mises theorems for the initial vorticity of two dimensional Navier Stokes from fixed sensors](#open_problem_ns_posterior_fixed_sensors) (Open Problem 10, page 447; open): Determine the posterior contraction rate for the initial vorticity of the two dimensional Navier Stokes equations from noisy observations at a fixed array of sensors and times, identify the functionals of the initial vorticity that admit a Bernstein von Mises theorem, and ask whether the posterior can be computed in polynomial time. New in this book.

#### Key terms

Hilbert's sixth problem, Hilbert's eighth problem, Riemann hypothesis, RH, Riemann xi function, de Bruijn Newman constant, backward heat equation, Pólya kernel, Polya kernel, Lee Yang property, ferromagnetic random variables, Pólya law, Biane Pitman Yor identity, Brownian excursion, generalized Gamma convolution, GGC, Thorin measure, exact sampling, Kac walk, entropy production, Navier Stokes, Bernstein von Mises, posterior contraction

<a id="ch-A"></a>

### Appendix A. Lévy Processes, Thorin Measures and Related Classes

Pages 451 to 454.

This appendix collects the definitions and standard results on infinite divisibility that the book uses, with references for the proofs. It defines Lévy processes, their characteristic exponent through the Lévy Khintchine formula, and the Lévy Itô decomposition into drift, Brownian motion and an independent Poisson jump part with Lévy measure $\nu$. It defines Bernstein, completely monotone, Stieltjes and complete Bernstein functions, and generalized Gamma convolutions (GGC): laws on $[0,\infty)$ with Laplace exponent $\phi(\lambda)=a\lambda+\int\log(1+\lambda/y)\,U(\mathrm{d}y)$, drift $a\ge0$ and Thorin measure $U$, which Stieltjes inversion of $\phi'$ recovers (the formula behind the computational strategy of Chapter 22). It states that the class of GGCs is closed under convolution and weak limits, that every GGC is self decomposable and unimodal, and that hyperbolically completely monotone (HCM) laws are GGCs. It then treats normal scale mixtures by Brownian subordination and extended generalized Gamma convolutions (EGGC), a class that contains the GGCs and the Student $t$, symmetric hyperbolic and logistic laws, and finally the Lee Yang measures of Newman (Section 7.7). The results are presented as standard, with chapter or section numbers of the references.

#### From the literature

- The Lévy Khintchine formula, the Lévy Itô decomposition, the characterization of self decomposable laws by their Lévy measure and the characteristic exponent of a Brownian subordinated process (Sato 1999).
- Bernstein, Stieltjes and complete Bernstein functions, and Bernstein's theorem on completely monotone functions (Schilling, Song and Vondraček 2012).
- Generalized Gamma convolutions and Thorin measures (Thorin 1977), and hyperbolically completely monotone laws, with proofs of their closure properties in Bondesson (1992); the lognormal law is a GGC (Thorin 1977).
- Every self decomposable law is unimodal (Yamazato 1978).
- Positive stable laws of index at most one half are HCM (Bosch and Simon 2016).
- Extended generalized Gamma convolutions (Thorin 1978; Bondesson 1992).
- The Lee Yang class of even measures (Newman 1974).

#### New results

No new results of this appendix are catalogued.

#### Key terms

Lévy process, infinitely divisible law, Lévy Khintchine formula, Lévy Itô decomposition, Lévy measure, Poisson point process, subordinator, Brownian subordination, Laplace exponent, Bernstein function, complete Bernstein function, Stieltjes function, completely monotone function, generalized Gamma convolution, GGC, Thorin measure, Stieltjes inversion, self decomposable law, unimodal law, hyperbolically completely monotone, HCM, generalized inverse Gaussian, normal scale mixture, extended generalized Gamma convolution, EGGC, Student t law, hyperbolic law, logistic law, Pólya Gamma law, Lee Yang measure, Newman class

<a id="ch-B"></a>

### Appendix B. Code and Reproducibility

Pages 455 to 470.

Each of the book's 32 figures is drawn by a Python script in the folder `code`: 28 compute their data, 3 replot recorded experiment results and one, the Lanford window, is a schematic. Ten tables have numbers that a script computes or reads. `figures.py` and `figures_color.py` draw 20 figures; `figures_pf.py`, `figures_pl.py` and `figures_msw.py` the filter figures of Chapter 20; `fk_posterior.py` (whose generator study needs PyTorch) and `ns2d_posterior.py` (which needs JAX) the posterior figures and tables of Chapter 12; `yor_catalogue.py` the table of Yor identity checks; six `mf_` scripts the Part IV figures, with `mf_gain.py` and `mf_gap.py` for two tables. The Part IV experiments are in `code/anc`, a copy of the ancillary files of the authors' manifold paper (scripts, recorded results, SLURM files). The figure and table scripts need Python 3, NumPy, SciPy and Matplotlib (NumPy 2.0 or later for three), fix any random seeds, overwrite the shipped figures unless run in a copy, and take under a second to 19 minutes on an Apple M2 laptop. The replicate studies take hours, so the book reads their recorded results; the authors reran them on a cluster, and the Navier Stokes experiment scripts in a copy of the folder, and matched the recorded results to a relative difference of at most $3\times10^{-10}$, except wall clock times and four entries (up to $6\times10^{-8}$). The chaotic Hénon Heiles and standard map figures can differ in detail on another machine, but not in structure. Some files in `code/anc` are outdated or absent. Three `pdflatex` runs rebuild the book.

#### From the literature

None.

#### New results

No new results of this appendix are catalogued.

#### Key terms

reproducibility, code, Python scripts, figure scripts, `figures.py`, `figures_color.py`, `fk_posterior.py`, `ns2d_posterior.py`, `yor_catalogue.py`, `hh_checks.py`, `code/anc`, `code/ns_checks`, ancillary files, recorded results, JSON, SLURM, fixed random seeds, replicate studies, GBC (generative Bayesian computation), pCN (preconditioned Crank Nicolson), NumPy, SciPy, Matplotlib, JAX, PyTorch, wall clock time, Hénon Heiles, standard map, rebuilding the book, pdflatex

<a id="ch-C"></a>

### Appendix C. A Probability Toolkit

Pages 471 to 474.

This appendix collects standard probability results used throughout the book, with references for the proofs. It covers weak convergence on Polish spaces (Prokhorov's theorem on tightness and relative compactness, the portmanteau theorem, Skorokhod's representation theorem) and the tightness, identification and uniqueness scheme of hydrodynamic limits; metrics on probability measures (total variation, Hellinger, bounded Lipschitz and Wasserstein $W_p$ distances, Pinsker's inequality, the comparison of total variation with Hellinger distance); martingales (Doob's convergence theorem and maximal inequality, optional stopping, Lévy's characterization of Brownian motion, the Dambis Dubins Schwarz time change); large deviations (the large deviation principle with a good rate function, the contraction principle, Varadhan's lemma, the Gärtner Ellis theorem, and the principles of Cramér, Sanov, Schilder and Donsker Varadhan, with Schilder's rate function the Cameron Martin norm, used in Chapter 12); and Markov semigroups and generators (Kolmogorov equations, invariant and reversible measures, the Dirichlet form, Poincaré and log Sobolev inequalities with convergence rates $e^{-t/C}$ and $e^{-2t/C}$, and the Bakry Émery criterion $\Gamma_2\ge K\Gamma$, which for the diffusion with generator $\Delta-\nabla V\cdot\nabla$ on a Riemannian manifold reads $\mathrm{Ric}+\nabla^2V\ge K$).

#### From the literature

- Prokhorov's theorem (Prokhorov 1956) and Skorokhod's representation theorem (Skorokhod 1956), with proofs of these and of the portmanteau theorem in Billingsley (1999).
- Pinsker's inequality and the total variation and Hellinger comparison (Tsybakov 2009); the bounded Lipschitz metric and weak convergence (Dudley 2002); the Wasserstein distance (Villani 2009).
- Doob's convergence theorem, maximal inequality and optional stopping (Kallenberg 2002); Lévy's characterization of Brownian motion and the Dambis Dubins Schwarz theorem (Revuz and Yor 1999).
- The large deviation principles of Cramér (sample means), Sanov (1957, empirical measures), Schilder (1966, Brownian paths) and Donsker and Varadhan (1975, occupation measures of Markov processes); the contraction principle, Varadhan's lemma and the Gärtner Ellis theorem (Dembo and Zeitouni 1998).
- Markov semigroups (Ethier and Kurtz 1986), Poincaré and log Sobolev inequalities (Bakry, Gentil and Ledoux 2014), the Bakry Émery criterion (Bakry and Émery 1985).

#### New results

No new results of this appendix are catalogued.

#### Key terms

weak convergence, Polish space, Prokhorov theorem, tightness, portmanteau theorem, Skorokhod representation theorem, total variation distance, Hellinger distance, bounded Lipschitz metric, Wasserstein distance, Pinsker inequality, martingale, Doob convergence theorem, Doob maximal inequality, optional stopping, Lévy characterization of Brownian motion, Dambis Dubins Schwarz theorem, large deviation principle, rate function, contraction principle, Varadhan lemma, Gärtner Ellis theorem, Cameron Martin space, Markov semigroup, Kolmogorov equations, invariant measure, reversible measure, Dirichlet form, Poincaré inequality, log Sobolev inequality, Bakry Émery criterion

<a id="ch-D"></a>

### Appendix D. A Chronology

Pages 475 to 478.

This appendix is a chronology of 78 dated entries, the events and results discussed in the book, from Gauss's derivation of the normal law of errors from the optimality of the arithmetic mean (1809) to the long time derivations of the Boltzmann equation and of fluid equations from hard spheres by Deng, Hani and Ma (2024 to 2025). It follows several threads in parallel: kinetic theory and the reversibility and recurrence objections (Maxwell, Boltzmann, Loschmidt, Poincaré, Zermelo), Hilbert's problems and the axiomatization of mechanics and probability, Brownian motion, quantum mechanics, ergodic theory, entropy and information (Shannon, Kolmogorov, Sinai, Landauer), the Ising model and the Lee Yang theorem, turbulence and Navier Stokes, Riemann's $\Xi$ function and the de Bruijn Newman constant, and filtering and Bayesian computation. It gives dates and attributions and proves nothing.

#### From the literature

The chronology dates, among others: Boltzmann's equation and H theorem (1872); Loschmidt's reversibility objection (1876); Boltzmann's counting derivation of the equilibrium distribution (1877; the form $S=k\log W$ is Planck's, of 1900); Poincaré's corrected memoir with the recurrence theorem (1890) and Zermelo's recurrence objection (1896); Hilbert's problems (1900); Einstein's paper on Brownian motion (1905); Wiener's construction of Brownian motion as a measure on paths (1923); Kolmogorov's Grundbegriffe (1933); de Finetti's representation theorem (1937); Onsager's solution of the two dimensional Ising model (1944); Shannon's theory of communication (1948); Lee and Yang's circle theorem (1952); Sanov's theorem (1957); Kolmogorov and Sinai on dynamical entropy (1958 to 1959); Lanford's theorem (1975); Thorin's proof that the lognormal law is infinitely divisible (1977); Golse and Saint Raymond's derivation of Navier Stokes from Boltzmann for weak solutions (2004); Mischler and Mouhot's completion of Kac's program (2013); Isett's proof of Onsager's conjecture (2018); Rodgers and Tao's proof of $\Lambda\ge0$ (2020); Deng, Hani and Ma on long time derivations from hard spheres (2024 to 2025).

#### New results

No new results of this appendix are catalogued.

#### Key terms

chronology, timeline, history of probability, history of statistical mechanics, Hilbert's problems, Boltzmann equation, H theorem, reversibility objection, recurrence objection, Poincaré recurrence theorem, Brownian motion, Kolmogorov axioms, ergodic theorems, Kolmogorov Sinai entropy, Ising model, Lee Yang circle theorem, Lanford theorem, Boltzmann Grad limit, Kac program, Onsager conjecture, Navier Stokes blowup, de Bruijn Newman constant, Maxwell's demon, Landauer principle, particle filter, particle learning

<a id="ch-E"></a>

### Appendix E. Notation

Pages 479 to 484.

This appendix is the notation guide of the book. It lists the symbols used in more than one chapter or throughout a long section, with the chapters where they occur and, for Part IV, the section, result or equation that defines each one. Four blocks cover probability, information and stochastic processes (probability, expectation, Gaussian law, types, Shannon and Boltzmann entropies, differential entropy, Fisher information, relative entropy $\mathrm{KL}$, total variation, bounded Lipschitz and Wasserstein distances, Brownian motion, Bessel process, Pólya Gamma law, Laplace and Lévy exponents, Perelman's entropy); mechanics, kinetic theory, fluids and quantum mechanics (Maxwellian, viscosity, density operator, von Neumann entropy, Nelson's stochastic mechanics); Part IV, the solution manifold (forward map, linearization and its adjoint, prior, posterior, Bernstein von Mises limit, information per mode, summary dimension); and inference as statistical mechanics (Gibbs measure, generator map, check loss, hidden Markov filters, Riemann's $\xi$ and $\Xi$). A last block lists the letters that mean different things in different chapters, such as $\alpha$, $\beta$, $\gamma$, $\varepsilon$, $\theta$, $\lambda$, $\nu$, $\rho$, $\sigma$, $\Gamma$, $\Pi$, $\Phi$, $D$, $H$, $T$ and the torus $\mathbb{T}^d$, whose side is $2\pi$ in Chapter 12, one in Chapters 4, 11 and 14 to 17 (with exceptions) and not fixed in Chapters 1 and 13.

#### From the literature

None.

#### New results

No new results of this appendix are catalogued.

#### Key terms

notation, list of symbols, nomenclature, glossary of symbols, symbol index, conventions, overloaded symbols, Shannon entropy, Boltzmann functional, differential entropy, Fisher information, relative entropy, Kullback Leibler divergence, total variation, Wasserstein distance, Maxwellian, density operator, von Neumann entropy, Nelson stochastic mechanics, forward map, solution manifold, information per mode, Bernstein von Mises limit, Gibbs measure, check loss, torus

## All results

The results that are new in the book, that come from the authors' own papers, or that correct one of those papers, as the book states them: 75 entries (58 proved, 11 conditional, 5 open, 1 counterexample). Results of other authors that the book presents are credited in the chapter summaries above.

Status: proved; conditional (proved assuming the named statements, which the book does not prove); open (stated as an open question); counterexample (a proved counterexample); withdrawn (found wrong after release; the entry says what was wrong and which version corrects it).

### Chapter 1. Hilbert's Sixth Problem

<a id="posterior_on_the_solution_manifold"></a>

#### Posterior on the solution manifold

Proposition 1.1, page 7 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: proved.

Statement. Let $X$ be a Polish space and $\Phi_t:X\to X$, $t\in[0,T]$, a dynamical system whose trajectory map $\Gamma(x)=(\Phi_t(x))_{t\in[0,T]}$ takes values in the space $C([0,T];X)$ of continuous paths (a Polish space under the uniform metric) and is Borel measurable. Let $\Pi$ be a prior probability measure on $X$. Suppose one observes, at times $t_1,\dots,t_m\in[0,T]$, $y_j=\mathcal{O}_j\big(\Phi_{t_j}(x)\big)+\eta_j$ for $j=1,\dots,m$, where the $\mathcal{O}_j$ are measurable maps from $X$ to a Euclidean space and the noise variables $\eta_1,\dots,\eta_m$ are independent of one another and of $x$ and have a common density $p_\eta$. When the normalizing constant is finite and positive, the posterior is $\Pi(\,\mathrm{d}x\mid y)\propto\prod_{j=1}^m p_\eta\big(y_j-\mathcal{O}_j(\Phi_{t_j}(x))\big)\,\Pi(\,\mathrm{d}x)$. Let $\mathcal{M}=\{(\Phi_t(x))_{t\in[0,T]}:x\in X\}$ be the solution manifold and let $P=\Gamma_\#\Pi(\cdot\mid y)$ be the pushforward of the posterior to $C([0,T];X)$. Then $\mathcal{M}$ is universally measurable and $P(\mathcal{M})=1$, and for every Borel functional $F$ of the trajectory that is nonnegative or $P$ integrable, $\mathbb{E}_P[F]=\mathbb{E}_{\Pi(\cdot\mid y)}[F\circ\Gamma]$. In particular every posterior predictive quantity is an average of exact solutions of the dynamics.

Source: [`source/chapters/ch01_hilbert.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ch01_hilbert.tex), label `prop:solution_manifold`.

### Chapter 7. Scale Mixtures, Thorin Measures and Shot Noise

<a id="polya_gamma_logistic_identity"></a>

#### Pólya Gamma integral identity for the logistic likelihood

Theorem 7.5, page 85 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. First stated in Polson, Scott and Windle (2013), Bayesian inference for logistic models using Pólya Gamma latent variables, Journal of the American Statistical Association 108, 1339 to 1349.

Status: proved.

Statement. For $b>0$ and $c\in\mathbb{R}$, the Pólya Gamma law $PG(b,c)$ is the law of $\omega=\frac{1}{2\pi^2}\sum_{k=1}^\infty \frac{g_k}{(k-\frac12)^2+c^2/(4\pi^2)}$, where $g_1,g_2,\dots$ are independent Gamma variables with shape $b$ and unit rate. Let $p(\cdot\mid b,0)$ be the density of $PG(b,0)$. Then for all $b>0$, $a\in\mathbb{R}$ and $\psi\in\mathbb{R}$, $\frac{(e^{\psi})^a}{(1+e^{\psi})^b}=2^{-b}e^{(a-b/2)\psi}\int_0^\infty e^{-\omega\psi^2/2}\,p(\omega\mid b,0)\,\mathrm{d}\omega$. Moreover, the conditional law of $\omega$ given $\psi$, that is the law with density proportional to $e^{-\omega\psi^2/2}p(\omega\mid b,0)$ in $\omega$, is $PG(b,\psi)$.

Source: [`source/chapters/ch05_mixtures.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ch05_mixtures.tex), label `thm:pg_identity`.

### Chapter 12. Navier Stokes as Inference on the Solution Manifold

<a id="gradient_stability_initial_condition_ns2d"></a>

#### Gradient stability for the initial condition of two dimensional Navier Stokes, with time zero observed

Proposition 12.8, page 153 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: proved.

Statement. Let $\nu,T,L>0$. Let $\mathbb{T}^2=(\mathbb{R}/2\pi\mathbb{Z})^2$, let $\dot H^{s}_\diamond$ denote the Sobolev space of order $s$ of divergence free, mean zero vector fields on $\mathbb{T}^2$, and let $f\in\dot H^{1}_\diamond$ be a forcing. Let $\mathcal{X}=[0,T]\times\mathbb{T}^2$ with the uniform probability measure, and let $e_1,e_2,\dots$ be the eigenfunctions of the Stokes operator on $\mathbb{T}^2$, orthonormal in $L^2$, with eigenvalues $\lambda_1\le\lambda_2\le\cdots$. For $D\ge1$ and $\theta\in\mathbb{R}^D$ let $\mathcal{G}(\theta)(t,x)=u_\theta(t,x)$ be the velocity of the solution of the two dimensional Navier Stokes equations with viscosity $\nu$, forcing $f$ and initial condition $\sum_{k\le D}\theta_ke_k$. Then there is a constant $c>0$, depending only on $\nu$, $T$, $\|f\|_{\dot H^{1}_\diamond}$, $L$ and the torus, such that
$\big\|v^\top\nabla\mathcal{G}(\theta)\big\|_{L^2(\mathcal{X})}\ge c\,D^{-1/2}\,|v|$
for every $D\ge1$, every $v\in\mathbb{R}^D$ and every $\theta\in\mathbb{R}^D$ with $\big\|\sum_{k\le D}\theta_ke_k\big\|_{\dot H^{2}_\diamond}\le L$. Here $v^\top\nabla\mathcal{G}(\theta)=\sum_{k\le D}v_k\,\partial\mathcal{G}(\theta)/\partial\theta_k$ is the derivative of $\mathcal{G}$ at $\theta$ in the direction $v$ and $|v|$ is the Euclidean norm.

Source: [`source/chapters/ext/ch10_nw.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/ch10_nw.tex), label `prop:gs_ns`.

<a id="bernstein_von_mises_for_generators"></a>

#### Bernstein von Mises for generators

Proposition 12.10, page 157 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: proved.

Statement. Let $\Pi_n(\cdot\mid y)$ be posterior distributions of a parameter $\theta$ given data $y$, let $L$ be a functional of the parameter, let $\hat L_n$ be a statistic, and let $H_n$ be a generator, a map that takes the data $y$ and a uniform random variable $U$ to a parameter value $H_n(y,U)$. Write $\tilde\Pi_n$ for the law of $\sqrt n\,(L\theta-\hat L_n)$ when $\theta\sim\Pi_n(\cdot\mid y)$, write $\tilde G_n$ for the law of $\sqrt n\,(L H_n(y,U)-\hat L_n)$ when $U$ is uniform, and let $d_{BL}$ be the bounded Lipschitz metric. Suppose that, in probability under the data generating law,
$d_{BL}\big(\tilde\Pi_n,N(0,\sigma^2)\big)\to0$ and $d_{BL}\big(\tilde G_n,\tilde\Pi_n\big)\to0.$
Then $d_{BL}\big(\tilde G_n,N(0,\sigma^2)\big)\to0$ in probability: the generated law satisfies the same Bernstein von Mises theorem as the posterior.

Source: [`source/chapters/ch10_ns_inference.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ch10_ns_inference.tex), label `prop:bvm_generators`.

### Chapter 14. The Inverse Problem on the Solution Manifold

<a id="the_limit_law_is_nondegenerate"></a>

#### Nondegeneracy of the Gaussian limit of the posterior trajectory for reaction diffusion equations

Lemma 14.3, page 189 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: proved.

Statement. Work in the setting of Theorem 1 of Nickl (2024), the Bernstein von Mises theorem for forward trajectories: $\Omega=[0,1]^d$ is the $d$ dimensional torus with $d\le3$, $T>0$, $f\in C_c^\infty(\mathbb{R})$, $\theta_0$ is a smooth initial condition, $u_\theta$ is the solution of $\partial_tu-\Delta u=f(u)$, $u(0)=\theta$, which is observed with standard normal noise at design points uniform on $[0,T]\times\Omega$, and $\theta$ has the rescaled Gaussian series prior of Theorem 1 of Nickl (2024), of integer regularity $\gamma>2+3d$. Let $\mathbb{I}_{\theta_0}$ be the linearization of $\theta\mapsto u_\theta$ at $\theta_0$, $\mathbb{I}_{\theta_0}^*$ its adjoint with respect to Lebesgue measure on $\Omega$ and on $[0,T]\times\Omega$, and $\mathcal{N}_{\theta_0}=N(0,T(\mathbb{I}_{\theta_0}^*\mathbb{I}_{\theta_0})^{-1})$ the Gaussian limit of the posterior of $\theta$. Let $0<t_{\min}<t_{\max}<\infty$, let $\mathscr{C}=C([t_{\min},t_{\max}],C(\Omega))$ with the supremum norm, and let $\mu$ be the law in $\mathscr{C}$ of the solution $U$ of $\partial_tU-\Delta U-f'(u_{\theta_0})U=0$ with $U(0)=\vartheta\sim\mathcal{N}_{\theta_0}$. Then the reproducing kernel Hilbert space of the Gaussian measure $\mu$ is a nontrivial linear subspace of $\mathscr{C}$, and $r\mapsto\mu(\|U\|_{\mathscr{C}}\le r)$ is continuous and strictly increasing on $[0,\infty)$.

Source: [`source/chapters/ext/m1a.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m1a.tex), label `m:lem:nondeg`.

<a id="manifold_gain_for_the_heat_equation"></a>

#### Manifold gain for the heat equation: prior on the initial condition against a space time Gaussian process prior

Proposition 14.5, page 193 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: proved.

Statement. Consider the heat equation $\partial_tu=\nu\Delta u$ with viscosity $\nu>0$ on the torus $\mathbb{T}^d=[0,1]^d$, where $\lambda_j$ are the eigenvalues of $-\Delta$ ($\lambda_j=4\pi^2|k_j|^2$ for the Fourier mode $k_j\in\mathbb{Z}^d\setminus\{0\}$), $\lambda_1$ is the smallest, and $(e_j)$ is the corresponding orthonormal eigenbasis. There are $N$ observations at design points uniform on $[0,T]\times\mathbb{T}^d$ with noise variance $\varsigma^2$, the variance that the model normalizes to one and that is carried as a symbol only to show where it enters. In the constrained model the prior is placed on the initial condition, with independent Gaussian coefficients of variances $\sigma_{0,j}^2=\rho^2(\lambda_j/\lambda_1)^{-\alpha}$, where $\alpha>(d+1)/2$, so that the field is $\sum_j\theta_je^{-\nu\lambda_jt}e_j$. In the unconstrained model, for comparison, the prior is a Gaussian process on the space time field $u(t,x)$ with Fourier variances $\sigma_{0,km}^2=\rho^2((\lambda_k+\omega_m^2)/\lambda_1)^{-\alpha}$, $\omega_m=2\pi m/T$, $m\in\mathbb{Z}$, where $k$ runs over the spatial modes (those with $\lambda_k\ge\lambda_1$), so that the two priors have comparable regularity in $x$. The Gram matrix of the design is replaced by its limit: $\operatorname{diag}(\iota_j)$ with $\iota_j=(1-e^{-2\nu\lambda_jT})/(2\nu\lambda_jT)$ in the constrained model, and the identity in the unconstrained one. Then:
(i) the constrained posterior standard deviation of $u(t,x)$ is $\big(\sum_je^{-2\nu\lambda_jt}(N\iota_j/\varsigma^2+\sigma_{0,j}^{-2})^{-1}\big)^{1/2}$, decreasing in $t$, and the effective number of parameters, $\#\{j:N\iota_j\sigma_{0,j}^2\ge\varsigma^2\}$, is, for $\varsigma=1$, of order $(N\rho^2/\nu T)^{d/(2\alpha+2)}$ as $\Lambda=(N\rho^2\lambda_1^\alpha/(2\nu T))^{1/(\alpha+1)}\to\infty$ with $\nu T\Lambda\geq1$, with constants that depend only on $\alpha$, $d$ and $\rho$;
(ii) the unconstrained posterior standard deviation is $\big(\sum_{k,m}(N/\varsigma^2+\sigma_{0,km}^{-2})^{-1}\big)^{1/2}$, independent of $(t,x)$, and its effective number of parameters, $\#\{(k,m):N\sigma_{0,km}^2\ge\varsigma^2\}$, is of order $N^{(d+1)/(2\alpha)}$ as $N\to\infty$;
(iii) the ratio of the unconstrained to the constrained standard deviation at time $t$ is at least $e^{\nu\lambda_1t}$ times its value at $t=0$, so it grows without bound as $t$ increases, at the rate at which the manifold contracts.

Source: [`source/chapters/ext/m1a.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m1a.tex), label `m:prop:gain`.

### Chapter 15. Adjoint Sufficient Statistics

<a id="adjoint_representation_of_the_sufficient_statistic"></a>

#### Adjoint representation of the sufficient statistic

Lemma 15.1, page 206 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: proved.

Statement. Let $(e_j)$ be an orthonormal basis of $L^2(\Omega)$, let $S_t$ be a strongly continuous semigroup on $L^2(\Omega)$ with $S_te_j=s_j(t)e_j$ and generator $A$, let $(t_i,x_i)\in[0,T]\times\Omega$ and $Y_i\in\mathbb{R}$ for $i\le N$, let $\Phi_{ij}=s_j(t_i)e_j(x_i)$ ($i\le N$, $j\le D$) be the design matrix, so that $(\Phi^\top Y)_j=\sum_{i\le N}Y_is_j(t_i)e_j(x_i)$, and let $r=\sum_{i\le N}Y_i\,\delta_{t_i}\otimes\delta_{x_i}$ be the empirical data measure on $[0,T]\times\Omega$. Then for every $h=\sum_jh_je_j\in\operatorname{span}\{e_j:j\le D\}$, $\langle\Phi^\top Y,h\rangle_{\mathbb{R}^D}=\sum_{i=1}^NY_i\,(S_{t_i}h)(x_i)=\big\langle h,\int_0^TS_t^*r(t)\,\mathrm{d}t\big\rangle$, so that $\Phi^\top Y$ is the coefficient vector of $w(0)$, where $w$ is the mild solution of the backward problem $-\partial_sw=A^*w+r$, $w(T)=0$.

Source: [`source/chapters/ext/m2a.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m2a.tex), label `m:lem:adjoint`.

<a id="exact_sufficiency_linear_case"></a>

#### Exact sufficiency, linear case

Proposition 15.2, page 207 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: proved.

Statement. Consider the linear model $Y=\Phi\theta+\varepsilon$ with $\theta\in\mathbb{R}^D$, design matrix $\Phi_{ij}=s_j(t_i)e_j(x_i)$ ($i\le N$, $j\le D$, where $S_te_j=s_j(t)e_j$ for a semigroup that is diagonal in the basis $(e_j)$), noise $\varepsilon\sim N(0,\mathrm{Id}_N)$ and Gaussian prior $\theta\sim N(0,\Sigma_0)$. Let $S_N=\Phi^\top Y$ be the adjoint statistic (the coefficient vector of $w(0)$, where $w$ solves the backward adjoint problem driven by the data) and $V_N=(\Phi^\top\Phi+\Sigma_0^{-1})^{-1}$. Then $S_N$ together with the design is sufficient for $\theta$; the posterior given $S_N$ is exactly the posterior given all the data, namely $N(V_NS_N,V_N)$; and the conditional quantile map is exactly affine: for each coordinate $j$ and $\tau\in(0,1)$, $Q_j(\tau\mid S_N)=(V_NS_N)_j+z_\tau(V_N)_{jj}^{1/2}$, where $z_\tau$ is the $\tau$ quantile of the standard normal law. The slope of this map in $S_N$ is $V_N$, not the identity. For the preconditioned summary $\tilde S_N=V_NS_N$, which is the posterior mean, the map $\tilde S_N\mapsto Q_j(\tau\mid S_N)$ has slope exactly one and, apart from the data independent scale term $z_\tau(V_N)_{jj}^{1/2}$, intercept zero. Consequently generative Bayesian computation (GBC) with summary $\tilde S_N$ and an identity plus scale generator is exact for every $N$, up to the estimation of the $D\times D$ scale from $M$ simulations; in the linear model that scale is $V_N$ itself and is known in closed form.

Source: [`source/chapters/ext/m2a.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m2a.tex), label `m:prop:linsuff`.

<a id="equivalence_with_the_efficient_centering"></a>

#### Equivalence of the one step efficient score summary with the efficient centering

Proposition 15.5, page 210 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: proved.

Statement. Let $\Omega=[0,1]^d$ be the torus, $T>0$, $\mathcal X=[0,T]\times\Omega$, and let $\mathscr{G}(\theta)=u_\theta$ be the solution map of an evolution equation with initial condition $\theta$ and values in $W$. The data are $Z^{(N)}=(Y_i,X_i)_{i\le N}$ with $Y_i=\mathscr{G}(\theta)(X_i)+\varepsilon_i$, $X_i$ i.i.d. uniform on $\mathcal X$ and $\varepsilon_i\sim N(0,I_W)$ independent. Let $(e_j)$ be the orthonormal Laplace eigenbasis of mean zero functions, with eigenvalues $\lambda_j\asymp j^{2/d}$; let the prior $\Pi$ be the law of $(\sqrt N\delta_N)^{-1}\sum_j\lambda_j^{-\gamma/2}g_je_j$ with $g_j$ i.i.d. $N(0,1)$ and $\delta_N=N^{-\gamma/(2\gamma+d)}$, and $\Pi_N=\Pi(\cdot\mid Z^{(N)})$ the posterior; let $\theta_0$ be the true initial condition, $P^N_{\theta_0}$ the law of the data, $\mathbb{I}_\vartheta$ the linearization of $\mathscr{G}$ at $\vartheta$, $\mathcal{N}_\vartheta=N(0,T(\mathbb{I}_\vartheta^*\mathbb{I}_\vartheta)^{-1})$, $J_N\asymp N\delta_N^2$ and $p_N$ the projection onto $\operatorname{span}\{e_j:j\le J_N\}$.

Suppose Conditions 1 and 2 of Nickl (2024) hold with integer $\gamma>\max(3\zeta+3d/2+2,\eta_0)$ and $k>\max(\zeta+5d/2,\eta_0)$ as in his Bernstein von Mises theorem ($\eta_0$ the index of his invertibility condition), that is, the prior above with Sobolev reproducing kernel space $H^\gamma$ and, for the forward map on balls of $H^{\bar\gamma}$, uniform $L^\infty$ bounds, $L^2$ Lipschitz continuity, a linearization at $\theta_0$ with quadratic remainder, $L^\infty$ mapping properties from $H^\zeta$ with $\zeta>d/2$, the stability estimate $\|\mathscr{G}(\theta)-\mathscr{G}(\theta_0)\|_{L^2(\mathcal X)}\ge c\|\theta-\theta_0\|_{H^{-1}}$ and an invertible information operator ($\bar\gamma$ is the Sobolev index of the localization ball, $\max(2,2\zeta)<\bar\gamma<\gamma-\max(1,d/2)$). Let $\kappa$ satisfy $2d+\zeta<\kappa<k-d/2$.

The one step efficient score summary is defined by cross fitting. The sample is split into two halves with index sets $\mathcal I_1,\mathcal I_2$ of sizes differing by at most one. For $b=1,2$ a preliminary estimate $\bar\theta^{[b]}_N$ is computed from half $b$ alone, takes values in the parameter space and satisfies $\|\bar\theta^{[b]}_N-\theta_0\|_{H^\xi}=O_P(\tilde\delta_N(\xi))$ for $0\le\xi\le\bar\gamma$, where $\tilde\delta_N(\xi)=\delta_N^{(\bar\gamma-\xi)/(\bar\gamma+1)}$. With $\bar e_j^{\,\vartheta}=T(\mathbb{I}_\vartheta^*\mathbb{I}_\vartheta)^{-1}e_j$, put for $j\le J_N$ $S_{N,j}=\frac12\sum_{b=1,2}\big[\langle e_j,\bar\theta^{[b]}_N\rangle+\frac1{|\mathcal I_{3-b}|}\sum_{i\in\mathcal I_{3-b}}\langle\mathbb{I}_{\bar\theta^{[b]}_N}p_N(\bar e_j^{\,\bar\theta^{[b]}_N})(X_i),\,Y_i-u_{\bar\theta^{[b]}_N}(X_i)\rangle_W\big]$ and $\hat S^{J_N}_N=\sum_{j\le J_N}S_{N,j}e_j$. The efficient centering of Nickl's proof is $\hat\theta_N=\sum_{j\ge1}\hat\Psi_{N,j}e_j$ with $\hat\Psi_{N,j}=\langle e_j,\theta_0\rangle+\frac1N\sum_{i=1}^N\langle\mathbb{I}_{\theta_0}p_N(\bar e_j^{\,\theta_0})(X_i),\varepsilon_i\rangle_W$.

Suppose further that $\sqrt N\,\tilde\delta_N(0)\tilde\delta_N(\zeta)\to0$; that $\gamma<(\bar\gamma+1)(\kappa-d/2)$ unless $\mathbb{I}^*_{\theta_0}\mathbb{I}_{\theta_0}$ is diagonal in $(e_j)$ or the preliminary estimates converge at the rate $\delta_N$ in $H^{-1}$; and that the weights depend on the linearization point in a Lipschitz way: for every $B>0$ there is $L=L(B)$ such that for all $\vartheta$ with $\|\vartheta\|_{H^{\bar\gamma}}\le B$ and all $j\le J_N$, $\|\mathbb{I}_\vartheta p_N(\bar e_j^{\,\vartheta})-\mathbb{I}_{\theta_0}p_N(\bar e_j^{\,\theta_0})\|_{L^2(\mathcal X)}\le L\,\|\vartheta-\theta_0\|_{H^\zeta}\|e_j\|_{H^{\kappa+2}}$. Then $\sqrt N\,\|\hat S^{J_N}_N-\hat\theta_N\|_{H^{-k-2}}\to0$ in $P^N_{\theta_0}$ probability, and consequently $\mathscr{W}_1\big(\operatorname{Law}(\sqrt N(\theta-\hat S^{J_N}_N)\mid Z^{(N)}),\mathcal{N}_{\theta_0}\big)\to0$ in $P^N_{\theta_0}$ probability, where $\mathscr{W}_1$ is the Wasserstein distance of order one on $H^{-k-2}$.

Source: [`source/chapters/ext/m2a.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m2a.tex), label `m:prop:suff`.

<a id="the_summary_in_sobolev_norms"></a>

#### The one step summary in Sobolev norms

Proposition 15.6, page 213 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: proved.

Statement. In Nickl's framework, for the cross fitted one step efficient score summary of the book (torus $\Omega=[0,1]^d$, data $Y_i=\mathscr{G}(\theta_0)(X_i)+\varepsilon_i$ at the true initial condition $\theta_0$ with $X_i$ i.i.d. uniform on $\mathcal X=[0,T]\times\Omega$ and $\varepsilon_i\sim N(0,I_W)$, orthonormal Laplace eigenbasis $(e_j)$ with eigenvalues $\lambda_j\asymp j^{2/d}$, rescaled Gaussian series prior with exponent $\gamma$ and $\delta_N=N^{-\gamma/(2\gamma+d)}$, $J_N\asymp N\delta_N^2$, $p_N$ the projection onto the first $J_N$ modes, $\mathbb{I}_\vartheta$ the linearization of $\mathscr{G}$ at $\vartheta$, $\tilde\delta_N(\xi)=\delta_N^{(\bar\gamma-\xi)/(\bar\gamma+1)}$), suppose that Conditions 1 and 2 of Nickl (2024) hold (the prior and, for the forward map on balls of $H^{\bar\gamma}$, uniform bounds, a linearization at $\theta_0$ with quadratic remainder, the stability estimate $\|\mathscr{G}(\theta)-\mathscr{G}(\theta_0)\|_{L^2(\mathcal X)}\ge c\|\theta-\theta_0\|_{H^{-1}}$ and an invertible information operator). Suppose that for every $B>0$ there are constants $0<c_B\le C_B<\infty$ such that for every $\vartheta$ in the parameter space with $\|\vartheta\|_{H^{\bar\gamma}}\le B$, $c_B\|h\|_{H^{-1}}\le\|\mathbb{I}_\vartheta h\|_{L^2(\mathcal X)}\le C_B\|h\|_{H^{-1}}$ for all $h\in L^2_0(\Omega)$ (with $\dot H^{-1}_\diamond$ and $\dot H_\diamond$ in place of $H^{-1}$ and $L^2_0(\Omega)$ for the Stokes and Navier Stokes equations), and that the preliminary estimates $\bar\theta^{[b]}_N$ of the cross fitted one step summary (each computed from one half sample alone, with values in the parameter space and $\|\bar\theta^{[b]}_N-\theta_0\|_{H^\xi}=O_P(\tilde\delta_N(\xi))$ for $0\le\xi\le\bar\gamma$) satisfy $\|\bar\theta^{[b]}_N-\theta_0\|_{H^{-1}}=O_P(\delta_N)$ for $b=1,2$. Then the projected one step statistic $\hat S^{J_N}_N$ satisfies $\|\hat S^{J_N}_N-\theta_0\|_{H^s}=O_P\big(N^{(s+1-\gamma)/(2\gamma+d)}\big)$ for every $-1\le s\le\gamma$. If moreover $\bar\gamma<\gamma-1$, then $\|\hat S^{J_N}_N-\theta_0\|_{L^2}=o_P(\tilde\delta_N(0))$ and $\|\hat S^{J_N}_N-\theta_0\|_{H^{\bar\gamma}}=o_P(1)$. For a linear forward map whose information operator is diagonal in $(e_j)$, as for the heat and Stokes equations, the same conclusions hold without the rate in $H^{-1}$.

Source: [`source/chapters/ext/m2a.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m2a.tex), label `m:prop:sumrate`.

<a id="preliminary_estimates_rate_in_h_minus_one"></a>

#### Preliminary estimates with the rate in $H^{-1}$

Lemma 15.7, page 215 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: proved.

Statement. In Nickl's framework (data $Y_i=\mathscr{G}(\theta_0)(X_i)+\varepsilon_i$ at the true initial condition $\theta_0$ on $\mathcal X=[0,T]\times\Omega$ with uniform design and standard Gaussian noise, rescaled Gaussian series prior with exponent $\gamma$ and $\delta_N=N^{-\gamma/(2\gamma+d)}$, $\tilde\delta_N(\xi)=\delta_N^{(\bar\gamma-\xi)/(\bar\gamma+1)}$), suppose that Conditions 1 and 2 of Nickl (2024) hold with $\gamma$ and $k$ as in his Bernstein von Mises theorem, and that $\bar\gamma<\gamma-d/2$. Let $\bar\theta^{[b]}_N$ be computed from the half sample $Z^{[b]}$ alone, with values in the parameter space and $\|\bar\theta^{[b]}_N\|_{H^{\bar\gamma}}=O_P(1)$. If $\|u_{\bar\theta^{[b]}_N}-u_{\theta_0}\|_{L^2(\mathcal X)}=O_P(\delta_N)$, then $\|\bar\theta^{[b]}_N-\theta_0\|_{H^{-1}}=O_P(\delta_N)$, and this rate in $H^{-1}$ implies $\|\bar\theta^{[b]}_N-\theta_0\|_{H^\xi}=O_P(\tilde\delta_N(\xi))$ for every $-1\le\xi\le\bar\gamma$. The posterior mean computed from $Z^{[b]}$ with the prior at the sample size of that half satisfies the rate in $H^{-1}$ and these rates; for the two dimensional Navier Stokes equations this holds in the setting of Theorem 2.11 of Konen and Nickl (2026) when $\bar\gamma\le11$.

Source: [`source/chapters/ext/m2a.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m2a.tex), label `m:lem:halfmean`.

<a id="summary_sobolev_rate_under_centering_hypotheses"></a>

#### Sobolev rates of the one step summary under the efficient centering hypotheses

Corollary 15.9, page 217 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: proved.

Statement. Assume all hypotheses of the equivalence of the one step efficient score summary $\hat S^{J_N}_N$ with the efficient centering $\hat\theta_N$ (catalog entry equivalence_with_the_efficient_centering): Conditions 1 and 2 of Nickl (2024) with $\gamma$ and $k$ as in his Bernstein von Mises theorem; $2d+\zeta<\kappa<k-d/2$; $\sqrt N\,\tilde\delta_N(0)\tilde\delta_N(\zeta)\to0$ with $\tilde\delta_N(\xi)=\delta_N^{(\bar\gamma-\xi)/(\bar\gamma+1)}$ and $\delta_N=N^{-\gamma/(2\gamma+d)}$; $\gamma<(\bar\gamma+1)(\kappa-d/2)$ unless $\mathbb{I}^*_{\theta_0}\mathbb{I}_{\theta_0}$ is diagonal in the Laplace eigenbasis $(e_j)$ or the preliminary estimates converge at the rate $\delta_N$ in $H^{-1}$; and the Lipschitz dependence of the weights on the linearization point, $\|\mathbb{I}_\vartheta p_N(\bar e_j^{\,\vartheta})-\mathbb{I}_{\theta_0}p_N(\bar e_j^{\,\theta_0})\|_{L^2(\mathcal X)}\le L(B)\|\vartheta-\theta_0\|_{H^\zeta}\|e_j\|_{H^{\kappa+2}}$ for all $\|\vartheta\|_{H^{\bar\gamma}}\le B$ and $j\le J_N$, where $\bar e_j^{\,\vartheta}=T(\mathbb{I}_\vartheta^*\mathbb{I}_\vartheta)^{-1}e_j$. Then for every $-1\le s\le\gamma$, $\|\hat S^{J_N}_N-\theta_0\|_{H^s}=O_P\big(N^{(s+1-\gamma)/(2\gamma+d)}\big)+o_P\big(N^{(s+k+2)/(2\gamma+d)-1/2}\big)$.

Source: [`source/chapters/ext/m2a.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m2a.tex), label `m:cor:sumsuff`.

<a id="the_information_operator_of_the_reaction_diffusion_class"></a>

#### The information operator of the reaction diffusion class

Lemma 15.11, page 219 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: proved.

Statement. Consider the reaction diffusion equation $\partial_tu-\Delta u=f(u)$, $u(0)=\theta$, on the torus $\Omega=[0,1]^d$ with $f\in C_c^\infty(\mathbb{R})$ and $d\le3$ (the class of Theorem 1 of Nickl (2024)), with smooth true initial condition $\theta_0$, $\zeta>d/2$ an index for which his Condition 2D holds, solution map $\mathscr{G}$, linearization $\mathbb{I}_\vartheta$ at $\vartheta$, parameter space the Sobolev space $H^{\bar\gamma}$ with $\bar\gamma>3+d/2$ (Theorem 5 of Nickl (2024) verifies his Condition 2 for this class), and $\mathcal X=[0,T]\times\Omega$. Let $\mathcal{L}$ be the solution operator of the heat equation $\partial_tu=\Delta u$ and $\mathcal{K}_\vartheta=\mathbb{I}_\vartheta^*\mathbb{I}_\vartheta-\mathcal{L}^*\mathcal{L}$, both compressed to $L^2_0(\Omega)$. For every $B>0$ there is a constant $C$, depending on $B$, $f$, $T$ and $d$, such that for all $\vartheta$ and $\vartheta+h$ with $H^{\bar\gamma}$ norms at most $B$: (i) $|\langle\mathcal{K}_\vartheta\phi,\psi\rangle|\le C\|\phi\|_{H^{-1}}\|\psi\|_{H^{-3}}$ for $\phi,\psi\in L^2_0(\Omega)$, so that the symmetric operator $\mathcal{K}_\vartheta$ extends to maps from $H^{-1}_0$ to $H^3_0$ and from $H^{-3}_0$ to $H^1_0$ with norms at most $C$; (ii) $\|\mathscr{G}(\vartheta+h)-\mathscr{G}(\vartheta)-\mathbb{I}_\vartheta h\|_{L^2(\mathcal X)}\le C\|h\|_{L^2}^2$; (iii) the weights of the one step summary satisfy the Lipschitz condition $\|\mathbb{I}_\vartheta p_N(\bar e_j^{\,\vartheta})-\mathbb{I}_{\theta_0}p_N(\bar e_j^{\,\theta_0})\|_{L^2(\mathcal X)}\le L\,\|\vartheta-\theta_0\|_{H^\zeta}\|e_j\|_{H^{\kappa+2}}$ for every $\kappa\ge-1$, with $\bar e_j^{\,\vartheta}=T(\mathbb{I}_\vartheta^*\mathbb{I}_\vartheta)^{-1}e_j$, $p_N$ the projection onto the first $J_N$ Laplace eigenfunctions $e_j$, and $L$ depending on $B$.

Source: [`source/chapters/ext/m2a.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m2a.tex), label `m:lem:rdinfo`.

<a id="the_summary_in_sobolev_norms_reaction_diffusion"></a>

#### The one step summary in Sobolev norms: reaction diffusion

Proposition 15.12, page 219 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: proved.

Statement. In the setting of the information operator lemma for the reaction diffusion class (the equation $\partial_tu-\Delta u=f(u)$ with $f\in C_c^\infty(\mathbb{R})$, $d\le3$, parameter space $H^{\bar\gamma}$ with $\bar\gamma>3+d/2$, Conditions 1 and 2 of Nickl (2024) as verified in his Theorem 5, integer exponent $\gamma>2+3d$ of the rescaled Gaussian series prior, smooth true initial condition $\theta_0$, $\delta_N=N^{-\gamma/(2\gamma+d)}$, $J_N\asymp N\delta_N^2$) let $\bar\gamma<\gamma-1$. Then for every choice of the preliminary estimates that the definition of the cross fitted one step summary allows (computed on each half sample, with values in the parameter space and $\|\bar\theta^{[b]}_N-\theta_0\|_{H^\xi}=O_P(\tilde\delta_N(\xi))$ for $0\le\xi\le\bar\gamma$, $\tilde\delta_N(\xi)=\delta_N^{(\bar\gamma-\xi)/(\bar\gamma+1)}$), the projected one step statistic satisfies $\|\hat S^{J_N}_N-\theta_0\|_{L^2}=o_P(\tilde\delta_N(0))$ and $\|\hat S^{J_N}_N-\theta_0\|_{H^{\bar\gamma}}=o_P(1)$.

Source: [`source/chapters/ext/m2a.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m2a.tex), label `m:prop:sumrd`.

<a id="the_regularized_summary_on_modes_heat_and_stokes"></a>

#### The regularized summary on $J_N$ modes: heat and Stokes

Proposition 15.13, page 220 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: proved.

Statement. Let $\mathscr{G}$ be the solution map of the heat equation $\partial_tu=\nu\Delta u$ on $\mathbb{T}^d$, with $W=\mathbb{R}$, or of the Stokes equations on $\mathbb{T}^2$, with $W=\mathbb{R}^2$ and $d=2$, and let $(e_j)$ be a real orthonormal eigenbasis of the mean zero functions, respectively of the divergence free mean zero fields, with $\sup_x|e_j(x)|_W\le\sqrt2$, as for the trigonometric basis; thus $s_j(t)=e^{-\nu\lambda_jt}$ and $\lambda_j\asymp j^{2/d}$. The data are $Z^{(N)}=(Y_i,X_i)_{i\le N}$ with $Y_i=\mathscr{G}(\theta_0)(X_i)+\varepsilon_i$, $X_i=(t_i,x_i)$ i.i.d. uniform on $[0,T]\times\mathbb{T}^d$ and $\varepsilon_i\sim N(0,I_W)$, where $\theta_0\in H^\gamma$ lies in the closed span of $(e_j)$ and $\gamma>d+1$ is the exponent of the prior $\Pi$, the law of $(\sqrt N\delta_N)^{-1}\sum_j\lambda_j^{-\gamma/2}g_je_j$ with $g_j$ i.i.d. $N(0,1)$ and $\delta_N=N^{-\gamma/(2\gamma+d)}$; let $k>d/2$, $J_N\asymp N\delta_N^2$ and $\iota_j=\frac1T\int_0^Ts_j(t)^2\,\mathrm{d}t$. Retain $D=D_N$ modes and give their coefficients the truncation of the prior, $N(0,\Sigma_0)$ with $\Sigma_0=\operatorname{diag}(\sigma_{0,j}^2)_{j\le D}$ and $\sigma_{0,j}^2=\lambda_j^{-\gamma}/(N\delta_N^2)$; write $\Pi^D(\cdot\mid Z^{(N)})$ for the resulting posterior and $\Phi$ for the $N\times D$ design matrix with entries $s_j(t_i)e_j(x_i)$ (a pair of rows per observation for Stokes). Suppose that $D_N\to\infty$, $\delta_N^2D_N^{2+2/d}\to0$ and $ND_N^{-2(k+2+\gamma)/d}\to0$, which holds for $D_N\asymp J_N$. Let $\hat S^{\rm reg}_N$ be the regularized one step summary computed on the $D$ retained modes from a pilot $\bar\theta_N$ in their span, which may depend on the data in any way: $\hat S^{\rm reg}_N=\bar\theta_N+(F_N+\Sigma_0^{-1})^{-1}\big(\Phi^\top(Y-\Phi\bar\theta_N)-\Sigma_0^{-1}\bar\theta_N\big)$ with $F_N=\Phi^\top\Phi$, which equals $(\Phi^\top\Phi+\Sigma_0^{-1})^{-1}\Phi^\top Y$, the posterior mean under the truncated prior, for every pilot. Let $\hat\theta_N=\theta_0+\sum_{j\le J_N}\xi_je_j$ with $\xi_j=(N\iota_j)^{-1}\sum_{i\le N}s_j(t_i)\langle e_j(x_i),\varepsilon_i\rangle_W$ be the efficient centering of Nickl (2024) for these equations, $\mathcal{N}_{\theta_0}$ the Gaussian law with covariance $\operatorname{diag}(1/\iota_j)$ in the basis $(e_j)$, and $\mathscr{W}_1$ the Wasserstein distance of order one on $H^{-k-2}$. Then, in $P^N_{\theta_0}$ probability where convergence in probability is meant:

(i) $\sqrt N\|\hat S^{\rm reg}_N-\hat\theta_N\|_{H^{-k-2}}\to0$ in probability; (ii) $\mathscr{W}_1\big(\operatorname{Law}(\sqrt N(\theta-\hat S^{\rm reg}_N)\mid Z^{(N)}),\mathcal{N}_{\theta_0}\big)\to0$ in probability for $\theta\sim\Pi^D(\cdot\mid Z^{(N)})$; (iii) $\sqrt N(\hat S^{\rm reg}_N-\theta_0)\to\mathcal{N}_{\theta_0}$ in distribution in $H^{-k-2}$; (iv) for the heat equation with integer $\gamma>3d+2$ and $k>3d$, Nickl's Bernstein von Mises theorem applies, (ii) holds also for $\theta$ drawn from the posterior $\Pi_N$ under the untruncated prior, and the mean $\tilde\theta_N$ of $\Pi_N$ satisfies $\sqrt N\|\hat S^{\rm reg}_N-\tilde\theta_N\|_{H^{-k-2}}\to0$ in probability; (v) for the heat equation, whenever the hypotheses of the equivalence of the cross fitted one step summary $\hat S^{J_N}_N$ with the efficient centering hold (catalog entry equivalence_with_the_efficient_centering), $\sqrt N\|\hat S^{\rm reg}_N-\hat S^{J_N}_N\|_{H^{-k-2}}\to0$ in probability.

Source: [`source/chapters/ext/m2a.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m2a.tex), label `m:prop:regheat`.

<a id="regularized_summary_fixed_prior_untruncated_posteriors"></a>

#### The regularized summary under a fixed prior, and the untruncated posteriors

Proposition 15.14, page 225 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: proved.

Statement. Let the setting be that of the regularized summary on $D=D_N$ modes for the heat equation $\partial_tu=\nu\Delta u$ on $\mathbb{T}^d$ ($W=\mathbb{R}$) or the Stokes equations on $\mathbb{T}^2$ ($W=\mathbb{R}^2$, $d=2$): $(e_j)$ a real orthonormal eigenbasis of the mean zero functions, respectively divergence free mean zero fields, with $\sup_x|e_j(x)|_W\le\sqrt2$; $s_j(t)=e^{-\nu\lambda_jt}$; data $Y_i=\mathscr{G}(\theta_0)(X_i)+\varepsilon_i$ with $X_i$ i.i.d. uniform on $[0,T]\times\mathbb{T}^d$ and $\varepsilon_i\sim N(0,I_W)$; $\iota_j=\frac1T\int_0^Ts_j(t)^2\,\mathrm{d}t$; $\hat S^{\rm reg}_N=(\Phi^\top\Phi+\Sigma_0^{-1})^{-1}\Phi^\top Y$ the regularized summary (posterior mean under the truncated prior) with $\Phi_{ij}=s_j(t_i)e_j(x_i)$; $\hat\theta_N=\theta_0+\sum_{j\le J_N}\xi_je_j$ with $\xi_j=(N\iota_j)^{-1}\sum_is_j(t_i)\langle e_j(x_i),\varepsilon_i\rangle_W$ the efficient centering; $\mathscr{W}_1$ the Wasserstein distance of order one on $H^{-k-2}$; $\mathcal{N}_{\theta_0}$ the Gaussian law with covariance $\operatorname{diag}(1/\iota_j)$. Take now $\theta_0\in H^\beta$ in the closed span of $(e_j)$ with $\beta>d/2$, $k>d/2-1$, and give the $D=D_N$ retained coefficients the fixed prior $\sigma_{0,j}^2=\rho^2\lambda_j^{-\alpha}$ with $\rho>0$ and $\alpha>d/2$ (not rescaled with $N$). Suppose that $\beta\ge\alpha-k-1$, that $D_N\to\infty$ with $\sup_NND_N^{-2(k+2+\beta)/d}<\infty$ (a condition void when $\theta_0$ has finitely many nonzero coefficients), and that $\alpha>d$ or $D_N^{2+2/d}/N\to0$, and form the centering $\hat\theta_N$ with the first $J_N$ modes, for any $J_N\to\infty$. Then (i) $\sqrt N\|\hat S^{\rm reg}_N-\hat\theta_N\|_{H^{-k-2}}\to0$ in probability, (ii) $\mathscr{W}_1(\operatorname{Law}(\sqrt N(\theta-\hat S^{\rm reg}_N)\mid Z^{(N)}),\mathcal{N}_{\theta_0})\to0$ in probability for $\theta$ drawn from the posterior under the truncated prior, (iii) $\sqrt N(\hat S^{\rm reg}_N-\theta_0)\to\mathcal{N}_{\theta_0}$ in distribution in $H^{-k-2}$, and (v) for the heat equation, $\sqrt N\|\hat S^{\rm reg}_N-\hat S^{J_N}_N\|_{H^{-k-2}}\to0$ in probability whenever the hypotheses of the equivalence of the cross fitted one step summary $\hat S^{J_N}_N$ with the efficient centering hold. If $\alpha>d$, (i) to (iii) hold also for $D=\infty$, that is, under the untruncated prior.

For the rescaled prior $\sigma_{0,j}^2=\lambda_j^{-\gamma}/(N\delta_N^2)$, $\delta_N=N^{-\gamma/(2\gamma+d)}$, $\gamma>d+1$, of the regularized summary on $J_N$ modes (catalog entry the_regularized_summary_on_modes_heat_and_stokes), the conclusions of that statement hold without its condition $\delta_N^2D_N^{2+2/d}\to0$, and its claims (i) to (iii) hold also for $D=\infty$, that is, for the posterior $\Pi_N$ under the untruncated rescaled prior and its mean $\tilde\theta_N$. Hence the last two claims of its part (iv) (that (ii) holds for $\theta$ drawn from $\Pi_N$ and that $\sqrt N\|\hat S^{\rm reg}_N-\tilde\theta_N\|_{H^{-k-2}}\to0$ in probability) hold for the Stokes equations as well, and for the heat equation without its restrictions on $\gamma$ and $k$; and when $\theta_0$ meets both sets of hypotheses, the regularized summaries under the two priors, and if $\alpha>d$ the untruncated posterior means, are $\sqrt N$ equivalent in $H^{-k-2}$.

Source: [`source/chapters/ext/m2a.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m2a.tex), label `m:prop:regfixed`.

<a id="the_regularized_summary_on_modes_reaction_diffusion"></a>

#### The regularized summary on $J_N$ modes: reaction diffusion

Proposition 15.16, page 228 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: proved.

Statement. Consider the reaction diffusion equation $\partial_tu-\Delta u=f(u)$, $u(0)=\theta$, on the torus $\Omega=[0,1]^d$ with $f\in C_c^\infty(\mathbb{R})$ and $d\le3$ (the class of Theorem 1 of Nickl (2024)), with the rescaled Gaussian series prior $\Pi$ of integer exponent $\gamma>2+3d$ ($\delta_N=N^{-\gamma/(2\gamma+d)}$, $J_N\asymp N\delta_N^2$), smooth true initial condition $\theta_0$, parameter space $H^{\bar\gamma}$ with $\bar\gamma>3+d/2$, and let $k>3d$, so that Theorem 5 of Nickl (2024) gives Conditions 1 and 2 with $\gamma$ and $k$ as in his Bernstein von Mises theorem. Retain $D=J_N$ modes with the truncated prior $\Sigma_0=\operatorname{diag}(\sigma_{0,j}^2)_{j\le J_N}$, $\sigma_{0,j}^2=\lambda_j^{-\gamma}/(N\delta_N^2)$. The sample is split into halves with index sets $\mathcal I_1,\mathcal I_2$; let the preliminary estimates $\bar\theta^{[b]}_N$ (computed from half $b$, with the rates of the cross fitted one step summary) lie in the span of $e_1,\dots,e_{J_N}$, as their projections do with the same rates. For $b=1,2$ let $\hat S^{{\rm reg},b}_N=\bar\theta^{[b]}_N+(F^b_N+\Sigma_0^{-1})^{-1}\big(\mathbb{I}^*_{\bar\theta^{[b]}_N}[\sum_{i\in\mathcal I_{3-b}}r_i\,\delta_{X_i}]-\Sigma_0^{-1}\bar\theta^{[b]}_N\big)$ with residuals $r_i=Y_i-u_{\bar\theta^{[b]}_N}(X_i)$ and $F^b_N$ the realized information $\mathbb{I}^*_{\bar\theta^{[b]}_N}\mathbb{I}_{\bar\theta^{[b]}_N}$ on the design points $X_i$, $i\in\mathcal I_{3-b}$, compressed to the retained modes, and put $\hat S^{\rm reg}_N=\frac12(\hat S^{{\rm reg},1}_N+\hat S^{{\rm reg},2}_N)$. Let $\hat\theta_N$ be the efficient centering of Nickl's proof, $\mathcal{N}_{\theta_0}=N(0,T(\mathbb{I}_{\theta_0}^*\mathbb{I}_{\theta_0})^{-1})$, $\Pi_N$ the posterior, $\tilde\theta_N$ its mean and $\mathscr{W}_1$ the Wasserstein distance of order one on $H^{-k-2}$. Then, in $P^N_{\theta_0}$ probability: (i) $\sqrt N\|\hat S^{\rm reg}_N-\hat\theta_N\|_{H^{-k-2}}\to0$; (ii) $\mathscr{W}_1(\operatorname{Law}(\sqrt N(\theta-\hat S^{\rm reg}_N)\mid Z^{(N)}),\mathcal{N}_{\theta_0})\to0$ for $\theta\sim\Pi_N$, the mean $\tilde\theta_N$ satisfies $\sqrt N\|\hat S^{\rm reg}_N-\tilde\theta_N\|_{H^{-k-2}}\to0$, and $\sqrt N(\hat S^{\rm reg}_N-\theta_0)\to\mathcal{N}_{\theta_0}$ in distribution in $H^{-k-2}$; (iii) under the hypotheses of the equivalence of the cross fitted one step summary $\hat S^{J_N}_N$ with the efficient centering other than the Lipschitz condition on the weights (which the information operator lemma for this class supplies), $\sqrt N\|\hat S^{\rm reg}_N-\hat S^{J_N}_N\|_{H^{-k-2}}\to0$.

Source: [`source/chapters/ext/m2a.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m2a.tex), label `m:prop:regrd`.

<a id="expected_utility_form_of_the_bernstein_von_mises_limit"></a>

#### Expected utility form of the Bernstein von Mises limit

Proposition 15.18, page 231 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: proved.

Statement. For the heat or the Stokes equation on the torus, with semigroup eigenvalues $s_j(t)=e^{-\nu\lambda_jt}$ in the Laplace eigenbasis $(e_j)$ ($\lambda_j\asymp j^{2/d}$), data $Y_i=\mathscr{G}(\theta)(X_i)+\varepsilon_i$ with $X_i$ i.i.d. uniform on $[0,T]\times\Omega$ and $\varepsilon_i\sim N(0,I_W)$, and per mode information $\iota_j=\frac1T\int_0^Ts_j(t)^2\,\mathrm{d}t$, consider the first $J$ modes with prior $\Pi^J=N(0,\Sigma_0)$, $\Sigma_0=\operatorname{diag}(\sigma_{0,j}^2)_{j\le J}$, in the Gaussian experiment that observes $\theta_j+(N\iota_j)^{-1/2}\xi_j$, $j\le J$, with independent standard normal $\xi_j$. Its information matrix is $\operatorname{diag}(N\iota_j)$, the population value of the Gram matrix $\Phi^\top\Phi$ of the design, and it is the $J$ mode experiment of the Bernstein von Mises limit, whose covariance is $T(\mathbb{I}^*\mathbb{I})^{-1}/N=\operatorname{diag}(1/(N\iota_j))$, where $\mathbb{I}$ is the forward map of the equation, which is linear. Write $\kappa_j=N\iota_j\sigma_{0,j}^2$ for the per mode ratio of information to prior precision, and let $I_N=\mathbb{E}^\Pi\big[\log\frac{\mathrm{d}\Pi^J(\cdot\mid Z^{(N)})}{\mathrm{d}\Pi^J}\,\big|\,Z^{(N)}\big]$ be the realized information gain, with $\Pi^J(\cdot\mid Z^{(N)})$ the posterior and $\tilde\theta^J_N$ the posterior mean. Then for every $N$ and $J$, $I_N=\frac12\sum_{j\le J}\big[\log(1+\kappa_j)-\frac{\kappa_j}{1+\kappa_j}\big]+\frac12\tilde\theta_N^{J\top}\Sigma_0^{-1}\tilde\theta^J_N$, and averaging over the prior predictive law gives the Lindley expected information gain $\mathbf{E}\,I_N=\frac12\log\det\big(\mathrm{Id}+\frac NT\mathbb{I}^*\mathbb{I}\,\Sigma_0\big)=\frac12\sum_{j\le J}\log(1+\kappa_j)$. In the linear model with $D=J$ modes, that is, with the realized information $\Phi^\top\Phi$ in place of $\operatorname{diag}(N\iota_j)$, both identities hold conditionally on the design, with the $\kappa_j$ replaced by the eigenvalues of $\Sigma_0^{1/2}\Phi^\top\Phi\,\Sigma_0^{1/2}$. Every mode contributes the strictly positive amount $\frac12\log(1+\kappa_j)$, and every mode has posterior variance $\sigma_{0,j}^2/(1+\kappa_j)$ strictly below its prior variance; the modes with $\kappa_j>1$ are those whose posterior variance falls below half the prior variance. Under the rescaled prior $\sigma_{0,j}^2=\lambda_j^{-\gamma}/(N\delta_N^2)$ with $\delta_N=N^{-\gamma/(2\gamma+d)}$ and $J=J_N\asymp N\delta_N^2$, the number of these is $J^{\rm eff}_N=\#\{j\le J_N:\kappa_j>1\}\asymp N^{\gamma d/((\gamma+1)(2\gamma+d))}=J_N^{\gamma/(\gamma+1)}=o(J_N)$, so the experiment is informative in every retained mode, but strongly informative in only a vanishing fraction of them.

Source: [`source/chapters/ext/m2a.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m2a.tex), label `m:prop:pr`.

<a id="exact_identities_for_any_forward_map"></a>

#### Exact identities for the information gain under any forward map

Lemma 15.21, page 233 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: proved.

Statement. Let $\mathscr{G}$ be a measurable forward map in the model $Y_i=\mathscr{G}(\theta)(X_i)+\varepsilon_i$ (design $X_i$ i.i.d. uniform on $\mathcal X=[0,T]\times\Omega$, noise $\varepsilon_i\sim N(0,I_W)$), and let the prior be a centered Gaussian measure under which the coordinates $\langle\theta,e_j\rangle$ in an orthonormal basis $(e_j)$ are independent with variances $\sigma_{0,j}^2>0$. For a number $J$ of modes let $\theta^J=(\langle\theta,e_j\rangle)_{j\le J}$, let $\Pi^J$ and $\Pi^J(\cdot\mid Z^{(N)})$ be its prior and posterior laws, $\Sigma^J_0=\operatorname{diag}(\sigma_{0,j}^2)_{j\le J}$, $m_N$ and $V_N$ the posterior mean and covariance of $\theta^J$, $I_N=\mathrm{KL}\big(\Pi^J(\cdot\mid Z^{(N)})\,\|\,\Pi^J\big)$ the realized information gain, $\mathbf{P}$ the prior predictive law (parameter $\vartheta\sim\Pi$, then data $Z^{(N)}\sim P^N_\vartheta$) and $\mathbf{E}$ its expectation. Then for every $N$ and $J$: (i) almost surely $I_N=\mathrm{KL}\big(N(m_N,V_N)\,\|\,\Pi^J\big)+\Gamma_N$, where $\Gamma_N=\mathrm{KL}\big(\Pi^J(\cdot\mid Z^{(N)})\,\|\,N(m_N,V_N)\big)\ge0$, and $\Gamma_N\le\mathrm{KL}\big(\Pi^J(\cdot\mid Z^{(N)})\,\|\,G\big)$ for every nondegenerate Gaussian law $G$ on $\mathbb{R}^J$; (ii) if $\int\|\mathscr{G}(\vartheta)\|^2_{L^\infty(\mathcal X)}\,\mathrm{d}\Pi(\vartheta)<\infty$, then $\mathbf{E}\,I_N=I(\theta^J;Z^{(N)})<\infty$ (the mutual information) and $\mathbf{E}\,I_N=\frac12\,\mathbf{E}\log\det\big(\Sigma^J_0V_N^{-1}\big)+\mathbf{E}\,\Gamma_N$. In the linear Gaussian models of the heat and Stokes equations the posterior is $N(m_N,V)$ with $V$ not depending on the data, so $\Gamma_N=0$ and (i) and (ii) reduce to the two displays of the expected utility form of the Bernstein von Mises limit.

Source: [`source/chapters/ext/m2a.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m2a.tex), label `m:lem:prexact`.

<a id="kullback_leibler_form_of_the_bernstein_von_mises_theorem"></a>

#### Kullback Leibler form of the Bernstein von Mises theorem

Theorem 15.22, page 234 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: proved.

Statement. In Nickl's framework (torus $\Omega=[0,1]^d$, data $Y_i=\mathscr{G}(\theta)(X_i)+\varepsilon_i$ with $X_i$ i.i.d. uniform on $\mathcal X=[0,T]\times\Omega$ and $\varepsilon_i\sim N(0,I_W)$, rescaled Gaussian series prior $\Pi$ with exponent $\gamma$ and $\delta_N=N^{-\gamma/(2\gamma+d)}$, true initial condition $\theta_0$, linearization $\mathbb{I}_{\theta_0}$ of $\mathscr{G}$ at $\theta_0$), assume the hypotheses of Nickl's Bernstein von Mises theorem (Conditions 1 and 2 of Nickl (2024) with $\gamma$ and $k$ as in his Theorem 2). Let $\mathscr{G}_{\rm lin}(\theta)=\mathscr{G}(\theta_0)+\mathbb{I}_{\theta_0}[\theta-\theta_0]$ and let $\Pi_{\rm lin}(\cdot\mid Z^{(N)})$ be the posterior in the model with $\mathscr{G}_{\rm lin}$ in place of $\mathscr{G}$, with the same prior and the same data. Then $\Pi_{\rm lin}(\cdot\mid Z^{(N)})$ is a Gaussian measure, and $\mathrm{KL}\big(\Pi(\cdot\mid Z^{(N)})\,\big\|\,\Pi_{\rm lin}(\cdot\mid Z^{(N)})\big)\to0$ in $P^N_{\theta_0}$ probability.

Source: [`source/chapters/ext/m2a.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m2a.tex), label `m:thm:prkl`.

<a id="realized_information_gain_with_efficient_information"></a>

#### Realized information gain of the posterior with the efficient information at the truth

Corollary 15.23, page 236 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: proved.

Statement. Under the hypotheses of the Kullback Leibler form of the Bernstein von Mises theorem (Nickl's Conditions 1 and 2 with $\gamma$ and $k$ as in his Theorem 2, with the prior and forward map as there; $\Pi_{\rm lin}$ the posterior of the model linearized at $\theta_0$), let $J$ be a number of modes, $\theta^J=(\langle\theta,e_j\rangle)_{j\le J}$ with prior $\Pi^J$ and prior variances $\sigma_{0,j}^2$, $m_N$ and $V_N$ the posterior mean and covariance of $\theta^J$, $I_N=\mathrm{KL}(\Pi^J(\cdot\mid Z^{(N)})\,\|\,\Pi^J)$ the realized information gain, and $\Gamma_N=\mathrm{KL}(\Pi^J(\cdot\mid Z^{(N)})\,\|\,N(m_N,V_N))$. Then $\Gamma_N\le\mathrm{KL}\big(\Pi(\cdot\mid Z^{(N)})\,\|\,\Pi_{\rm lin}(\cdot\mid Z^{(N)})\big)$ for every $J$, so $\Gamma_N\to0$ in $P^N_{\theta_0}$ probability uniformly in $J$. For fixed $J$, in $P^N_{\theta_0}$ probability, $NV_N\to\Sigma_J(\theta_0)=\big(T\langle e_j,(\mathbb{I}^*_{\theta_0}\mathbb{I}_{\theta_0})^{-1}e_{j'}\rangle\big)_{j,j'\le J}$, the covariance of the first $J$ coordinates under $\mathcal{N}_{\theta_0}=N(0,T(\mathbb{I}^*_{\theta_0}\mathbb{I}_{\theta_0})^{-1})$, which is positive definite, and $I_N=\frac12\sum_{j\le J}\big[\log(1+\kappa_j)-\frac{\kappa_j}{1+\kappa_j}\big]+\frac12\,m_N^\top(\Sigma^J_0)^{-1}m_N+o_P(1)$, where the $\kappa_j$ are the eigenvalues of $N(\Sigma^J_0)^{1/2}\Sigma_J(\theta_0)^{-1}(\Sigma^J_0)^{1/2}$ and $\Sigma_0^J=\operatorname{diag}(\sigma_{0,j}^2)_{j\le J}$. For the heat and Stokes equations $\Sigma_J(\theta_0)=\operatorname{diag}(1/\iota_j)$ and $\kappa_j=N\iota_j\sigma_{0,j}^2$, where $\iota_j=\frac1T\int_0^Te^{-2\nu\lambda_jt}\,\mathrm{d}t$.

Source: [`source/chapters/ext/m2a.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m2a.tex), label `m:cor:prreal`.

<a id="kullback_leibler_bernstein_von_mises_navier_stokes"></a>

#### Kullback Leibler form of the Bernstein von Mises theorem for the Navier Stokes equations

Proposition 15.24, page 236 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: proved.

Statement. Let $\Omega=[0,1]^2$ be the torus, $\nu>0$, let $f$ and the true initial condition $\theta_0$ be smooth divergence free mean zero fields ($f,\theta_0\in\dot H^\infty_\diamond$), $W=\mathbb{R}^2$, and let $\mathscr{G}(\theta)=u_\theta$ be the solution map of the two dimensional Navier Stokes equations $\frac{\mathrm{d}u}{\mathrm{d}t}+\nu Au+B[u,u]=f$, $u(0)=\theta$, on divergence free mean zero fields, with Stokes operator $A=-\Delta$ and $B[u,v]=P[(u\cdot\nabla)v]$ ($P$ the projection onto divergence free fields). Let the data be $Y_i=\mathscr{G}(\theta)(X_i)+\varepsilon_i$ with $X_i$ i.i.d. uniform on $[0,T]\times\Omega$ and $\varepsilon_i\sim N(0,I_W)$, let the prior $\Pi$ be the rescaled Gaussian series prior on $\dot H_\diamond$ with $d=2$ and exponent $\gamma>12$, which is the prior of Theorem 2.11 of Konen and Nickl (2026) with $\alpha=\gamma$, and let $(e_j)$ be a real orthonormal eigenbasis of $A$ in $\dot H_\diamond$ with nondecreasing eigenvalues. Then the conclusions of the Kullback Leibler form of the Bernstein von Mises theorem and of its corollary on the realized information gain hold: the posterior $\Pi_{\rm lin}(\cdot\mid Z^{(N)})$ of the model linearized at $\theta_0$ is Gaussian and $\mathrm{KL}(\Pi(\cdot\mid Z^{(N)})\,\|\,\Pi_{\rm lin}(\cdot\mid Z^{(N)}))\to0$ in $P^N_{\theta_0}$ probability; for every number $J$ of modes the Kullback Leibler divergence $\Gamma_N$ of the posterior of the first $J$ coordinates from the Gaussian law with the same mean and covariance is at most that divergence; and for fixed $J$ the realized information gain is given up to $o_P(1)$ by the Gaussian formula with the efficient information at $\theta_0$.

Source: [`source/chapters/ext/m2a.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m2a.tex), label `m:prop:prklns`.

<a id="entropic_van_trees_bound"></a>

#### Entropic van Trees bound

Proposition 15.25, page 238 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: proved.

Statement. Let $\mathscr{G}$ be a measurable forward map in the model $Y_i=\mathscr{G}(\theta)(X_i)+\varepsilon_i$ ($X_i$ i.i.d. uniform on $\mathcal X=[0,T]\times\Omega$, $\varepsilon_i\sim N(0,I_W)$), let the prior $\Pi$ be a centered Gaussian measure under which the coordinates $\langle\theta,e_j\rangle$ are independent with variances $\sigma_{0,j}^2>0$, and assume $\int\|\mathscr{G}(\vartheta)\|^2_{L^\infty(\mathcal X)}\,\mathrm{d}\Pi(\vartheta)<\infty$. Fix the number of modes $J$, let $\theta^J=(\langle\theta,e_j\rangle)_{j\le J}$, $\Sigma^J_0=\operatorname{diag}(\sigma_{0,j}^2)_{j\le J}$, $I_N=\mathrm{KL}(\Pi^J(\cdot\mid Z^{(N)})\,\|\,\Pi^J)$ the realized information gain, $\mathbf{E}$ the expectation under the prior predictive law, and $\mathcal J^J_N(\vartheta)=\frac NT\big(\langle\mathbb{I}_\vartheta e_j,\mathbb{I}_\vartheta e_{j'}\rangle_{L^2(\mathcal X)}\big)_{j,j'\le J}$ the $J$ block of the Fisher information of $N$ observations at $\vartheta$, with $\mathbb{I}_\vartheta$ the linearization of $\mathscr{G}$ at $\vartheta$. Assume that for $\Pi$ almost every $\eta$ in the closed span of $(e_j)_{j>J}$ the map $x\mapsto\mathscr{G}(\eta+\sum_{j\le J}x_je_j)$ from $\mathbb{R}^J$ into $C(\mathcal X)$ is continuously differentiable, with partial derivatives $\mathbb{I}_\vartheta e_j$ at $\vartheta=\eta+\sum_{j\le J}x_je_j$. If $\bar{\mathcal J}^J_N=\int\mathcal J^J_N(\vartheta)\,\mathrm{d}\Pi(\vartheta)$ is finite, then for every $N$, $\mathbf{E}\,I_N=I(\theta^J;Z^{(N)})\le\frac12\log\det\big(\mathrm{Id}+(\Sigma^J_0)^{1/2}\,\bar{\mathcal J}^J_N\,(\Sigma^J_0)^{1/2}\big)$. If moreover the prior is the rescaled Gaussian series prior with exponent $\gamma>d$, and the matrix $\mathcal J^J_N(\vartheta)/N$, which does not depend on $N$, is continuous at $\vartheta=0$ for the supremum norm, bounded by a polynomial in $\|\vartheta\|_\infty$, and invertible at $\vartheta=0$, then for fixed $J$, $\mathbf{E}\,I_N\le\frac12\log\det\big(\mathrm{Id}+(\Sigma^J_0)^{1/2}\,\mathcal J^J_N(0)\,(\Sigma^J_0)^{1/2}\big)+o(1)$.

Source: [`source/chapters/ext/m2a.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m2a.tex), label `m:prop:prvt`.

<a id="reaction_diffusion_expected_gain_at_prior_center"></a>

#### Reaction diffusion: the expected gain is set at the center of the prior

Proposition 15.26, page 239 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: proved.

Statement. Let $\partial_tu=\Delta u+f(u)$, $u(0)=\theta$, on the torus $\Omega=[0,1]^d$ with $f\in C_c^\infty(\mathbb{R})$ and $d\le3$, observed as in the model $Y_i=\mathscr{G}(\theta)(X_i)+\varepsilon_i$ with $X_i$ i.i.d. uniform on $\mathcal X=[0,T]\times\Omega$ and $\varepsilon_i\sim N(0,1)$; let $(e_j)$ be the real trigonometric basis, of the functions $\sqrt2\cos(2\pi k\cdot x)$ and $\sqrt2\sin(2\pi k\cdot x)$ with eigenvalues $\lambda_j$; let the prior $\Pi$ be the rescaled Gaussian series prior with exponent $\gamma>d$ and variances $\sigma_{0,j}^2=\lambda_j^{-\gamma}/(N\delta_N^2)$, $\delta_N=N^{-\gamma/(2\gamma+d)}$; and let the number of modes $J$ be fixed. Let $I_N$ be the realized information gain for the first $J$ modes and $\mathbf{E}$ the expectation under the prior predictive law. Let $v$ solve $v'=f(v)$, $v(0)=0$, $\chi(t)=\int_0^tf'(v(s))\,\mathrm{d}s$, $\iota^0_j=\frac1T\int_0^Te^{2\chi(t)-2\lambda_jt}\,\mathrm{d}t$ and $\kappa^0_j=N\iota^0_j\sigma_{0,j}^2$ (the information at the center of the prior). Then: (i) $\mathbf{E}\,I_N\le\frac12\sum_{j\le J}\log(1+\kappa^0_j)+o(1)$. (ii) If $f$ vanishes on $[-a,a]$ for some $a>0$, then $\iota^0_j=\iota_j=(1-e^{-2\lambda_jT})/(2\lambda_jT)$, the value for the heat equation with $\nu=1$, and $\mathbf{E}\,I_N=\frac12\sum_{j\le J}\log(1+\kappa^0_j)+o(1)$. (iii) Let $d\ge2$ and let $f$ be as in (ii), with moreover $f\ge0$, $f$ nondecreasing on $(-\infty,b]$ and strictly increasing on $(a,b)$ for some $b>a$. The first mode $e_1$, with $\lambda_1=4\pi^2$, is $\sqrt2\cos(2\pi x_p)$ or $\sqrt2\sin(2\pi x_p)$ for some coordinate $p$; let $\theta_0(x)=A\cos(2\pi x_q)$ with $q\ne p$ and $a<A<b$, and let $T$ be so small that the solution of $w'=f(w)$, $w(0)=A$, stays at most $b$ on $[0,T]$. Then $\|\mathbb{I}_{\theta_0}e_1\|^2_{L^2(\mathcal X)}>T\iota_1$, and for $J=1$, writing $\mathcal J^1_N(\theta_0)=\frac NT\|\mathbb{I}_{\theta_0}e_1\|^2_{L^2(\mathcal X)}$ for the Fisher information at $\theta_0$, $\frac12\log\big(1+\sigma^2_{0,1}\mathcal J^1_N(\theta_0)\big)-\mathbf{E}\,I_N\to\frac12\log\frac{\|\mathbb{I}_{\theta_0}e_1\|^2_{L^2(\mathcal X)}}{T\iota_1}>0$. (iv) Under the hypotheses of (iii), let $\psi(r)=(1-e^{-2\lambda_1r})/(2\lambda_1)$, let $\psi(T-t)f'(u_{\theta_0}(t,x))<2$ for $(t,x)\in\mathcal X$ (as when $T\sup f'<2$), and let $\lambda_j=\lambda_1$ for $j\le J$. Then $\Sigma_J(0)-\Sigma_J(\theta_0)$ is positive definite, where $\Sigma_J(\vartheta)=\big(T\langle e_j,(\mathbb{I}^*_\vartheta\mathbb{I}_\vartheta)^{-1}e_{j'}\rangle\big)_{j,j'\le J}$ is the covariance of the Bernstein von Mises limit in the first $J$ modes and $\Sigma_J(0)=\mathrm{Id}/\iota_1$, and $\frac12\log\det\big(\mathrm{Id}+N\sigma^2_{0,1}\Sigma_J(\theta_0)^{-1}\big)-\mathbf{E}\,I_N\to\frac12\log\det\big(\Sigma_J(0)\Sigma_J(\theta_0)^{-1}\big)>0$.

Source: [`source/chapters/ext/m2a.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m2a.tex), label `m:prop:prrd`.

<a id="quadratic_variation_and_the_sufficient_statistic"></a>

#### Quadratic variation and the sufficient statistic

Proposition 15.28, page 243 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: proved.

Statement. In the linear model $Y=\Phi\theta+\varepsilon$ with design matrix $\Phi_{ij}=s_j(t_i)e_j(x_i)$ and unknown noise variance $\varsigma^2$ ($\varepsilon\sim N(0,\varsigma^2\mathrm{Id}_N)$), conditionally on the design the pair $\big(\Phi^\top Y,\ \|Y\|^2\big)$ is sufficient for $(\theta,\varsigma^2)$, and the conditional law of $\theta$ given the pair and $\varsigma^2$ depends on the data only through $\Phi^\top Y$. If instead the observation noise is replaced by an observed diffusion path on $[0,T]$ with unknown diffusion coefficient, $\mathrm{d}Y_t=\mathscr{G}(\theta)(t)\,\mathrm{d}t+\sigma(t)\,\mathrm{d}B_t$, the coefficient is identified by the quadratic variation, the likelihood ratio for $\theta$ is the Girsanov density, and the sufficient statistic for $\theta$ is again the adjoint evolution driven by the data, now with the data measure replaced by $\mathrm{d}Y_t/\sigma^2(t)$.

Source: [`source/chapters/ext/m2a.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m2a.tex), label `m:prop:qv`.

<a id="one_step_summary_under_four_abc_criteria"></a>

#### The one step summary under four ABC criteria: Bayes risk optimal up to o(1), all four attained in the J mode Gaussian projection

Proposition 15.29, page 244 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: conditional on The uniform Bernstein von Mises statement (Assumption U of the chapter), applied both to the one step summary and to the posterior mean: sets of parameters of prior probability tending to one on which the Wasserstein distance between the posterior of the rescaled, recentered parameter and the Gaussian limit tends to zero uniformly in the truth, with uniform integrability of these discrepancies, Lipschitz dependence of the limit on the truth, first moment bounds on the limits, concentration of the posterior given the summary around the summary, and smallness of the discrepancy conditional on the summary at the true parameter; the book does not prove it (Open Question Uniformity). Also the uniform moment bound (MB) of order two plus a positive power on the rescaled posterior radius under the prior predictive law, which the book proves only for the linear Gaussian model and assumes for nonlinear forward maps..

Statement. Work in Nickl's framework (torus $\Omega=[0,1]^d$, data $Y_i=\mathscr{G}(\theta)(X_i)+\varepsilon_i$ with $X_i$ i.i.d. uniform on $\mathcal X=[0,T]\times\Omega$ and $\varepsilon_i\sim N(0,I_W)$, Laplace eigenbasis $(e_j)$ with eigenvalues $\lambda_j$, rescaled Gaussian series prior $\Pi$ with exponent $\gamma$ and variances $\sigma_{0,j}^2$, $\delta_N=N^{-\gamma/(2\gamma+d)}$, $J_N\asymp N\delta_N^2$, linearization $\mathbb{I}_\vartheta$ of $\mathscr{G}$, $\mathcal{N}_\vartheta=N(0,T(\mathbb{I}_\vartheta^*\mathbb{I}_\vartheta)^{-1})$, $\tilde\theta_N$ the posterior mean). Assume the hypotheses of Nickl's Bernstein von Mises theorem (Conditions 1 and 2 of Nickl (2024) with $\gamma$ and $k$ as in his Theorem 2) and the hypotheses of the equivalence of the cross fitted one step efficient score summary $\hat S_N=\hat S^{J_N}_N$ with the efficient centering (catalog entry equivalence_with_the_efficient_centering); assume the uniform Bernstein von Mises statement (Assumption U) both with $S_N=\hat S_N$ and with $S_N=\tilde\theta_N$; and assume the uniform moment bound (MB): for some $\varpi>0$, $\sup_N\mathbf{E}\,\|\sqrt N(\theta-\hat S_N)\|^{2+\varpi}_{H^{-k-2}}+\sup_N\mathbf{E}\,\|\sqrt N(\theta-\tilde\theta_N)\|^{2+\varpi}_{H^{-k-2}}<\infty$, the expectations being under the prior predictive law $\mathbf{P}=\Pi\otimes P^N_\vartheta$ (parameter $\vartheta\sim\Pi$, then data $Z^{(N)}\sim P^N_\vartheta$).

Let $\mathcal S_J$ be the class of all measurable statistics $S=g(Z^{(N)})$ taking values in a $J$ dimensional subspace of $H^{-k-2}$, with $J=J_N$; let $P_J$ be the projection onto $\operatorname{span}\{e_j:j\le J\}$, $\theta^J=P_J\theta$, and $\mathscr{W}_1=\mathscr{W}_{1,H^{-k-2}}$. In the first $J$ modes put $\Sigma_J(\vartheta)=\big(T\langle e_j,(\mathbb{I}_\vartheta^*\mathbb{I}_\vartheta)^{-1}e_{j'}\rangle\big)_{j,j'\le J}$ (the covariance of $\mathcal{N}_\vartheta$), $\mathcal J^J_N(\vartheta)=\frac NT\big(\langle e_j,\mathbb{I}^*_\vartheta\mathbb{I}_\vartheta e_{j'}\rangle\big)_{j,j'\le J}$ (the $J$ block of the Fisher information of $N$ observations), $\Sigma^J_0=\operatorname{diag}(\sigma_{0,j}^2)_{j\le J}$ and $V^J_N(\vartheta)=\big(\mathcal J^J_N(\vartheta)+(\Sigma^J_0)^{-1}\big)^{-1}$. For $S\in\mathcal S_J$ consider four criteria: (i) the expected posterior entropy $\mathcal H_N(S)=\mathbf{E}\,H\big(\operatorname{Law}(\theta^J\mid S)\big)$, to be minimized; (ii) $\mathcal F_N(S)=\log\det\mathcal J_N(S)$, where $\mathcal J_N(S)$ is the efficient Fisher information carried at $\theta_0$ by the induced experiment $\{\operatorname{Law}_\theta(S)\}$ about the $J$ mode subparameter $(\langle e_j,\theta\rangle)_{j\le J}$, to be maximized; (iii) the $L^2$ Bayes risk $\mathcal R_N(S)=N\,\mathbf{E}\,\|\theta-\mathbf{E}[\theta\mid S]\|^2_{H^{-k-2}}$, to be minimized; (iv) the expected information gain $\mathcal U_N(S)=I(\theta^J;S)$ (mutual information), to be maximized.

Then $\hat S_N\in\mathcal S_J$, and: (a) (exact at every $N$) for every $S\in\mathcal S_J$, $\mathcal H_N(S)\ge\mathcal H_N(Z^{(N)})$, $\mathcal F_N(S)\le\mathcal F_N(Z^{(N)})$, $\mathcal R_N(S)\ge\mathcal R_N(Z^{(N)})$ and $\mathcal U_N(S)\le\mathcal U_N(Z^{(N)})$; moreover (i) and (iv) are one criterion, since $\mathcal U_N(S)=H\big(\operatorname{Law}(\theta^J)\big)-\mathcal H_N(S)$ for every $N$ and every $S$, so entropy minimization and information gain maximization have identical optimizers exactly. (b) Under (MB), $\mathcal R_N(\hat S_N)-\mathcal R_N(Z^{(N)})\to0$ and both terms are bounded in $N$. If moreover the weighted traces $t(\vartheta)=T\sum_{j\ge1}(1+\lambda_j)^{-k-2}\langle e_j,(\mathbb{I}_\vartheta^*\mathbb{I}_\vartheta)^{-1}e_j\rangle$ of the limits $\mathcal{N}_\vartheta$ satisfy $\sup_N\int t^{1+\varpi/2}\,\mathrm{d}\Pi<\infty$, as they do for the heat and Stokes equations, where $t$ is constant, then both terms equal $\varrho_N+o(1)$ with $\varrho_N=\int t(\vartheta)\,\mathrm{d}\Pi(\vartheta)$, which depends on $N$ only through the rescaled prior $\Pi$ and is bounded; so $\hat S_N$ attains the criterion (iii) optimum within $\mathcal S_J$ up to $o(1)$. (c) Call the $J$ mode Gaussian projection at $\vartheta$ the linear Gaussian experiment with parameter $\theta^J\in\mathbb{R}^J$, prior $N(0,\Sigma^J_0)$ and information matrix $\mathcal J^J_N(\vartheta)$, in which the modes beyond $J$ are known; criteria (i) and (iv) are evaluated in it at the parameter $\vartheta\sim\Pi$ that generates the data, and criterion (ii) at $\vartheta=\theta_0$. In it the regularized form of $\hat S_N$ is exactly sufficient, so $\operatorname{Law}(\theta^J\mid\hat S_N)=\operatorname{Law}(\theta^J\mid Z^{(N)})=N(\cdot,V^J_N(\vartheta))$ there, and all four criteria take identical values at $\hat S_N$ and at the full data, namely $\mathcal H^\star_N=\frac12\int\log\det\big(2\pi e\,V^J_N(\vartheta)\big)\,\mathrm{d}\Pi(\vartheta)$, $\mathcal U^\star_N=\frac12\int\log\det\big(\Sigma^J_0\,V^J_N(\vartheta)^{-1}\big)\,\mathrm{d}\Pi(\vartheta)$, which equals $\frac12\sum_{j\le J}\log(1+\kappa_j)$ with $\kappa_j=N\iota_j\sigma_{0,j}^2$ for the heat and Stokes equations (where $V^J_N(\vartheta)$ does not depend on $\vartheta$ and is diagonal), and $\mathcal F^\star_N=\log\det\mathcal J^J_N(\theta_0)$. For a nonlinear forward map the integral defining $\mathcal U^\star_N$ need not equal its value at $\theta_0$. In the exact experiment, where the modes beyond $J$ are unknown parameters, the efficient information for the first $J$ modes is the Schur complement $N\Sigma_J(\theta_0)^{-1}\preceq\mathcal J^J_N(\theta_0)$, and $\hat S_N$ attains $\log\det\big(N\Sigma_J(\theta_0)^{-1}\big)$ asymptotically, for each fixed $J$; the two values of criterion (ii) agree when $\mathbb{I}^*_{\theta_0}\mathbb{I}_{\theta_0}$ is diagonal in $(e_j)$. For the heat and Stokes equations the $J$ mode Gaussian projection does not depend on $\vartheta$ and is the limit of the exact experiment at the $\sqrt N$ scale in $\mathscr{W}_1$; when $\mathbb{I}^*_{\theta_0}\mathbb{I}_{\theta_0}$ couples the first $J$ modes with the others it is not that limit.

For criteria (i), (ii) and (iv), part (c) is a statement about the $J$ mode Gaussian projection and not about the exact finite $N$ functionals: the book does not claim, and the hypotheses do not give, $\mathcal H_N(\hat S_N)-\mathcal H_N(Z^{(N)})\to0$ or $\mathcal F_N(\hat S_N)-\mathcal F_N(Z^{(N)})\to0$ for the exact laws, because differential entropy, Kullback Leibler divergence and Fisher information are not continuous along $\mathscr{W}_1$ convergence. Criterion (iii) is the exception, being a second moment functional.

Source: [`source/chapters/ext/m2b.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m2b.tex), label `m:prop:abcopt`.

<a id="the_adjoint_statistic_is_the_pls_projection"></a>

#### The adjoint statistic is the PLS projection

Proposition 15.32, page 252 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: proved.

Statement. Consider the linear model $Y=\Phi\theta+\varepsilon$ with design matrix $\Phi_{ij}=s_j(t_i)e_j(x_i)$ ($i\le N$, $j\le D$), prior $\theta\sim N(0,\Sigma_0)$ and noise $\varepsilon\sim N(0,\mathrm{Id}_N)$ independent of $\theta$, and treat the raw data $Y\in\mathbb{R}^N$ as the pool of candidate statistics. The first partial least squares (PLS) direction for predicting a coordinate $\theta_j$ from $Y$ is the vector $w\in\mathbb{R}^N$ maximizing $\mathrm{Cov}(\theta_j,w^\top Y)$ subject to $\|w\|=1$, and $\mathrm{Cov}(\theta_j,w^\top Y)=w^\top\mathrm{Cov}(Y,\theta_j)=w^\top\Phi\,\Sigma_0\mathbf{u}_j$, where $\mathbf{u}_j$ is the $j$th unit vector of $\mathbb{R}^D$; so the direction is $\Phi\Sigma_0\mathbf{u}_j/\|\Phi\Sigma_0\mathbf{u}_j\|$ and the corresponding score is proportional to $(\Sigma_0\Phi^\top Y)_j$. Collecting $j\le D$ and absorbing the fixed prior covariance, the PLS scores are exactly the coordinates of the adjoint statistic $\Phi^\top Y$ (the coefficient vector of the time zero value of the backward adjoint solution driven by the data), which is sufficient. In particular a single PLS component per parameter coordinate suffices, and no further components add information.

Source: [`source/chapters/ext/m2b.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m2b.tex), label `m:prop:pls`.

<a id="deep_pls_structure_of_the_gbc_summary"></a>

#### Deep PLS structure of the GBC summary

Proposition 15.34, page 253 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: conditional on Part (ii) for the posterior given the scores alone assumes the uniform Bernstein von Mises statement (Assumption U), which the book does not prove (Open Question Uniformity), in addition to the hypotheses of the equivalence of the one step summary with the efficient centering..

Statement. Let $\mathscr{G}$ be a nonlinear forward map in Nickl's framework and let the summary be the cross fitted one step efficient score summary $\hat S_N=\hat S^{J_N}_N$ (catalog entry equivalence_with_the_efficient_centering), whose coordinates average over the two folds the preliminary estimate coordinate $\langle e_j,\bar\theta^{[b]}_N\rangle$ plus the average, over the other half sample, of the residual $Y_i-u_{\bar\theta^{[b]}_N}(X_i)$ projected on the direction $\mathbb{I}_{\bar\theta^{[b]}_N}p_N(\bar e_j^{\,\bar\theta^{[b]}_N})(X_i)$. Then: (i) the first stage is a linear projection of the residuals onto the directions $\mathbb{I}_{\bar\theta_N}p_N(\bar e_j)$, that is, a partial least squares step with directions supplied by the linearized forward map rather than estimated from the simulations; (ii) the second stage, the map from the projected scores $s$ to the posterior, is asymptotically the identity plus a scale, namely the conditional quantile map satisfies $Q_j(\tau\mid s)=s_j+z_\tau\sigma_j/\sqrt N+o(N^{-1/2})$, with $z_\tau$ the $\tau$ quantile of the standard normal law and $\sigma_j^2=T\langle e_j,(\mathbb{I}^*_{\theta_0}\mathbb{I}_{\theta_0})^{-1}e_j\rangle$, read in the Wasserstein sense, under the hypotheses of the equivalence of $\hat S_N$ with the efficient centering for the posterior given all of the data, and under Assumption U as well for the posterior given the scores alone; so under these hypotheses the deep part of deep PLS has an asymptotically trivial link.

Source: [`source/chapters/ext/m2b.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m2b.tex), label `m:prop:dpls`.

<a id="jiang_wong_under_bernstein_von_mises"></a>

#### Jiang Wong under a uniform Bernstein von Mises assumption: the posterior mean summary is asymptotically sufficient

Theorem 15.38, page 256 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: conditional on The uniform Bernstein von Mises assumption (Assumption U, clauses (U1) to (U4)) for the posterior mean, and for the one step statistic the same assumption for that statistic; the book does not prove it (Open Question 17.18, Uniformity)..

Statement. Let $Z^{(N)}=(Y_i,X_i)_{i\le N}$ with $Y_i=\mathscr{G}(\theta)(X_i)+\varepsilon_i$, $X_i$ i.i.d. uniform on $[0,T]\times\Omega$ and independent $\varepsilon_i\sim N(0,I_W)$, where $\mathscr{G}(\theta)=u_\theta$ is the solution map of an evolution equation with initial condition $\theta$. Let the prior $\Pi$ be the law of $(\sqrt N\delta_N)^{-1}\sum_j\lambda_j^{-\gamma/2}g_je_j$, with $(e_j,\lambda_j)$ the Laplace eigenpairs, $g_j$ i.i.d. $N(0,1)$ and $\delta_N=N^{-\gamma/(2\gamma+d)}$, and let the prior and the forward map satisfy Conditions 1 and 2 of Nickl (2024) with the constants of his Bernstein von Mises theorem (integer $\gamma>\max(3\zeta+3d/2+2,\eta_0)$ and $k>\max(\zeta+5d/2,\eta_0)$, where $\zeta>d/2$ and $\eta_0$ are the indices of his Condition 2), so that, with $\tilde\theta_N=E^\Pi[\theta\mid Z^{(N)}]$ the posterior mean, $\mathbb{I}_\vartheta$ the linearization of $\mathscr{G}$ at $\vartheta$, $\mathcal{N}_\vartheta=N(0,T(\mathbb{I}^*_\vartheta\mathbb{I}_\vartheta)^{-1})$ and $\mathscr{W}_1$ the Wasserstein distance of order one on the negative Sobolev space $H^{-k-2}$, $\mathscr{W}_1\big(\operatorname{Law}(\sqrt N(\theta-\tilde\theta_N)\mid Z^{(N)}),\mathcal{N}_{\theta_0}\big)\to0$ in $P^N_{\theta_0}$ probability, $\theta_0$ being the true initial condition and $P^N_\vartheta$ the law of the data under $\vartheta$. Let $\mathbf{P}=\Pi\otimes P^N_\vartheta$ be the joint law of a parameter $\vartheta$ drawn from the prior and data drawn given it, which is also the law under which the GBC training pairs are simulated.

Assume the uniform Bernstein von Mises assumption for the summary $S_N=\tilde\theta_N$: there are sets $\Theta_N$ such that (U1) $\Pi(\Theta_N)\to1$, $\theta_0\in\Theta_N$ for all large $N$, and $\sup_{\vartheta\in\Theta_N}E^N_\vartheta\,\mathscr{W}_1\big(\operatorname{Law}(\sqrt N(\theta-S_N)\mid Z^{(N)}),\mathcal{N}_\vartheta\big)\to0$; (U2) these discrepancies are uniformly integrable under the prior predictive law; (U3) $\vartheta\mapsto T(\mathbb{I}^*_\vartheta\mathbb{I}_\vartheta)^{-1}$, into bounded operators $H^{-k-2}\to H^{-k-4}$, and $\vartheta\mapsto\mathcal{N}_\vartheta$, into the probability measures on $H^{-k-2}$ with the distance $\mathscr{W}_1$, are Lipschitz on $(\Theta_N,\|\cdot\|_{H^\zeta})$ with constants that do not depend on $N$, the first moments $m_1(\vartheta)=\int\|x\|_{H^{-k-2}}\,\mathrm{d}\mathcal{N}_\vartheta(x)$ satisfy $\int_{\Theta_N^c}m_1\,\mathrm{d}\Pi\to0$ and $\Pi(\Theta_N^c)\sup_{\Theta_N}m_1\to0$, $S_N\in\Theta_N$ with probability tending to one, and $E^\Pi[\|\theta-S_N\|_{H^\zeta}\mid S_N]\to0$; (U4) for every $\theta_0\in\Theta_N$, $E\big[\mathscr{W}_1\big(\operatorname{Law}(\sqrt N(\theta-S_N)\mid Z^{(N)}),\mathcal{N}_{\theta_0}\big)\mid S_N\big]\to0$ in $P^N_{\theta_0}$ probability.

Let $\tau_N=\operatorname{Law}(\sqrt N(\theta-\tilde\theta_N)\mid Z^{(N)})$ be the exact recentered posterior and $\tau^{\rm S}_N=\operatorname{Law}(\sqrt N(\theta-\tilde\theta_N)\mid\tilde\theta_N)$ the recentered posterior given the posterior mean statistic alone, both conditional laws under $\mathbf{P}$. Then $\mathscr{W}_1(\tau^{\rm S}_N,\mathcal{N}_{\tilde\theta_N})\to0$ and $\mathscr{W}_1(\tau_N,\tau^{\rm S}_N)\to0$ in $\mathbf{P}$ probability, and, because $\theta_0\in\Theta_N$, both also hold in $P^N_{\theta_0}$ probability with $\mathcal{N}_{\tilde\theta_N}$ replaced by $\mathcal{N}_{\theta_0}$. The same holds with $\tilde\theta_N$ replaced by the cross fitted one step efficient score statistic $\hat S^{J_N}_N$ (catalog entry equivalence_with_the_efficient_centering) when the assumption above holds with $S_N=\hat S^{J_N}_N$ and the hypotheses of that entry hold. In words: whenever a Bernstein von Mises theorem holds uniformly over prior typical truths, the posterior mean summary, or any summary $\sqrt N$ equivalent to it in $H^{-k-2}$, is asymptotically sufficient in Wasserstein distance of order one at the $\sqrt N$ scale.

Source: [`source/chapters/ext/m2c.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m2c.tex), label `m:thm:jwbvm`.

<a id="gbc_with_the_posterior_mean_summary"></a>

#### GBC with the posterior mean summary

Corollary 15.40, page 258 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: conditional on The convergence at the root N scale assumes the uniform Bernstein von Mises assumption (Assumption U, clauses (U1) to (U4), stated clause by clause in the entry jiang_wong_under_bernstein_von_mises) for the posterior mean, which the book does not prove (Open Question 17.18, Uniformity); the two identities at finite N are unconditional..

Statement. Let data $Z^{(N)}$ come from a forward map and rescaled Gaussian series prior $\Pi$ that satisfy Conditions 1 and 2 of Nickl (2024) with the constants of his Bernstein von Mises theorem, as in the catalog entry jiang_wong_under_bernstein_von_mises, where $T$ is the length of the observation window, $\mathbb{I}_\vartheta$ the linearization of the forward map at $\vartheta$, and $\zeta>d/2$ and $k$ the Sobolev indices of that theorem; let $\Pi_N=\Pi(\cdot\mid Z^{(N)})$ be the posterior, $\tilde\theta_N$ its mean, $V(Z^{(N)})=\mathrm{Var}(\theta\mid Z^{(N)})$ its covariance, $\theta_0$ the true parameter, and $\mathscr{W}_1$ the Wasserstein distance of order one on the negative Sobolev space $H^{-k-2}$. Let $\Pi^{\rm S}_N=\operatorname{Law}(\theta\mid\tilde\theta_N)$, the conditional law, under the joint law of prior and data, of the parameter given the posterior mean statistic alone; it is the target of generative Bayesian computation (GBC) with the posterior mean summary and an exact generator. Then for every $N$ the mean of $\Pi^{\rm S}_N$ equals the posterior mean $\tilde\theta_N$ and its covariance is $E[V(Z^{(N)})\mid\tilde\theta_N]$. If moreover the uniform Bernstein von Mises assumption holds with $S_N=\tilde\theta_N$ (sets $\Theta_N$ of prior mass tending to one that contain $\theta_0$, on which the recentered posterior is uniformly close to its Gaussian limit $N(0,T(\mathbb{I}^*_\vartheta\mathbb{I}_\vartheta)^{-1})$, with the integrability, Lipschitz, moment and conditional clauses (U1) to (U4) stated in that entry), then $\sqrt N\,\mathscr{W}_1(\Pi^{\rm S}_N,\Pi_N)\to0$ in $P^N_{\theta_0}$ probability, and also in probability under the joint law of prior and data; this is the accuracy condition (G1) that the book's transfer theorem places on a GBC posterior.

Source: [`source/chapters/ext/m2c.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m2c.tex), label `m:cor:jwgbc`.

<a id="sufficiency_gap"></a>

#### Sufficiency gap in the linear Gaussian model: Rao Blackwell lower bound and transport entropy upper bound

Theorem 15.41, page 258 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: proved.

Statement. In the linear Gaussian model $Y=\Phi\theta+\varepsilon$ with $\theta\sim N(0,\Sigma_0)$ in $\mathbb{R}^D$ and $\varepsilon\sim N(0,\varsigma^2\mathrm{Id})$ independent of $\theta$, let $Z=Y$ be the full data and $S=AY$ any linear statistic. Then the posteriors $\Pi(\cdot\mid Z)$ and $\Pi(\cdot\mid S)$ are Gaussian with covariances $V_Z=\mathrm{Var}(\theta\mid Z)\preceq V_S=\mathrm{Var}(\theta\mid S)$ that do not depend on the data. Let $\mathscr{W}_1$ be the Wasserstein distance of order one on $\mathbb{R}^D$ with the Euclidean norm and $\Delta I=I(\theta;Z)-I(\theta;S)\ge0$ the mutual information deficit. Then: (i) (lower bound, Rao Blackwell) $\mathscr{W}_1(\Pi(\cdot\mid S),\Pi(\cdot\mid Z))\ge\|\xi\|$, where $\xi=E[\theta\mid S]-E[\theta\mid Z]$ is a centered Gaussian vector with covariance $V_S-V_Z$, so that $E\|\xi\|^2=\mathrm{tr}(V_S-V_Z)$ and $\sqrt{\mathrm{tr}(V_S-V_Z)-\|V_S-V_Z\|_{op}}\le E\|\xi\|\le\sqrt{\mathrm{tr}(V_S-V_Z)}$; (ii) (upper bound, transport entropy) $E_Z\,\mathscr{W}_1(\Pi(\cdot\mid Z),\Pi(\cdot\mid S))\le\sqrt{2\|V_S\|_{op}\,\Delta I}$, where $\Delta I=\tfrac12\log\det(V_SV_Z^{-1})$; (iii) the lower bound $\|\xi\|$ of (i) vanishes almost surely, and the upper bound of (ii) vanishes, if and only if $V_S=V_Z$, if and only if $S$ is Bayes sufficient, that is, $\operatorname{Law}(\theta\mid S)=\operatorname{Law}(\theta\mid Z)$ almost surely; for the adjoint statistic $S=\Phi^\top Y$ both vanish identically. Consequently, for any GBC posterior $\hat\Pi$ built on $S$, with generator error $\epsilon_{\rm gen}=\mathscr{W}_1(\hat\Pi,\Pi(\cdot\mid S))$, in expectation over the data $E\,\mathscr{W}_1(\hat\Pi,\Pi(\cdot\mid Z))\ge\sqrt{\mathrm{tr}(V_S-V_Z)-\|V_S-V_Z\|_{op}}-E\,\epsilon_{\rm gen}$ and $E\,\mathscr{W}_1(\hat\Pi,\Pi(\cdot\mid Z))\le E\,\epsilon_{\rm gen}+\sqrt{2\|V_S\|_{op}\,\Delta I}$.

Source: [`source/chapters/ext/m2c.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m2c.tex), label `m:thm:gap`.

<a id="sufficiency_gap_beyond_the_linear_model"></a>

#### Sufficiency gap beyond the linear model

Proposition 15.42, page 260 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: proved.

Statement. Let a parameter $\theta$, expanded in the Laplace eigenbasis $(e_j)$ with eigenvalues $\lambda_j$, have a prior $\Pi$, let $Z^{(N)}$ be the data and $\mathbf P$ the joint law of parameter and data, and let $k$ be the index of the negative Sobolev space $H^{-k-2}$ in which the posterior is compared with its Gaussian limit. Let $S=S(Z^{(N)})$ be a statistic, fix $D$, and write $\mathscr{W}_{1,w}$ for the Wasserstein distance of order one between laws of the first $D$ coordinates $(\langle e_j,\theta\rangle)_{j\le D}$ in the norm $\|x\|_w^2=\sum_{j\le D}(1+\lambda_j)^{-k-2}x_j^2$ that $H^{-k-2}$ induces on them. Suppose that there are a linear Gaussian model $Y_G=\Phi_G\theta+\varepsilon_G$ on $\mathbb{R}^D$, with prior $N(0,\Sigma_0)$, $\varepsilon_G\sim N(0,\mathrm{Id})$ and posterior $\Pi_G$, a linear statistic $S_G=AY_G$, and a coupling of $(Z^{(N)},S)$ under $\mathbf P$ with $(Y_G,S_G)$ under the Gaussian model, such that $\sqrt N\,E\,\mathscr{W}_{1,w}\big(\Pi(\cdot\mid Z^{(N)}),\Pi_G(\cdot\mid Y_G)\big)\to0$ and $\sqrt N\,E\,\mathscr{W}_{1,w}\big(\Pi(\cdot\mid S),\Pi_G(\cdot\mid S_G)\big)\to0$. Let $V_Z\preceq V_S$ be the posterior covariances of the Gaussian model given $Y_G$ and given $S_G$, $\Delta I=\tfrac12\log\det(V_SV_Z^{-1})$, and take traces and operator norms in $\|\cdot\|_w$, that is, $\mathrm{tr}_wV=\mathrm{tr}(\Lambda_wV\Lambda_w)$ and $\|V\|_{op,w}=\|\Lambda_wV\Lambda_w\|_{op}$ with $\Lambda_w=\operatorname{diag}((1+\lambda_j)^{-(k+2)/2})$. Then the sufficiency gap at the $\sqrt N$ scale, $\Upsilon_N=\sqrt N\,E\,\mathscr{W}_{1,w}\big(\Pi(\cdot\mid S),\Pi(\cdot\mid Z^{(N)})\big)$, satisfies $\Upsilon_N\ge\sqrt{N\,\mathrm{tr}_w(V_S-V_Z)-N\|V_S-V_Z\|_{op,w}}-o(1)$ and $\Upsilon_N\le\sqrt{2N\|V_S\|_{op,w}\,\Delta I}+o(1)$. For the heat and Stokes equations with viscosity $\nu$ and observation window $[0,T]$, in the Gaussian experiment that observes $\theta_j+(N\iota_j)^{-1/2}\xi_j$, $j\le D$, with independent standard normal $\xi_j$, independent priors $\theta_j\sim N(0,\sigma^2_{0,j})$, per mode information $\iota_j=(1-e^{-2\nu\lambda_jT})/(2\nu\lambda_jT)$ and $\kappa_j=N\iota_j\sigma^2_{0,j}$, and with $S$ its first $J'$ coordinates, the hypotheses hold with no error, $N(V_S-V_Z)$ is diagonal with entries $0$ for $j\le J'$ and $N\sigma^2_{0,j}\kappa_j/(1+\kappa_j)$ for $J'<j\le D$, and $\Delta I=\tfrac12\sum_{J'<j\le D}\log(1+\kappa_j)$; with $a_j=(1+\lambda_j)^{-k-2}N\sigma^2_{0,j}\kappa_j/(1+\kappa_j)$ the lower bound is $\big(\sum_{J'<j\le D}a_j-\max_{J'<j\le D}a_j\big)^{1/2}$.

Source: [`source/chapters/ext/m2c.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m2c.tex), label `m:prop:gapnl`.

<a id="sufficiency_gap_admissible_gaussian_models"></a>

#### The Gaussian comparison models admitted by the first hypothesis of the nonlinear sufficiency gap bounds

Proposition 15.43, page 261 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: conditional on Clauses (U1) and (U2) of the uniform Bernstein von Mises assumption (Assumption U, stated clause by clause in the entry jiang_wong_under_bernstein_von_mises) for some summary, and for part (ii) clause (U3) as well; the book does not prove them (Open Question 17.18, Uniformity)..

Statement. Let data $Z^{(N)}$ come from the forward map and observation model of Nickl's (2024) Bernstein von Mises theorem (catalog entry jiang_wong_under_bernstein_von_mises), and let $\Pi$ be a prior, which may depend on $N$, as the rescaled Gaussian series prior of that theorem does, or not, let $\mathcal{N}_\vartheta=N(0,T(\mathbb{I}^*_\vartheta\mathbb{I}_\vartheta)^{-1})$ be the Gaussian limit at the parameter $\vartheta$, with $T$ the length of the observation window and $\mathbb{I}_\vartheta$ the linearization of the forward map at $\vartheta$, on the negative Sobolev space $H^{-k-2}$ ($\zeta>d/2$ and $k$ the Sobolev indices of Nickl's theorem), and let $\mathbf P$ be the joint law of a parameter drawn from the prior and the data. With $(e_j,\lambda_j)$ the Laplace eigenpairs, fix $D$, let $\Lambda_w=\operatorname{diag}((1+\lambda_j)^{-(k+2)/2})_{j\le D}$, let $\mathscr{W}_{1,w}$ be the Wasserstein distance of order one for laws of the first $D$ coordinates in the norm $\|x\|_w=|\Lambda_wx|$, and let $\Sigma_D(\vartheta)$ be the covariance matrix of the first $D$ coordinates under $\mathcal{N}_\vartheta$. For symmetric positive semidefinite $D\times D$ matrices $V,V'$ and a unit vector $u\in\mathbb{R}^D$ put $\sigma_u(V)=(u^\top\Lambda_wV\Lambda_wu)^{1/2}$ and $\mathrm{dist}_w(V,V')=\max_{|u|=1}|\sigma_u(V)-\sigma_u(V')|$. Consider a linear Gaussian model $Y_G=\Phi_G\theta+\varepsilon_G$ on $\mathbb{R}^D$ with prior $N(0,\Sigma_0)$, $\varepsilon_G\sim N(0,\mathrm{Id})$, posterior $\Pi_G$ and posterior covariance $V_Z$ given $Y_G$, with a coupling of $Z^{(N)}$ under $\mathbf P$ with $Y_G$; its first hypothesis in the nonlinear sufficiency gap bounds (catalog entry sufficiency_gap_beyond_the_linear_model) is $\sqrt N\,E\,\mathscr{W}_{1,w}\big(\Pi(\cdot\mid Z^{(N)}),\Pi_G(\cdot\mid Y_G)\big)\to0$.

Let some summary $S_N$ satisfy clauses (U1) and (U2) of the uniform Bernstein von Mises assumption: there are sets $\Theta_N$ with $\Pi(\Theta_N)\to1$ and $\theta_0\in\Theta_N$ for all large $N$ such that $\sup_{\vartheta\in\Theta_N}E^N_\vartheta\,\mathscr{W}_{1,H^{-k-2}}\big(\operatorname{Law}(\sqrt N(\theta-S_N)\mid Z^{(N)}),\mathcal{N}_\vartheta\big)\to0$, and these discrepancies are uniformly integrable under the prior predictive law. Let $\vartheta\mapsto\Sigma_D(\vartheta)$ be measurable. Then for every such linear Gaussian model and every coupling, $\sqrt N\,E\,\mathscr{W}_{1,w}\big(\Pi(\cdot\mid Z^{(N)}),\Pi_G(\cdot\mid Y_G)\big)\ge\sqrt{2/\pi}\int\mathrm{dist}_w\big(\Sigma_D(\vartheta),NV_Z\big)\,\mathrm{d}\Pi(\vartheta)-o(1)$, with an $o(1)$ that depends neither on the model nor on the coupling. Consequently: (i) if the prior does not depend on $N$, the first hypothesis holds for some Gaussian model only if $\Sigma_D$ is $\Pi$ almost surely constant; (ii) if $E^\Pi\|\theta\|_{H^\zeta}\to0$, as under the rescaled prior with $\gamma$ as in Nickl's theorem, and clause (U3) holds with $0\in\Theta_N$ for all $N$ (Lipschitz dependence of $T(\mathbb{I}^*_\vartheta\mathbb{I}_\vartheta)^{-1}$ and of $\mathcal{N}_\vartheta$ on $\vartheta\in\Theta_N$ in the $H^\zeta$ norm, with the moment and localization clauses stated in the catalog entry jiang_wong_under_bernstein_von_mises), then $\int\mathrm{dist}_w\big(\Sigma_D(\vartheta),\Sigma_D(0)\big)\,\mathrm{d}\Pi(\vartheta)\to0$, and the first hypothesis forces $NV_Z\to\Sigma_D(0)$, the inverse information at the prior mean read in the first $D$ coordinates; in particular a Gaussian model with $NV_Z\to\Sigma_D(\theta_0)$, the covariance of the Bernstein von Mises limit at the truth, satisfies it only if $\Sigma_D(\theta_0)=\Sigma_D(0)$.

Source: [`source/chapters/ext/m2c.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m2c.tex), label `m:prop:gapreq`.

<a id="sufficiency_gap_hypotheses_from_centering_clt"></a>

#### A sufficient condition for the nonlinear sufficiency gap hypotheses in terms of the centering

Lemma 15.44, page 263 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: conditional on Clauses (U1) to (U3) of the uniform Bernstein von Mises assumption (Assumption U, stated clause by clause in the entry jiang_wong_under_bernstein_von_mises) for the centering $S_N$, with the prior mean 0 in every localization set; the book does not prove them (Open Question 17.18, Uniformity)..

Statement. Let data $Z^{(N)}$, a prior $\Pi$, the joint law $\mathbf P$ of parameter and data, the Gaussian limits $\mathcal{N}_\vartheta=N(0,T(\mathbb{I}^*_\vartheta\mathbb{I}_\vartheta)^{-1})$ on the negative Sobolev space $H^{-k-2}$, the weighted norm $\|x\|_w^2=\sum_{j\le D}(1+\lambda_j)^{-k-2}x_j^2$ on the first $D$ coordinates in the Laplace eigenbasis, the distance $\mathscr{W}_{1,w}$, and the covariance $\Sigma_D(\vartheta)$ of the first $D$ coordinates under $\mathcal{N}_\vartheta$ be as in the catalog entry sufficiency_gap_admissible_gaussian_models, and let $P_D$ map $\theta$ to its first $D$ coordinates. Let a summary $S_N$ satisfy clauses (U1) to (U3) of the uniform Bernstein von Mises assumption (stated in the catalog entry jiang_wong_under_bernstein_von_mises) with $0\in\Theta_N$ for all $N$, and let $E^\Pi\|\theta\|_{H^\zeta}\to0$. Then for every statistic $S=S(Z^{(N)})$, $\mathbf E\,\mathscr{W}_{1,H^{-k-2}}\big(\operatorname{Law}(\sqrt N\theta\mid S),\operatorname{Law}(\sqrt NS_N\mid S)*\mathcal{N}_0\big)\to0$, where $*$ is convolution and $\mathcal{N}_0$ is the Gaussian limit at the prior mean $0$. Let a linear Gaussian model $Y_G=\Phi_G\theta_G+\varepsilon_G$ on $\mathbb{R}^D$, with prior $N(0,\Sigma_0)$, $\varepsilon_G\sim N(0,\mathrm{Id})$ and posterior covariance $V_Z$ given $Y_G$, satisfy $NV_Z\to\Sigma_D(0)$, write $m_G=E[\theta_G\mid Y_G]$, let $S_G=AY_G$ be a linear statistic, and let a coupling of $S$ under $\mathbf P$ with $S_G$ under the Gaussian model satisfy $E\,\mathscr{W}_{1,w}\big(\operatorname{Law}(\sqrt NP_DS_N\mid S),\operatorname{Law}(\sqrt Nm_G\mid S_G)\big)\to0$. Then it extends to a coupling of $(Z^{(N)},S)$ with $(Y_G,S_G)$ under which both hypotheses of the nonlinear sufficiency gap bounds hold: $\sqrt N\,E\,\mathscr{W}_{1,w}\big(\Pi(\cdot\mid Z^{(N)}),\Pi_G(\cdot\mid Y_G)\big)\to0$ and $\sqrt N\,E\,\mathscr{W}_{1,w}\big(\Pi(\cdot\mid S),\Pi_G(\cdot\mid S_G)\big)\to0$.

Source: [`source/chapters/ext/m2c.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m2c.tex), label `m:lem:gapred`.

<a id="two_coordinate_model_sufficiency_gap_depends_on_summary"></a>

#### A two coordinate model in which the sufficiency gap hypotheses depend on the summary

Proposition 15.45, page 264 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: counterexample, proved.

Statement. Let $\theta\in\mathbb{R}^2$ have the prior $N(0,s_N^2\mathrm{Id})$ with $s_N\to0$ and $Ns_N^2\to\infty$, and let $Y_i=G(\theta)+\varepsilon_i$, $i\le N$, with independent $\varepsilon_i\sim N(0,\mathrm{Id})$ and $G(\theta)=(\theta_1+\theta_2^2,\theta_2)$. The mean $X$ of the $Y_i$ is sufficient, $DG(\theta)$ has rows $(1,2\theta_2)$ and $(0,1)$, and $(DG(\theta)^\top DG(\theta))^{-1}$ has first diagonal entry $1+4\theta_2^2$. Let $\mathscr{W}_1$ be the Wasserstein distance of order one on $\mathbb{R}^2$ with the Euclidean norm and $\mathrm{dist}(V,V')=\max_{|u|=1}|(u^\top Vu)^{1/2}-(u^\top V'u)^{1/2}|$. A linear Gaussian model on $\mathbb{R}^2$ is $Y_G=\Phi_G\theta_G+\varepsilon_G$ with a prior $N(0,\Sigma_0)$ and $\varepsilon_G\sim N(0,\mathrm{Id})$, with posterior $\Pi_G$ and posterior covariance $V_Z$ given $Y_G$; for $\theta_\ast\in\mathbb{R}^2$ the Gaussian model at $\theta_\ast$ is $Y_G=\sqrt N\,DG(\theta_\ast)\theta_G+\varepsilon_G$ with the prior $N(0,s_N^2\mathrm{Id})$. For a statistic $S$ of $X$, a linear statistic $S_G$ of $Y_G$ and a coupling, the first hypothesis of the nonlinear sufficiency gap bounds is $\sqrt N\,E\,\mathscr{W}_1(\Pi(\cdot\mid X),\Pi_G(\cdot\mid Y_G))\to0$ and the second is $\sqrt N\,E\,\mathscr{W}_1(\Pi(\cdot\mid S),\Pi_G(\cdot\mid S_G))\to0$; those bounds hold in this setting with the same proof. Then:

(a) coupled through $\theta_G=\theta$ and $\varepsilon_G=\sqrt N(X-G(\theta))$, the Gaussian model at the prior mean $\theta_\ast=0$ satisfies the first hypothesis;

(b) for every linear Gaussian model on $\mathbb{R}^2$ and every coupling, $\liminf_N\sqrt N\,E\,\mathscr{W}_1(\Pi(\cdot\mid X),\Pi_G(\cdot\mid Y_G))\ge\sqrt{2/\pi}\,\liminf_N\mathrm{dist}(NV_Z,\mathrm{Id})$; for a point $\theta_0\in\mathbb{R}^2$ the Gaussian model at $\theta_\ast=\theta_0$ has $NV_Z\to(DG(\theta_0)^\top DG(\theta_0))^{-1}$, so it fails the first hypothesis whenever $\theta_{0,2}\ne0$, by at least $\sqrt{2/\pi}\,((1+4\theta_{0,2}^2)^{1/2}-1)$;

(c) let $S=X_1$, the first coordinate of the adjoint statistic $DG(0)^\top X$ at the prior mean, which is also the one step summary $\bar\theta+DG(\bar\theta)^{-1}(X-G(\bar\theta))$ from $\bar\theta=0$; if $\sqrt Ns_N^2\to\infty$, then for every linear Gaussian model on $\mathbb{R}^2$, every linear statistic $S_G$ and every coupling, $\sqrt N\,E\,\mathscr{W}_1(\Pi(\cdot\mid S),\Pi_G(\cdot\mid S_G))\to\infty$, and its ratio to $\sqrt Ns_N^2$ has $\liminf$ at least $c_\ast=\sup_{0<\tau\le1/2}\kappa_\tau/(2(1-\tau))$, where $\kappa_\tau=\big|\sqrt{2x_\tau/\pi}\,e^{-x_\tau/2}-\sqrt{2x_{1-\tau}/\pi}\,e^{-x_{1-\tau}/2}\big|$ and $x_\tau$ is the $\tau$ quantile of the $\chi^2_1$ law (numerically $c_\ast=0.1588$, attained near $\tau=0.204$);

(d) let $S'=X_1-X_2^2$, the first coordinate of the maximum likelihood estimator $G^{-1}(X)$, which is also the one step summary from any preliminary estimate with $\bar\theta_2=X_2$, and let $S_G=Y_{G,1}/\sqrt N$ in the Gaussian model at $\theta_\ast=0$, coupled as in (a); then $\sqrt N\,E\,\mathscr{W}_1(\Pi(\cdot\mid S'),\Pi_G(\cdot\mid S_G))\to0$, so both hypotheses hold for $S'$ with this model and coupling.

Source: [`source/chapters/ext/m2c.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m2c.tex), label `m:prop:gaptoy`.

<a id="effective_dimension_under_dissipation"></a>

#### Effective dimension under dissipation

Theorem 15.46, page 267 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: conditional on Part (ii) for a nonlinear forward map assumes the hypotheses of the book's Theorem 16.10 (Bernstein von Mises for the identity skip quantile generator), among them the uniform Bernstein von Mises assumption (Assumption U, open: Open Question 17.18), the whitened training residual assumption (U2') (the whitened training residuals $\mathcal{D}^{-1/2}\sqrt N(\theta^{(m)}-\hat S^{(m)}_N)$, $\mathcal{D}=\operatorname{diag}(1/\iota_j)$, split, conditionally i.i.d. given the data, into a part whose projections on unit vectors have sub Gaussian norms given the data bounded in probability uniformly over the unit vectors and whose conditional second moment matrix tends in operator norm to the whitened limit covariance $\mathrm{Id}+\Xi$, and a remainder whose conditional mean square norm tends to zero, all in $P^N_{\theta_0}$ probability; the book proves it for training parameters drawn from a proposal localized at the preliminary estimate, under the other hypotheses, and it fails in general for a nonlinear forward map when they are drawn from the prior) and the error bounds $\|\hat S_N-\theta_0\|_{L^2}=o_P(\tilde\delta_N(0))$, with $\tilde\delta_N(0)$ the posterior contraction rate in $L^2$, and $\|\hat S_N-\theta_0\|_{H^{\bar\gamma}}=o_P(1)$, $\bar\gamma\ge2$, on the summary, which the book leaves open for a nonlinear forward map other than reaction diffusion when the preliminary estimates have only the rates of the summary's definition; parts (i) and (iii) and the linear case of part (ii) assume nothing unproved..

Statement. Consider the heat equation, or the Stokes equation on divergence free fields, on the torus $\mathbb{T}^d=[0,1]^d$ with viscosity $\nu$, Laplace eigenpairs $(e_j,\lambda_j)$ with $\lambda_j=4\pi^2|k|^2$ for the $j$th lattice mode $k\in\mathbb{Z}^d\setminus\{0\}$, $N$ noisy observations of the solution at points uniform on $[0,T]\times\mathbb{T}^d$, per mode information $\iota_j=(1-e^{-2\nu\lambda_jT})/(2\nu\lambda_jT)$, and prior variances $\sigma^2_{0,j}=\rho^2(\lambda_j/\lambda_1)^{-\alpha}$ for the coefficients $\langle e_j,\theta\rangle$ of the initial condition. Define the effective dimension $J_{\rm eff}=\#\{j:N\iota_j\sigma^2_{0,j}\ge1\}$, the number of modes in which the data at least halve the prior variance. Then:

(i) $J_{\rm eff}=\#\{j:\lambda_j^{\alpha+1}\le c_jN\rho^2\lambda_1^\alpha/(2\nu T)\}$ with $c_j=1-e^{-2\nu\lambda_jT}\in[1-e^{-2\nu\lambda_1T},1]$; hence, as $\Lambda=(N\rho^2\lambda_1^\alpha/(2\nu T))^{1/(\alpha+1)}\to\infty$ with $\nu T\Lambda\ge1$, and with constants that depend only on $\alpha$, $d$ and $\rho$, $J_{\rm eff}\asymp(N\rho^2/(\nu T))^{d/(2(\alpha+1))}\asymp N^{d/(2\alpha+2)}(\nu T)^{-d/(2\alpha+2)}$. For $d=2$ this is $N^{1/(\alpha+1)}$, which for $\alpha=\gamma$ is the order of the dimension $J_N=N\delta_N^2=N^{1/(\gamma+1)}$, $\delta_N=N^{-\gamma/(2\gamma+d)}$, of the summary in Nickl's (2024) Bernstein von Mises theorem; at fixed $N$, viscosity or observation time reduces the effective dimension polynomially once $\nu T\ge\lambda_1^{-1}(2/(N\rho^2))^{1/\alpha}$, and for every $\nu T$ the count is at most $\#\{j:\lambda_j\le\lambda_1(N\rho^2)^{1/\alpha}\}$, because $\iota_j\le1$.

(ii) In the linear model (the model truncated to $D$ modes, $Y=\Phi\theta+\varepsilon$ with unit noise variance, prior covariance $\Sigma_0$ and posterior covariance $V_N=(\Phi^\top\Phi+\Sigma_0^{-1})^{-1}$), the identity skip generator, which adds to the summary a fixed linear map of standard Gaussian noise, is exact to leading order with the analytic scale $(N\iota_j+\sigma_{0,j}^{-2})^{-1/2}$, is exact with the scale $V_N^{1/2}$, and requires no training. For a nonlinear forward map whose information operator has the form $\mathbb{I}^*\mathbb{I}=\mathcal{L}^*\mathcal{L}+\mathcal{K}$, with $\mathcal{L}$ the Stokes (heat) solution operator and $\mathcal{K}$ compact and gaining two derivatives, assume the hypotheses of the book's Bernstein von Mises theorem for the identity skip quantile generator, namely Conditions 1 and 2 of Nickl (2024), the uniform Bernstein von Mises assumption for the one step summary $\hat S_N$, the whitened training residual assumption (U2'), the hypotheses under which $\hat S_N$ is $\sqrt N$ equivalent to the efficient centering, and error bounds on $\hat S_N$. Write the limit covariance on the first $J_N$ modes as $\Sigma=\mathcal{D}^{1/2}(\mathrm{Id}+\Xi)\mathcal{D}^{1/2}$ with $\mathcal{D}=\operatorname{diag}(1/\iota_j)$, where $\Xi$ is the compression to the first $J_N$ modes of the compact operator $\Xi_\infty=(\mathrm{Id}+K')^{-1}-\mathrm{Id}$, $K'=T^{-1}\mathcal{D}^{1/2}\mathcal{K}\mathcal{D}^{1/2}$, so that $\|\Xi P_{>J}\|_{op}\le\|\Xi_\infty P_{>J}\|_{op}\to0$ as $J\to\infty$ uniformly in $N$, with $P_{>J}$ the projection onto the modes $j>J$. The generator of that theorem is $\widehat G(s,U)=s+N^{-1/2}\mathcal{D}^{1/2}\hat C_M^{1/2}q(U)$, with $U$ uniform on $[0,1]^{J_N}$, $q$ the standard normal quantile function applied coordinatewise, and $\hat C_M$ the uncentered second moment matrix of the whitened training residuals $\mathcal{D}^{-1/2}\sqrt N(\theta^{(m)}-\hat S^{(m)}_N)$, $m\le M$. Given a cut $J'=J'_N\le J_N$ with $J'\to\infty$, the hybrid generator replaces the head $\hat C_M^{1/2}$ by $(\hat C^{\rm hyb}_M)^{1/2}$, where $\hat C^{\rm hyb}_M=\operatorname{diag}(\hat C^{J'}_M,\mathrm{Id})$ and $\hat C^{J'}_M$ is the second moment matrix of the first $J'$ whitened coordinates, so that it learns the correction to the analytic scale $\mathcal{D}^{1/2}$ on the first $J'$ modes only and uses the analytic scale beyond. Then $\|\hat C^{\rm hyb}_M-(\mathrm{Id}+\Xi)\|_{op}\le O_P\big(\sqrt{J'/M}+J'/M\big)+2\|\Xi_\infty P_{>J'}\|_{op}+o_P(1)$, and the conclusion of that theorem (the GBC posterior $\hat\Pi$ satisfies $\sqrt N\,\mathscr{W}_{1,H^{-k-2}}(\hat\Pi,\Pi_N)\to0$ in $P^N_{\theta_0}$ probability, $\Pi_N$ being the posterior and $\mathscr{W}_{1,H^{-k-2}}$ the Wasserstein distance of order one on the negative Sobolev space $H^{-k-2}$, together with the tail and moment condition (G2) of the book's transfer theorem) holds for the hybrid generator with $J'/M_N\to0$ in place of $J_N/M_N\to0$; with the cut $J'=\min(J_{\rm eff},J_N)$ it suffices that $J_{\rm eff}/M_N\to0$.

(iii) In the Gaussian experiment that observes $\theta_j+(N\iota_j)^{-1/2}\xi_j$ with independent standard normal $\xi_j$ and independent priors $\theta_j\sim N(0,\sigma^2_{0,j})$, a generator that reproduces the posterior center exactly but uses the prior spread for the modes $j>J'$ incurs a Wasserstein penalty, of order one in the Euclidean norm, of at most $\sqrt{2/\pi}\sum_{j>J'}\sigma_{0,j}\big(1-(1+N\iota_j\sigma^2_{0,j})^{-1/2}\big)\le\sqrt{1/(2\pi)}\sum_{j>J'}N\iota_j\sigma^3_{0,j}$, which decays like $(J')^{1-(3\alpha+2)/d}$ when the sum is replaced by its integral.

Source: [`source/chapters/ext/m2c.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m2c.tex), label `m:thm:jeff`.

<a id="sufficiency_versus_the_raw_data"></a>

#### Sufficiency versus the raw data: simulation cost of a generator trained without a summary

Theorem 15.47, page 269 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: conditional on The second claim (the hybrid generator trained on the sufficient statistic) assumes the hypotheses of part (ii) of the effective dimension theorem, which include those of the book's Theorem 16.10: the uniform Bernstein von Mises assumption (Assumption U, open: Open Question 17.18), the whitened training residual assumption (U2') (the whitened training residuals $\mathcal{D}^{-1/2}\sqrt N(\theta^{(m)}-\hat S^{(m)}_N)$, $\mathcal{D}=\operatorname{diag}(1/\iota_j)$, split, conditionally i.i.d. given the data, into a part whose projections on unit vectors have sub Gaussian norms given the data bounded in probability uniformly over the unit vectors and whose conditional second moment matrix tends in operator norm to the whitened limit covariance $\mathrm{Id}+\Xi$, and a remainder whose conditional mean square norm tends to zero, all in $P^N_{\theta_0}$ probability; the book proves it for training parameters drawn from a proposal localized at the preliminary estimate, under the other hypotheses, and it fails in general for a nonlinear forward map when they are drawn from the prior) and the error bounds $\|\hat S_N-\theta_0\|_{L^2}=o_P(\tilde\delta_N(0))$, with $\tilde\delta_N(0)$ the posterior contraction rate in $L^2$, and $\|\hat S_N-\theta_0\|_{H^{\bar\gamma}}=o_P(1)$, $\bar\gamma\ge2$, on the summary, which the book leaves open for a nonlinear forward map other than reaction diffusion when the preliminary estimates have only the rates of the summary's definition. The first claim, the lower bound on the number of simulations, is unconditional..

Statement. Let a generator be trained on $M$ i.i.d. simulated pairs to reproduce the conditional law of $\theta$ given the raw observation vector $Y\in\mathbb{R}^N$ (or $\mathbb{R}^{2N}$ for a vector field), with no summary, and let it be required to be accurate uniformly over the class $\mathcal{Q}_\beta(N)$ of conditional quantile maps $(\tau,s)\mapsto Q(\tau\mid s)$ on $[0,1]\times[0,1]^N$ that have Hölder norm of order $\beta$ at most one and are nondecreasing in $\tau$, the inputs having a law on $[0,1]^N$ with a Lebesgue density bounded above by $C_\mu$ and below by a positive constant. Then the number of simulations needed for $\sqrt N\,E\,\mathscr{W}_1(\hat\Pi,\Pi(\cdot\mid Y))\to0$, with $\hat\Pi$ the law the generator reports and $\mathscr{W}_1$ the Wasserstein distance of order one, satisfies $M\ge cN^{(2\beta+N)/(2\beta)}$ for all large $N$, where $c=C_\mu^{-1}$; the right side grows faster than any exponential in $N$. For the heat or Stokes model with prior variances $\sigma^2_{0,j}=\rho^2(\lambda_j/\lambda_1)^{-\alpha}$, viscosity $\nu$, observation window $[0,T]$ and effective dimension $J_{\rm eff}=\#\{j:N\iota_j\sigma^2_{0,j}\ge1\}\asymp N^{d/(2\alpha+2)}(\nu T)^{-d/(2\alpha+2)}$ (catalog entry effective_dimension_under_dissipation), the hybrid generator of part (ii) of that entry with the cut $\min(J_{\rm eff},J_N)$, trained on the sufficient statistic, which uses the Bernstein von Mises structure that the uniform class does not, satisfies the accuracy condition (G1), $\sqrt N\,\mathscr{W}_{1,H^{-k-2}}(\hat\Pi,\Pi_N)\to0$ in $P^N_{\theta_0}$ probability with $\Pi_N$ the posterior, as soon as $J_{\rm eff}/M\to0$, conditionally on the hypotheses of part (ii) of that entry, which include those of the book's Theorem 16.10 and the uniform Bernstein von Mises assumption.

Source: [`source/chapters/ext/m2c.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m2c.tex), label `m:thm:raw`.

### Chapter 16. Transfer, Generators and Localized Training

<a id="bvm_for_gbc"></a>

#### Transfer of Bernstein von Mises guarantees to the GBC posterior (BvM for GBC)

Theorem 16.2, page 275 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: proved.

Statement. Setting. Let $\Omega=[0,1]^d$ be the torus, $T>0$ and $\mathcal{X}=[0,T]\times\Omega$. The data are $Z^{(N)}=(Y_i,X_i)_{i\le N}$ with $Y_i=u_\theta(X_i)+\varepsilon_i$, where $u_\theta=\mathscr{G}(\theta)$ solves an evolution equation with initial condition $\theta$, the $X_i$ are i.i.d. uniform on $\mathcal{X}$ and the $\varepsilon_i\sim N(0,I_W)$ are independent of them. Let $(e_j)$ be the Laplace eigenbasis, with eigenvalues $\lambda_j\asymp j^{2/d}$; let the prior $\Pi$ be the law of $(\sqrt N\delta_N)^{-1}\sum_j\lambda_j^{-\gamma/2}g_je_j$ with $g_j$ i.i.d. $N(0,1)$ and $\delta_N=N^{-\gamma/(2\gamma+d)}$; let $\Pi_N=\Pi(\cdot\mid Z^{(N)})$ be the posterior, $\theta_0$ the true initial condition and $P^N_{\theta_0}$ the law of the data. Let $\mathbb{I}_{\theta_0}$ be the linearization of $\mathscr{G}$ at $\theta_0$ and $\mathcal{N}_{\theta_0}=N(0,T(\mathbb{I}^*_{\theta_0}\mathbb{I}_{\theta_0})^{-1})$. Assume Conditions 1 and 2 of Nickl (2024): the prior above and, for the forward map on Sobolev balls, (A) uniform $L^\infty$ bounds, (B) $L^2$ Lipschitz continuity, (C) a linearization $\mathbb{I}_{\theta_0}$ with quadratic remainder, (D) $L^\infty$ mapping properties from $H^\zeta$ with $\zeta>d/2$, (E) the stability estimate $\|\mathscr{G}(\theta)-\mathscr{G}(\theta_0)\|_{L^2(\mathcal{X})}\ge c\|\theta-\theta_0\|_{H^{-1}}$ and (F) invertibility of the information operator ($\Delta\mathbb{I}^*_{\theta_0}\mathbb{I}_{\theta_0}$ a homeomorphism of $H^\eta_0$ for $\eta\ge\eta_0$), with integer $\gamma>\max(3\zeta+3d/2+2,\eta_0)$ and $k>\max(\zeta+5d/2,\eta_0)$.

Accuracy conditions. Let $\mathscr{W}_1$ be the Wasserstein distance of order one on $H^{-k-2}(\Omega)$. Let $\bar\gamma$ be the Sobolev index of the localization ball, chosen as in the proofs of Nickl (2024) and of Konen and Nickl (2026) in $\max(2,2\zeta)<\bar\gamma<\gamma-\max(1,d/2)$; put $\tilde\delta_N(\xi)=\delta_N^{(\bar\gamma-\xi)/(\bar\gamma+1)}$, $\bar\Theta_{N,L}=\{\|\theta\|_{H^{\bar\gamma}}\le L\}\cap\{\|\theta-\theta_0\|_{H^\xi}\le L\tilde\delta_N(\xi)\ \text{for all}\ 0\le\xi<\bar\gamma\}$, and $q=4$ in the setting of Theorem 1 of Nickl (2024), $q=4\bar\gamma$ in that of Theorem 1.1 of Konen and Nickl (2026). Let $\widehat\Pi_N$ be the GBC posterior (the law of the generator's output at the observed data, a measurable function of $Z^{(N)}$ and of simulation randomness drawn independently of $Z^{(N)}$) and $\hat\theta^{G}_N$ its mean. Assume that, in $P^N_{\theta_0}$ probability as $N\to\infty$: (G1) $\sqrt N\,\mathscr{W}_1(\widehat\Pi_N,\Pi_N)\to0$; (G2) for some $b>0$ and $L$, $\widehat\Pi_N(\bar\Theta_{N,L}^c)\le e^{-bN\delta_N^2}$ and $\mathbb{E}^{\widehat\Pi_N}\|\theta\|^q_{H^{\bar\gamma}}=O_P(1)$.

Then:
(i) $\mathscr{W}_1\big(\operatorname{Law}(\sqrt N(\theta-\hat\theta^{G}_N)\mid\theta\sim\widehat\Pi_N),\mathcal{N}_{\theta_0}\big)\to0$ in $P^N_{\theta_0}$ probability, and $\sqrt N(\hat\theta^{G}_N-\theta_0)\to\mathcal{N}_{\theta_0}$ in distribution in $H^{-k-2}$.
(ii) If in addition the forward map satisfies the hypotheses of Theorem 1 of Nickl (2024) (the reaction diffusion equation $\partial_tu-\Delta u=f(u)$ with $f\in C^\infty_c(\mathbb{R})$, $d\le3$, integer $\gamma>2+3d$ and $\theta_0$ smooth, with $\mathscr{C}=C([t_{\min},t_{\max}],C(\Omega))$ for $0<t_{\min}<t_{\max}<\infty$) or of Theorem 1.1 of Konen and Nickl (2026) (the two dimensional Navier Stokes equations, with the space of trajectories $\mathscr{C}$ of that theorem), and $\mu$ is the law in $\mathscr{C}$ of the solution $U$ of the equation linearized at $u_{\theta_0}$ with $U(0)\sim\mathcal{N}_{\theta_0}$, then $\mathscr{W}_{1,\mathscr{C}}\big(\operatorname{Law}(\sqrt N(u_\theta-u_{\hat\theta^{G}_N})\mid\theta\sim\widehat\Pi_N),\mu\big)\to0$ in probability and $\sqrt N(u_{\hat\theta^{G}_N}-u_{\theta_0})\to\mu$ in distribution in $\mathscr{C}$.
(iii) Under (ii), for $\Phi:\mathscr{C}\to\mathbb{B}$ Hadamard differentiable into a Banach space $\mathbb{B}$, $\sqrt N(\Phi(u_{\hat\theta^{G}_N})-\Phi(u_{\theta_0}))\to\dot\Phi_{u_{\theta_0}}[U]$ in distribution, $U\sim\mu$, and the GBC credible band $C^{G}_N=\{u\in\mathscr{C}:\|u-u_{\hat\theta^{G}_N}\|_{\mathscr{C}}\le R_N\}$, with $R_N$ the $1-\beta$ quantile of $\|u_\theta-u_{\hat\theta^{G}_N}\|_{\mathscr{C}}$ under $\theta\sim\widehat\Pi_N$, satisfies $P^N_{\theta_0}(u_{\theta_0}\in C^{G}_N)\to1-\beta$, and $\sqrt N R_N\to c>0$.
(iv) In the Navier Stokes case of (ii), let $\theta_{N,h}=\theta_0+h/\sqrt N$, and let $\dot H^{\infty}_\diamond$ be the smooth, divergence free, mean zero vector fields on the torus. For every $h\in\dot H^{\infty}_\diamond$, under $P^N_{\theta_{N,h}}$, $\sqrt N(\hat\theta^{G}_N-\theta_{N,h})\to\mathcal{N}_{\theta_0}$ in distribution in $H^{-k-2}$ and $\sqrt N(u_{\hat\theta^{G}_N}-u_{\theta_{N,h}})\to\mu$ in distribution in $\mathscr{C}$; that is, $u_{\hat\theta^{G}_N}$ is a regular estimator sequence of the state at $\theta_0$ whose limit law $\mu$ attains the bound of Theorem 1.2 of Konen and Nickl (2026) (Theorem 2.10 there for a general $\Phi$). Consequently, with $\Phi$ as in (iii) and $\Phi=\operatorname{Id}$ permitted, $\Phi(u_{\hat\theta^{G}_N})$ is efficient among regular estimator sequences by the convolution theorem, and for every bounded, continuous, subconvex loss $\ell:\mathbb{B}\to[0,\infty)$ it attains the local asymptotic minimax bound:
$$\sup_{J\subset\dot H^{\infty}_\diamond,\ |J|<\infty}\ \liminf_{N\to\infty}\ \max_{h\in J}\ \mathbb{E}^N_{\theta_{N,h}}\,\ell\Big(\sqrt N\big(\Phi(u_{\hat\theta^{G}_N})-\Phi(u_{\theta_{N,h}})\big)\Big)=\mathbb{E}\,\ell\big(\dot\Phi_{u_{\theta_0}}[U]\big),\qquad U\sim\mu.$$

Source: [`source/chapters/ext/m3a.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m3a.tex), label `m:thm:main`.

<a id="solve_then_simulate_equals_simulate_the_limit"></a>

#### Solve then simulate equals simulate the limit: tangent linear forward simulation of GBC draws

Corollary 16.4, page 280 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: conditional on Only the plug in bound of the second part is conditional: its proof uses the set $\Theta_N$ and the Lipschitz clause (U3) of the uniform Bernstein von Mises assumption (Assumption U, stated clause by clause in the entry jiang_wong_under_bernstein_von_mises), which the book does not prove; the first part, and the rate for the GBC mean in the Sobolev norm of Condition 2D, whose proof uses only the transfer theorem and the moment clause of (G2), need only the hypotheses of the transfer theorem..

Statement. Let $\widehat\Pi_N$ be a GBC posterior with mean $\hat\theta^{G}_N$ that satisfies the hypotheses of part (ii) of the transfer theorem (catalog entry bvm_for_gbc): data $Y_i=u_\theta(X_i)+\varepsilon_i$ on $\mathcal{X}=[0,T]\times\Omega$ with Nickl's rescaled Gaussian series prior and posterior $\Pi_N$, Conditions 1 and 2 of Nickl (2024) with integer $\gamma>\max(3\zeta+3d/2+2,\eta_0)$ and $k>\max(\zeta+5d/2,\eta_0)$, the accuracy conditions (G1) $\sqrt N\,\mathscr{W}_{1,H^{-k-2}}(\widehat\Pi_N,\Pi_N)\to0$ and (G2) (mass at most $e^{-bN\delta_N^2}$ off the localization set and $\mathbb{E}^{\widehat\Pi_N}\|\theta\|^q_{H^{\bar\gamma}}=O_P(1)$, with $\bar\gamma$, $\delta_N$ and $q$ as in that entry), and the hypotheses of Theorem 1 of Nickl (2024) (reaction diffusion) or of Theorem 1.1 of Konen and Nickl (2026) (two dimensional Navier Stokes), with $\mathscr{C}$ the space of trajectories of those theorems. Let $\mathbb{I}_\vartheta$ be the linearization of $\theta\mapsto u_\theta$ at $\vartheta$, $\mathcal{N}_\vartheta=N(0,T(\mathbb{I}^*_\vartheta\mathbb{I}_\vartheta)^{-1})$, and let $\mu$ be the law of the solution of the tangent linear equation linearized at $u_{\theta_0}$ with initial datum drawn from $\mathcal{N}_{\theta_0}$. Then the law of $\sqrt N(u_\theta-u_{\hat\theta^{G}_N})$ obtained by pushing $\theta\sim\widehat\Pi_N$ through the nonlinear solver and the law $\mu$ obtained by pushing $\mathcal{N}_{\theta_0}$ through the tangent linear equation are asymptotically equal in $\mathscr{W}_{1,\mathscr{C}}$.

Suppose in addition that Assumption U (uniform Bernstein von Mises) holds with a set $\Theta_N$ that contains $\hat\theta^{G}_N$ with probability tending to one: for the summary $S_N$, (U1) $\Pi(\Theta_N)\to1$, $\theta_0\in\Theta_N$ for all large $N$ and $\sup_{\vartheta\in\Theta_N}\mathbb{E}^N_\vartheta\,\mathscr{W}_{1,H^{-k-2}}\big(\operatorname{Law}(\sqrt N(\theta-S_N)\mid Z^{(N)}),\mathcal{N}_\vartheta\big)\to0$; (U2) these discrepancies are uniformly integrable under the prior predictive law; (U3) $\vartheta\mapsto T(\mathbb{I}^*_\vartheta\mathbb{I}_\vartheta)^{-1}$ is Lipschitz from $(\Theta_N,\|\cdot\|_{H^\zeta})$ into bounded operators $H^{-k-2}\to H^{-k-4}$ and $\vartheta\mapsto\mathcal{N}_\vartheta$ is Lipschitz from $(\Theta_N,\|\cdot\|_{H^\zeta})$ into the laws on $H^{-k-2}$ with the distance $\mathscr{W}_{1,H^{-k-2}}$, with constants free of $N$, the first moments $m_1(\vartheta)=\int\|x\|_{H^{-k-2}}\,\mathrm{d}\mathcal{N}_\vartheta(x)$ satisfy $\int_{\Theta_N^c}m_1\,\mathrm{d}\Pi\to0$ and $\Pi(\Theta_N^c)\sup_{\Theta_N}m_1\to0$, $S_N\in\Theta_N$ with probability tending to one and $\mathbb{E}^\Pi[\|\theta-S_N\|_{H^\zeta}\mid S_N]\to0$; (U4) for every $\theta_0\in\Theta_N$, $\mathbb{E}\big[\mathscr{W}_{1,H^{-k-2}}\big(\operatorname{Law}(\sqrt N(\theta-S_N)\mid Z^{(N)}),\mathcal{N}_{\theta_0}\big)\mid S_N\big]\to0$ in $P^N_{\theta_0}$ probability. Suppose also that, for the index $\zeta>d/2$ of Condition 2D of Nickl (2024), $\vartheta\mapsto\mathbb{I}_\vartheta$ is Lipschitz from an $H^\zeta$ ball about $\theta_0$ into the bounded operators $H^{-k-2}\to\mathscr{C}$. Then
$$\varrho_N:=\|\hat\theta^{G}_N-\theta_0\|_{H^\zeta}=O_P\big(N^{-(\bar\gamma-\zeta)/(2(\bar\gamma+k+2))}\big)\to0,$$
and, writing $U^\vartheta$ for the solution of the tangent equation linearized at $u_\vartheta$ with initial datum drawn from $\mathcal{N}_\vartheta$ (so that $U^{\theta_0}$ has law $\mu$), the forward simulation step may replace the nonlinear solves by the tangent equation linearized at $\hat\theta^{G}_N$ with initial law $N(0,T(\mathbb{I}^*_{\hat\theta^{G}_N}\mathbb{I}_{\hat\theta^{G}_N})^{-1}/N)$, with plug in error
$$\mathscr{W}_{1,\mathscr{C}}\Big(\operatorname{Law}\big(\sqrt N(u_\theta-u_{\hat\theta^{G}_N})\mid\theta\sim\widehat\Pi_N\big),\ \operatorname{Law}\big(U^{\hat\theta^{G}_N}\big)\Big)\le o_P(1)+C\varrho_N,$$
where $C$ depends only on the Lipschitz constant of $\vartheta\mapsto\mathbb{I}_\vartheta$, on the Lipschitz constant of $\vartheta\mapsto\mathcal{N}_\vartheta$ in $\mathscr{W}_{1,H^{-k-2}}$ from (U3), on the norm of $\mathbb{I}_{\theta_0}:H^{-k-2}\to\mathscr{C}$ and on the first moment of $\mathcal{N}_{\theta_0}$ in $H^{-k-2}$.

Source: [`source/chapters/ext/m3a.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m3a.tex), label `m:cor:commute`.

<a id="bernstein_von_mises_for_the_identity_skip_quantile_generator"></a>

#### Bernstein von Mises for the identity skip Gaussian head quantile generator, conditional on the uniform hypothesis

Theorem 16.10, page 285 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: conditional on Assumption U (uniform Bernstein von Mises) for the one step summary, clause (U4) included, which the book states as open (Open Question Uniformity); Assumption (U2') on the whitened training residuals, which the book proves for localized training proposals (catalog entry whitened_residual_assumption_under_a_localized_proposal) and which fails in general for training parameters drawn from the prior when the forward map is nonlinear; and the bounds on the error of the summary (smaller order than the localization rate in L2 and tending to zero in the Sobolev norm of the localization ball), which the same open question asks for..

Statement. Setting. Data $Y_i=u_\theta(X_i)+\varepsilon_i$, $i\le N$, with $X_i$ i.i.d. uniform on $\mathcal{X}=[0,T]\times\Omega$, $\Omega=[0,1]^d$ the torus, $\varepsilon_i\sim N(0,I_W)$ independent, $u_\theta$ the solution of an evolution equation with initial condition $\theta$; $(e_j)$ the Laplace eigenbasis with eigenvalues $\lambda_j\asymp j^{2/d}$; the prior $\Pi$ the law of $(\sqrt N\delta_N)^{-1}\sum_j\lambda_j^{-\gamma/2}g_je_j$, $g_j$ i.i.d. $N(0,1)$, $\delta_N=N^{-\gamma/(2\gamma+d)}$; $\Pi_N$ the posterior, $\theta_0$ the truth, $P^N_{\theta_0}$ the law of the data $Z^{(N)}$; $\mathbb{I}_\vartheta$ the linearization of $\theta\mapsto u_\theta$ at $\vartheta$ and $\mathcal{N}_\vartheta=N(0,T(\mathbb{I}^*_\vartheta\mathbb{I}_\vartheta)^{-1})$. Assume Conditions 1 and 2 of Nickl (2024) (as in catalog entry bvm_for_gbc) with integer $\gamma>\max(3\zeta+3d/2+2,\eta_0)$ and $k>\max(\zeta+5d/2,\eta_0)$, $\zeta>d/2$ the index of Condition 2D; let $\bar\gamma$ satisfy $\max(2,2\zeta)<\bar\gamma<\gamma-\max(1,d/2)$ and $\tilde\delta_N(\xi)=\delta_N^{(\bar\gamma-\xi)/(\bar\gamma+1)}$.

Summary and generator. Let $J=J_N\asymp N\delta_N^2$, $p_N$ the projection onto the first $J$ modes, and $\hat S_N\in\mathbb{R}^J$ the cross fitted one step efficient score summary: the sample is split into halves $\mathcal{I}_1,\mathcal{I}_2$, preliminary estimates $\bar\theta^{[b]}_N$ computed from half $b$ satisfy $\|\bar\theta^{[b]}_N-\theta_0\|_{H^\xi}=O_P(\tilde\delta_N(\xi))$ for $0\le\xi\le\bar\gamma$, and $\hat S_{N,j}=\frac12\sum_{b=1,2}\big[\langle e_j,\bar\theta^{[b]}_N\rangle+|\mathcal{I}_{3-b}|^{-1}\sum_{i\in\mathcal{I}_{3-b}}\langle\mathbb{I}_{\bar\theta^{[b]}_N}p_N(T(\mathbb{I}^*_{\bar\theta^{[b]}_N}\mathbb{I}_{\bar\theta^{[b]}_N})^{-1}e_j)(X_i),Y_i-u_{\bar\theta^{[b]}_N}(X_i)\rangle_W\big]$ for $j\le J$. Let $\mathcal{D}=\operatorname{diag}(1/\iota_j)=T(\mathcal{L}^*\mathcal{L})^{-1}$ be the information diagonal of the heat (or Stokes) solution operator $\mathcal{L}$, $\iota_j=(1-e^{-2\nu\lambda_jT})/(2\nu\lambda_jT)$, and write $\Sigma=T(\mathbb{I}^*_{\theta_0}\mathbb{I}_{\theta_0})^{-1}$ restricted to the first $J$ modes as $\Sigma=\mathcal{D}^{1/2}(\operatorname{Id}+\Xi)\mathcal{D}^{1/2}$. From $M$ simulated pairs $(\theta^{(m)},Z^{(m)})$ with summaries $\hat S^{(m)}_N$ form the whitened residuals $W^{(m)}=\mathcal{D}^{-1/2}\sqrt N(\theta^{(m)}-\hat S^{(m)}_N)\in\mathbb{R}^J$ and $\hat C_M=M^{-1}\sum_mW^{(m)}W^{(m)\top}$, and let $\widehat G(s,U)=s+N^{-1/2}\mathcal{D}^{1/2}\hat C_M^{1/2}\Phi^{-1}(U)$, $U\sim\mathrm{Unif}[0,1]^J$, with $\Phi^{-1}$ the standard normal quantile function applied coordinatewise; the GBC posterior $\widehat\Pi_N$ is the law of $\widehat G(\hat S_N,U)$ given the data and the training sample, that is $N(\hat S_N,N^{-1}\mathcal{D}^{1/2}\hat C_M\mathcal{D}^{1/2})$.

Hypotheses. (a) Assumption U with $S_N=\hat S_N$, clause (U4) included: there is a set $\Theta_N$ with (U1) $\Pi(\Theta_N)\to1$, $\theta_0\in\Theta_N$ for all large $N$ and $\sup_{\vartheta\in\Theta_N}\mathbb{E}^N_\vartheta\,\mathscr{W}_{1,H^{-k-2}}\big(\operatorname{Law}(\sqrt N(\theta-S_N)\mid Z^{(N)}),\mathcal{N}_\vartheta\big)\to0$; (U2) these discrepancies are uniformly integrable under the prior predictive law; (U3) $\vartheta\mapsto T(\mathbb{I}^*_\vartheta\mathbb{I}_\vartheta)^{-1}$ is Lipschitz from $(\Theta_N,\|\cdot\|_{H^\zeta})$ into bounded operators $H^{-k-2}\to H^{-k-4}$ and $\vartheta\mapsto\mathcal{N}_\vartheta$ is Lipschitz from $(\Theta_N,\|\cdot\|_{H^\zeta})$ into the laws on $H^{-k-2}$ with $\mathscr{W}_{1,H^{-k-2}}$, with constants free of $N$, the first moments $m_1(\vartheta)=\int\|x\|_{H^{-k-2}}\,\mathrm{d}\mathcal{N}_\vartheta(x)$ satisfy $\int_{\Theta_N^c}m_1\,\mathrm{d}\Pi\to0$ and $\Pi(\Theta_N^c)\sup_{\Theta_N}m_1\to0$, $S_N\in\Theta_N$ with probability tending to one and $\mathbb{E}^\Pi[\|\theta-S_N\|_{H^\zeta}\mid S_N]\to0$; (U4) for every $\theta_0\in\Theta_N$, $\mathbb{E}\big[\mathscr{W}_{1,H^{-k-2}}\big(\operatorname{Law}(\sqrt N(\theta-S_N)\mid Z^{(N)}),\mathcal{N}_{\theta_0}\big)\mid S_N\big]\to0$ in $P^N_{\theta_0}$ probability. (b) Assumption (U2'): $W^{(m)}=W^{(m)}_{g}+W^{(m)}_{r}$ with the pairs $(W^{(m)}_{g},W^{(m)}_{r})$ i.i.d. given $Z^{(N)}$, $\varkappa_N=\sup_{\|v\|_2=1}\|\langle v,W^{(m)}_{g}\rangle\|_{\psi_2\mid Z^{(N)}}=O_P(1)$ under $P^N_{\theta_0}$, where $\|\chi\|_{\psi_2\mid Z^{(N)}}=\inf\{K>0:\mathbb{E}[e^{\chi^2/K^2}\mid Z^{(N)}]\le2\}$, and, in $P^N_{\theta_0}$ probability, $\mathbb{E}[\|W^{(m)}_{r}\|_2^2\mid Z^{(N)}]\to0$ and $\|\mathbb{E}[W^{(m)}_{g}W^{(m)\top}_{g}\mid Z^{(N)}]-(\operatorname{Id}+\Xi)\|_{op}\to0$. (c) The hypotheses of the equivalence of the one step summary with the efficient centering (catalog entry equivalence_with_the_efficient_centering), its two conditions on the exponents included: $\sqrt N\,\tilde\delta_N(0)\tilde\delta_N(\zeta)\to0$, $\gamma<(\bar\gamma+1)(\kappa-d/2)$ for some $2d+\zeta<\kappa<k-d/2$ unless $\mathbb{I}^*_{\theta_0}\mathbb{I}_{\theta_0}$ is diagonal in $(e_j)$ or the preliminary estimates converge at the rate $\delta_N$ in $H^{-1}$, and, for every $B>0$, a constant $L(B)$ with $\|\mathbb{I}_\vartheta p_N(T(\mathbb{I}^*_\vartheta\mathbb{I}_\vartheta)^{-1}e_j)-\mathbb{I}_{\theta_0}p_N(T(\mathbb{I}^*_{\theta_0}\mathbb{I}_{\theta_0})^{-1}e_j)\|_{L^2(\mathcal{X})}\le L(B)\|\vartheta-\theta_0\|_{H^\zeta}\|e_j\|_{H^{\kappa+2}}$ for all $\vartheta$ with $\|\vartheta\|_{H^{\bar\gamma}}\le B$ and all $j\le J_N$. (d) $\|\hat S_N-\theta_0\|_{L^2}=o_P(\tilde\delta_N(0))$ and $\|\hat S_N-\theta_0\|_{H^{\bar\gamma}}=o_P(1)$.

Conclusion. If $M=M_N$ satisfies $J_N/M_N\to0$, then $\sqrt N\,\mathscr{W}_{1,H^{-k-2}}(\widehat\Pi_N,\Pi_N)\to0$ in $P^N_{\theta_0}$ probability (condition (G1) of the transfer theorem) and condition (G2) of that theorem holds (mass at most $e^{-bN\delta_N^2}$ off the localization set and $\mathbb{E}^{\widehat\Pi_N}\|\theta\|^q_{H^{\bar\gamma}}=O_P(1)$). Consequently the conclusions of the transfer theorem (catalog entry bvm_for_gbc) hold for the GBC posterior produced by this generator, those of its parts (ii) to (iv) under the additional hypotheses stated there.

Source: [`source/chapters/ext/m3b.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m3b.tex), label `m:thm:qnnA`.

<a id="no_uniform_guarantee_for_quantile_generators"></a>

#### No uniform guarantee: minimax lower bound for conditional quantile generators over monotone Hölder classes

Theorem 16.15, page 290 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: proved.

Statement. For $\beta>0$ and $J\in\mathbb{N}$ let $\mathcal{Q}_\beta(J)$ be the set of maps $(\tau,s)\mapsto Q(\tau\mid s)$ from $[0,1]\times[0,1]^J$ to $\mathbb{R}$ such that (i) $\|Q\|_{C^\beta}\le1$, where, with $\ell$ the largest integer strictly below $\beta$, $\|Q\|_{C^\beta}=\max_{|\alpha|\le\ell}\|\partial^\alpha Q\|_\infty+\max_{|\alpha|=\ell}\sup_{z\ne z'}|\partial^\alpha Q(z)-\partial^\alpha Q(z')|/\|z-z'\|_2^{\beta-\ell}$, the maxima running over multi indices on $\mathbb{R}^{1+J}$; (ii) $\tau\mapsto Q(\tau\mid s)$ is nondecreasing for every $s$. Let $P_{Q,s}=Q(\cdot\mid s)_\#\mathrm{Unif}[0,1]$ be the law that $Q$ encodes at $s$ and $\mathscr{W}_{1,\mathbb{R}}$ the Wasserstein distance of order one on the line. The training sample consists of $M$ i.i.d. copies of $(S,\theta)$ with $S\sim\mu$ and $\theta\mid S\sim P_{Q,S}$, where the design law $\mu$ on $[0,1]^J$ has a Lebesgue density bounded above by $C_\mu$ and below by $c_\mu>0$ (so $C_\mu\ge1$). A generator is any measurable, possibly randomized, map $\hat P_M$ from the training sample and a summary value $s$ to a probability measure $\hat P_M(\cdot\mid s)$ on $\mathbb{R}$.

Let $\beta>0$, $J\ge1$, and let $s_0\in[0,1]^J$ be at Euclidean distance at least $1/8$ from the boundary. There is a constant $c=c(\beta)>0$, depending only on $\beta$ and on two fixed profile functions, and in particular not on $J$, such that for every $M\ge1$ and every generator $\hat P_M$,
$$\sup_{Q\in\mathcal{Q}_\beta(J)}P\Big(\mathscr{W}_{1,\mathbb{R}}\big(\hat P_M(\cdot\mid s_0),P_{Q,s_0}\big)\ge c\,(C_\mu M)^{-\beta/(2\beta+J)}\Big)\ge\frac18,$$
the probability being over the $M$ training pairs, and consequently
$$\inf_{\hat P_M}\ \sup_{Q\in\mathcal{Q}_\beta(J)}\mathbb{E}\,\mathscr{W}_{1,\mathbb{R}}\big(\hat P_M(\cdot\mid s_0),P_{Q,s_0}\big)\ge\frac c8\,(C_\mu M)^{-\beta/(2\beta+J)}.$$
Consequently, if a GBC generator trained on $M_N$ pairs is required to satisfy the accuracy condition (G1) of the transfer theorem at the summary value $s_0$ uniformly over $\mathcal{Q}_\beta(J_N)$, that is, if $\sqrt N\,\mathscr{W}_{1,\mathbb{R}}(\hat P_{M_N}(\cdot\mid s_0),P_{Q,s_0})\to0$ in probability is to hold for every conditional quantile map in the class (reading this as (G1), which compares with the posterior given all the data, uses the asymptotic sufficiency of the summary and so Assumption U of the book), then necessarily $\sqrt N\,(C_\mu M_N)^{-\beta/(2\beta+J_N)}\to0$, hence
$$M_N\ge C_\mu^{-1}N^{(2\beta+J_N)/(2\beta)}=C_\mu^{-1}N^{1+J_N/(2\beta)}\qquad\text{for all large }N,$$
which grows faster than any polynomial in $N$ as soon as $J_N\to\infty$.

Source: [`source/chapters/ext/m3b.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m3b.tex), label `m:thm:qnnB`.

<a id="quantile_generator_exponent_attained_for_beta_at_most_one"></a>

#### The minimax exponent for conditional quantile generators is attained for Hölder smoothness at most one (histogram generator)

Proposition 16.16, page 293 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: proved.

Statement. For $\beta>0$ and $J\in\mathbb{N}$ let $\mathcal{Q}_\beta(J)$ be the set of maps $(\tau,s)\mapsto Q(\tau\mid s)$ from $[0,1]\times[0,1]^J$ to $\mathbb{R}$ with $C^\beta$ norm at most one (for $\beta\le1$, $\|Q\|_\infty+\sup_{z\ne z'}|Q(z)-Q(z')|/\|z-z'\|_2^\beta\le1$ on $[0,1]^{1+J}$) that are nondecreasing in $\tau$ for every $s$; let $P_{Q,s}=Q(\cdot\mid s)_\#\mathrm{Unif}[0,1]$, let $\mathscr{W}_{1,\mathbb{R}}$ be the Wasserstein distance of order one on the line, and let the training pairs $(S^{(i)},\theta^{(i)})$, $i\le M$, be i.i.d. with $S\sim\mu$ and $\theta\mid S\sim P_{Q,S}$, where $\mu$ has a Lebesgue density on $[0,1]^J$ bounded below by $c_\mu>0$ and above by $C_\mu$.

Let $\beta\in(0,1]$, partition $[0,1]^J$ into $m^J$ cubes of side $h=1/m$ with $m=\max\{1,\lfloor M^{1/(2\beta+J)}\rfloor\}$, and let $\hat P_M(\cdot\mid s)$ be the empirical law of $\{\theta^{(i)}:S^{(i)}\in B(s)\}$, where $B(s)$ is the cube containing $s$, and any fixed law on $[-1,1]$ if that cube contains no $S^{(i)}$. Then
$$\sup_{Q\in\mathcal{Q}_\beta(J)}\ \sup_{s\in[0,1]^J}\ \mathbb{E}\,\mathscr{W}_{1,\mathbb{R}}\big(\hat P_M(\cdot\mid s),P_{Q,s}\big)\le C(\beta,c_\mu)\,J^{\beta/2}\,M^{-\beta/(2\beta+J)},$$
with $C(\beta,c_\mu)$ depending only on $\beta$ and $c_\mu$. In particular, at fixed $\beta$ and $J$ a single explicit estimator has risk $O(M^{-\beta/(2\beta+J)})=o(M^{-\beta/(2\beta+J+1)})$, so no lower bound with the exponent $\beta/(2\beta+J+1)$ and a positive constant can hold: it is the summary dimension, and not the summary dimension plus one, that governs the problem.

Source: [`source/chapters/ext/m3b.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m3b.tex), label `m:prop:qnnUB`.

<a id="quantile_generator_exponent_attained_for_beta_between_one_and_two"></a>

#### The minimax exponent for conditional quantile generators is attained for smoothness between one and two by jittered local linear quantile regression

Proposition 16.19, page 295 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: proved.

Statement. For $\beta>0$ and $J\in\mathbb{N}$ let $\mathcal{Q}_\beta(J)$ be the set of maps $(\tau,s)\mapsto Q(\tau\mid s)$ from $[0,1]\times[0,1]^J$ to $\mathbb{R}$ with $\|Q\|_{C^\beta}\le1$, where, with $\ell$ the largest integer strictly below $\beta$, $\|Q\|_{C^\beta}=\max_{|\alpha|\le\ell}\|\partial^\alpha Q\|_\infty+\max_{|\alpha|=\ell}\sup_{z\ne z'}|\partial^\alpha Q(z)-\partial^\alpha Q(z')|/\|z-z'\|_2^{\beta-\ell}$ (maxima over multi indices on $\mathbb{R}^{1+J}$), and with $\tau\mapsto Q(\tau\mid s)$ nondecreasing for every $s$. Let $P_{Q,s}=Q(\cdot\mid s)_\#\mathrm{Unif}[0,1]$, $\mathscr{W}_{1,\mathbb{R}}$ the Wasserstein distance of order one on the line, and let the training pairs $(S^{(i)},\theta^{(i)})$, $i\le M$, be i.i.d. with $S\sim\mu$ and $\theta\mid S\sim P_{Q,S}$, where $\mu$ has a Lebesgue density on $[0,1]^J$ between $c_\mu>0$ and $C_\mu$. Let $s_0\in[0,1]^J$ be at Euclidean distance at least $1/8$ from the boundary.

Let $\beta\in(1,2]$ and $J\ge1$. Put $h=\min\{1/8,M^{-1/(2\beta+J)}\}$, $I=\{i\le M:\|S^{(i)}-s_0\|_2\le h\}$, and for $i\in I$ let $X_i=(S^{(i)}-s_0)/h$ and $\tilde\theta_i=\theta^{(i)}+h^\beta V_i$, where $V_1,\dots,V_M$ are i.i.d. uniform on $[0,1]$ and independent of the training pairs. For $\tau\in(0,1)$ let $\rho_\tau(r)=r(\tau-\mathbf{1}\{r<0\})$, and let $(\hat a_\tau,\hat b_\tau)$ be the minimizer of least Euclidean norm of $(a,b)\mapsto\sum_{i\in I}\rho_\tau(\tilde\theta_i-a-b\cdot X_i)$ over $\mathbb{R}\times\mathbb{R}^J$ when the vectors $(1,X_i)$, $i\in I$, span $\mathbb{R}^{1+J}$, and $(\hat a_\tau,\hat b_\tau)=0$ otherwise. Let $\hat Q(\tau)=\max\{-1,\min\{1,\hat a_\tau\}\}$ and $\hat P_M(\cdot\mid s_0)=\hat Q_\#\mathrm{Unif}[0,1]$. There is a constant $C$ depending only on $\beta$, $J$, $c_\mu$ and $C_\mu$ such that for every $M\ge1$
$$\sup_{Q\in\mathcal{Q}_\beta(J)}\mathbb{E}\,\mathscr{W}_{1,\mathbb{R}}\big(\hat P_M(\cdot\mid s_0),P_{Q,s_0}\big)\le C\,M^{-\beta/(2\beta+J)}.$$
In particular, for every $\beta\le2$, at fixed $\beta$ and $J$ no lower bound with the exponent $\beta/(2\beta+J+1)$ and a positive constant can hold.

Source: [`source/chapters/ext/m3b.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m3b.tex), label `m:prop:qnnUB2`.

<a id="a_quantile_fit_is_nearly_monotone_in_its_error"></a>

#### A local linear quantile fit is nearly monotone in its error (deterministic lemma for monotone Hölder quantile maps)

Lemma 16.21, page 296 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: proved.

Statement. Let $\beta\in(1,2]$, $J\ge1$, and let $Q:[0,1]\times[0,1]^J\to\mathbb{R}$, $(\tau,s)\mapsto Q(\tau\mid s)$, satisfy $\|Q\|_{C^\beta}=\max_{|\alpha|\le1}\|\partial^\alpha Q\|_\infty+\max_{|\alpha|=1}\sup_{z\ne z'}|\partial^\alpha Q(z)-\partial^\alpha Q(z')|/\|z-z'\|_2^{\beta-1}\le1$ (multi indices on $\mathbb{R}^{1+J}$) and be nondecreasing in $\tau$ for every $s$. Let $s_0\in[0,1]^J$ be at Euclidean distance at least $1/8$ from the boundary, $h\in(0,1/8]$, $\bar B=\{x\in\mathbb{R}^J:\|x\|_2\le1\}$, $C_G=2\max\{(2\sqrt J)^{1/\beta},2^{3+1/\beta}\}$, $K=2^{\beta-1}C_G^\beta$ and $\eta=(K+\sqrt J+1)h^\beta$. For $x\in\bar B$ let $F_x$ be the distribution function of $P_{Q,s_0+hx}=Q(\cdot\mid s_0+hx)_\#\mathrm{Unif}[0,1]$ and
$$\tilde F_x(y)=h^{-\beta}\int_{y-h^\beta}^{y}F_x(t)\,\mathrm{d}t,$$
the distribution function of $\theta+h^\beta V$ for $\theta\sim P_{Q,s_0+hx}$ and an independent $V\sim\mathrm{Unif}[0,1]$; for $\tau\in(0,1)$ let $T_\tau(x)=Q(\tau\mid s_0)+h\nabla_sQ(\tau\mid s_0)\cdot x$. Let $\tau\in(0,1)$, let $p:\mathbb{R}^J\to\mathbb{R}$ be affine, and put $w=p-T_\tau$ and $\delta(x)=\tilde F_x(p(x))-\tau$. Then for all $x,x'\in\bar B$ and $t\ge0$:
(i) if $\delta(x)>0$ then $w(x)\ge-\eta$, and if $\delta(x)<0$ then $w(x)\le\eta$;
(ii) if $w(x')\le t$ and $w(x)>3t+4\eta$ then $\delta(x')\le\delta(x)$, and if $w(x')\ge-t$ and $w(x)<-3t-4\eta$ then $\delta(x)\le\delta(x')$;
(iii) if $w(x)>\eta$ then $\delta(x)\ge\min\{\frac23(w(x)-\eta),1-\tau\}$, and if $w(x)<-\eta$ then $-\delta(x)\ge\min\{\frac23(-w(x)-\eta),\tau\}$.

Source: [`source/chapters/ext/m3b.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m3b.tex), label `m:lem:qrep`.

<a id="moment_conditions_force_a_small_fit"></a>

#### Moment conditions force a small local linear quantile fit

Lemma 16.22, page 298 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: proved.

Statement. Let $\beta\in(1,2]$, $J\ge1$, and let $Q:[0,1]\times[0,1]^J\to\mathbb{R}$, $(\tau,s)\mapsto Q(\tau\mid s)$, satisfy $\|Q\|_{C^\beta}=\max_{|\alpha|\le1}\|\partial^\alpha Q\|_\infty+\max_{|\alpha|=1}\sup_{z\ne z'}|\partial^\alpha Q(z)-\partial^\alpha Q(z')|/\|z-z'\|_2^{\beta-1}\le1$ (multi indices on $\mathbb{R}^{1+J}$) and be nondecreasing in $\tau$ for every $s$. Let $s_0\in[0,1]^J$ be at Euclidean distance at least $1/8$ from the boundary, $h\in(0,1/8]$, $\bar B=\{x\in\mathbb{R}^J:\|x\|_2\le1\}$, $C_G=2\max\{(2\sqrt J)^{1/\beta},2^{3+1/\beta}\}$, $K=2^{\beta-1}C_G^\beta$ and $\eta=(K+\sqrt J+1)h^\beta$. For $x\in\bar B$ let $F_x$ be the distribution function of $Q(\cdot\mid s_0+hx)_\#\mathrm{Unif}[0,1]$ and $\tilde F_x(y)=h^{-\beta}\int_{y-h^\beta}^yF_x(t)\,\mathrm{d}t$. Let $\tau\in(0,1)$, $T_\tau(x)=Q(\tau\mid s_0)+h\nabla_sQ(\tau\mid s_0)\cdot x$, $p:\mathbb{R}^J\to\mathbb{R}$ affine, $w=p-T_\tau$ and $\delta(x)=\tilde F_x(p(x))-\tau$.

Let $g$ be a probability density on $\bar B$ with $g\le g_+$, let $\omega_{J-1}$ be the volume of the unit ball of $\mathbb{R}^{J-1}$ (with $\omega_0=1$), and put $C_R=1+\frac{20}{3}g_+\omega_{J-1}$ and $c_B=12C_R(1+\sqrt J)$. Let $\kappa\ge0$ be such that $|\int\delta g|\le\kappa$ and $|\int\delta(x)x_kg(x)\,\mathrm{d}x|\le\kappa$ for $k=1,\dots,J$. If $\min\{\tau,1-\tau\}>5c_B\kappa$, then
$$\sup_{x\in\bar B}|w(x)|\le32\,C_R\,\eta+20\,C_R\,c_B\,\kappa.$$

Source: [`source/chapters/ext/m3b.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m3b.tex), label `m:lem:qbary`.

<a id="quantile_generator_exponent_attained_for_beta_above_two_with_bounded_densities"></a>

#### The minimax exponent for conditional quantile generators is attained for smoothness above two when the conditional densities are bounded

Proposition 16.25, page 302 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: proved.

Statement. For $\beta>0$ and $J\in\mathbb{N}$ let $\mathcal{Q}_\beta(J)$ be the set of maps $(\tau,s)\mapsto Q(\tau\mid s)$ from $[0,1]\times[0,1]^J$ to $\mathbb{R}$ with $\|Q\|_{C^\beta}\le1$, where, with $\ell$ the largest integer strictly below $\beta$, $\|Q\|_{C^\beta}=\max_{|\alpha|\le\ell}\|\partial^\alpha Q\|_\infty+\max_{|\alpha|=\ell}\sup_{z\ne z'}|\partial^\alpha Q(z)-\partial^\alpha Q(z')|/\|z-z'\|_2^{\beta-\ell}$ (maxima over multi indices on $\mathbb{R}^{1+J}$), and with $\tau\mapsto Q(\tau\mid s)$ nondecreasing for every $s$. For $\beta>1$ and $\underline c\in(0,1]$ let $\mathcal{Q}_\beta(J;\underline c)$ be the set of $Q\in\mathcal{Q}_\beta(J)$ with $\partial_\tau Q\ge\underline c$ on $[0,1]\times[0,1]^J$, so that every $P_{Q,s}=Q(\cdot\mid s)_\#\mathrm{Unif}[0,1]$ has a density between $1$ and $1/\underline c$ on its support and no atom. Let $\mathscr{W}_{1,\mathbb{R}}$ be the Wasserstein distance of order one on the line, let the training pairs $(S^{(i)},\theta^{(i)})$, $i\le M$, be i.i.d. with $S\sim\mu$ and $\theta\mid S\sim P_{Q,S}$, where $\mu$ has a Lebesgue density on $[0,1]^J$ between $c_\mu>0$ and $C_\mu$, and let $s_0\in[0,1]^J$ be at Euclidean distance at least $1/8$ from the boundary.

Let $\beta>2$, $J\ge1$ and $\underline c\in(0,1]$. Let $L_\ell$ be the number of multi indices $\alpha$ on $\mathbb{R}^J$ with $|\alpha|\le\ell$ and $\Psi(x)=(x^\alpha)_{|\alpha|\le\ell}\in\mathbb{R}^{L_\ell}$. Put $h=\min\{1/8,M^{-1/(2\beta+J)}\}$, $I=\{i\le M:\|S^{(i)}-s_0\|_2\le h\}$ and $X_i=(S^{(i)}-s_0)/h$ for $i\in I$. For $\tau\in(0,1)$ let $\rho_\tau(r)=r(\tau-\mathbf{1}\{r<0\})$ and let $\hat c_\tau$ be the minimizer of least Euclidean norm of $c\mapsto\sum_{i\in I}\rho_\tau(\theta^{(i)}-c\cdot\Psi(X_i))$ over $\mathbb{R}^{L_\ell}$ when the vectors $\Psi(X_i)$, $i\in I$, span $\mathbb{R}^{L_\ell}$, and $\hat c_\tau=0$ otherwise. Let $\hat Q(\tau)=\max\{-1,\min\{1,\hat c_\tau\cdot\Psi(0)\}\}$ and $\hat P_M(\cdot\mid s_0)=\hat Q_\#\mathrm{Unif}[0,1]$. There is a constant $C$ depending only on $\beta$, $J$, $c_\mu$, $C_\mu$ and $\underline c$ such that for every $M\ge1$
$$\sup_{Q\in\mathcal{Q}_\beta(J;\underline c)}\mathbb{E}\,\mathscr{W}_{1,\mathbb{R}}\big(\hat P_M(\cdot\mid s_0),P_{Q,s_0}\big)\le C\,M^{-\beta/(2\beta+J)}.$$
The two maps in the proof of the lower bound (catalog entry no_uniform_guarantee_for_quantile_generators) have $\partial_\tau Q\ge\frac18$, so with that theorem and the case $1<\beta\le2$ (catalog entry quantile_generator_exponent_attained_for_beta_between_one_and_two) the exponent $\beta/(2\beta+J)$ is the minimax exponent over $\mathcal{Q}_\beta(J;\underline c)$ at an interior point for every $\beta>1$ when $\underline c\le\frac18$.

Source: [`source/chapters/ext/m3b.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m3b.tex), label `m:prop:qnnUB3`.

<a id="a_polynomial_quantile_fit_when_the_densities_are_bounded"></a>

#### A local polynomial quantile fit is uniformly small when the conditional densities are bounded

Lemma 16.26, page 303 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: proved.

Statement. For $\beta>1$, $J\ge1$ and $\underline c\in(0,1]$ let $\ell$ be the largest integer strictly below $\beta$ and let $Q:[0,1]\times[0,1]^J\to\mathbb{R}$, $(\tau,s)\mapsto Q(\tau\mid s)$, satisfy $\|Q\|_{C^\beta}\le1$, where $\|Q\|_{C^\beta}=\max_{|\alpha|\le\ell}\|\partial^\alpha Q\|_\infty+\max_{|\alpha|=\ell}\sup_{z\ne z'}|\partial^\alpha Q(z)-\partial^\alpha Q(z')|/\|z-z'\|_2^{\beta-\ell}$ (maxima over multi indices on $\mathbb{R}^{1+J}$), be nondecreasing in $\tau$ for every $s$, and satisfy $\partial_\tau Q\ge\underline c$ on $[0,1]\times[0,1]^J$. Let $s_0\in[0,1]^J$ be at Euclidean distance at least $1/8$ from the boundary, $h\in(0,1/8]$, $\tau\in(0,1)$, $\bar B=\{x\in\mathbb{R}^J:\|x\|_2\le1\}$ with volume $\omega_J$, $F_x$ the distribution function of $Q(\cdot\mid s_0+hx)_\#\mathrm{Unif}[0,1]$ for $x\in\bar B$, and $T^\ell_\tau(x)=\sum_{|\alpha|\le\ell}\partial_s^\alpha Q(\tau\mid s_0)\,h^{|\alpha|}x^\alpha/\alpha!$, the Taylor polynomial of degree $\ell$ in $s$ written in the rescaled variable. Let $L_\ell$ be the number of multi indices $\alpha$ on $\mathbb{R}^J$ with $|\alpha|\le\ell$, $\Psi(x)=(x^\alpha)_{|\alpha|\le\ell}$, $c_\ell\in(0,1]$ the largest number with $\int_{\bar B}u^2\ge c_\ell\,\omega_J\sup_{\bar B}u^2$ for every polynomial $u$ of degree at most $\ell$, $K_\ell$ the smallest number with $\max_\alpha|c_\alpha|\le K_\ell\sup_{\bar B}|c\cdot\Psi|$ for every $c\in\mathbb{R}^{L_\ell}$, and $K_T=J^{\ell/2}/\ell!$.

Let $p$ be a polynomial of degree at most $\ell$, $w=p-T^\ell_\tau$ and $\delta(x)=F_x(p(x))-\tau$. Let $g$ be a probability density on $\bar B$ with $g\ge g_->0$, and let $\kappa\ge0$ be such that $|\int\delta(x)x^\alpha g(x)\,\mathrm{d}x|\le\kappa$ for $|\alpha|\le\ell$. Put
$$c_7=(g_-\omega_Jc_\ell)^{1/2},\qquad\bar\kappa=L_\ell K_\ell\kappa+6K_Th^\beta/\underline c.$$
If $\min\{\tau,1-\tau\}>2\sqrt2\,\bar\kappa/c_7^3$, then $\sup_{\bar B}|w|\le8\bar\kappa/c_7^4$.

Source: [`source/chapters/ext/m3b.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m3b.tex), label `m:lem:qpoly`.

<a id="no_two_point_bound_gives_a_smaller_exponent"></a>

#### No two point lower bound gives a smaller exponent for conditional quantile generators

Proposition 16.27, page 304 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: proved.

Statement. For $\beta>0$ and $J\in\mathbb{N}$ let $\mathcal{Q}_\beta(J)$ be the set of maps $(\tau,s)\mapsto Q(\tau\mid s)$ from $[0,1]\times[0,1]^J$ to $\mathbb{R}$ with $\|Q\|_{C^\beta}\le1$, where, with $\ell$ the largest integer strictly below $\beta$, $\|Q\|_{C^\beta}=\max_{|\alpha|\le\ell}\|\partial^\alpha Q\|_\infty+\max_{|\alpha|=\ell}\sup_{z\ne z'}|\partial^\alpha Q(z)-\partial^\alpha Q(z')|/\|z-z'\|_2^{\beta-\ell}$ (maxima over multi indices on $\mathbb{R}^{1+J}$), and with $\tau\mapsto Q(\tau\mid s)$ nondecreasing for every $s$. Let $P_{Q,s}=Q(\cdot\mid s)_\#\mathrm{Unif}[0,1]$, $\mathscr{W}_{1,\mathbb{R}}$ the Wasserstein distance of order one on the line, and let a training pair be $(S,\theta)$ with $S\sim\mu$ and $\theta\mid S\sim P_{Q,S}$, where $\mu$ has a Lebesgue density on $[0,1]^J$ between $c_\mu>0$ and $C_\mu$. Let $s_0\in[0,1]^J$ be at Euclidean distance at least $1/8$ from the boundary.

Let $\beta>0$ and $J\ge1$. There is a constant $c_8>0$ depending only on $\beta$ and $J$ such that for all $Q_0,Q_1\in\mathcal{Q}_\beta(J)$, with $P^{(i)}$ the joint law of one pair under $Q_i$ and $\Delta=\mathscr{W}_{1,\mathbb{R}}(P_{Q_0,s_0},P_{Q_1,s_0})$, the squared Hellinger distance satisfies
$$H^2\big(P^{(1)},P^{(0)}\big)\ge c_8\,c_\mu\,\Delta^{2+J/\beta}.$$
Consequently, for every such pair and every $M\ge1$ some generator $\hat P_M$ trained on $M$ i.i.d. pairs has $\mathbb{E}\,\mathscr{W}_{1,\mathbb{R}}(\hat P_M(\cdot\mid s_0),P_{Q_i,s_0})\le\{2/(c_8c_\mu M)\}^{\beta/(2\beta+J)}$ for $i=0$ and $i=1$, so that no lower bound drawn from two maps in $\mathcal{Q}_\beta(J)$ has an exponent smaller than $\beta/(2\beta+J)$.

Source: [`source/chapters/ext/m3b.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m3b.tex), label `m:prop:qnntwo`.

<a id="contraction_under_a_network_prior"></a>

#### Posterior contraction for the initial condition of a PDE under a sparse deep ReLU network (Polson Ročková) prior

Theorem 16.28, page 306 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: proved.

Statement. Consider data $Z^{(N)}=(Y_i,X_i)_{i\le N}$ with $Y_i=\mathscr{G}(\theta)(X_i)+\varepsilon_i$, $X_i$ i.i.d. uniform on $\mathcal{X}=[0,T]\times\mathbb{T}^d$ and $\varepsilon_i\sim N(0,I_W)$ i.i.d. and independent of them, where $\mathscr{G}(\theta)$ is the solution of an evolution equation with initial condition $\theta:\mathbb{T}^d\to\mathbb{R}$, and let $P^N_{\theta_0}$ be the law of the data under $\theta_0$. Let $\Pi$ be the Polson Ročková spike and slab prior on deep ReLU networks $\theta:\mathbb{T}^d\to\mathbb{R}$ with their width and sparsity hyperpriors and a depth of order $\log N$, let $\Theta_N$ be the associated sieve, let $p$ be the input dimension of the networks in $\Theta_N$ ($p=d$ when networks on $[0,1]^d$ approximate the restriction of $\theta_0$ to $[0,1]^d$, or $p=2d$ when every network is composed with the periodic embedding $x\mapsto(\cos2\pi x_1,\sin2\pi x_1,\dots,\cos2\pi x_d,\sin2\pi x_d)$), and set
$$B_N:=1+\sup_{\theta\in\Theta_N}\big(\|\theta\|_{L^\infty(\mathbb{T}^d)}+\operatorname{Lip}(\theta)\big),$$
so that $\sup_{\theta\in\Theta_N}\|\theta\|_{H^1(\mathbb{T}^d)}\lesssim B_N$. Let $\theta_0\in C^\alpha(\mathbb{T}^d)$ with $d/2+1<\alpha<p$. Suppose the forward map satisfies Conditions 2A, 2B and 2E of Nickl (2024) on $L^\infty$ balls (uniform $L^\infty$ bounds, $L^2$ Lipschitz continuity, and the stability estimate $\|\mathscr{G}(\theta)-\mathscr{G}(\theta_0)\|_{L^2(\mathcal{X})}\ge c\|\theta-\theta_0\|_{H^{-1}}$). Then with $\epsilon_N=N^{-\alpha/(2\alpha+p)}\log^\delta N$, $\delta>1$, there are $L,L'>0$ with
$$\Pi\big(\theta:\|\mathscr{G}(\theta)-\mathscr{G}(\theta_0)\|_{L^2(\mathcal{X})}\le L\epsilon_N\mid Z^{(N)}\big)\to1,\qquad\Pi\big(\theta:\|\theta-\theta_0\|_{H^{-1}}\le L\epsilon_N\mid Z^{(N)}\big)\to1,$$
in $P^N_{\theta_0}$ probability, and, by interpolation between $H^{-1}$ and $H^1$ along the sieve,
$$\Pi\big(\theta:\|\theta-\theta_0\|_{L^2}\le L'(B_N\epsilon_N)^{1/2}\mid Z^{(N)}\big)\to1$$
in $P^N_{\theta_0}$ probability. The third statement is a rate only when $B_N\epsilon_N\to0$.

Source: [`source/chapters/ext/m3c.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m3c.tex), label `m:thm:PR`.

<a id="exactness_of_the_one_step_summary"></a>

#### Exactness of the one step summary in the linear Gaussian model

Lemma 16.32, page 310 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: proved.

Statement. In the linear model $Y=\Phi\theta+\varepsilon$, $\varepsilon\sim N(0,\varsigma^2\operatorname{Id}_N)$, with prior $\theta\sim N(0,\Sigma_0)$, let $F=\Phi^\top\Phi/\varsigma^2$ and $\Sigma_N=(F+\Sigma_0^{-1})^{-1}$, and let the one step summary be evaluated at any point $\bar\theta$:
$$S(Y)=\bar\theta+\Sigma_N\Big(\Phi^\top\big(Y-\Phi\bar\theta\big)/\varsigma^2-\Sigma_0^{-1}\bar\theta\Big).$$
Then $S(Y)=\Sigma_N\big(F\theta+\Phi^\top\varepsilon/\varsigma^2\big)$ identically in $\bar\theta$: the summary is exactly the posterior mean, and in particular does not depend on the linearization point.

Source: [`source/chapters/ext/m3c.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m3c.tex), label `m:lem:exact`.

<a id="residual_law_under_a_localized_proposal"></a>

#### Residual law under a localized training proposal: prior fraction mean and variance inflation

Theorem 16.33, page 310 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: proved.

Statement. In the linear model $Y=\Phi\theta+\varepsilon$, $\varepsilon\sim N(0,\varsigma^2\operatorname{Id}_N)$, with prior $N(0,\Sigma_0)$ on $D$ retained modes, let $F=\Phi^\top\Phi/\varsigma^2$, $\Sigma_N=(F+\Sigma_0^{-1})^{-1}$, and for a point $\bar\theta$ let $S(Y)=\bar\theta+\Sigma_N(\Phi^\top(Y-\Phi\bar\theta)/\varsigma^2-\Sigma_0^{-1}\bar\theta)$ (which equals the posterior mean). Let the training parameter be drawn from $q_c=N(\bar\theta,c^2\Sigma_N)$, independent of $\varepsilon$, so that $c$ is the localization radius in posterior standard deviations, let $R=\theta-S(Y)$, and let $P=\Sigma_N\Sigma_0^{-1}$ be the prior fraction operator, with eigenvalues $p_1,\dots,p_D$, and $s_j=1-p_j$. Then
$$\mathbb{E}_{q_c}(R)=P\bar\theta,\qquad\operatorname{Var}_{q_c}(R)=c^2P\Sigma_NP^\top+\Sigma_NF\Sigma_N,$$
both without further hypotheses. If in addition $\Sigma_0$ and $\Phi^\top\Phi$ commute, so that one orthonormal basis diagonalizes $P$, $\Sigma_N$ and $F$ together, then in that basis $\operatorname{Var}_{q_c}(R)_j=\Sigma_{N,j}(s_j+c^2p_j^2)$. Consequently:
(i) under the prior itself, $\mathbb{E}(R)=0$ and $\operatorname{Var}(R)=\Sigma_N$, so the identity head is exact;
(ii) under $q_c$ the residual has the mean $P\bar\theta$, the prior shrinkage of the proposal center, which does not depend on $c$ and is of first order in the prior fraction; a head that adds the sample mean of the residuals to the center therefore displaces the GBC posterior by $P\bar\theta$, whereas a head that centers the residuals, or subtracts $P\bar\theta$ analytically, does not;
(iii) with the mean removed, the head misstates the posterior standard deviation in direction $j$ by the factor $\sqrt{s_j+c^2p_j^2}$, so the relative error in posterior standard deviations is
$$\beta(c)=\frac1D\sum_{j\le D}\Big|\sqrt{s_j+c^2p_j^2}-1\Big|,$$
which is $O(\max_jp_j)$ as $c\to0$ and grows like $c\,\frac1D\sum_jp_j$ for large $c$.

Source: [`source/chapters/ext/m3c.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m3c.tex), label `m:thm:locbias`.

<a id="localized_design_meets_gbc_accuracy_conditions"></a>

#### The localized GBC design (center and rescale) meets the accuracy conditions (G1) and (G2) in the linear Gaussian model

Corollary 16.37, page 315 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: proved.

Statement. In the linear model $Y=\Phi\theta+\varepsilon$, $\varepsilon\sim N(0,\varsigma^2\operatorname{Id}_N)$, with prior $N(0,\Sigma_0)$, let $F=\Phi^\top\Phi/\varsigma^2$, $\Sigma_N=(F+\Sigma_0^{-1})^{-1}$, and suppose $\Sigma_0$ and $\Phi^\top\Phi$ commute; let $P=\Sigma_N\Sigma_0^{-1}$, with eigenvalues $p_j$, $s_j=1-p_j$, and for a preliminary estimate $\bar\theta_N$ let $S(Y)=\bar\theta_N+\Sigma_N(\Phi^\top(Y-\Phi\bar\theta_N)/\varsigma^2-\Sigma_0^{-1}\bar\theta_N)$, the posterior mean, so that the exact posterior is $\Pi_N=N(S(Y),\Sigma_N)$. Consider the localized GBC generator: training parameters $\theta^{(m)}\sim q_c=N(\bar\theta_N,c^2\Sigma_N)$, $m\le M$, with simulated data $Y^{(m)}$; an identity head with the residuals $\theta^{(m)}-S(Y^{(m)})$ centered at their sample mean, whitened by the sample covariance of the centered residuals rescaled by $(s_j+c^2p_j^2)^{-1/2}$ in the eigenbasis of $P$, and centered at $S(Y)$ for the observed data, with no residual mean added to the center, no affine head and no importance weighting back to the prior; let $\widehat\Pi_N$ be the law it produces. Then:
(i) (exactness in population) for every $c>0$ and every center $\bar\theta_N$, the law the head produces at the observed data is exactly the posterior $N(S(Y),\Sigma_N)$: localization contributes no bias at all;
(ii) (finite $M$) with $M=M_N$ simulations and $J=J_N$ retained modes, the rescaled sample covariance of the centered residuals equals $\Sigma_N^{1/2}(\operatorname{Id}+\Delta_M)\Sigma_N^{1/2}$, where $\|\Delta_M\|_{op}=O_P(\sqrt{J_N/M_N}+J_N/M_N)$ does not depend on $c$; hence, when $\Sigma_{N,j}\lesssim\lambda_j/N$ on the retained modes ($\lambda_j$ the Laplace eigenvalues), as for the heat and Stokes equations, and $k>d/2$, $\mathscr{W}_{1,H^{-k-2}}(\widehat\Pi_N,\Pi_N)=O_P\big(N^{-1/2}(\sqrt{J_N/M_N}+J_N/M_N)\big)$, the distance being the Wasserstein distance of order one for the norm $\|x\|^2=\sum_j\lambda_j^{-k-2}x_j^2$ on the coefficients in the first $J$ Laplace modes, so the accuracy condition (G1) $\sqrt N\,\mathscr{W}_{1,H^{-k-2}}(\widehat\Pi_N,\Pi_N)\to0$ holds whenever $J_N/M_N\to0$, at every radius, and the condition (G2) (exponentially small mass off the localization set and moments of every order) holds whenever the exact posterior $N(S(Y),\Sigma_N)$ satisfies its first clause;
(iii) consequently the transfer theorem (catalog entry bvm_for_gbc) applies verbatim to this algorithm, its accuracy assumption being discharged.

Source: [`source/chapters/ext/m3c.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m3c.tex), label `m:cor:locG`.

<a id="the_gram_matrix_of_the_whitened_weights"></a>

#### Gram matrix of the whitened weights of the one step training summary

Lemma 16.41, page 319 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: proved.

Statement. Let $\mathcal{X}=[0,T]\times\Omega$ with $X$ uniform on $\mathcal{X}$, let $(e_j)$ be the Laplace eigenbasis of $\Omega=[0,1]^d$ (the torus), $P_J$ the orthogonal projection onto $\operatorname{span}\{e_j:j\le J\}\cong\mathbb{R}^J$ and $Q_J=\operatorname{Id}-P_J$. Let $\mathbb{I}_{\bar\vartheta}$ be the linearization at a point $\bar\vartheta$ of the solution map $\theta\mapsto u_\theta$, with values in $\mathbb{R}^{d_W}$ valued functions on $\mathcal{X}$, let $\mathcal{D}=\operatorname{diag}(1/\iota_j)$ be the heat (or Stokes) information diagonal, and define $K'_{\bar\vartheta}$ by $\operatorname{Id}+K'_{\bar\vartheta}=T^{-1}\mathcal{D}^{1/2}\mathbb{I}^*_{\bar\vartheta}\mathbb{I}_{\bar\vartheta}\mathcal{D}^{1/2}$, that is $\langle f,(\operatorname{Id}+K'_{\bar\vartheta})g\rangle=\mathbb{E}\langle(\mathbb{I}_{\bar\vartheta}\mathcal{D}^{1/2}f)(X),(\mathbb{I}_{\bar\vartheta}\mathcal{D}^{1/2}g)(X)\rangle_W$. Let $\mathcal{A}=\operatorname{Id}+K'_{\bar\vartheta}$ be bounded on $\ell^2$ with $\mathcal{A}\succeq a\operatorname{Id}$ for some $a>0$, and write $B_J=P_J\mathcal{A}^{-1}P_J$. Let the whitened weights be the $J\times d_W$ matrix $\phi(x)$ defined by $\phi(x)^\top v=(\mathbb{I}_{\bar\vartheta}\mathcal{D}^{1/2}P_J\mathcal{A}^{-1}v)(x)$ for $v\in\mathbb{R}^J$ (equivalently, row $j$ is $\iota_j^{1/2}$ times the weight function $\mathbb{I}_{\bar\vartheta}P_J(T(\mathbb{I}^*_{\bar\vartheta}\mathbb{I}_{\bar\vartheta})^{-1}e_j)$ of the one step summary linearized at $\bar\vartheta$), and $G_\phi=\mathbb{E}\,\phi(X)\phi(X)^\top$ their Gram matrix. Then
$$G_\phi=B_J+B_JP_J\mathcal{A}Q_J(Q_J\mathcal{A}Q_J)^{-1}Q_J\mathcal{A}P_JB_J,$$
so that $G_\phi\succeq B_J\succeq\|\mathcal{A}\|^{-1}_{op}\operatorname{Id}$ and $\|G_\phi-B_J\|_{op}\le a^{-3}\|K'_{\bar\vartheta}Q_J\|^2_{op}$.

Source: [`source/chapters/ext/m3c.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m3c.tex), label `m:lem:u2pgram`.

<a id="no_sub_gaussian_envelope_for_the_whole_residual"></a>

#### No sub Gaussian envelope uniform in the dimension for the whole whitened training residual with fresh designs

Proposition 16.42, page 319 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: proved.

Statement. Let $\mathcal{X}=[0,T]\times\Omega$, $\Omega=[0,1]^d$ the torus, with $X$ uniform on $\mathcal{X}$, and let $\mathbb{I}_\vartheta$ be the linearization at $\vartheta$ of the solution map $\theta\mapsto u_\theta$, whose values are $\mathbb{R}^{d_W}$ valued functions on $\mathcal{X}$. Let $\mathcal{D}=\operatorname{diag}(1/\iota_j)$ be the heat (or Stokes) information diagonal, $\iota_j=(1-e^{-2\nu\lambda_jT})/(2\nu\lambda_jT)$ with $\lambda_j$ the Laplace eigenvalues, $\operatorname{Id}+K'_\vartheta=T^{-1}\mathcal{D}^{1/2}\mathbb{I}^*_\vartheta\mathbb{I}_\vartheta\mathcal{D}^{1/2}$, and $P_J$ the projection onto the first $J$ eigenfunctions $e_1,\dots,e_J$. Fix a linearization point $\bar\vartheta$ determined by the data $Z^{(N)}$ at which $\mathcal{A}=\operatorname{Id}+K'_{\bar\vartheta}$ is bounded and invertible, let $\phi(x)$ be the $J\times d_W$ matrix with $\phi(x)^\top v=(\mathbb{I}_{\bar\vartheta}\mathcal{D}^{1/2}P_J\mathcal{A}^{-1}v)(x)$ for $v\in\mathbb{R}^J$ (rows $\phi_j(x)^\top$), $G_\phi=\mathbb{E}\,\phi(X)\phi(X)^\top$ and $b_J=\operatorname{ess\,sup}_x\|\phi(x)\|^2_{op}$. Let each simulated data set $Z^{(m)}$ be drawn at a training parameter $\theta^{(m)}$ with its own design points $X^{(m)}_i$, i.i.d. uniform on $\mathcal{X}$, and its own noise $\varepsilon^{(m)}_i\sim N(0,I_W)$, independent of each other and of $\theta^{(m)}$, let the training summary be the one step summary linearized once at $\bar\vartheta$ with the population information and no prior term, $\hat S^{(m)}_{N,j}=\langle e_j,\bar\vartheta\rangle+N^{-1}\sum_{i\le N}\langle\iota_j^{-1/2}\phi_j(X^{(m)}_i),Y^{(m)}_i-u_{\bar\vartheta}(X^{(m)}_i)\rangle_W$ for $j\le J$, and let $W^{(m)}=\mathcal{D}^{-1/2}\sqrt N(P_J\theta^{(m)}-\hat S^{(m)}_N)$ be the whitened residual. Let the training parameters have any law given $Z^{(N)}$, and write $\|\chi\|_{\psi_2\mid Z^{(N)}}=\inf\{K>0:\mathbb{E}[e^{\chi^2/K^2}\mid Z^{(N)}]\le2\}$. Then for every $N$, every $J$ and every unit vector $v\in\mathbb{R}^J$
$$\big\|\langle v,W^{(m)}\rangle\big\|^2_{\psi_2\mid Z^{(N)}}\ge2\operatorname{ess\,sup}_x\|\phi(x)^\top v\|^2_W,\qquad\sup_{\|u\|_2=1}\big\|\langle u,W^{(m)}\rangle\big\|^2_{\psi_2\mid Z^{(N)}}\ge2b_J\ge\frac{2\,\mathrm{tr}\,G_\phi}{d_W}.$$
If $\mathcal{A}$ is bounded and $\mathcal{A}\succeq a\operatorname{Id}$ for some $a>0$, then $\mathrm{tr}\,G_\phi\ge J\|\mathcal{A}\|^{-1}_{op}$. For the heat and Stokes equations, observed from time zero, $G_\phi=\operatorname{Id}_J$ and $\|\langle e_J,W^{(m)}\rangle\|^2_{\psi_2\mid Z^{(N)}}\ge2\|e_J\|^2_{L^\infty}/\iota_J\ge2/\iota_J$, which grows like $\lambda_J$; for the real trigonometric basis the bound is $4/\iota_J$.

Source: [`source/chapters/ext/m3c.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m3c.tex), label `m:prop:u2pfalse`.

<a id="whitened_residual_assumption_under_a_localized_proposal"></a>

#### The whitened training residual assumption (U2') holds under a localized training proposal

Theorem 16.43, page 320 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: proved.

Statement. Setting. Data $Z^{(N)}$: $Y_i=u_\theta(X_i)+\varepsilon_i$, $i\le N$, $X_i$ i.i.d. uniform on $\mathcal{X}=[0,T]\times\Omega$, $\Omega=[0,1]^d$ the torus, $\varepsilon_i\sim N(0,I_W)$ in $\mathbb{R}^{d_W}$; $(e_j)$ the Laplace eigenbasis with eigenvalues $\lambda_j$; $\theta_0$ the truth and $P^N_{\theta_0}$ the law of the data; Nickl's rescaled Gaussian series prior with $\delta_N=N^{-\gamma/(2\gamma+d)}$, and $\tilde\delta_N(\xi)=\delta_N^{(\bar\gamma-\xi)/(\bar\gamma+1)}$ with $\bar\gamma$ the Sobolev index of the localization ball. Let $\mathbb{I}_\vartheta$ be the linearization of $\theta\mapsto u_\theta$ at $\vartheta$, $\mathcal{D}=\operatorname{diag}(1/\iota_j)$ the heat (or Stokes) information diagonal with $\iota_j=(1-e^{-2\nu\lambda_jT})/(2\nu\lambda_jT)$, $\operatorname{Id}+K'_\vartheta=T^{-1}\mathcal{D}^{1/2}\mathbb{I}^*_\vartheta\mathbb{I}_\vartheta\mathcal{D}^{1/2}$, $P_J$ the projection onto the first $J$ modes and $\operatorname{Id}+\Xi=P_J(\operatorname{Id}+K'_{\theta_0})^{-1}P_J$. Let $\bar\theta_N$ be a preliminary estimate computed from half of the sample with $\|\bar\theta_N-\theta_0\|_{H^\xi}=O_P(\tilde\delta_N(\xi))$ for $0\le\xi\le\bar\gamma$, and let $J=J_N\asymp N^{d/(2\gamma+d)}$. Let the training parameters be
$$\theta^{(m)}=\bar\theta_N+N^{-1/2}\mathcal{D}^{1/2}\mathcal{V}_N^{1/2}\xi^{(m)},\qquad m\le M,$$
where $\mathcal{V}_N$ is a positive semidefinite $J\times J$ matrix determined by $Z^{(N)}$ with $\|\mathcal{V}_N\|_{op}=O_P(1)$, and the $\xi^{(m)}$ are i.i.d. standard normal on $\mathbb{R}^J$ given $Z^{(N)}$, conditioned on $\|\xi^{(m)}\|_2^2\le4J$ when the forward map is nonlinear. Each simulated data set has its own uniform design $X^{(m)}_i$ and noise $\varepsilon^{(m)}_i$. With $\phi(x)$ the $J\times d_W$ matrix given by $\phi(x)^\top v=(\mathbb{I}_{\bar\theta_N}\mathcal{D}^{1/2}P_J(\operatorname{Id}+K'_{\bar\theta_N})^{-1}v)(x)$, rows $\phi_j(x)^\top$, the training summary is $\hat S^{(m)}_{N,j}=\langle e_j,\bar\theta_N\rangle+N^{-1}\sum_{i\le N}\langle\iota_j^{-1/2}\phi_j(X^{(m)}_i),Y^{(m)}_i-u_{\bar\theta_N}(X^{(m)}_i)\rangle_W$, $j\le J$ (linearized once at $\bar\theta_N$, population information, no prior term), and the whitened residuals are $W^{(m)}=\mathcal{D}^{-1/2}\sqrt N(P_J\theta^{(m)}-\hat S^{(m)}_N)$, used uncentered and unrescaled by the identity skip Gaussian head generator (catalog entry bernstein_von_mises_for_the_identity_skip_quantile_generator). Assumption (U2') means: $W^{(m)}=W^{(m)}_{g}+W^{(m)}_{r}$ with pairs i.i.d. given $Z^{(N)}$, $\varkappa_N=\sup_{\|v\|_2=1}\|\langle v,W^{(m)}_{g}\rangle\|_{\psi_2\mid Z^{(N)}}=O_P(1)$, where $\|\chi\|_{\psi_2\mid Z^{(N)}}=\inf\{K>0:\mathbb{E}[e^{\chi^2/K^2}\mid Z^{(N)}]\le2\}$, and, in $P^N_{\theta_0}$ probability, $\mathbb{E}[\|W^{(m)}_{r}\|^2_2\mid Z^{(N)}]\to0$ and $\|\mathbb{E}[W^{(m)}_{g}W^{(m)\top}_{g}\mid Z^{(N)}]-(\operatorname{Id}+\Xi)\|_{op}\to0$.

Conditions on the linearization, with a constant $a_\star>0$ and, for every $B>0$, constants $L_\star$ and $C_\infty$ that may depend on $B$, required for all $\vartheta$ with $\|\vartheta\|_{H^{\bar\gamma}}\le B$: (I1) $\operatorname{Id}+K'_{\theta_0}$ is bounded on $\ell^2$, $K'_{\theta_0}$ is compact and $\operatorname{Id}+K'_{\theta_0}\succeq a_\star\operatorname{Id}$; (I2) $\|(\mathbb{I}_\vartheta-\mathbb{I}_{\theta_0})\mathcal{D}^{1/2}\|_{\ell^2\to L^2}\le L_\star\|\vartheta-\theta_0\|_{H^\zeta}$, where $\|\mathcal{T}\|_{\ell^2\to L^2}=\sup_{\|g\|_2\le1}(\mathbb{E}\|(\mathcal{T}g)(X)\|^2_W)^{1/2}$ with $X$ uniform on $\mathcal{X}$; (I3) $\|\mathbb{I}_\vartheta h\|_{L^\infty(\mathcal{X})}\le C_\infty\|h\|_{H^\zeta}$ for all $h\in H^\zeta$.

Then:
(a) for the heat and Stokes equations, observed from time zero, with $\gamma>d+2$, Assumption (U2') holds with $\Xi=0$, $\varkappa_N\le4/\sqrt3$ and $W^{(m)}_{g}=-\mathbf{1}_{\mathcal{B}_m}N^{-1/2}\sum_i\phi(X^{(m)}_i)\varepsilon^{(m)}_i$, where $\mathcal{B}_m=\{\|\hat G^{(m)}_\phi-\operatorname{Id}\|_{op}\le1\}$ and $\hat G^{(m)}_\phi=N^{-1}\sum_{i\le N}\phi(X^{(m)}_i)\phi(X^{(m)}_i)^\top$;
(b) for a nonlinear forward map, Assumption (U2') holds under Conditions 1 and 2 of Nickl (2024) with integer $\gamma>\max(3\zeta+3d/2+2,\eta_0)$ and $k>\max(\zeta+5d/2,\eta_0)$ ($\zeta>d/2$ the index of Condition 2D), $\bar\gamma<\gamma-1$, $\sqrt N\,\tilde\delta_N(0)\tilde\delta_N(\zeta)\to0$, and (I1) to (I3);
(c) let $\Sigma_0$ be positive definite, $\Sigma_N=(F_{\bar\theta_N}+\Sigma_0^{-1})^{-1}$ with $F_{\bar\theta_N}$ the realized information on $J$ modes, and $a_\star=1$ in case (a); under the hypotheses of (a) or (b), with probability tending to one $N^{-1}\mathcal{D}^{1/2}F_{\bar\theta_N}\mathcal{D}^{1/2}\succeq(a_\star/12)\operatorname{Id}$, and then $\mathcal{V}_N=c^2N\mathcal{D}^{-1/2}\Sigma_N\mathcal{D}^{-1/2}$ has $\|\mathcal{V}_N\|_{op}\le12c^2/a_\star$.

Source: [`source/chapters/ext/m3c.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m3c.tex), label `m:thm:u2ploc`.

<a id="the_linearization_of_the_reaction_diffusion_class"></a>

#### Linearization conditions (I1) to (I4) for the reaction diffusion class

Lemma 16.44, page 324 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: proved.

Statement. Let $\Omega=[0,1]^d$ be the torus with $d\le3$, $T>0$, $\mathcal{X}=[0,T]\times\Omega$, and let $u_\vartheta$ solve $\partial_tu-\Delta u=f(u)$, $u(0)=\vartheta$, with $f\in C^\infty_c(\mathbb{R})$ (the setting of Theorem 1 of Nickl (2024), with integer $\gamma>2+3d$), let $\theta_0\in C^\infty$ and $K_f=\sup|f'|$, and let $\mathbb{I}_\vartheta h$ be the solution $U$ of $\partial_tU=\Delta U+f'(u_\vartheta)U$, $U(0)=h$. Let $\mathcal{D}=\operatorname{diag}(1/\iota_j)$ be the heat information diagonal in the Laplace eigenbasis, $\operatorname{Id}+K'_\vartheta=T^{-1}\mathcal{D}^{1/2}\mathbb{I}^*_\vartheta\mathbb{I}_\vartheta\mathcal{D}^{1/2}$, and $\|\mathcal{T}\|_{\ell^2\to L^2}=\sup_{\|g\|_2\le1}(\mathbb{E}|(\mathcal{T}g)(X)|^2)^{1/2}$ with $X$ uniform on $\mathcal{X}$. Consider the conditions, with a constant $a_\star>0$ and, for every $B>0$, constants $L_\star$, $C_\infty$, $C_Q$ that may depend on $B$, for all $\vartheta,\vartheta'$ with $\|\vartheta\|_{H^{\bar\gamma}},\|\vartheta'\|_{H^{\bar\gamma}}\le B$: (I1) $\operatorname{Id}+K'_{\theta_0}$ is bounded on $\ell^2$, $K'_{\theta_0}$ is compact and $\operatorname{Id}+K'_{\theta_0}\succeq a_\star\operatorname{Id}$; (I2) $\|(\mathbb{I}_\vartheta-\mathbb{I}_{\theta_0})\mathcal{D}^{1/2}\|_{\ell^2\to L^2}\le L_\star\|\vartheta-\theta_0\|_{H^\zeta}$; (I3) $\|\mathbb{I}_\vartheta h\|_{L^\infty(\mathcal{X})}\le C_\infty\|h\|_{H^\zeta}$ for all $h\in H^\zeta$; (I4) $\|u_{\vartheta'}-u_\vartheta-\mathbb{I}_\vartheta[\vartheta'-\vartheta]\|_{L^\infty(\mathcal{X})}\le C_Q\|\vartheta'-\vartheta\|^2_{H^\zeta}$. Then (I1) to (I4) hold for every $\zeta>d/2$ and every $\bar\gamma>\max(1,\zeta)$, and $\|\operatorname{Id}+K'_\vartheta\|_{op}$ is bounded by a constant that depends only on $K_f$ and $T$.

Source: [`source/chapters/ext/m3c.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m3c.tex), label `m:lem:rdlin`.

<a id="the_linearization_of_the_navier_stokes_equations"></a>

#### Linearization conditions (I1) to (I4) for the two dimensional Navier Stokes equations

Lemma 16.45, page 325 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: proved.

Statement. Consider the incompressible Navier Stokes equations on the two dimensional torus, as in Konen and Nickl (2026), with forcing $f\in\dot H^{1}_\diamond$ and initial condition $\theta_0\in\dot H^{2}_\diamond$, where $\dot H^{s}_\diamond$ is the Sobolev space of order $s$ of divergence free, mean zero vector fields; let $u_\vartheta$ be the solution with initial condition $\vartheta$, $\mathbb{I}_\vartheta$ the linearization of $\vartheta\mapsto u_\vartheta$ (the solution of the equation linearized at $u_\vartheta$), $\mathcal{X}=[0,T]\times\mathbb{T}^2$, $\mathcal{D}=\operatorname{diag}(1/\iota_j)$ the Stokes information diagonal and $\operatorname{Id}+K'_\vartheta=T^{-1}\mathcal{D}^{1/2}\mathbb{I}^*_\vartheta\mathbb{I}_\vartheta\mathcal{D}^{1/2}$. Consider the conditions, with a constant $a_\star>0$ and, for every $B>0$, constants $L_\star$, $C_\infty$, $C_Q$ that may depend on $B$, for all $\vartheta,\vartheta'$ with $\|\vartheta\|_{H^{\bar\gamma}},\|\vartheta'\|_{H^{\bar\gamma}}\le B$: (I1) $\operatorname{Id}+K'_{\theta_0}$ is bounded on $\ell^2$, $K'_{\theta_0}$ is compact and $\operatorname{Id}+K'_{\theta_0}\succeq a_\star\operatorname{Id}$; (I2) $\|(\mathbb{I}_\vartheta-\mathbb{I}_{\theta_0})\mathcal{D}^{1/2}\|_{\ell^2\to L^2}\le L_\star\|\vartheta-\theta_0\|_{H^\zeta}$, with $\|\mathcal{T}\|_{\ell^2\to L^2}=\sup_{\|g\|_2\le1}(\mathbb{E}\|(\mathcal{T}g)(X)\|^2)^{1/2}$ for $X$ uniform on $\mathcal{X}$; (I3) $\|\mathbb{I}_\vartheta h\|_{L^\infty(\mathcal{X})}\le C_\infty\|h\|_{H^\zeta}$ for all $h\in H^\zeta$; (I4) $\|u_{\vartheta'}-u_\vartheta-\mathbb{I}_\vartheta[\vartheta'-\vartheta]\|_{L^\infty(\mathcal{X})}\le C_Q\|\vartheta'-\vartheta\|^2_{H^\zeta}$. Then (I2) to (I4) hold with $\zeta=2$ for every $\bar\gamma\ge2$. If moreover $f,\theta_0\in\dot H^{\infty}_\diamond$, as in Theorem 2.11 of Konen and Nickl (2026), then, with (I1), which the book proves for Navier Stokes by the Fredholm alternative, and with Condition 2C (linearization with quadratic remainder) from their Proposition 3.8(iii), every hypothesis on the forward map of part (b) of the theorem on the whitened residual assumption under a localized proposal (catalog entry whitened_residual_assumption_under_a_localized_proposal) holds, with their Condition 2.12 in place of Condition 2 of Nickl (2024) and $\gamma=\alpha>12>3\zeta+3d/2+2$.

Source: [`source/chapters/ext/m3c.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m3c.tex), label `m:lem:nslin`.

<a id="centered_and_rescaled_residuals_for_a_nonlinear_forward_map"></a>

#### Centered and rescaled training residuals for a nonlinear forward map with a reused design

Proposition 16.47, page 327 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: proved.

Statement. Use the setting of the theorem on the whitened residual assumption under a localized proposal (catalog entry whitened_residual_assumption_under_a_localized_proposal): data $Y_i=u_\theta(X_i)+\varepsilon_i$ on $\mathcal{X}=[0,T]\times\Omega$ with the observed design $(X_i)_{i\le N}$, a preliminary estimate $\bar\theta_N$, $J=J_N$ retained modes with projection $P_J$, the linearization $\mathbb{I}_\vartheta$ of $\theta\mapsto u_\theta$ and the heat (or Stokes) information diagonal $\mathcal{D}$. Let $\Sigma_0$ be positive definite, $\Sigma_N=(F_{\bar\theta_N}+\Sigma_0^{-1})^{-1}$ with $F_{\bar\theta_N}$ the realized information on $J$ modes, $c>0$, and $\theta^{(m)}=\bar\theta_N+c\Sigma_N^{1/2}\xi^{(m)}$, $m\le M$, with the $\xi^{(m)}$ i.i.d. standard normal on $\mathbb{R}^J$ given the data, conditioned on $\|\xi^{(m)}\|^2_2\le4J$. Let the simulated data sets reuse the observed design and draw fresh noise, and let $S^{(m)}$ be their regularized one step summaries on $J$ modes formed at $\bar\theta_N$ with this $\Sigma_N$, $S^{(m)}=\bar\theta_N+\Sigma_N\big(\mathbb{I}^*_{\bar\theta_N}\big[\sum_ir^{(m)}_i\delta_{X_i}\big]-\Sigma_0^{-1}\bar\theta_N\big)$ with residuals $r^{(m)}_i=Y^{(m)}_i-u_{\bar\theta_N}(X_i)$, and $S(Y)$ the same summary of the observed data. Let $Q$ be the rescaling of the localized GBC algorithm, multiplication by $(s_j+c^2p_j^2)^{-1/2}$ in the eigenbasis of $P=\Sigma_N\Sigma_0^{-1}$, whose eigenvalues are $p_j$, with $s_j=1-p_j$. Then
$$\Sigma_N^{-1/2}Q\big(P_J\theta^{(m)}-S^{(m)}\big)=\mu_N+W^{(m)}_{g}+W^{(m)}_{r}$$
with $\mu_N$ determined by $Z^{(N)}$, and under the hypotheses of part (b) of that theorem (Conditions 1 and 2 of Nickl (2024) with integer $\gamma>\max(3\zeta+3d/2+2,\eta_0)$ and $k>\max(\zeta+5d/2,\eta_0)$, $\bar\gamma<\gamma-1$, $\sqrt N\,\tilde\delta_N(0)\tilde\delta_N(\zeta)\to0$, and the linearization conditions (I1) to (I3)) and the quadratic remainder condition (I4) $\|u_{\vartheta'}-u_\vartheta-\mathbb{I}_\vartheta[\vartheta'-\vartheta]\|_{L^\infty(\mathcal{X})}\le C_Q\|\vartheta'-\vartheta\|^2_{H^\zeta}$ on $H^{\bar\gamma}$ balls, the pairs $(W^{(m)}_{g},W^{(m)}_{r})$ satisfy Assumption (U2') with $\operatorname{Id}$ in place of $\operatorname{Id}+\Xi$ (i.i.d. given the data, $\sup_{\|v\|_2=1}\|\langle v,W^{(m)}_{g}\rangle\|_{\psi_2\mid Z^{(N)}}=O_P(1)$, $\mathbb{E}[\|W^{(m)}_{r}\|^2_2\mid Z^{(N)}]\to0$ and $\|\mathbb{E}[W^{(m)}_{g}W^{(m)\top}_{g}\mid Z^{(N)}]-\operatorname{Id}\|_{op}\to0$ in probability), and $\max_m\|W^{(m)}_{r}\|_2\to0$ in probability. If $J_N/M_N\to0$, the head of the localized GBC algorithm, centered at $S(Y)$, produces a law $\widehat\Pi_N$ with $\sqrt N\,\mathscr{W}_{1,H^{-k-2}}\big(\widehat\Pi_N,N(S(Y),\Sigma_N)\big)\to0$ in probability.

Source: [`source/chapters/ext/m3c.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m3c.tex), label `m:prop:locres`.

### Chapter 17. Heat, Navier Stokes and Schrödinger: Examples and Experiments

<a id="gram_concentration_and_the_finite_bernstein_von_mises_error"></a>

#### Gram matrix concentration and the finite N Bernstein von Mises error for the heat equation

Proposition 17.1, page 332 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: proved.

Statement. Let $e_1,\dots,e_D$ be real orthonormal eigenfunctions of the Laplacian on $\mathbb{T}^d$, $-\Delta e_j=\lambda_je_j$, with $\|e_j\|_\infty\le\sqrt2$ for all $j\le D$. Consider the heat equation $\partial_tu=\nu\Delta u$ with $\nu>0$ and initial condition $\theta=\sum_{j\le D}\theta_je_j$, observed at $N$ independent points $(t_i,x_i)$ drawn uniformly from $[0,T]\times\mathbb{T}^d$ with unit variance Gaussian noise, so that $Y=\Phi\theta+\varepsilon$ with design matrix $\Phi_{ij}=e^{-\nu\lambda_jt_i}e_j(x_i)$, $i\le N$, $j\le D$. Put $\iota_j=\frac1T\int_0^Te^{-2\nu\lambda_jt}\,\mathrm{d}t=(1-e^{-2\nu\lambda_jT})/(2\nu\lambda_jT)$ and suppose $N\ge D\log D$. Then, with the absolute constant $c=12$, $\|N^{-1}\Phi^\top\Phi-\operatorname{diag}(\iota_j)\|_{op}\le c\sqrt{D\log D/N}$ with probability at least $1-D^{-1}$. Consequently, on the same event, if $c\sqrt{D\log D/N}<\min_j\iota_j$ then, for a Gaussian prior $N(0,\Sigma_0)$ on $\theta$ with $\Sigma_0$ positive definite, the exact posterior covariance $V_N=(\Phi^\top\Phi+\Sigma_0^{-1})^{-1}$ and its Bernstein von Mises prediction $\bar V_N=(N\operatorname{diag}(\iota_j)+\Sigma_0^{-1})^{-1}$ satisfy $\|NV_N-N\bar V_N\|_{op}\le c\sqrt{D\log D/N}\,\big/\,\big(\min_j\iota_j\,(\min_j\iota_j-c\sqrt{D\log D/N})\big)$.

Source: [`source/chapters/ext/m4a.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m4a.tex), label `m:prop:gram`.

<a id="information_operator_of_nls_about_a_plane_wave"></a>

#### Information operator of the cubic nonlinear Schrödinger equation about a plane wave (Bogoliubov blocks)

Proposition 17.5, page 356 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: proved.

Statement. Let $\kappa\in\mathbb{R}$, $d\le2$, and let $u$ solve the cubic nonlinear Schrödinger equation $i\partial_tu+\Delta u=\kappa|u|^2u$ on $\mathbb{T}^d$ with the constant real initial condition $\theta_0=a$, so that $u_0(t)=a\,e^{-i\kappa a^2t}$. The linearization at $u_0$ is $i\partial_tU+\Delta U=\kappa(2|u_0|^2U+u_0^2\bar U)$, $U(0)=h$. Writing $U=e^{-i\kappa a^2t}(\phi+i\psi)$ with $\phi,\psi$ real, the Fourier coefficients $(\phi_p,\psi_p)$ at the wave vector $p=2\pi k$, $k\in\mathbb{Z}^d$, satisfy $\frac{d}{dt}(\phi_p,\psi_p)^\top=A_p(\phi_p,\psi_p)^\top$ with $A_p=\begin{pmatrix}0&|p|^2\\-(|p|^2+2\kappa a^2)&0\end{pmatrix}$, where $|p|^2=4\pi^2|k|^2$ is the eigenvalue of $-\Delta$ at that mode. Put $\omega_p^2=|p|^2(|p|^2+2\kappa a^2)$ (the Bogoliubov dispersion relation) and let $M_p(t)=e^{tA_p}$ be the propagator. Then, with $(\mathrm{Re}\,U,\mathrm{Im}\,U)$ observed at points uniform on $[0,T]\times\mathbb{T}^d$, the information operator of the linearized model (the linearization composed with its adjoint in unnormalized $L^2([0,T]\times\mathbb{T}^d)$) is block diagonal over Fourier modes with $2\times2$ blocks $\Theta_p(T)=\int_0^TM_p(t)^\top M_p(t)\,\mathrm{d}t$ acting on $(\phi_p(0),\psi_p(0))$.
In the stable case $\omega_p^2>0$ (which excludes the block $p=0$, where $\omega_0=0$), with $\omega=\omega_p$ and $r=\omega_p/|p|^2=(1+2\kappa a^2/|p|^2)^{1/2}$: $M_p(t)=\begin{pmatrix}\cos\omega t&r^{-1}\sin\omega t\\-r\sin\omega t&\cos\omega t\end{pmatrix}$ and $\Theta_p(T)=\frac T2\begin{pmatrix}1+r^2&0\\0&1+r^{-2}\end{pmatrix}+\frac{\sin2\omega T}{4\omega}\begin{pmatrix}1-r^2&0\\0&1-r^{-2}\end{pmatrix}+\frac{\sin^2\omega T}{2\omega}(r^{-1}-r)\begin{pmatrix}0&1\\1&0\end{pmatrix}$, so that $\Theta_p(T)=T\operatorname{Id}+O(\kappa a^2T/|p|^2)+O(|p|^{-2})$ as $|p|\to\infty$, and $\det\Theta_p(T)\ge T^2$ for every $p$ and every $T>0$.
In the unstable case $\omega_p^2<0$ (which happens for $\kappa<0$ and $|p|^2<2|\kappa|a^2$, the modulational or Benjamin Feir instability), with $\gamma=|\omega_p|$ and $\rho=\gamma/|p|^2$: $M_p(t)=\begin{pmatrix}\cosh\gamma t&\rho^{-1}\sinh\gamma t\\\rho\sinh\gamma t&\cosh\gamma t\end{pmatrix}$ and $\Theta_p(T)=\frac T2\begin{pmatrix}1-\rho^2&0\\0&1-\rho^{-2}\end{pmatrix}+\frac{\sinh2\gamma T}{4\gamma}\begin{pmatrix}1+\rho^2&0\\0&1+\rho^{-2}\end{pmatrix}+\frac{\sinh^2\gamma T}{2\gamma}(\rho+\rho^{-1})\begin{pmatrix}0&1\\1&0\end{pmatrix}$; as $\gamma T\to\infty$ the largest eigenvalue of $\Theta_p(T)$ is asymptotic to $(\rho+\rho^{-1})^2e^{2\gamma T}/(8\gamma)$ and its smallest eigenvalue tends to $1/(2\gamma)$.

Source: [`source/chapters/ext/m4d.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m4d.tex), label `m:prop:bog`.

<a id="bogoliubov_block_determinant_trace_and_smallest_eigenvalue"></a>

#### Determinant, trace and smallest eigenvalue of the Bogoliubov information block

Lemma 17.6, page 359 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: proved.

Statement. Let $\kappa\in\mathbb{R}$ and $a\in\mathbb{R}$, and consider the cubic nonlinear Schrödinger equation $i\partial_tu+\Delta u=\kappa|u|^2u$ on $\mathbb{T}^d$ linearized about the constant solution $u_0(t)=a\,e^{-i\kappa a^2t}$. For the wave vector $p=2\pi k$, $k\in\mathbb{Z}^d$, let $A_p=\begin{pmatrix}0&|p|^2\\-(|p|^2+2\kappa a^2)&0\end{pmatrix}$, $M_p(t)=e^{tA_p}$, $\omega_p^2=|p|^2(|p|^2+2\kappa a^2)$ and $\Theta_p(T)=\int_0^TM_p(t)^\top M_p(t)\,\mathrm{d}t$ (the $2\times2$ block of the information operator of the linearization over $[0,T]\times\mathbb{T}^d$). Write $\omega=\omega_p$ and $r=r_p=\omega_p/|p|^2$ in the elliptic case $\omega_p^2>0$, and $\gamma=\gamma_p=|\omega_p|$ and $\rho=\rho_p=\gamma_p/|p|^2$ in the hyperbolic case $\omega_p^2<0$. Then for every $T>0$:
(i) $\det M_p(t)=1$ for all $t$, and consequently $\det\Theta_p(T)\ge T^2$ for every $p$ and every $T>0$, with no restriction on $\omega_pT$.
(ii) For $p\ne0$ in the elliptic case, $\det\Theta_p(T)=T^2+\frac{(r-r^{-1})^2}{4}\big(T^2-\frac{\sin^2\omega T}{\omega^2}\big)$; in the hyperbolic case, $\det\Theta_p(T)=T^2+\frac{(\rho+\rho^{-1})^2}{4}\big(\gamma^{-2}\sinh^2\gamma T-T^2\big)$. At $p=0$, $\Theta_0(T)=T\begin{pmatrix}1+\frac43s^2&-s\\-s&1\end{pmatrix}$ with $s=\kappa a^2T$, so that $\det\Theta_0(T)=T^2(1+\frac13s^2)$.
(iii) In the elliptic case, $\mathrm{tr}\,\Theta_p(T)=2T+(r-r^{-1})^2\int_0^T\sin^2\omega t\,\mathrm{d}t\le T(r^2+r^{-2})$, and $\mathrm{tr}\,\Theta_0(T)=T(2+\frac43s^2)$.
(iv) In the elliptic case, $\lambda_{\min}(\Theta_p(T))\ge T/(r_p^2+r_p^{-2})$ and $\lambda_{\min}(\Theta_0(T))\ge T/4$. If $r_p\ge1$ this implies $\lambda_{\min}\ge T/(1+r_p^2)$; if $r_p<1$ the bound $T/(1+r_p^2)$ is false in general, so $r_p^2+r_p^{-2}$ cannot be replaced by $1+r_p^2$.
(v) In the defocusing case $\kappa>0$, $1<r_p^2\le1+2\kappa a^2/\lambda_1$ for $p\ne0$, where $\lambda_1=4\pi^2$ is the smallest nonzero eigenvalue of $-\Delta$ on $\mathbb{T}^d$, and $\inf_p\lambda_{\min}(\Theta_p(T))\ge\dfrac{T\lambda_1}{4(\lambda_1+\kappa a^2)}$ and $\sup_{p\ne0}\lambda_{\max}(\Theta_p(T))\le\dfrac{2T(\lambda_1+\kappa a^2)}{\lambda_1}$.
(vi) In the focusing band $\omega_p^2<0$, as $\gamma_pT\to\infty$, $\lambda_{\max}(\Theta_p(T))\sim\mathrm{tr}\,\Theta_p(T)\sim(\rho_p+\rho_p^{-1})^2e^{2\gamma_pT}/(8\gamma_p)$ and $\lambda_{\min}(\Theta_p(T))=\det\Theta_p(T)/\lambda_{\max}(\Theta_p(T))\to1/(2\gamma_p)$; the bound $\lambda_{\min}\ge T^2/\mathrm{tr}\,\Theta_p(T)$ still holds but is exponentially small in $\gamma_pT$, and the condition number satisfies $\lambda_{\max}/\lambda_{\min}\sim\frac14(\rho_p+\rho_p^{-1})^2e^{2\gamma_pT}$.

Source: [`source/chapters/ext/m4d.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m4d.tex), label `m:lem:bogmin`.

<a id="linearized_stability_and_condition_2f_analogue_for_the_defocusing_plane_wave"></a>

#### Linearized stability and the analogue of Condition 2F for the defocusing NLS plane wave

Corollary 17.7, page 362 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: proved.

Statement. Let $\kappa>0$ (defocusing), $d\le2$ and $a\in\mathbb{R}$, let $\Omega=\mathbb{T}^d$ and $\mathcal{X}=[0,T]\times\mathbb{T}^d$, and let $\mathbb{I}_{\theta_0}$ be the linearization at the plane wave $u_0(t)=a\,e^{-i\kappa a^2t}$ (initial condition $\theta_0=a$) of the solution map of $i\partial_tu+\Delta u=\kappa|u|^2u$, namely $h\mapsto U$ with $i\partial_tU+\Delta U=\kappa(2|u_0|^2U+u_0^2\bar U)$, $U(0)=h$, with adjoint $\mathbb{I}_{\theta_0}^*$ taken with respect to unnormalized $L^2(\mathcal{X})$. Let $\lambda_1=4\pi^2$ be the smallest nonzero eigenvalue of $-\Delta$ and set $c_\star^2=\dfrac{T\lambda_1}{4(\lambda_1+\kappa a^2)}$ and $C_\star^2=\max\Big\{\dfrac{2T(\lambda_1+\kappa a^2)}{\lambda_1},\ T\big(2+\tfrac43\kappa^2a^4T^2\big)\Big\}$. Then for every $h\in L^2(\mathbb{T}^d;\mathbb{C})$, $c_\star^2\|h\|_{L^2(\Omega)}^2\le\|\mathbb{I}_{\theta_0}h\|_{L^2(\mathcal{X})}^2=\langle h,\mathbb{I}_{\theta_0}^*\mathbb{I}_{\theta_0}h\rangle\le C_\star^2\|h\|_{L^2(\Omega)}^2$, and consequently:
(a) $\mathbb{I}_{\theta_0}^*\mathbb{I}_{\theta_0}$ is a homeomorphism of $H^\eta(\mathbb{T}^d)$ for every $\eta\in\mathbb{R}$, with the explicit constants $c_\star^2,C_\star^2$; this is the analogue of Nickl's Condition 2F (invertibility of the information operator: $\Delta\mathbb{I}^*\mathbb{I}$ is a homeomorphism of $H^\eta_0$ for $\eta\ge\eta_0$) without the factor $\Delta$ and with $\eta_0=0$, while Condition 2F as stated fails because $\Delta\mathbb{I}_{\theta_0}^*\mathbb{I}_{\theta_0}$ loses two derivatives;
(b) $\|\mathbb{I}_{\theta_0}h\|_{L^2(\mathcal{X})}\ge c_\star\|h\|_{L^2(\Omega)}\ge c_\star\|h\|_{H^{-1}(\Omega)}$, which is the estimate of Nickl's Condition 2E (the stability estimate $\|\mathscr{G}(\theta)-\mathscr{G}(\theta_0)\|_{L^2(\mathcal{X})}\ge c\|\theta-\theta_0\|_{H^{-1}}$ for the solution map $\mathscr{G}$) with the linearization $\mathbb{I}_{\theta_0}$ in place of $\mathscr{G}$ and the stronger norm $L^2$ rather than $H^{-1}$;
(c) the Gaussian measure $\mathcal{N}_{\theta_0}=N\big(0,T(\mathbb{I}_{\theta_0}^*\mathbb{I}_{\theta_0})^{-1}\big)=N\big(0,T\operatorname{diag}\Theta_p(T)^{-1}\big)$ has per block covariance $T\Theta_p(T)^{-1}$ with $\|T\Theta_p(T)^{-1}\|\le T/\lambda_{\min}(\Theta_p(T))\le4(\lambda_1+\kappa a^2)/\lambda_1$ uniformly in $p$ and in $T$, so that $\mathcal{N}_{\theta_0}$ is tight on $H^{-s}(\mathbb{T}^d)$ for every $s>d/2$.

Source: [`source/chapters/ext/m4d.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m4d.tex), label `m:cor:condE`.

<a id="stability_of_the_cubic_nls_solution_map"></a>

#### Stability of the cubic NLS solution map

Proposition 17.8, page 364 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: proved.

Statement. Let $\kappa\ne0$ be real, $d\in\{1,2\}$, $\Omega=\mathbb{T}^d$ and $\mathcal{X}=[0,T]\times\Omega$, and let $u,v$ solve $i\partial_tu+\Delta u=\kappa|u|^2u$ on $[0,T]\times\mathbb{T}^d$ with initial data $\theta,\vartheta$ in $H^1$ if $d=1$ and in $H^2$ if $d=2$; write $\mathscr{G}(\theta)=u_\theta$ for the solution map. Suppose $\|u(t)\|_{L^\infty}\le M_\infty$ and $\|v(t)\|_{L^\infty}\le M_\infty$ for $t\le T$, with $M_\infty>0$. Then for $t\le T$, $e^{-6|\kappa|M_\infty^2t}\|\theta-\vartheta\|_{L^2(\Omega)}^2\le\|u(t)-v(t)\|_{L^2(\Omega)}^2\le e^{6|\kappa|M_\infty^2t}\|\theta-\vartheta\|_{L^2(\Omega)}^2$, and, with the unnormalized norm of $L^2(\mathcal{X})$, $\|\mathscr{G}(\theta)-\mathscr{G}(\vartheta)\|_{L^2(\mathcal{X})}^2\ge\dfrac{1-e^{-6|\kappa|M_\infty^2T}}{6|\kappa|M_\infty^2}\|\theta-\vartheta\|_{L^2(\Omega)}^2\ge Te^{-6|\kappa|M_\infty^2T}\|\theta-\vartheta\|_{H^{-1}(\Omega)}^2$. A bound $M_\infty=M_\infty(T,\kappa,B)$ valid for all data in a ball of radius $B$ exists in each of the following cases: (a) $d=1$, either sign of $\kappa$, every ball of $H^1$; (b) $d=2$, $\kappa>0$, every ball of $H^2$; (c) $d=2$, $\kappa<0$, the balls of $H^2$ with $2|\kappa|C_2B^2T<1$, where $C_2$ is a constant such that $\||f|^2f\|_{H^2}\le C_2\|f\|_{H^2}^3$. On such a ball Nickl's Condition 2E holds for $\mathscr{G}$ (the stability estimate $\|\mathscr{G}(\theta)-\mathscr{G}(\vartheta)\|_{L^2(\mathcal{X})}\ge c\|\theta-\vartheta\|_{H^{-1}}$), with the stronger norm $L^2$ on the right and the constant $c=T^{1/2}e^{-3|\kappa|M_\infty^2T}$; Condition 2A (uniform $L^\infty$ bounds) holds with the bound $M_\infty$; and the upper bound gives the $L^2$ Lipschitz estimate of Condition 2B, $\|\mathscr{G}(\theta)-\mathscr{G}(\vartheta)\|_{L^2(\mathcal{X})}^2\le\dfrac{e^{6|\kappa|M_\infty^2T}-1}{6|\kappa|M_\infty^2}\|\theta-\vartheta\|_{L^2(\Omega)}^2$.

Source: [`source/chapters/ext/m4d.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m4d.tex), label `m:prop:nlsstab`.

<a id="linear_schrodinger_transfer"></a>

#### Linear Schrödinger transfer: exact posterior and Bernstein von Mises theorem

Proposition 17.10, page 366 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: proved.

Statement. Consider the linear Schrödinger equation $i\partial_tu=-\Delta u$ on $\mathbb{T}^d$, $u_\theta(t)=e^{it\Delta}\theta=\sum_je^{-i\lambda_jt}\theta_je_j$ for $\theta\in L^2(\mathbb{T}^d;\mathbb{C})$, where $e_j(x)=e^{2\pi ik_j\cdot x}$ is the Fourier basis and $\lambda_j=4\pi^2|k_j|^2\asymp j^{2/d}$ is nondecreasing. The data $Z^{(N)}$ are $Y_i=u_{\theta_0}(t_i,x_i)+\varepsilon_i$ at $N$ independent points $(t_i,x_i)$ uniform on $[0,T]\times\mathbb{T}^d$, with noise whose real and imaginary parts are independent standard Gaussian, where $\theta_0$ is the true initial condition. The prior is the Gaussian series prior of Nickl, $\theta=\sum_{j\le D}\theta_je_j$ truncated to the first $D=D_N$ modes, in which the real and the imaginary part of $\theta_j$ are independent with precision $\rho^{-2}\lambda_j^\alpha$, where $\rho^{-2}=N\delta_N^2$, $\delta_N=N^{-\gamma/(2\gamma+d)}$, $\alpha=\gamma$ and $\gamma>d/2$. Let $\tilde\theta_N$ be the posterior mean, let $\Phi_{ij}=e^{-i\lambda_jt_i}e_j(x_i)$ be the design matrix with adjoint summary $(\Phi^*Y)_j=\sum_ie^{i\lambda_jt_i}\overline{e_j(x_i)}Y_i$, and let $N(0,\operatorname{Id})$ denote complex white noise, whose real and imaginary parts are independent with covariance $\operatorname{Id}$. Then:
(a) the posterior is exactly Gaussian, the adjoint summary $\Phi^*Y$ together with the design is exactly sufficient, and the quantile map of generative Bayesian computation (the map from the summary to the posterior quantiles) is exactly affine, with per mode scale $(N+\rho^{-2}\lambda_j^\alpha)^{-1/2}$ in the real and in the imaginary part when the Gram matrix $\Phi^*\Phi$ of the design is replaced by its limit $N\operatorname{Id}$;
(b) if $D_N\to\infty$ and $D_N=o(N^{d/(2\gamma+d)})$, then $\mathscr{W}_{1,H^{-a}}\big(\operatorname{Law}(\sqrt N(\theta-\tilde\theta_N)\mid Z^{(N)}),N(0,\operatorname{Id})\big)\to0$ in probability (under the data law with true initial condition $\theta_0$) for every $a>d/2$, where $\mathscr{W}_{1,H^{-a}}$ is the Wasserstein distance of order one on $H^{-a}(\mathbb{T}^d;\mathbb{C})$;
(c) if in addition $\theta_0\in H^\gamma$ and $N\lambda_{D_N}^{-(a+\gamma)}\to0$, then $\sqrt N(\tilde\theta_N-\theta_0)\xrightarrow{d}N(0,\operatorname{Id})$ in $H^{-a}$; the choice $D_N\asymp N^{d/(2\gamma+d)}/\log N$ meets the conditions of (b) and (c) for every $a>d/2$;
(d) (b) and (c) hold with $u_\theta(t)$, $u_{\tilde\theta_N}(t)$ and $u_{\theta_0}(t)$ in place of $\theta$, $\tilde\theta_N$ and $\theta_0$, at every $t$ and uniformly in $t$, with the same limit $e^{it\Delta}_\#N(0,\operatorname{Id})=N(0,\operatorname{Id})$, and no supremum norm statement holds at any $t$.

Source: [`source/chapters/ext/m4d.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m4d.tex), label `m:prop:sch`.

<a id="the_transfer_theorem_for_the_linear_schrodinger_equation"></a>

#### The transfer theorem for the linear Schrödinger equation

Corollary 17.11, page 370 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: proved.

Statement. Work in the setting of the linear Schrödinger transfer result: data from the linear Schrödinger equation $i\partial_tu=-\Delta u$ on $\mathbb{T}^d$ with true initial condition $\theta_0\in H^\gamma$, $\gamma>d/2$, observed with noise whose real and imaginary parts are independent standard Gaussian at $N$ independent uniform points of $[0,T]\times\mathbb{T}^d$; the Gaussian series prior of Nickl truncated to the first $D_N$ modes, with precision $\rho^{-2}\lambda_j^\gamma$ for the real and for the imaginary part of the $j$th coefficient, $\rho^{-2}=N\delta_N^2$, $\delta_N=N^{-\gamma/(2\gamma+d)}$; the exact posterior $\Pi_N$ with mean $\tilde\theta_N$; $D_N\to\infty$, $D_N=o(N^{d/(2\gamma+d)})$; and, for a fixed $a>d/2$, $N\lambda_{D_N}^{-(a+\gamma)}\to0$. Let $\widehat\Pi_N$ be a measure produced by generative Bayesian computation (GBC), with mean $\hat\theta^{\mathrm G}_N$, such that $\sqrt N\,\mathscr{W}_{1,H^{-a}}(\widehat\Pi_N,\Pi_N)\to0$ in probability (the exact posterior $\widehat\Pi_N=\Pi_N$ satisfies this). Let $N(0,\operatorname{Id})$ denote complex white noise, whose real and imaginary parts are independent with covariance $\operatorname{Id}$. Then:
(i) $\mathscr{W}_{1,H^{-a}}\big(\operatorname{Law}(\sqrt N(\theta-\hat\theta^{\mathrm G}_N)\mid\theta\sim\widehat\Pi_N),N(0,\operatorname{Id})\big)\to0$ in probability and $\sqrt N(\hat\theta^{\mathrm G}_N-\theta_0)\xrightarrow{d}N(0,\operatorname{Id})$ in $H^{-a}$;
(ii) the statements of (i) hold for $u_\theta(t)$, $u_{\hat\theta^{\mathrm G}_N}(t)$ and $u_{\theta_0}(t)$ at every $t$, uniformly in $t$, with the same limit;
(iii) for a map $\Phi:H^{-a}\to\mathbb{B}$ into a Banach space $\mathbb{B}$ that is Hadamard differentiable at $u_{\theta_0}(t)$, $\sqrt N\big(\Phi(u_{\hat\theta^{\mathrm G}_N}(t))-\Phi(u_{\theta_0}(t))\big)\xrightarrow{d}\dot\Phi_{u_{\theta_0}(t)}[W]$ with $W\sim N(0,\operatorname{Id})$, and the ball in $H^{-a}$ about $\hat\theta^{\mathrm G}_N$ of $\widehat\Pi_N$ probability $1-\beta$ contains $\theta_0$ with probability tending to $1-\beta$ under the data law with true initial condition $\theta_0$;
(iv) under the data law with true initial condition $\theta_0+h/\sqrt N$, for every $h\in H^\gamma$, (i) to (iii) hold with $\theta_0+h/\sqrt N$ in place of $\theta_0$, so that $\hat\theta^{\mathrm G}_N$ is a regular estimator sequence, and for $\psi\in H^a$ the limit $N(0,\|\psi\|_{L^2}^2)$ of $\sqrt N\,\mathrm{Re}\langle\psi,\hat\theta^{\mathrm G}_N-\theta_0\rangle$ is the efficient one, so that $\mathrm{Re}\langle\psi,\hat\theta^{\mathrm G}_N\rangle$ is efficient among regular estimator sequences of $\mathrm{Re}\langle\psi,\theta\rangle$.

Source: [`source/chapters/ext/m4d.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m4d.tex), label `m:cor:schtransfer`.

<a id="beyond_the_plane_wave"></a>

#### Beyond the plane wave: information operator of cubic NLS about a multimode background

Open Question 17.12, page 371 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: open.

Statement. Open question. For the cubic nonlinear Schrödinger equation $i\partial_tu+\Delta u=\kappa|u|^2u$ on $\mathbb{T}^d$ ($d\le2$), one computes the information operator $\mathbb{I}_{\theta_0}^*\mathbb{I}_{\theta_0}$ of the linearization (adjoint in unnormalized $L^2([0,T]\times\mathbb{T}^d)$) about a constant background $\theta_0=a$ exactly, mode by mode, through the Bogoliubov dispersion relation. Extend this to a multimode background $u_0$: write $\mathbb{I}_{\theta_0}^*\mathbb{I}_{\theta_0}=T\operatorname{Id}+\mathcal{R}+\mathcal{K}$ with $\mathcal{K}$ compact and $\mathcal{R}$ supported on the four wave resonant manifold $\{(k_1,k_2,k_3,k_4):k_1+k_2=k_3+k_4,\ \lambda_{k_1}+\lambda_{k_2}=\lambda_{k_3}+\lambda_{k_4}\}$, where $\lambda_k=4\pi^2|k|^2$, and characterize the triples $(\kappa,\theta_0,T)$ for which $T\operatorname{Id}+\mathcal{R}$ is uniformly invertible. In the focusing case, prove a Bernstein von Mises theorem for fixed $T$ with constants exponential in the largest modulational growth rate.

Source: [`source/chapters/ext/m4d.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m4d.tex), label `m:op:planewave`.

<a id="lsm_gbc_dictionary_for_optimal_stopping_and_the_inverse_problem"></a>

#### LSM is GBC for optimal stopping; GBC is LSM for the inverse problem (Longstaff Schwartz dictionary)

Proposition 17.13, page 372 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: proved.

Statement. Let $(X_t)$ be a Markov process, $V_{t+1}$ a payoff with $\mathbb{E}V_{t+1}^2<\infty$, $C_t(x)=\mathbb{E}[V_{t+1}\mid X_t=x]$ the continuation value, and $L_1,\dots,L_K$ basis functions such that the $L_k(X_t)$ are square integrable and linearly independent in $L^2$. As the number of simulated paths grows, the Longstaff Schwartz regression coefficients $\hat\beta_t=\operatorname*{arg\,min}_\beta\sum_m\big(V^{(m)}_{t+1}-\sum_k\beta_kL_k(X^{(m)}_t)\big)^2$ converge almost surely to the coefficients of the $L^2$ projection of $C_t$ onto $\mathrm{span}\{L_k\}$, and $C_t(x)$ is the posterior mean summary $\mathbb{E}[\theta\mid S]$ for the "parameter" $\theta=V_{t+1}$ given the "data" $S=X_t$. Conversely, Step 2 of the generative Bayesian computation (GBC) algorithm (the fit of a generator of the parameter given the summary on the training pairs simulated in Step 1, with $\theta^{(m)}$ drawn from the prior and $Z^{(m)}$ from the model) with the mean regression loss and basis functions of the summary $S_N$ is an LSM regression with the following roles: paths correspond to prior draws $\theta^{(m)}$, the state $X_t$ to the summary $S_N(Z^{(m)})$, the payoff $V_{t+1}$ to $\theta^{(m)}$, and the continuation value to the posterior mean $\mathbb{E}[\theta\mid S_N]$. In the linear Gaussian case (the linear model $Y=\Phi\theta+\varepsilon$ with standard Gaussian noise, a Gaussian prior and $S_N=\Phi^\top Y$ the adjoint statistic), with the design held fixed, the posterior mean is linear in $S_N$, so a linear basis is exact, just as LSM with a linear basis is exact when the continuation value is linear in the state.

Source: [`source/chapters/ext/m4e.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m4e.tex), label `m:prop:lsm`.

<a id="two_limit_convergence_of_the_regression_summary"></a>

#### Two limit convergence of the regression summary (least squares Monte Carlo and GBC)

Theorem 17.14, page 373 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: conditional on Only the identification of the limit in case (c), the one step summary, is conditional: it rests on the book's theorem on the Jiang Wong posterior mean summary under Bernstein von Mises, which assumes Assumption U (a Bernstein von Mises statement for the posterior, uniform over a set of parameters of prior probability tending to one and small also conditionally on the observed summary), which the book does not prove and lists as an open question, and on the hypotheses of the book's proposition equating the one step summary with Nickl's efficient centering. The limits in the number of simulations and of basis functions, and cases (a) and (b), are proved without it..

Statement. Let $\Pi$ be a prior on $\theta$, taking values in $\mathbb{R}^D$ or in a separable Hilbert space, with $\mathbb{E}\|\theta\|^2<\infty$; let data $Z$ be drawn from the observation model given $\theta$ and let $S=S_N(Z)$ be a summary statistic. Let $(\theta^{(m)},S^{(m)})_{m\le M}$ be independent draws of $(\theta,S)$ from this prior predictive law (Step 1 of generative Bayesian computation), let $\operatorname{Law}(S)$ be the law of $S$, let $\{L_k\}$ be an orthonormal basis of $L^2(\operatorname{Law}(S))$, and let $\hat m_{K,M}(s)=\sum_{k\le K}\hat\beta_kL_k(s)$ be the least squares regression of $\theta^{(m)}$ on $L_1(S^{(m)}),\dots,L_K(S^{(m)})$, coordinate by coordinate. Then for fixed $K$, $\hat m_{K,M}\to m_K:=\sum_{k\le K}\langle\mathbb{E}[\theta\mid S],L_k\rangle L_k$ almost surely in $L^2(\operatorname{Law}(S))$ as $M\to\infty$, and $m_K\to\mathbb{E}[\theta\mid S]$ in $L^2(\operatorname{Law}(S))$ as $K\to\infty$. If moreover $\sum_{k\le K}L_k(s)^2\le bK$ for all $s$ and $K$ and some constant $b$ (as for a basis bounded by $\sqrt b$), and $K_M\to\infty$ with $K_M\log K_M/M\to0$, then $\hat m_{K_M,M}\to\mathbb{E}[\theta\mid S]$ in $L^2(\operatorname{Law}(S))$ in probability. The regression recovers $\mathbb{E}[\theta\mid S]$, the posterior mean given the summary, and not the posterior mean $m(Z)=\mathbb{E}[\theta\mid Z^{(N)}]$ itself: always $\mathbb{E}[\theta\mid S]=\mathbb{E}[m(Z)\mid S]$, and this equals $m(Z)$ if and only if $m(Z)$ is $\sigma(S)$ measurable. Moreover:
(a) if $S=m(Z)$ then $\mathbb{E}[\theta\mid S]=S=m(Z)$ exactly, for every $N$;
(b) if, in the linear model $Y=\Phi\theta+\varepsilon$ with standard Gaussian noise and Gaussian prior, $S$ is the adjoint statistic $\Phi^\top Y$ with the design held at its observed value in Step 1, or the pair $(\Phi^\top Y,\Phi^\top\Phi)$ when the design is drawn afresh, then $S$ is sufficient and $\mathbb{E}[\theta\mid S]=m(Z)$ exactly, for every $N$;
(c) if $S=\hat S^{J_N}_N$ is the one step efficient score statistic (a cross fitted Gauss Newton step from a preliminary estimate, projected on the first $J_N$ modes), then, under Assumption U for $S_N=\hat S^{J_N}_N$ (a uniform Bernstein von Mises statement) and the hypotheses of the proposition equating this statistic with Nickl's efficient centering (among them Conditions 1 and 2 of Nickl (2024) and the rate and Lipschitz weight conditions of that proposition), $\sqrt N\,\|\mathbb{E}[\theta\mid S]-m(Z)\|_{H^{-k-2}}\to0$ in probability, where $k$ is the Sobolev index of Nickl's Bernstein von Mises theorem.
Consequently, under (a) or (b) the regression summary $\hat m_{K_M,M}(S)$, the center of the GBC posterior built on it, converges to the exact posterior mean $m(Z)$ in the double limit, in $L^2(\operatorname{Law}(S))$, that is, on average over the prior predictive law of the data and not at a fixed observed value; under (c) it agrees with it only to $o(N^{-1/2})$ in $H^{-k-2}$.

Source: [`source/chapters/ext/m4e.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m4e.tex), label `m:thm:lsmgbc`.

<a id="the_adjoint_statistic_is_a_storvik_statistic"></a>

#### The adjoint statistic is a Storvik statistic

Proposition 17.15, page 376 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: proved.

Statement. Consider the linear model $Y=\Phi\theta+\varepsilon$ with unit variance Gaussian noise and Gaussian prior $\theta\sim N(0,\Sigma_0)$ on $\mathbb{R}^D$, in which the $i$th row of the design matrix $\Phi$ is $\phi_i^\top$ with $\phi_i=(s_j(t_i)e_j(x_i))_{j\le D}$ ($s_j(t)$ being the time factor of the diagonal linear evolution, for example $e^{-\nu\lambda_jt}$ for the heat equation), and order the observations by time. The sufficient statistic $S_n=\Phi_{1:n}^\top Y_{1:n}$ and the Gram matrix $G_n=\Phi_{1:n}^\top\Phi_{1:n}$ of the first $n$ observations satisfy the recursions $S_{n+1}=S_n+\phi_{n+1}Y_{n+1}$ and $G_{n+1}=G_n+\phi_{n+1}\phi_{n+1}^\top$, and the posterior after $n$ observations is $N\big((G_n+\Sigma_0^{-1})^{-1}S_n,\,(G_n+\Sigma_0^{-1})^{-1}\big)$. Consequently the sequential scheme that carries $(S_n,G_n)$ and, at each step, draws particles independently from this Gaussian is exact: $(S_n,G_n)$ is a deterministic function of the first $n$ observations, each new observation is absorbed by the rank one update above, and every particle is an exact draw from the posterior after $n$ observations.

Source: [`source/chapters/ext/m4e.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m4e.tex), label `m:prop:storvik`.

<a id="uniformity"></a>

#### Uniformity: the uniform Bernstein von Mises assumption and related open hypotheses

Open Question 17.18, page 380 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: open.

Statement. Open question. Prove the uniform Bernstein von Mises assumption (Assumption U of the book), with the rate $\bar\epsilon_N\to0$ used in the book's theorem on the identity skip quantile generator. Assumption U: for a summary statistic $S_N$, a prior $\Pi$, a true parameter $\theta_0$, observations on $[0,T]\times\mathbb{T}^d$, the linearization $\mathbb{I}_\vartheta$ at $\vartheta$ of the solution map, $\mathcal{N}_\vartheta=N\big(0,T(\mathbb{I}_\vartheta^*\mathbb{I}_\vartheta)^{-1}\big)$, and Sobolev indices $k$ and $\zeta>d/2$ as in Nickl's Bernstein von Mises theorem and Condition 2D, there is a set $\Theta_N$ of parameters such that (U1) $\Pi(\Theta_N)\to1$, $\theta_0\in\Theta_N$ for all large $N$, and $\bar\epsilon_N:=\sup_{\vartheta\in\Theta_N}\mathbb{E}^{\mathbb{N}}_\vartheta\,\mathscr{W}_{1,H^{-k-2}}\big(\operatorname{Law}(\sqrt N(\theta-S_N)\mid Z^{(N)}),\mathcal{N}_\vartheta\big)\to0$, where $\mathbb{E}^{\mathbb{N}}_\vartheta$ is the expectation under the data law with parameter $\vartheta$; (U2) these discrepancies are uniformly integrable under the prior predictive law; (U3) $\vartheta\mapsto T(\mathbb{I}_\vartheta^*\mathbb{I}_\vartheta)^{-1}$ is Lipschitz from $(\Theta_N,\|\cdot\|_{H^\zeta})$ into bounded operators $H^{-k-2}\to H^{-k-4}$ and $\vartheta\mapsto\mathcal{N}_\vartheta$ is Lipschitz from $(\Theta_N,\|\cdot\|_{H^\zeta})$ into the probability measures on $H^{-k-2}$ with the distance $\mathscr{W}_{1,H^{-k-2}}$, both with constants that do not depend on $N$, the first moments $\mathrm{m}_1(\vartheta)=\int\|x\|_{H^{-k-2}}\,\mathrm{d}\mathcal{N}_\vartheta(x)$ satisfy $\int_{\Theta_N^c}\mathrm{m}_1\,\mathrm{d}\Pi\to0$ and $\Pi(\Theta_N^c)\sup_{\Theta_N}\mathrm{m}_1\to0$, $S_N\in\Theta_N$ with probability tending to one, and $\mathbb{E}^\Pi[\|\theta-S_N\|_{H^\zeta}\mid S_N]\to0$; (U4) for every $\theta_0\in\Theta_N$, $\mathbb{E}\big[\mathscr{W}_{1,H^{-k-2}}\big(\operatorname{Law}(\sqrt N(\theta-S_N)\mid Z^{(N)}),\mathcal{N}_{\theta_0}\big)\,\big|\,S_N\big]\to0$ in probability under the data law with true parameter $\theta_0$. The proof is to proceed by tracking the constants of Theorem 2 of Nickl (2024) and Theorem 2.8 of Konen and Nickl (2026) over the localization sets, and the same is asked for the uniform second moment bound used in the book's proposition on the one step summary under four approximate Bayesian computation criteria.

Source: [`source/chapters/ext/m4e.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ext/m4e.tex), label `m:op:unif`.

### Chapter 20. Filters, Gates and Local Rules

<a id="the_gain_of_the_score_function_filter"></a>

#### Gain of the score function filter under scale mixture noise

Proposition 20.8, page 421 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: proved.

Statement. Let $\theta$ be a real random variable with the normal law $N(m,P)$ of mean $m$ and variance $P>0$, and let $y=\theta+v$ be an observation with noise $v$. Let $\lambda$ be a positive random variable with law $\pi$ that is independent of $\theta$, and suppose that, given $\lambda$, the noise $v$ is independent of $\theta$ with the normal law $N(0,r/\lambda)$, where $r>0$. For $\lambda>0$ write $K_\lambda=P\lambda/(P\lambda+r)$ for the Kalman gain when the noise variance is $r/\lambda$. Then $\mathbb{E}[\theta\mid y]=(1-K)\,m+K\,y$ with $K=\mathbb{E}[K_\lambda\mid y]\in(0,1)$, and $\mathrm{Var}(\theta\mid y)=(1-K)P+(y-m)^2\,\mathrm{Var}(K_\lambda\mid y)$. The gain $K$ depends on $y$ only through $|y-m|$ and is nonincreasing in $|y-m|$. If $\lambda\equiv1$ then $K=P/(P+r)$.

Source: [`source/chapters/ch14_filters.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ch14_filters.tex), label `prop:gates_bayes`.

<a id="gamma_law_of_the_shot_noise_neuron"></a>

#### Gamma law and Thorin measure of the shot noise neuron

Theorem 20.9, page 423 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: proved.

Statement. Let the input spikes $t_k$ form a Poisson process of rate $\lambda>0$ on $\mathbb{R}$. Attach to the $k$th spike a mark $(\tau_k,\kappa_k)$, the marks being independent with a common law $M$ on $(0,\infty)^2$ and independent of the spike times, and given the marks let the amplitude $A_k$ be exponential with rate $\kappa_k$. Let $V=\sum_{t_k\le t}A_k e^{-(t-t_k)/\tau_k}$ be the stationary potential at time $t$. Then for every $\theta>0$, with both sides possibly equal to $+\infty$, $-\log\mathbb{E}\,e^{-\theta V}=\lambda\int\tau\log\big(1+\theta/\kappa\big)\,M(\mathrm{d}\tau,\mathrm{d}\kappa)=\int\log\big(1+\theta/y\big)\,U(\mathrm{d}y)$, where $U$ is the image of the measure $\lambda\tau\,M(\mathrm{d}\tau,\mathrm{d}\kappa)$ under $(\tau,\kappa)\mapsto\kappa$. If $\int\log(1+1/y)\,U(\mathrm{d}y)<\infty$, which is the condition that $U$ be a Thorin measure, then $V$ is a generalized Gamma convolution with Thorin measure $U$ and zero drift, that is, $\mathbb{E}\,e^{-\theta V}=\exp\big(-\int\log(1+\theta/y)\,U(\mathrm{d}y)\big)$ for $\theta>0$. Otherwise $V=\infty$ almost surely. In particular, if all marks equal $(\tau,\kappa)$ then $V$ has the Gamma law with shape $\lambda\tau$ and rate $\kappa$, and if $\tau_k$ and $\kappa_k$ are independent and $\kappa_k$ has law $\nu$ then $U=\lambda\,\mathbb{E}[\tau_k]\,\nu$.

Source: [`source/chapters/ch14_filters.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ch14_filters.tex), label `thm:shot_noise_neuron`.

### Chapter 22. Open Problems and the Bridge to Hilbert's Eighth Problem

<a id="open_problem_yor_exact_samplers"></a>

#### Open problem: exact samplers for Brownian functionals from Kent's eigenvalue expansion

Open Problem 4, page 445 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: open.

Statement. Open problem, posed as a program in the book. Kent's theorem writes the hitting time of a level $b$ by a regular one dimensional diffusion, started at a reflecting or entrance boundary $a$, as $\sum_{n\geq1}E_n/\lambda_n$, where $E_1,E_2,\dots$ are independent standard exponential variables and $0<\lambda_1<\lambda_2<\cdots$ are the eigenvalues of minus the generator on $(a,b)$ with Dirichlet condition at $b$ and the reflecting or entrance condition at $a$. For each $n$, the remainder $\sum_{k>n}E_k/\lambda_k$ after the first $n$ terms is a generalized Gamma convolution (a law on $[0,\infty)$ with Laplace transform $s\mapsto e^{-\phi(s)}$, $\phi(s)=cs+\int_{(0,\infty)}\log(1+s/y)\,U(\mathrm{d}y)$, where $c\geq0$ and $U$ is the Thorin measure) with an explicit Thorin measure. The problem is to identify a class of regular diffusions for which this remainder can be sampled exactly with finite expected cost, to prove that the resulting sampler is exact, and to use it to build a library of exact samplers for Brownian functionals.

Source: [`source/chapters/ch16_open.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ch16_open.tex), label `prob:yor`.

<a id="open_problem_kac_entropy_production_ggc_mixtures"></a>

#### Open problem: uniform entropy production bound for the Kac walk on conditioned products of normal scale mixtures

Open Problem 8, page 446 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: open.

Statement. Open problem. Consider the Kac walk with $N$ particles and total collision rate $N$: the velocities $v=(v_1,\dots,v_N)$ lie on the sphere $S^{N-1}(\sqrt N)=\{\sum_{i\leq N}v_i^2=N\}$, and at rate $N$ a pair $(i,j)$ is chosen uniformly and an angle $\theta$ uniformly on $[0,2\pi)$, and the pair is rotated by $\theta$. Let $\sigma_N$ be the uniform probability law on the sphere. For a probability density $F$ with respect to $\sigma_N$ let $H_N(F)=\int F\log F\,\mathrm{d}\sigma_N$ be its relative entropy with respect to $\sigma_N$, and let $D_N(F)=-\frac{\mathrm{d}}{\mathrm{d}t}H_N(F_t)\big|_{t=0}$ be the rate at which $H_N$ decreases at time zero along the master equation of the walk, where $F_t$ is the solution started at $F_0=F$. For comparison, Villani's argument gives $D_N(F)\geq2H_N(F)/(N-1)$ for every $F$, and Gao, Wang and Xia state in a 2026 preprint that $2/(N-1)$ is the best constant over all $F$. For a probability density $f$ on $\mathbb{R}$ let $Z_N(f)=\int\prod_{i\leq N}f(v_i)\,\sigma_N(\mathrm{d}v)$ and $F^f_N(v)=Z_N(f)^{-1}\prod_{i\leq N}f(v_i)$. Fix $M>3$ and let $\mathcal{G}_M$ be the set of bounded probability densities $f$ on $\mathbb{R}$ that are normal scale mixtures, $f(v)=\int(2\pi s)^{-1/2}e^{-v^2/(2s)}\,G(\mathrm{d}s)$ with a mixing law $G$ on $[0,\infty)$ that is a generalized Gamma convolution (a law on $[0,\infty)$ with Laplace transform $\exp(-cs-\int_{(0,\infty)}\log(1+s/y)\,U(\mathrm{d}y))$ for some $c\geq0$ and some measure $U$ on $(0,\infty)$ with $\int\log(1+1/y)\,U(\mathrm{d}y)<\infty$, the Thorin measure), and that satisfy $\int v^2f(v)\,\mathrm{d}v=1$ and $\int v^4f(v)\,\mathrm{d}v\leq M$. The question is whether there is $\lambda>0$, depending only on $M$, such that $D_N(F^f_N)\geq\lambda H_N(F^f_N)$ for every $N\geq2$ and every $f\in\mathcal{G}_M$.

Source: [`source/chapters/ch16_open.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ch16_open.tex), label `prob:kinetic`.

<a id="open_problem_ns_posterior_fixed_sensors"></a>

#### Open problem: posterior contraction and Bernstein von Mises theorems for the initial vorticity of two dimensional Navier Stokes from fixed sensors

Open Problem 10, page 447 of Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1. New in this book.

Status: open.

Statement. Open problem. Konen and Nickl prove a functional Bernstein von Mises theorem for the posterior of the trajectory of the two dimensional Navier Stokes equations on the torus, with root $N$ consistent prediction of future states in the supremum norm, for a Gaussian prior on the initial condition and $N$ noisy observations at uniformly random points of space and time. The authors know of no corresponding result for sensors at fixed locations or for other priors. The problem is to determine the posterior contraction rate for the initial vorticity from noisy point observations at a fixed array of sensors and times, in terms of the number of sensors, the number of times and the noise level, and to identify the functionals of the initial vorticity that admit a Bernstein von Mises theorem. A companion question is whether the posterior of the initial vorticity can be computed in time polynomial in the data size and the dimension.

Source: [`source/chapters/ch16_open.tex`](https://github.com/VadimSokolov/hilbert6/blob/v1.0.0/source/chapters/ch16_open.tex), label `prob:inference`.

## License

Text, figures and PDF: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/). Code: [MIT](https://opensource.org/license/mit).

This page is generated from the book's repository at [v1.0.0](https://github.com/VadimSokolov/hilbert6/tree/v1.0.0).

<!-- Generated by bookrepo.py from book.yaml and results.yaml. Edit those files, not this one. -->
