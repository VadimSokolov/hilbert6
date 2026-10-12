"""Is the residual floor due to a homoscedastic head?  Test a scale that depends on
the summary (conditional/heteroscedastic head)."""
import numpy as np, json, time
exec(open('relin.py').read().split("r=np.random.default_rng(555)")[0])
r=np.random.default_rng(31); Lc=np.linalg.cholesky(Cov); c=5.0; M=1100
TH=th_map+c*(Lc@r.normal(size=(D,M))).T
t0=time.time(); GG=np.array([G(TH[m]) for m in range(M)])
Ysim=GG+SIGMA*r.normal(size=(M,2*N))
S=np.array([S_k(Ysim[m],2) for m in range(M)]); s_obs=S_k(Y,2)
np.savez('hetero_cache.npz',TH=TH,S=S,s_obs=s_obs); print("built %.0fs"%(time.time()-t0),flush=True)
lap=score(th_map+(Lc@r.normal(size=(D,8000))).T); print("Laplace %.4f"%lap,flush=True)
X=np.hstack([np.ones((M,1)),S]); B=np.linalg.lstsq(X,TH,rcond=None)[0]
R=TH-X@B; ctr=np.r_[1,s_obs]@B
# (a) homoscedastic head
C=np.cov(R.T); L=np.linalg.cholesky(C+1e-10*np.eye(D)); W=np.linalg.solve(L,R.T).T
idx=r.integers(0,M,8000); print("homoscedastic  %.4f"%score(ctr+(L@W[idx].T).T),flush=True)
# (b) heteroscedastic: log-variance linear in the (whitened) summary
Z=np.linalg.solve(Lc,(S-th_map).T).T                     # summary in posterior units
A=np.hstack([np.ones((M,1)),Z,Z**2])
logv=np.log(np.maximum(R**2,1e-12))
Gm=np.linalg.lstsq(A,logv,rcond=None)[0]
sd_hat=np.exp(0.5*(A@Gm))                                 # M x D predicted sd
Rn=R/sd_hat                                               # standardised residuals
Cn=np.cov(Rn.T); Ln=np.linalg.cholesky(Cn+1e-10*np.eye(D)); Wn=np.linalg.solve(Ln,Rn.T).T
z_obs=np.linalg.solve(Lc,(s_obs-th_map)); a_obs=np.r_[1,z_obs,z_obs**2]
sd_obs=np.exp(0.5*(a_obs@Gm))
print("hetero (sd model R^2 per coord):",np.round(1-np.var(logv-A@Gm,axis=0)/np.var(logv,axis=0),3),flush=True)
print("heteroscedastic %.4f"%score(ctr+sd_obs*(Ln@Wn[idx].T).T),flush=True)
# (c) diagnostic: does Var(R) really vary across the ball?
q=np.linalg.norm(Z,axis=1); lo,hi=q<np.median(q), q>=np.median(q)
print("sd(R) inner half:",np.round(R[lo].std(0),3)); print("sd(R) outer half:",np.round(R[hi].std(0),3))
