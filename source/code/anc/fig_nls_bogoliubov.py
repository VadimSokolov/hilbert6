"""Figure 4 of gbc_initial_condition.tex: information blocks Theta_p(T) of the
cubic NLS linearised about a plane wave (Proposition 11.x, Bogoliubov system).
Run: python fig_nls_bogoliubov.py
"""
import numpy as np, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
plt.rcParams.update({'font.size':10,'font.family':'serif'})
tr=np.trapezoid
def info(p2, ka2, T=1.0, n=4000):
    """Theta_p(T) = int_0^T M_p(t)^T M_p(t) dt for the 2x2 Bogoliubov propagator.
    p2 = |p|^2 (lambda_p), ka2 = kappa a^2 (defocusing >0, focusing <0)."""
    w2 = p2*(p2+2*ka2); ts=np.linspace(0,T,n)
    if w2>0:
        w=np.sqrt(w2); c=np.cos(w*ts); s=np.sin(w*ts); r=w/p2
        M=np.array([[c, (1/r)*s],[-r*s, c]])
    else:
        g=np.sqrt(-w2); c=np.cosh(g*ts); s=np.sinh(g*ts); r=g/p2
        M=np.array([[c, (1/r)*s],[r*s, c]])
    I=np.zeros((2,2))
    for i in range(2):
        for j in range(2):
            I[i,j]=tr(np.sum(M[:,i,:]*M[:,j,:],axis=0),ts)
    return I
ps=np.arange(1,41); lam=lambda p: 4*np.pi**2*p**2
fig,ax=plt.subplots(1,2,figsize=(9,3.4))
for ka2,ls,lab in [(0.0,'k-','free'),(20.0,'b--',r'defocusing, $\kappa a^2=20$'),(-20.0,'r-.',r'focusing, $\kappa a^2=-20$')]:
    ev=np.array([np.linalg.eigvalsh(info(lam(p),ka2)) for p in ps])
    ax[0].semilogy(ps,ev[:,1],ls,label=lab); ax[0].semilogy(ps,ev[:,0],ls,alpha=0.4)
ax[0].set_xlabel(r'$|p|$'); ax[0].set_ylabel('eigenvalues of per-pair information'); ax[0].legend(fontsize=8); ax[0].set_title('NLS about a plane wave, $T=1$')
Ts=np.linspace(0.05,3,60)
for frac,ls in [(0.2,'-'),(0.5,'--'),(0.9,'-.')]:
    ka2=-0.6*lam(1); p2=frac*2*abs(ka2)
    ax[1].semilogy(Ts,[np.linalg.eigvalsh(info(p2,ka2,T=t))[1] for t in Ts],ls,label=r'$|p|^2/(2|\kappa| a^2)=%.1f$'%frac)
ax[1].plot(Ts,Ts,'k:',label=r'$T$ (free)'); ax[1].set_xlabel(r'$T$'); ax[1].set_ylabel('largest eigenvalue'); ax[1].legend(fontsize=8); ax[1].set_title('Modulational instability amplifies information')
plt.tight_layout(); plt.savefig('fig_nls.pdf')
# Free-case check. With kappa a^2 = 0 the Bogoliubov propagator M_p(t) is the identity
# for every t, so Theta_p(T) = int_0^T Id dt = T*Id exactly, for any T. The convention is
# the unnormalised one of eq:modeinfo: <e_j, L*L e_j> = int_0^T e^{-2 nu lambda_j t} dt
# = T * iota_j, so I*I carries a factor T and the Bernstein-von Mises covariance is
# T (I*I)^{-1}, i.e. per-pair scale T Theta_p(T)^{-1}/N. Everything here runs at T = 1,
# where T*Id happens to be the identity; that coincidence, not a normalisation, is why
# the matrix printed below is Id.
T_free = 1.0
print("free case check, Theta_p(T) = T*Id exactly; at T = %g this is:" % T_free)
print(info(lam(3), 0.0, T=T_free))
for p in [1,2,4,8,16]:
    print(p, "defocusing eig:", np.round(np.linalg.eigvalsh(info(lam(p),20.0)),4), " focusing eig:", np.round(np.linalg.eigvalsh(info(lam(p),-20.0)),4))
