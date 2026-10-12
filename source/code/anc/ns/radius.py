"""Open Problem 5.1: optimal radius of the GBC training proposal."""
import numpy as np, json, time
from ns_solver import NS2D, MODES, theta_to_w0h
d=np.load('cache.npz')
post=d['post']; th_map=d['th_map']; Cov=d['Cov']; J=d['J']; g_map=d['g_map']
Y=d['Y']; SIGMA=float(d['SIGMA']); prior_sd=d['prior_sd']; D=len(th_map)
NU,T,NSTEPS,N=0.005,1.0,80,int(d['N'])
ns=NS2D(n=24,nu=NU,T=T,nsteps=NSTEPS)
r=np.random.default_rng(202)
# rebuild the same design as full.py (same seed sequence)
rr=np.random.default_rng(100); _=rr.normal(size=D)*prior_sd
it=rr.integers(0,NSTEPS+1,N); ix=rr.integers(0,ns.n,N); iy=rr.integers(0,ns.n,N)
def fields(th):
    s,_=ns.solve(theta_to_w0h(th,ns)); U=np.empty((len(s),ns.n,ns.n)); V=np.empty_like(U)
    for i,wh in enumerate(s): U[i],V[i]=ns.velocity(wh)
    return U,V
def G(th):
    U,V=fields(th); return np.concatenate([U[it,ix,iy],V[it,ix,iy]])
assert np.allclose(G(th_map), g_map, atol=1e-8), "design mismatch"
Fi=np.linalg.inv(J.T@J/SIGMA**2+np.diag(1/prior_sd**2))
summ=lambda Yv: th_map+Fi@(J.T@(Yv-g_map)/SIGMA**2-th_map/prior_sd**2)
s_obs=summ(Y)
def w1(a,b):
    q=np.linspace(0.005,0.995,199); return np.mean(np.abs(np.quantile(a,q)-np.quantile(b,q)))
def score(s): return float(np.mean([w1(s[:,j],post[:,j])/np.std(post[:,j]) for j in range(D)]))
Lc=np.linalg.cholesky(Cov); M=1200
out={}
for c in [0.5,1.0,2.0,3.0,5.0,8.0,14.0]:
    TH=th_map+c*(Lc@r.normal(size=(D,M))).T
    t0=time.time(); GG=np.array([G(TH[m]) for m in range(M)])
    S=np.array([summ(GG[m]+SIGMA*r.normal(size=2*N)) for m in range(M)])
    for lin in [False,True]:
        if lin:
            X=np.hstack([np.ones((M,1)),S]); B=np.linalg.lstsq(X,TH,rcond=None)[0]
            R=TH-X@B; ctr=np.r_[1,s_obs]@B
        else:
            R=TH-S; ctr=s_obs
        C=np.cov(R.T); L=np.linalg.cholesky(C+1e-10*np.eye(D)); W=np.linalg.solve(L,R.T).T
        idx=r.integers(0,M,8000)
        out[f'c{c}_{"lin" if lin else "id"}']=score(ctr+(L@W[idx].T).T)
    print("c=%4.1f  id %.4f  lin %.4f   (%.0fs)"%(c,out[f'c{c}_id'],out[f'c{c}_lin'],time.time()-t0),flush=True)
out['laplace']=score(th_map+(Lc@r.normal(size=(D,8000))).T)
print("laplace %.4f"%out['laplace'])
json.dump(out,open('radius.json','w'),indent=1)
