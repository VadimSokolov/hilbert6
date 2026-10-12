"""Monte Carlo error of the Metropolis reference, per coordinate.

Table 5's comparison is read in units of the reference's own sampling error, so that
error is measured rather than assumed.  Reads the chain cached by full.py and reports
ess = n/iact and se_over_psd = 1/sqrt(ess): the standard error of the reference's
posterior mean, in units of its posterior standard deviation.  -> results/ns/mcmc_error.json

Two estimators of the integrated autocorrelation time are computed.  The reported one
truncates the autocorrelation sum at the first lag with rho < 0.05, which discards part
of the tail and so is optimistic about the chain.  Geyer's initial positive sequence is
computed alongside as a check; it gives a mean se/psd of about 0.066 against 0.063 here.
The paper uses the smaller value, which is the conservative choice for the claim it
supports: the smaller the reference's own error, the harder it is to call GBC and the
Laplace approximation indistinguishable at that resolution.  Both give the same verdict.
"""
import json, os
import numpy as np

d = np.load('cache.npz')
post = d['post']                      # (n, D) chain after burn-in
n, D = post.shape


def acf(x):
    x = x - x.mean()
    m = len(x)
    f = np.fft.rfft(x, 2 * m)
    a = np.fft.irfft(f * np.conj(f))[:m].real
    return a / a[0]


def iact_cut(r, thresh=0.05):
    """Sum the autocorrelation up to the first lag below thresh."""
    k = int(np.argmax(r[1:] < thresh)) + 1
    return 1.0 + 2.0 * r[1:k].sum()


def iact_geyer(r):
    """Geyer's initial positive sequence: sum consecutive pairs while positive."""
    s, k = 0.0, 0
    while 2 * k + 1 < len(r):
        pair = r[2 * k] + r[2 * k + 1]
        if pair <= 0:
            break
        s += pair
        k += 1
    return max(2.0 * s - 1.0, 1.0)


rs = [acf(post[:, j]) for j in range(D)]
iact = [float(iact_cut(r)) for r in rs]
geyer = [float(iact_geyer(r)) for r in rs]
ess = [n / t for t in iact]
se = [1.0 / np.sqrt(e) for e in ess]
se_geyer = [float(np.sqrt(t / n)) for t in geyer]

os.makedirs('../results/ns', exist_ok=True)
json.dump({'iact': iact, 'ess': ess, 'se_over_psd': se,
           'iact_geyer': geyer, 'se_over_psd_geyer': se_geyer},
          open('../results/ns/mcmc_error.json', 'w'), indent=1)
print('n = %d   mean se/psd = %.4f   (Geyer cross-check %.4f)'
      % (n, np.mean(se), np.mean(se_geyer)))
