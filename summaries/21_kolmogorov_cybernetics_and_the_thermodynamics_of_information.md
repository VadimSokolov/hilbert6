# Chapter 21. Kolmogorov, Cybernetics and the Thermodynamics of Information

<!-- cite:begin -->
From *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation* by Nick Polson and Vadim Sokolov (2026), chapter 21. Cite as Polson and Sokolov (2026), *On Hilbert's 6th Problem: Probability, Mechanics and Bayesian Computation*, edition 1, https://doi.org/10.5281/zenodo.23327515. Book page: https://vsokolov.org/books/hilbert6/. Source: https://github.com/VadimSokolov/hilbert6.
<!-- cite:end -->

The chapter asks what Hilbert's sixth problem means for inference regarded as a physical process, starting from Kolmogorov's view of machines that learn and Wiener's cybernetics. It presents Kolmogorov's superposition theorem (the Kolmogorov Arnold representation, Hilbert's thirteenth problem) without proof, algorithmic information (Kolmogorov complexity, the universal prior, minimum description length), and Maxwell's demon with the Szilard engine and Landauer's principle. It proves a Landauer bound in information theoretic form: for a memory with finitely many states of equal energy and a heat bath that start independent, the bath in its Gibbs state, and evolve under reversible dynamics, the expected energy gained by the bath is at least $k_BT\log2$ per bit of entropy lost by the memory. It proves Kelly's theorem on optimal growth and proportional betting, a recursive self learning bound from the data processing inequality (without a verifier the information about the target never exceeds its initial value, and a verifier channel of capacity $C$ bits per round adds at most $C$ per round), Jarzynski's equality, and a lower bound on the heat dissipated in resetting a memory that stores reconstructions at a given average distortion. Crooks' theorem and the Sagawa Ueda inequality are quoted without proof.

## From the literature

Kolmogorov's superposition theorem (Kolmogorov 1957) and Arnold's theorem on functions of three variables (Arnold 1957); Kolmogorov complexity (Kolmogorov 1965); minimum description length and stochastic complexity (Rissanen 1978, 1996); the Szilard engine (Szilard 1929); Landauer's principle (Landauer 1961) and its experimental confirmation (Bérut and coauthors 2012); reversible measurement (Bennett 1982); Kelly's theorem (Kelly 1956); Jarzynski's equality (Jarzynski 1997; for Markov dynamics, Jarzynski 1997 and Crooks 2000); Crooks' fluctuation theorem (Crooks 1999); annealed importance sampling (Neal 2001); the generalized second law with feedback (Sagawa and Ueda 2010); rate distortion theory and the data processing inequality, as treated by Cover and Thomas (2006); the algorithms of Blahut (1972) and Arimoto (1972).

## New results

<!-- results:begin -->
- [Information bound for recursive self learning](../RESULTS.md#recursive_self_learning_information_bound) (Proposition 21.4, page 433; proved): A model that is updated only from its own state and from fresh randomness independent of the target gains no information about the target, and with a verifier of capacity C bits per round it gains at most C bits per round. New in this book.
<!-- results:end -->

## Key terms

Kolmogorov Arnold representation theorem, Kolmogorov superposition theorem, Hilbert's thirteenth problem, Kolmogorov complexity, algorithmic information, universal prior, minimum description length, stochastic complexity, Maxwell's demon, Szilard engine, Landauer principle, Landauer bound, Kelly criterion, data processing inequality, recursive self learning, cybernetics, Jarzynski equality, Crooks theorem, Sagawa Ueda, rate distortion, Blahut Arimoto algorithm
