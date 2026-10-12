"""Open problem: does a re-linearised (multi-step Gauss-Newton) summary remove the
c^4 term and beat the one-step summary?  S_k(Y) = k Gauss-Newton steps from a FIXED
start (the observed-data MAP), using only Y -- so it is a genuine statistic."""
import numpy as np, json, time
from ns_solver import NS2D, MODES, theta_to_w0h
d=np.load('cache.npz')
post=d['post']; th_map=d['th_map']; Cov=d['Cov']; J0=d['J']; g_map=d['g_map']
Y=d['Y']; SIGMA=float(d['SIGMA']); prior_sd=d['prior_sd']; D=len(th_map); N=int(d['N'])
ns=NS2D(n=24,nu=0.005,T=1.0,nsteps=80)
rr=np.random.default_rng(100); _=rr.normal(size=D)*prior_sd
it=rr.integers(0,81,N); ix=rr.integers(0,ns.n,N); iy=rr.integers(0,ns.n,N)
def G(th):
    s,_=ns.solve(theta_to_w0h(th,ns)); U=np.empty((len(s),ns.n,ns.n)); V=np.empty_like(U)
    for i,wh in enumerate(s): U[i],V[i]=ns.velocity(wh)
    return np.concatenate([U[it,ix,iy],V[it,ix,iy]])
P0inv=np.diag(1/prior_sd**2)
def jac(th,eps=1e-4):
    b=G(th); Jm=np.empty((len(b),D))
    for j in range(D):
        tp=th.copy(); tp[j]+=eps; Jm[:,j]=(G(tp)-b)/eps
    return b,Jm
def S_k(Yv,k):
    """k Gauss-Newton steps from the fixed start th_map, using only Yv."""
    th=th_map.copy(); g,Jm=g_map,J0            # step 1 reuses the cached J at th_map
    for i in range(k):
        H=Jm.T@Jm/SIGMA**2+P0inv
        th=th+np.linalg.solve(H,Jm.T@(Yv-g)/SIGMA**2-P0inv@th)
        if i<k-1: g,Jm=jac(th)
    return th
def w1(a,b):
    q=np.linspace(0.005,0.995,199); return np.mean(np.abs(np.quantile(a,q)-np.quantile(b,q)))
def score(s): return float(np.mean([w1(s[:,j],post[:,j])/np.std(post[:,j]) for j in range(D)]))
r=np.random.default_rng(555); Lc=np.linalg.cholesky(Cov); M=500
out={'laplace':score(th_map+(Lc@r.normal(size=(D,8000))).T)}
print("Laplace %.4f"%out['laplace'],flush=True)
for c in [2.0,6.0]:
    TH=th_map+c*(Lc@r.normal(size=(D,M))).T
    t0=time.time(); GG=np.array([G(TH[m]) for m in range(M)])
    Ysim=GG+SIGMA*r.normal(size=(M,2*N))
    for k in [1,2]:
        S=np.array([S_k(Ysim[m],k) for m in range(M)])
        s_obs=S_k(Y,k)
        for lin in [False,True]:
            if lin:
                X=np.hstack([np.ones((M,1)),S]); B=np.linalg.lstsq(X,TH,rcond=None)[0]
                R=TH-X@B; ctr=np.r_[1,s_obs]@B
            else:
                R=TH-S; ctr=s_obs
            C=np.cov(R.T); L=np.linalg.cholesky(C+1e-10*np.eye(D)); W=np.linalg.solve(L,R.T).T
            idx=r.integers(0,M,8000)
            out[f'c{c}_k{k}_{"lin" if lin else "id"}']=score(ctr+(L@W[idx].T).T)
        print("  c=%.1f k=%d: id %.4f  lin %.4f  (%.0fs)"%(c,k,out[f'c{c}_k{k}_id'],out[f'c{c}_k{k}_lin'],time.time()-t0),flush=True)
json.dump(out,open('relin.json','w'),indent=1)
