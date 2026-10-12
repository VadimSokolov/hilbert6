"""Advection-to-dissipation ratio of the tangent operator at the Taylor-Green vortex.

Forms the Jacobian of the vorticity right-hand side at u_TG on the 2pi-torus and
reports, per wavenumber shell, the ratio of the off-diagonal row sum of moduli to
the diagonal nu|k|^2.  This is the quantitative content of "K is compact" in the
Fredholm decomposition of the information operator.  Writes results/ns/advection.json.
"""
import json, os
import numpy as np
from ns_solver import NS2D

n, nu, A = 48, 0.01, 1.0
S = NS2D(n=n, nu=nu, T=0.5, nsteps=1)
x = 2 * np.pi * np.arange(n) / n
X1, X2 = np.meshgrid(x, x, indexing='ij')
wh0 = np.fft.fft2(2 * A * np.sin(X1) * np.sin(X2)).ravel()   # vorticity of u_TG

m = n * n
rhs = lambda v: S.rhs(v.reshape(n, n)).ravel()
base, eps = rhs(wh0), 1e-6
J = np.empty((m, m), complex)
for j in range(m):
    e = np.zeros(m, complex); e[j] = eps
    J[:, j] = (rhs(wh0 + e) - base) / eps

kk = np.sqrt(S.K2).ravel()
diag = np.abs(np.diag(J))
off = np.abs(J).sum(1) - diag
keep = (kk > 0) & S.mask.ravel()

shells = {}
for tgt in (1, 2, 4, 8, 16, 32):
    s = keep & (np.abs(kk - tgt) < 1e-9)
    if s.any():
        r = off[s] / diag[s]
        shells[str(tgt)] = dict(ratio=float(r.mean()), lo=float(r.min()), hi=float(r.max()),
                                offsum=float(off[s].mean()), diag=float(diag[s].mean()))
big = keep & (kk >= 6) & (kk <= n // 3)
c = off[big] / (A * kk[big])                    # off-diagonal row sum in units of A|k|
out = dict(n=n, nu=nu, A=A,
           shells=shells,
           const_med=float(np.median(c)), const_lo=float(np.percentile(c, 10)),
           const_hi=float(np.percentile(c, 90)),
           crossover=float(np.median(off[big] / diag[big] * kk[big])))
os.makedirs('../results/ns', exist_ok=True)
json.dump(out, open('../results/ns/advection.json', 'w'), indent=1)
print(json.dumps(out, indent=1))
