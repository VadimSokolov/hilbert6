"""Finding 5.8 (final form): the residual mean under a localised proposal is the prior
shrinkage of the proposal centre, E_q[theta - S] = P theta_bar, P = Sigma_N Sigma_0^{-1}.
Centring the residuals removes it. Uses hetero_cache.npz (TH, S, s_obs) and cache.npz."""
import numpy as np, json
d=np.load('cache.npz'); h=np.load('hetero_cache.npz')
post=d['post']; th_map=d['th_map']; Cov=d['Cov']; prior_sd=d['prior_sd']; D=len(th_map)
TH=h['TH']; S=h['S']; s_obs=h['s_obs']; psd=post.std(0); pm=post.mean(0); M=len(TH)
P=Cov@np.diag(1/prior_sd**2)
r=np.random.default_rng(3)
def w1(a,b):
    q=np.linspace(0.005,0.995,199); return np.mean(np.abs(np.quantile(a,q)-np.quantile(b,q)))
def score(s): return float(np.mean([w1(s[:,j],post[:,j])/psd[j] for j in range(D)]))
out={}
mu=(TH-S).mean(0); out['resid_mean_emp']=(mu/psd).tolist(); out['resid_mean_theory']=((P@th_map)/psd).tolist()
R=TH-S; L=np.linalg.cholesky(np.cov(R.T)); W=np.linalg.solve(L,(R-mu).T).T; idx=r.integers(0,M,8000)
out['id_uncentred']=score(s_obs+mu+(L@W[idx].T).T)
out['id_centred']=score(s_obs+(L@W[idx].T).T)
out['id_analytic']=score(s_obs+(mu-P@th_map)+(L@W[idx].T).T)
X=np.hstack([np.ones((M,1)),S]); B=np.linalg.lstsq(X,TH,rcond=None)[0]; Ra=TH-X@B
La=np.linalg.cholesky(np.cov(Ra.T)); Wa=np.linalg.solve(La,Ra.T).T
out['affine']=score(np.r_[1,s_obs]@B+(La@Wa[idx].T).T)
lap=th_map+(np.linalg.cholesky(Cov)@r.normal(size=(D,8000))).T
out['laplace']=score(lap); out['laplace_oracle_centre']=score(lap-th_map+pm)
out['id_oracle_centre']=score(pm+(L@W[idx].T).T)
out['MAP_minus_pm']=float(np.mean(np.abs(th_map-pm)/psd))
out['spread_ratio_gbc']=(np.sqrt(np.diag(np.cov(R.T)))/psd).tolist(); out['spread_ratio_laplace']=(np.sqrt(np.diag(Cov))/psd).tolist()
for k,v in out.items(): print("%-24s"%k, np.round(v,3) if isinstance(v,list) else "%.4f"%v)
json.dump(out,open('centring.json','w'),indent=1)
