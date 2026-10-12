"""Manifold gain for the two dimensional heat equation (Table m:tab:gain).

Run from this folder: python3 mf_gain.py   (prints the table; writes no file, draws no random numbers).

Settings of the table: N = 2000 observations with noise variance varsigma^2 = 1, nu = 0.01, T = 1, alpha = 3;
both priors use the spatial modes k in Z^2 with 0 < max(|k1|, |k2|) <= 12 (no spatial mean mode),
lambda_k = 4 pi^2 |k|^2.

Constrained arm (on the solution manifold): the prior is on the initial condition, coefficient k with prior
variance rho^2 (lambda_k/lambda_1)^(-alpha), rho = 1, damped by exp(-nu lambda_k t); observations spread over [0, T]
give the information N iota_k / varsigma^2 with iota_k = (1 - exp(-2 nu lambda_k T))/(2 nu lambda_k T).
Unconstrained arm (space time Gaussian process): one coefficient per spatial mode k and temporal frequency m with
|m| <= 40, prior variance rho_u^2 (mu_{k,m}/lambda_1)^(-alpha) with mu_{k,m} = lambda_k + (2 pi m/T)^2, and the
information N / varsigma^2 per coefficient.

Matched priors: the two priors have the same alpha and the same spatial modes, and they give every observation the
same prior variance. An observation is u(X_i) plus noise with X_i uniform on [0, T] x [0, 1]^2, so the prior variance
of its signal u(X_i) is the average over [0, T] of the pointwise prior variance of u(t, x): sum_k iota_k sigma_k^2 in
the constrained arm (iota_k is the average of exp(-2 nu lambda_k t)) and sum_{k,m} sigma_{k,m}^2 in the unconstrained
arm, where it does not depend on t. Equating the two fixes rho_u. The pointwise prior variance of the constrained
arm decreases in t, from sum_k sigma_k^2 at t = 0; that of the unconstrained arm is the same at every t.
MATCHED = False gives rho_u = 1 instead, the same rho in both priors, which is the setting of the table of the paper.

The posterior standard deviation of u(t, x) at a point is the root of the sum of the posterior variances of the
coefficients (times exp(-2 nu lambda_k t) in the constrained arm); the effective parameters are the coefficients
whose information is at least the prior precision, N iota_k sigma_k^2 >= varsigma^2 (N sigma_{k,m}^2 >= varsigma^2
unconstrained).
"""
import numpy as np

N, NU, T, ALPHA, RHO, VARSIGMA = 2000, 0.01, 1.0, 3.0, 1.0, 1.0
K_MAX, M_MAX = 12, 40
TIMES = (0.0, 0.05, 0.2, 0.5, 1.0)
MATCHED = True

lam1 = 4 * np.pi ** 2
a = np.arange(-K_MAX, K_MAX + 1)
A, B = np.meshgrid(a, a, indexing="ij")
k2 = (A ** 2 + B ** 2).ravel().astype(float)
k2 = k2[k2 > 0]                                                   # 0 < max(|k1|, |k2|) <= K_MAX
lam = lam1 * k2

# constrained arm
iota = (1 - np.exp(-2 * NU * lam * T)) / (2 * NU * lam * T)
s0 = RHO ** 2 * (lam / lam1) ** (-ALPHA)
v = 1.0 / (N * iota / VARSIGMA ** 2 + 1.0 / s0)
jeff_c = int(np.sum(N * iota * s0 >= VARSIGMA ** 2))
sd_c = {t: np.sqrt(np.sum(np.exp(-2 * NU * lam * t) * v)) for t in TIMES}
prior_c = {t: np.sqrt(np.sum(np.exp(-2 * NU * lam * t) * s0)) for t in TIMES}
obs_var = np.sum(iota * s0)                                       # prior variance of an observation (signal part)

# unconstrained arm, scaled to the same prior variance of an observation
m = np.arange(-M_MAX, M_MAX + 1)
mu = (lam[:, None] + (2 * np.pi * m / T)[None, :] ** 2).ravel()
base = (mu / lam1) ** (-ALPHA)
RHO_U = np.sqrt(obs_var / base.sum()) if MATCHED else 1.0
s0u = RHO_U ** 2 * base
jeff_u = int(np.sum(N * s0u >= VARSIGMA ** 2))
sd_u = np.sqrt(np.sum(1.0 / (N / VARSIGMA ** 2 + 1.0 / s0u)))

print(f"spatial modes {k2.size}, temporal frequencies {m.size}")
print(f"prior scale: constrained rho = {RHO:.3f}, unconstrained rho = {RHO_U:.4f}")
print(f"prior sd of u(X_i), X_i uniform: constrained {np.sqrt(obs_var):.3f}, unconstrained {np.sqrt(s0u.sum()):.3f}")
print(f"pointwise prior sd: constrained {prior_c[TIMES[0]]:.3f} (t = {TIMES[0]:g}) to {prior_c[TIMES[-1]]:.3f} "
      f"(t = {TIMES[-1]:g}), unconstrained {np.sqrt(s0u.sum()):.3f}")
print(f"effective parameters: constrained {jeff_c}, unconstrained {jeff_u}")
print("t        constrained   unconstrained   ratio")
for t in TIMES:
    print(f"{t:<6g}   {sd_c[t]:11.6f}   {sd_u:13.6f}   {sd_u / sd_c[t]:6.4f}")
