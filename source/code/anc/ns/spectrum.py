"""Information spectrum J^T J as observations are restricted to [T0,T]:
the Nickl-Titi barrier in the finite-dimensional Galerkin model."""
import numpy as np, json
from ns_solver import NS2D, MODES, theta_to_w0h
D=len(MODES); lam=np.array([4*np.pi**2*(kx**2+ky**2) for kx,ky in MODES],float)
NU,T,NSTEPS,N,SIGMA,SCALE=0.005,1.0,80,80,0.45,1.5
ns=NS2D(n=24,nu=NU,T=T,nsteps=NSTEPS); prior_sd=SCALE*(lam/lam[0])**(-1.0)
d=np.load('cache.npz'); th_map=d['th_map']
def fields(th):
    s,_=ns.solve(theta_to_w0h(th,ns)); U=np.empty((len(s),ns.n,ns.n)); V=np.empty_like(U)
    for i,wh in enumerate(s): U[i],V[i]=ns.velocity(wh)
    return U,V
r=np.random.default_rng(21)
res={}
for T0f in [0.0,0.1,0.25,0.5]:
    t_lo=int(T0f*NSTEPS)
    it=r.integers(t_lo,NSTEPS+1,N); ix=r.integers(0,ns.n,N); iy=r.integers(0,ns.n,N)
    def G(th):
        U,V=fields(th); return np.concatenate([U[it,ix,iy],V[it,ix,iy]])
    b=G(th_map); J=np.empty((len(b),D))
    for j in range(D):
        tp=th_map.copy(); tp[j]+=1e-4; J[:,j]=(G(tp)-b)/1e-4
    F=J.T@J/SIGMA**2
    ev=np.linalg.eigvalsh(F)
    post_sd=np.sqrt(np.diag(np.linalg.inv(F+np.diag(1/prior_sd**2))))
    res[T0f]={'eig':ev.tolist(),'cond':float(ev[-1]/ev[0]),
              'post_sd':post_sd.tolist(),'prior_sd':prior_sd.tolist(),
              'shrink':float(np.mean(post_sd/prior_sd))}
    print("T0=%.2f  lam_min %.3g  lam_max %.3g  cond %.3g  mean post_sd/prior_sd %.3f"%(
        T0f,ev[0],ev[-1],ev[-1]/ev[0],res[T0f]['shrink']),flush=True)
# functional: energy at final time -- how well determined?
print()
for T0f in [0.0,0.5]:
    F=np.array(res[T0f]['eig'])
    print("T0=%.2f posterior sd per mode:"%T0f, np.round(res[T0f]['post_sd'],4))
json.dump(res,open('spectrum.json','w'),indent=1)
