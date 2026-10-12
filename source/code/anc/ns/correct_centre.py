"""Open problem: correct the centre by the third-derivative (Laplace) term
   E[theta] - MAP ~ (1/2) H^{-1} g,  g_a = d/dtheta_a tr(H^{-1} grad^2 log pi)(theta*).
Apply to both Laplace and GBC; compare to the MCMC posterior mean."""
import numpy as np, json, time
exec(open('relin.py').read().split("r=np.random.default_rng(555)")[0])
h=np.load('hetero_cache.npz'); TH=h['TH']; S=h['S']; s_obs=h['s_obs']
psd=post.std(0); pm=post.mean(0)
def logpost(th): return -0.5*np.sum((Y-G(th))**2)/SIGMA**2-0.5*np.sum((th/prior_sd)**2)
def grad(th,e=1e-4):
    g=np.empty(D)
    for a in range(D):
        tp=th.copy(); tm=th.copy(); tp[a]+=e; tm[a]-=e; g[a]=(logpost(tp)-logpost(tm))/(2*e)
    return g
def hess(th,e=2e-3):
    Hm=np.empty((D,D))
    for a in range(D):
        tp=th.copy(); tm=th.copy(); tp[a]+=e; tm[a]-=e; Hm[a]=(grad(tp)-grad(tm))/(2*e)
    return 0.5*(Hm+Hm.T)
t0=time.time()
Hs=-hess(th_map); Hi=np.linalg.inv(Hs)
print("exact Hessian vs Gauss-Newton: rel diff %.3f"%(np.linalg.norm(Hs-np.linalg.inv(Cov))/np.linalg.norm(Hs)),flush=True)
def f(th): return np.trace(Hi@hess(th))
g=np.empty(D); e=3e-3
for a in range(D):
    tp=th_map.copy(); tm=th_map.copy(); tp[a]+=e; tm[a]-=e; g[a]=(f(tp)-f(tm))/(2*e)
corr=0.5*Hi@g
print("third-derivative computation %.0fs"%(time.time()-t0))
print("MAP - pm        /psd:",np.round((th_map-pm)/psd,3))
print("correction      /psd:",np.round(corr/psd,3))
print("MAP+corr - pm   /psd:",np.round((th_map+corr-pm)/psd,3))
print("mean |offset|: MAP %.3f  corrected %.3f"%(np.mean(np.abs(th_map-pm)/psd),np.mean(np.abs(th_map+corr-pm)/psd)))
r=np.random.default_rng(5); M=len(TH)
def w1(a,b):
    q=np.linspace(0.005,0.995,199); return np.mean(np.abs(np.quantile(a,q)-np.quantile(b,q)))
def score(s): return float(np.mean([w1(s[:,j],post[:,j])/psd[j] for j in range(D)]))
Lc=np.linalg.cholesky(Hi); idx=r.integers(0,M,8000)
lap=th_map+(Lc@r.normal(size=(D,8000))).T; lapc=lap+corr
R=TH-S; mu=R.mean(0); L=np.linalg.cholesky(np.cov(R.T)); W=np.linalg.solve(L,(R-mu).T).T
# rescale residual spread by the predicted inflation sqrt(s_j + c^2 p_j^2) in the P-eigenbasis (c=5)
P=Cov@np.diag(1/prior_sd**2); ev,V=np.linalg.eig(P); ev=ev.real; V=V.real
infl=np.sqrt((1-ev)+25*ev**2); Dfl=V@np.diag(1/infl)@np.linalg.inv(V)
gbc=s_obs+(L@W[idx].T).T; gbc_c=s_obs+corr+(Dfl@(L@W[idx].T)).T
out={'laplace':score(lap),'laplace_corrected':score(lapc),'gbc_centred':score(gbc),
     'gbc_centred_corrected_deflated':score(gbc_c),'gbc_corrected_only':score(gbc+corr),
     'offset_MAP':float(np.mean(np.abs(th_map-pm)/psd)),'offset_corrected':float(np.mean(np.abs(th_map+corr-pm)/psd))}
for k,v in out.items(): print("%-32s %.4f"%(k,v))
json.dump(out,open('correct_centre.json','w'),indent=1)
