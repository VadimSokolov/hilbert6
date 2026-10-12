import numpy as np, json, matplotlib
matplotlib.use('Agg'); import matplotlib.pyplot as plt
plt.rcParams.update({'font.size':9,'font.family':'serif'})
v=json.load(open('variants.json')); sp=json.load(open('spectrum_hi.json')); rad=json.load(open('radius.json'))
fig,ax=plt.subplots(1,3,figsize=(13.2,3.3))
Ms=[400,800,1600]
ax[0].axhline(v['laplace'],color='k',lw=1.4,label='Laplace / BvM')
ax[0].plot(Ms,[v[f'global_identity_M{M}'] for M in Ms],'o--',color='crimson',label='prior training, identity head')
ax[0].plot(Ms,[v[f'global_linear_M{M}'] for M in Ms],'s--',color='darkorange',label='prior training, affine head')
ax[0].plot(Ms,[v[f'local_train_identity_M{M}'] for M in Ms],'^-',color='steelblue',label='localised training, identity head')
ax[0].plot(Ms,[v[f'local_train_linear_M{M}'] for M in Ms],'v-',color='navy',label='localised training, affine head')
ax[0].set_xscale('log'); ax[0].set_yscale('log'); ax[0].set_xlabel('training simulations $M$')
ax[0].set_ylabel(r'$\mathscr{W}_1$ to exact posterior / posterior s.d.')
ax[0].set_title('(a) Accuracy vs training size'); ax[0].legend(fontsize=6.3,loc='center left')
cs=[0.5,1.0,2.0,3.0,5.0,8.0,14.0]
ax[1].axhline(rad['laplace'],color='k',lw=1.4,label='Laplace / BvM')
ax[1].plot(cs,[rad[f'c{c}_id'] for c in cs],'^-',color='steelblue',label='identity head')
ax[1].plot(cs,[rad[f'c{c}_lin'] for c in cs],'v-',color='navy',label='affine head')
ax[1].set_xscale('log'); ax[1].set_yscale('log')
ax[1].set_xlabel(r'localisation radius $c$ (proposal $N(\hat\theta,c^2H_N^{-1})$)')
ax[1].set_ylabel(r'$\mathscr{W}_1$ / posterior s.d.'); ax[1].set_title('(b) Optimal localisation radius')
ax[1].legend(fontsize=7)
MODES=[(1,0),(0,1),(1,1),(2,0),(0,2),(2,1),(2,2),(3,0),(0,3),(3,2),(4,0),(4,3),(5,0),(5,4)]
# ns_solver.py integrates on the 2pi-torus and decays mode k at nu*|k|^2, so lambda_k = |k|^2.
# Using 4 pi^2 |k|^2 here overstates the Stokes suppression by a factor exp(2 nu (4pi^2-1)|k|^2 T0).
lam=np.array([float(kx**2+ky**2) for kx,ky in MODES]); nu=0.005; T=1.0; T0v=0.5; o=np.argsort(lam)
base=np.array(sp['0.0']['diagF'])[o]
for T0,st,c in [('0.0','o-','k'),('0.25','s--','steelblue'),('0.5','^-.','crimson')]:
    F=np.array(sp[T0]['diagF'])[o]
    ax[2].plot(np.sqrt(lam[o]),F/base,st,color=c,ms=4,label=r'measured, $T_0=%s$'%T0)
a=2*nu*lam[o]
pred=((np.exp(-a*T0v)-np.exp(-a*T))/(T-T0v))/((1-np.exp(-a*T))/T)
ax[2].plot(np.sqrt(lam[o]),pred,':',color='gray',lw=2,
           label=r'Stokes prediction, $T_0=0.5$')
ax[2].set_ylim(0,1.6); ax[2].axhline(1.0,color='0.85',lw=0.8,zorder=0)
ax[2].set_xlabel(r'$|k|$'); ax[2].set_ylabel(r'information relative to $T_0=0$')
ax[2].set_title(r'(c) No viscous barrier: $2\nu\lambda_kT\leq0.41$', fontsize=9)
ax[2].legend(fontsize=6.5)
plt.tight_layout(); plt.savefig('fig_ns_study.pdf'); print('ok')
