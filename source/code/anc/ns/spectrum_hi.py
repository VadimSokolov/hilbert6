"""Table 5 (advective transfer): per-mode Fisher information of the NONLINEAR 2D
Navier-Stokes forward map as the observation window is restricted to [T0,T],
with an extended mode set reaching |k|^2 = 41.  -> spectrum_hi.json
Compare with the Stokes prediction exp(-2 nu lambda_k T0)."""
import numpy as np, json
import ns_solver
from ns_solver import NS2D, theta_to_w0h

# extended mode set (overrides the 6-mode default used elsewhere)
M2=[(1,0),(0,1),(1,1),(2,0),(0,2),(2,1),(2,2),(3,0),(0,3),(3,2),(4,0),(4,3),(5,0),(5,4)]
ns_solver.MODES=M2
from ns_solver import MODES
D=len(MODES); lam=np.array([4*np.pi**2*(kx**2+ky**2) for kx,ky in MODES],float)
NU,T,NSTEPS,N,SIGMA,SCALE=0.005,1.0,80,120,0.45,1.5
ns=NS2D(n=32,nu=NU,T=T,nsteps=NSTEPS); prior_sd=SCALE*(lam/lam[0])**(-1.0)
th_map=np.array([0.6,-0.4,0.3,0.25,-0.2,0.15,0.1,0.1,-0.08,0.06,0.05,0.04,0.03,0.02])[:D]

def fields(th):
    s,_=ns.solve(theta_to_w0h(th,ns)); U=np.empty((len(s),ns.n,ns.n)); V=np.empty_like(U)
    for i,wh in enumerate(s): U[i],V[i]=ns.velocity(wh)
    return U,V

r=np.random.default_rng(21); res={}
print("mode |k|^2 and nu*lambda*T:",
      [(int(kx**2+ky**2), round(NU*l*T,2)) for (kx,ky),l in zip(MODES,lam)])
for T0f in [0.0,0.1,0.25,0.5]:
    t_lo=int(T0f*NSTEPS)
    it=r.integers(t_lo,NSTEPS+1,N); ix=r.integers(0,ns.n,N); iy=r.integers(0,ns.n,N)
    def G(th):
        U,V=fields(th); return np.concatenate([U[it,ix,iy],V[it,ix,iy]])
    b=G(th_map); J=np.empty((len(b),D))
    for j in range(D):
        tp=th_map.copy(); tp[j]+=1e-4; J[:,j]=(G(tp)-b)/1e-4
    F=J.T@J/SIGMA**2; ev=np.linalg.eigvalsh(F)
    psd=np.sqrt(np.diag(np.linalg.inv(F+np.diag(1/prior_sd**2))))
    res[T0f]={'eig':ev.tolist(),'diagF':np.diag(F).tolist(),
              'post_sd':psd.tolist(),'shrink':(psd/prior_sd).tolist()}
    print("T0=%.2f cond %.3g | per-mode Fisher: %s"%(T0f,ev[-1]/ev[0],
          np.array2string(np.diag(F),precision=1,max_line_width=200)),flush=True)
json.dump({str(k):v for k,v in res.items()},open('spectrum_hi.json','w'),indent=1)
