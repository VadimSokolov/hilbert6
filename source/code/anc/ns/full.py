import numpy as np, time, json
from ns_solver import NS2D, MODES, theta_to_w0h
D=len(MODES); lam=np.array([4*np.pi**2*(kx**2+ky**2) for kx,ky in MODES],float)
NU,T,NSTEPS,N,SIGMA,SCALE=0.005,1.0,80,80,0.45,1.5
ns=NS2D(n=24,nu=NU,T=T,nsteps=NSTEPS); prior_sd=SCALE*(lam/lam[0])**(-1.0)
def fields(th):
    s,_=ns.solve(theta_to_w0h(th,ns)); U=np.empty((len(s),ns.n,ns.n)); V=np.empty_like(U)
    for i,wh in enumerate(s): U[i],V[i]=ns.velocity(wh)
    return U,V
r=np.random.default_rng(100)
th0=r.normal(size=D)*prior_sd
it=r.integers(0,NSTEPS+1,N); ix=r.integers(0,ns.n,N); iy=r.integers(0,ns.n,N)
def G(th):
    U,V=fields(th); return np.concatenate([U[it,ix,iy],V[it,ix,iy]])
Y=G(th0)+SIGMA*r.normal(size=2*N)
def jac(th,eps=1e-4):
    b=G(th); J=np.empty((len(b),D))
    for j in range(D):
        tp=th.copy(); tp[j]+=eps; J[:,j]=(G(tp)-b)/eps
    return b,J
th=np.zeros(D)
for _ in range(10):
    g,J=jac(th); H=J.T@J/SIGMA**2+np.diag(1/prior_sd**2)
    th=th+np.linalg.solve(H,J.T@(Y-g)/SIGMA**2-th/prior_sd**2)
th_map=th; g_map,J=jac(th_map); H=J.T@J/SIGMA**2+np.diag(1/prior_sd**2); Cov=np.linalg.inv(H)
t0=time.time()
def mcmc(nit,burn,seed):
    rr=np.random.default_rng(seed)
    ll=lambda t:-0.5*np.sum((Y-G(t))**2)/SIGMA**2-0.5*np.sum((t/prior_sd)**2)
    t=th_map.copy(); lp=ll(t); s=1.0; acc=0; out=[]; L=np.linalg.cholesky(Cov)
    for i in range(nit):
        p=t+s*(L@rr.normal(size=D)); lpp=ll(p)
        if np.log(rr.uniform())<lpp-lp: t,lp=p,lpp; acc+=1
        if i%200==199: s*=np.exp(acc/200-0.30); acc=0
        if i>=burn: out.append(t.copy())
    return np.array(out)
post=mcmc(6000,1500,55); print("mcmc %.0fs"%(time.time()-t0),flush=True)
M=1600
t0=time.time()
TH_g=r.normal(size=(M,D))*prior_sd                       # global (prior) training
L_loc=np.linalg.cholesky(Cov)
TH_l=th_map+3.0*(L_loc@r.normal(size=(D,M))).T           # localised training
GG_g=np.empty((M,2*N)); GG_l=np.empty((M,2*N))
for m in range(M): GG_g[m]=G(TH_g[m]); GG_l[m]=G(TH_l[m])
print("train %.0fs"%(time.time()-t0),flush=True)
np.savez('cache.npz',th0=th0,Y=Y,th_map=th_map,Cov=Cov,J=J,g_map=g_map,post=post,
         TH_g=TH_g,GG_g=GG_g,TH_l=TH_l,GG_l=GG_l,prior_sd=prior_sd,SIGMA=SIGMA,N=N)
print("saved")
