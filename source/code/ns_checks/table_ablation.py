"""Ablation of the last row of the lower panel of the Navier Stokes table.

Same computation as anc/ns/correct_centre.py (same seeds and the same order of random
draws, so its recorded numbers are reproduced), plus:
  * the generator of the last row WITHOUT the cubic shift of the center
    (residuals centered and rescaled by the predicted inflation only, which is where
    Algorithm loc stops), scored on exactly the same draws;
  * the shift itself in posterior standard deviations;
  * the resampling noise of the generator's own 8000 draws: the scores of the rescaled
    generator with and without the shift, and of the centered generator, over twenty
    further resampling seeds (the residual pool and everything else held fixed).
Reads cache.npz (full.py) and hetero_cache.npz (hetero.py). Writes table_ablation.json.
"""
import numpy as np, json, time
exec(open('relin.py').read().split("r=np.random.default_rng(555)")[0])
h = np.load('hetero_cache.npz'); TH = h['TH']; S = h['S']; s_obs = h['s_obs']
psd = post.std(0); pm = post.mean(0)
def logpost(th): return -0.5*np.sum((Y-G(th))**2)/SIGMA**2-0.5*np.sum((th/prior_sd)**2)
def grad(th, e=1e-4):
    g = np.empty(D)
    for a in range(D):
        tp = th.copy(); tm = th.copy(); tp[a] += e; tm[a] -= e; g[a] = (logpost(tp)-logpost(tm))/(2*e)
    return g
def hess(th, e=2e-3):
    Hm = np.empty((D, D))
    for a in range(D):
        tp = th.copy(); tm = th.copy(); tp[a] += e; tm[a] -= e; Hm[a] = (grad(tp)-grad(tm))/(2*e)
    return 0.5*(Hm+Hm.T)
t0 = time.time()
Hs = -hess(th_map); Hi = np.linalg.inv(Hs)
rel = float(np.linalg.norm(Hs-np.linalg.inv(Cov))/np.linalg.norm(Hs))
def f(th): return np.trace(Hi@hess(th))
g = np.empty(D); e = 3e-3
for a in range(D):
    tp = th_map.copy(); tm = th_map.copy(); tp[a] += e; tm[a] -= e; g[a] = (f(tp)-f(tm))/(2*e)
corr = 0.5*Hi@g
print("third derivative computation %.0fs" % (time.time()-t0), flush=True)
r = np.random.default_rng(5); M = len(TH)
def w1(a, b):
    q = np.linspace(0.005, 0.995, 199); return np.mean(np.abs(np.quantile(a, q)-np.quantile(b, q)))
def score(s): return float(np.mean([w1(s[:, j], post[:, j])/psd[j] for j in range(D)]))
Lc = np.linalg.cholesky(Hi); idx = r.integers(0, M, 8000)
lap = th_map+(Lc@r.normal(size=(D, 8000))).T; lapc = lap+corr
R = TH-S; mu = R.mean(0); L = np.linalg.cholesky(np.cov(R.T)); W = np.linalg.solve(L, (R-mu).T).T
P = Cov@np.diag(1/prior_sd**2); ev, V = np.linalg.eig(P); ev = ev.real; V = V.real
infl = np.sqrt((1-ev)+25*ev**2); Dfl = V@np.diag(1/infl)@np.linalg.inv(V)
gbc = s_obs+(L@W[idx].T).T; gbc_c = s_obs+corr+(Dfl@(L@W[idx].T)).T
out = {'laplace': score(lap), 'laplace_corrected': score(lapc), 'gbc_centred': score(gbc),
       'gbc_centred_corrected_deflated': score(gbc_c), 'gbc_corrected_only': score(gbc+corr),
       'offset_MAP': float(np.mean(np.abs(th_map-pm)/psd)),
       'offset_corrected': float(np.mean(np.abs(th_map+corr-pm)/psd))}
out['gbc_centred_deflated_NO_shift'] = score(s_obs+(Dfl@(L@W[idx].T)).T)
out['exact_vs_gauss_newton_hessian_rel_diff'] = rel
out['summary_minus_MAP_maxabs'] = float(np.max(np.abs(s_obs-th_map)))
out['shift_over_psd'] = (corr/psd).tolist()
out['max_abs_shift_over_psd'] = float(np.max(np.abs(corr/psd)))
out['eigenvalues_of_P'] = np.sort(ev).tolist()
out['inflation_predicted'] = np.sort(infl).tolist()
# resampling noise of the generator's own 8000 draws
rows = {'deflated_no_shift': [], 'deflated_with_shift': [], 'centred': [], 'paired_shift_effect': []}
for seed in range(1000, 1020):
    rr = np.random.default_rng(seed); ii = rr.integers(0, M, 8000)
    base = (L@W[ii].T).T
    a = score(s_obs+(Dfl@base.T).T); b = score(s_obs+corr+(Dfl@base.T).T)
    rows['deflated_no_shift'].append(a); rows['deflated_with_shift'].append(b)
    rows['centred'].append(score(s_obs+base)); rows['paired_shift_effect'].append(b-a)
for k, v in rows.items():
    out['resample_'+k+'_mean'] = float(np.mean(v)); out['resample_'+k+'_sd'] = float(np.std(v, ddof=1))
    out['resample_'+k+'_min'] = float(np.min(v)); out['resample_'+k+'_max'] = float(np.max(v))
for k, v in out.items():
    print("%-44s" % k, np.round(v, 5) if isinstance(v, list) else "%.5f" % v)
json.dump(out, open('table_ablation.json', 'w'), indent=1)
