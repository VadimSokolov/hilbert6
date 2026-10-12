"""Skewness of the reference chains against the skewness an exactly Gaussian chain of the
same length and autocorrelation shows by sampling error alone.
(1) main run: mean absolute marginal skewness of the chain cached by full.py, its
    integrated autocorrelation time (estimator of mcmc_error.py), and the Gaussian floor;
(2) the regimes: Gaussian floor for chains of 3000 draws at the autocorrelation times
    read from regimes_amplitude.json and regimes_posterior.json if present.
Writes skew_check.json."""
import json, os
import numpy as np
from scipy.stats import skew
d = np.load('cache.npz'); post = d['post']; n, D = post.shape
def acf(x):
    x = x - x.mean(); m = len(x); f = np.fft.rfft(x, 2*m); a = np.fft.irfft(f*np.conj(f))[:m].real; return a/a[0]
def iact_cut(r, thresh=0.05):
    k = int(np.argmax(r[1:] < thresh)) + 1; return 1.0 + 2.0*r[1:k].sum()
iact = float(np.mean([iact_cut(acf(post[:, j])) for j in range(D)]))
out = {'main_n': int(n), 'main_mean_abs_skew': float(np.abs(skew(post, axis=0)).mean()), 'main_iact': iact}
rng = np.random.default_rng(3)
def chain(m, tau):
    phi = (tau-1)/(tau+1); e = rng.normal(size=m+500)*np.sqrt(1-phi**2); x = np.zeros(m+500)
    for i in range(1, m+500): x[i] = phi*x[i-1] + e[i]
    return x[500:]
def floor(m, tau, reps=300):
    v = np.array([np.mean([abs(skew(chain(m, tau))) for j in range(D)]) for rep in range(reps)])
    return {'n': m, 'iact': tau, 'mean': float(v.mean()), 'sd': float(v.std()),
            'p05': float(np.percentile(v, 5)), 'p95': float(np.percentile(v, 95))}
out['floor_main'] = floor(n, iact)
for reg in ['amplitude', 'posterior']:
    f = 'regimes_%s.json' % reg
    tau = json.load(open(f))['iact_mean'] if os.path.exists(f) else 20.0
    out['floor_' + reg] = floor(3000, tau)
for k, v in out.items(): print(k, v)
json.dump(out, open('skew_check.json', 'w'), indent=1)
