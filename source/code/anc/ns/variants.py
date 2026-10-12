import numpy as np, json
d=np.load('cache.npz'); r=np.random.default_rng(4)
post=d['post']; th_map=d['th_map']; Cov=d['Cov']; J=d['J']; g_map=d['g_map']
Y=d['Y']; SIGMA=float(d['SIGMA']); prior_sd=d['prior_sd']; th0=d['th0']; D=len(th_map)
Fi=np.linalg.inv(J.T@J/SIGMA**2+np.diag(1/prior_sd**2))
def summ(Yv): return th_map+Fi@(J.T@(Yv-g_map)/SIGMA**2-th_map/prior_sd**2)
s_obs=summ(Y)
def w1(a,b):
    q=np.linspace(0.005,0.995,199); return np.mean(np.abs(np.quantile(a,q)-np.quantile(b,q)))
def score(smp): return float(np.mean([w1(smp[:,j],post[:,j])/np.std(post[:,j]) for j in range(D)]))
lap=th_map+(np.linalg.cholesky(Cov)@r.normal(size=(D,8000))).T
print("Laplace/BvM      : %.4f"%score(lap))
def build(TH,GG,M,mode,K=None):
    S=np.array([summ(GG[m]+SIGMA*r.normal(size=len(Y))) for m in range(M)])
    if mode=='identity':
        R=TH[:M]-S
        C=np.cov(R.T); L=np.linalg.cholesky(C+1e-10*np.eye(D)); W=np.linalg.solve(L,R.T).T
        idx=r.integers(0,M,8000); return s_obs+(L@W[idx].T).T
    if mode=='linear':                    # learn affine map S->theta (regression adjustment)
        X=np.hstack([np.ones((M,1)),S]); B=np.linalg.lstsq(X,TH[:M],rcond=None)[0]
        R=TH[:M]-X@B
        C=np.cov(R.T); L=np.linalg.cholesky(C+1e-10*np.eye(D)); W=np.linalg.solve(L,R.T).T
        idx=r.integers(0,M,8000); return (np.r_[1,s_obs]@B)+(L@W[idx].T).T
    if mode=='local':                     # localise then affine
        Ci=np.linalg.inv(Cov); dist=np.einsum('ij,jk,ik->i',S-s_obs,Ci,S-s_obs)
        sel=np.argsort(dist)[:K]
        Ss,Ts=S[sel],TH[:M][sel]
        X=np.hstack([np.ones((K,1)),Ss]); B=np.linalg.lstsq(X,Ts,rcond=None)[0]
        R=Ts-X@B
        C=np.cov(R.T); L=np.linalg.cholesky(C+1e-10*np.eye(D)); W=np.linalg.solve(L,R.T).T
        idx=r.integers(0,K,8000); return (np.r_[1,s_obs]@B)+(L@W[idx].T).T
res={'laplace':score(lap)}
for M in [400,800,1600]:
    res[f'global_identity_M{M}']=score(build(d['TH_g'],d['GG_g'],M,'identity'))
    res[f'global_linear_M{M}']  =score(build(d['TH_g'],d['GG_g'],M,'linear'))
    res[f'local_train_identity_M{M}']=score(build(d['TH_l'],d['GG_l'],M,'identity'))
    res[f'local_train_linear_M{M}']  =score(build(d['TH_l'],d['GG_l'],M,'linear'))
for K in [200,400,800]:
    res[f'global_localised_K{K}']=score(build(d['TH_g'],d['GG_g'],1600,'local',K))
for k,v in res.items(): print("%-28s %.4f"%(k,v))
json.dump(res,open('variants.json','w'),indent=1)
