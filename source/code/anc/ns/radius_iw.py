import numpy as np, json, time
from ns_solver import NS2D, MODES, theta_to_w0h
d=np.load('cache.npz')
post=d['post']; th_map=d['th_map']; Cov=d['Cov']; J=d['J']; g_map=d['g_map']
Y=d['Y']; SIGMA=float(d['SIGMA']); prior_sd=d['prior_sd']; D=len(th_map); N=int(d['N'])
ns=NS2D(n=24,nu=0.005,T=1.0,nsteps=80)
rr=np.random.default_rng(100); _=rr.normal(size=D)*prior_sd
it=rr.integers(0,81,N); ix=rr.integers(0,ns.n,N); iy=rr.integers(0,ns.n,N)
def G(th):
    s,_=ns.solve(theta_to_w0h(th,ns)); U=np.empty((len(s),ns.n,ns.n)); V=np.empty_like(U)
    for i,wh in enumerate(s): U[i],V[i]=ns.velocity(wh)
    return np.concatenate([U[it,ix,iy],V[it,ix,iy]])
Fi=np.linalg.inv(J.T@J/SIGMA**2+np.diag(1/prior_sd**2))
summ=lambda Yv: th_map+Fi@(J.T@(Yv-g_map)/SIGMA**2-th_map/prior_sd**2)
s_obs=summ(Y); Lc=np.linalg.cholesky(Cov)
def w1(a,b):
    q=np.linspace(0.005,0.995,199); return np.mean(np.abs(np.quantile(a,q)-np.quantile(b,q)))
def score(s): return float(np.mean([w1(s[:,j],post[:,j])/np.std(post[:,j]) for j in range(D)]))
r=np.random.default_rng(303); M=1200; out={}
for c in [1.0,2.0,3.0,5.0,8.0]:
    TH=th_map+c*(Lc@r.normal(size=(D,M))).T
    GG=np.array([G(TH[m]) for m in range(M)])
    S=np.array([summ(GG[m]+SIGMA*r.normal(size=2*N)) for m in range(M)])
    lp=-0.5*np.sum((TH/prior_sd)**2,axis=1)
    z=np.linalg.solve(c*Lc,(TH-th_map).T).T; lq=-0.5*np.sum(z**2,axis=1)
    w=np.exp((lp-lq)-(lp-lq).max()); w/=w.sum(); ess=1/np.sum(w**2)
    for name,wt in [('unw',np.full(M,1/M)),('iw',w)]:
        X=np.hstack([np.ones((M,1)),S]); Wd=np.diag(wt)
        B=np.linalg.solve(X.T@Wd@X+1e-9*np.eye(D+1),X.T@Wd@TH)
        R=TH-X@B; mu=(wt[:,None]*R).sum(0); Rc=R-mu
        C=(wt[:,None]*Rc).T@Rc/(1-np.sum(wt**2)); L=np.linalg.cholesky(C+1e-10*np.eye(D))
        Wn=np.linalg.solve(L,Rc.T).T
        idx=r.choice(M,8000,p=wt)
        out[f'c{c}_{name}']=score(np.r_[1,s_obs]@B+mu+(L@Wn[idx].T).T)
    print("c=%4.1f  ESS %5.0f  unweighted %.4f  IW %.4f"%(c,ess,out[f'c{c}_unw'],out[f'c{c}_iw']),flush=True)
    out[f'c{c}_ess']=float(ess)
json.dump(out,open('radius_iw.json','w'),indent=1)
