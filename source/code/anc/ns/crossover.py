"""Stronger nonlinearity: does GBC overtake the Laplace/BvM approximation?

Two regimes, selected by the first argument.

  amplitude  raise the signal at the baseline noise (SCALE 1.5 -> 2.0, SIGMA 0.45),
             so the advection-to-dissipation ratio AT/nu goes up but the posterior
             stays narrow.                                   -> crossover2.json
  posterior  widen the posterior (SIGMA 0.45 -> 1.30) with the signal raised too,
             so the map is sampled over a region it is not affine across.
                                                             -> crossover3.json

Both share the seed, so the two JSONs differ only through (SIGMA, SCALE).
"""
import sys
REGIME = sys.argv[1] if len(sys.argv) > 1 else 'posterior'
SIGMA, SCALE, OUT = {'amplitude': (0.45, 2.0, 'crossover2.json'),
                     'posterior': (1.30, 3.0, 'crossover3.json')}[REGIME]
import numpy as np, json, time
from ns_solver import NS2D, MODES, theta_to_w0h
from scipy.stats import skew, kurtosis
D=len(MODES); lam=np.array([4*np.pi**2*(kx**2+ky**2) for kx,ky in MODES],float)
NU,T,NSTEPS,N=0.005,1.0,100,25
ns=NS2D(n=24,nu=NU,T=T,nsteps=NSTEPS); prior_sd=SCALE*(lam/lam[0])**(-1.0)
r=np.random.default_rng(404)
th0=r.normal(size=D)*prior_sd
it=r.integers(0,NSTEPS+1,N); ix=r.integers(0,ns.n,N); iy=r.integers(0,ns.n,N)
def G(th):
    s,_=ns.solve(theta_to_w0h(th,ns)); U=np.empty((len(s),ns.n,ns.n)); V=np.empty_like(U)
    for i,wh in enumerate(s): U[i],V[i]=ns.velocity(wh)
    return np.concatenate([U[it,ix,iy],V[it,ix,iy]])
G0=G(th0); Y=G0+SIGMA*r.normal(size=2*N)
print("signal sd %.2f noise %.2f  A/nu ~ %.0f"%(np.std(G0),SIGMA,np.abs(th0).max()/NU),flush=True)
def jac(th,eps=1e-4):
    b=G(th); Jm=np.empty((len(b),D))
    for j in range(D):
        tp=th.copy(); tp[j]+=eps; Jm[:,j]=(G(tp)-b)/eps
    return b,Jm
th=np.zeros(D)
for _ in range(12):
    g,Jm=jac(th); H=Jm.T@Jm/SIGMA**2+np.diag(1/prior_sd**2)
    th=th+np.linalg.solve(H,Jm.T@(Y-g)/SIGMA**2-th/prior_sd**2)
th_map=th; g_map,Jm=jac(th_map); H=Jm.T@Jm/SIGMA**2+np.diag(1/prior_sd**2); Cov=np.linalg.inv(H)
Lc=np.linalg.cholesky(Cov)
t0=time.time()
def mcmc(nit,burn,seed):
    q=np.random.default_rng(seed)
    ll=lambda t:-0.5*np.sum((Y-G(t))**2)/SIGMA**2-0.5*np.sum((t/prior_sd)**2)
    t=th_map.copy(); lp=ll(t); s=1.0; acc=0; out=[]
    for i in range(nit):
        p=t+s*(Lc@q.normal(size=D)); lpp=ll(p)
        if np.log(q.uniform())<lpp-lp: t,lp=p,lpp; acc+=1
        if i%200==199: s*=np.exp(acc/200-0.30); acc=0
        if i>=burn: out.append(t.copy())
    return np.array(out)
post=mcmc(4000,1000,77); print("mcmc %.0fs skew %.3f exkurt %.3f"%(
    time.time()-t0,np.abs(skew(post,axis=0)).mean(),np.abs(kurtosis(post,axis=0)).mean()),flush=True)
def w1(a,b):
    q=np.linspace(0.005,0.995,199); return np.mean(np.abs(np.quantile(a,q)-np.quantile(b,q)))
def score(s): return float(np.mean([w1(s[:,j],post[:,j])/np.std(post[:,j]) for j in range(D)]))
lap=th_map+(Lc@r.normal(size=(D,8000))).T
res={'laplace':score(lap),'skew':float(np.abs(skew(post,axis=0)).mean()),
     'exkurt':float(np.abs(kurtosis(post,axis=0)).mean())}
print("Laplace %.4f"%res['laplace'],flush=True)
Fi=np.linalg.inv(Jm.T@Jm/SIGMA**2+np.diag(1/prior_sd**2))
summ=lambda Yv: th_map+Fi@(Jm.T@(Yv-g_map)/SIGMA**2-th_map/prior_sd**2)
s_obs=summ(Y); M=1200
for c in [2.0]:
    TH=th_map+c*(Lc@r.normal(size=(D,M))).T
    GG=np.array([G(TH[m]) for m in range(M)])
    S=np.array([summ(GG[m]+SIGMA*r.normal(size=2*N)) for m in range(M)])
    for lin in [False,True]:
        if lin:
            X=np.hstack([np.ones((M,1)),S]); B=np.linalg.lstsq(X,TH,rcond=None)[0]
            R=TH-X@B; ctr=np.r_[1,s_obs]@B
        else:
            R=TH-S; ctr=s_obs
        C=np.cov(R.T); L=np.linalg.cholesky(C+1e-10*np.eye(D)); W=np.linalg.solve(L,R.T).T
        idx=r.integers(0,M,8000)
        res[f'gbc_c{c}_{"lin" if lin else "id"}']=score(ctr+(L@W[idx].T).T)
    print("c=%.1f  id %.4f  lin %.4f"%(c,res[f'gbc_c{c}_id'],res[f'gbc_c{c}_lin']),flush=True)
import os
os.makedirs('../results/ns', exist_ok=True)
json.dump(res, open(os.path.join('../results/ns', OUT), 'w'), indent=1)
print('wrote', OUT)
