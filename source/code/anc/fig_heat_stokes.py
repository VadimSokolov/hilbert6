"""Figures 1-3 of gbc_initial_condition.tex.
fig_heat.pdf     : per-mode information iota_k(T0) and trajectory posterior s.d. vs t
fig_tg.pdf       : advection/dissipation ratio for linearised NS about Taylor-Green
fig_heat_gbc.pdf : heat equation on T^1, exact posterior vs BvM prediction at N=2000
Run: python fig_heat_stokes.py   (numpy, matplotlib)
"""
import os

import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size':10,'font.family':'serif'})

PAPER = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'paper')
out = lambda n: os.path.join(PAPER, n)

nu=0.01; T=1.0
def lam(k2): return 4*np.pi**2*k2
def iota(k2,T0):
    # per-mode information (1/(T-T0)) int_{T0}^T e^{-2 nu lam t} dt, eq. (iota) in the paper
    l=lam(k2); return (np.exp(-2*nu*l*T0)-np.exp(-2*nu*l*T))/(2*nu*l*(T-T0))

# ---- Figure 1 ----
ks=np.arange(1,41)
fig,ax=plt.subplots(1,2,figsize=(9,3.4))
YFLOOR = 1e-24     # curves below this leave the frame; see the caption
for T0,ls in [(0,'-'),(0.05,'--'),(0.2,'-.'),(0.5,':')]:
    y = iota(ks**2,T0)
    ax[0].semilogy(ks, y, ls, label=r'$T_0=%g$'%T0)
    # mark where a curve leaves the frame, so the reader sees it exits rather than ends
    below = np.where(y < YFLOOR)[0]
    if len(below):
        ax[0].plot([ks[below[0]]], [YFLOOR*3], 'v', ms=4,
                   color=ax[0].lines[-1].get_color(), clip_on=False)
# the whole point is the contrast between polynomial and exponential decay, and at
# the untruncated range (down to 1e-253) the polynomial curve is a flat line
ax[0].set_ylim(YFLOOR, 3.0)
ax[0].set_xlabel(r'$|k|$'); ax[0].set_ylabel(r'per-mode information $\iota_k(T_0)$'); ax[0].legend(fontsize=8); ax[0].set_title('Heat / Stokes information per mode')
# At any fixed truncation the sum is finite at t=0, so a single K_max shows a
# plateau, not the divergence.  Sweeping K_max is what exhibits it: sd(0) grows
# like K_max^2, and the plateau level rises without bound.
ts=np.logspace(-5,0,240)
Nn=10**4
for K,ls in [(16,':'),(32,'-.'),(64,'--'),(128,'-')]:
    kx,ky=np.meshgrid(np.arange(-K,K+1),np.arange(-K,K+1)); k2=(kx**2+ky**2).ravel(); k2=k2[k2>0]
    k2=k2[k2<=K*K]
    sd=[np.sqrt(np.sum(np.exp(-2*nu*lam(k2)*t)/(Nn*iota(k2,0)))) for t in ts]
    ax[1].loglog(ts,sd,ls,label=r'$K_{\max}=%d$'%K)
ax[1].set_xlabel(r'$t$'); ax[1].set_ylabel(r'posterior s.d. of $u_\theta(t,x)$'); ax[1].legend(fontsize=8,title=r'$N=10^4$',title_fontsize=8)
ax[1].set_title(r'Trajectory uncertainty against truncation')
plt.tight_layout(); plt.savefig(out('fig_heat.pdf'))

print("Table 1: k, iota(0), iota(0.05), iota(0.2), 1/iota(0)")
for k in [1,2,4,8,16,32]:
    print(k, "%.3e %.3e %.3e %.3e"%(iota(k*k,0),iota(k*k,0.05),iota(k*k,0.2),1/iota(k*k,0)))

# ---- Figure 3 (Taylor-Green coupling ratio) ----
fig,ax=plt.subplots(figsize=(4.5,3.4))
kk=np.arange(1,41)
for A,ls in [(0.1,'-'),(1.0,'--'),(5.0,'-.')]:
    ax.semilogy(kk, A*2*np.pi*kk/(nu*lam(kk**2)), ls, label=r'$A=%g$'%A)
ax.axhline(1,color='k',lw=0.6)
ax.set_xlabel(r'$|k|$'); ax.set_ylabel(r'advection / dissipation ratio $2\pi A|k|/(\nu\lambda_k)$'); ax.legend(); ax.set_title('Taylor--Green background, $\\nu=0.01$')
plt.tight_layout(); plt.savefig(out('fig_tg.pdf'))

# Figure 2 (fig_heat_gbc.pdf) is produced by fig_heat_gbc.py, which reads
# results/paper_figs.json.  The earlier inline version lived here and would
# overwrite that figure with a stale two-panel one, so it has been removed.
