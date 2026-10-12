"""Sufficiency gap of a truncated adjoint statistic in the two dimensional heat model (Table m:tab:gap).

Run from this folder: python3 mf_gap.py   (prints the table; writes no file, draws no random numbers).

Model: modes k in Z^2 with 0 < |k|_inf <= 8 ordered by |k| (D = 288), lambda_k = 4 pi^2 |k|^2, prior variances
rho^2 (lambda_k/lambda_1)^(-alpha) with alpha = 3 and rho = 1, nu = 0.01, T = 1, N = 2000 observations with unit
noise variance. The entries are computed from the population information diag(N iota_j), not from a realized
design: the posterior variance given the full data is V_Z = (N iota_j + 1/sigma_{0,j}^2)^(-1), and the summary that
keeps the first J' coordinates of Phi^T Y has V_S = V_Z on the kept modes and the prior variance on the others.
All lengths are in units of the mean posterior standard deviation u = mean_j (V_Z)_jj^(1/2).

Columns: J'; mutual information deficit Delta I = (1/2) sum log(V_S/V_Z) in nats; Rao Blackwell displacement
sqrt(tr(V_S - V_Z)); transport entropy upper bound sqrt(2 ||V_S|| Delta I); penalty of a generator that
reproduces the exact center and copies the prior spread beyond J'; then the lower bound
sqrt(tr(V_S - V_Z) - ||V_S - V_Z||_op), its ratio to the Rao Blackwell column, and the ratio of the upper bound
to the Rao Blackwell column.
"""
import numpy as np

N, NU, T, ALPHA, RHO, NOISE_VAR = 2000, 0.01, 1.0, 3.0, 1.0, 1.0
J_PRIME = (4, 8, 16, 20, 32, 48, 288)

ks = [(a, b) for a in range(-8, 9) for b in range(-8, 9) if (a, b) != (0, 0)]
ks.sort(key=lambda k: k[0] ** 2 + k[1] ** 2)
k2 = np.array([a * a + b * b for a, b in ks], float)
lam = 4 * np.pi ** 2 * k2
D = len(lam)
s0 = RHO ** 2 * (lam / lam[0]) ** (-ALPHA)                      # prior variances sigma_{0,j}^2
iota = (1 - np.exp(-2 * NU * lam * T)) / (2 * NU * lam * T)
VZ = 1.0 / (N * iota / NOISE_VAR + 1.0 / s0)                    # posterior variances given the full data
unit = np.mean(np.sqrt(VZ))
J_eff = int(np.sum(N * iota * s0 >= 1.0))
print(f"D = {D} modes, J_eff = {J_eff}, mean posterior sd u = {unit:.6g}")
print("    J'   Delta I (nats)   RB rms   T1 upper   prior spread penalty   lower bound   lower/RB   T1/RB")
worst_low, worst_t1 = (-1.0, 0), (-1.0, 0)
for Jp in J_PRIME:
    VS = np.where(np.arange(D) < Jp, VZ, s0)
    c = VS - VZ
    dI = 0.5 * np.sum(np.log(VS / VZ))
    rb = np.sqrt(c.sum()) / unit
    t1 = np.sqrt(2 * VS.max() * dI) / unit
    pen = np.sqrt(2 / np.pi) * np.sum(np.sqrt(s0[Jp:]) * (1 - (1 + N * iota[Jp:] * s0[Jp:] / NOISE_VAR) ** -0.5)) / unit
    low = np.sqrt(max(c.sum() - c.max(), 0.0)) / unit
    row = f"{Jp:6d}   {dI:14.2f}   {rb:6.1f}   {t1:8.1f}   {pen:20.2f}   {low:11.2f}"
    if rb > 0:
        row += f"   {low / rb:8.3f}   {t1 / rb:5.2f}"
        worst_low = max(worst_low, (1 - low / rb, Jp))
        worst_t1 = max(worst_t1, (t1 / rb, Jp))
    print(row)
print(f"largest relative difference between the lower bound and the RB column: {100 * worst_low[0]:.1f} percent (J' = {worst_low[1]})")
print(f"largest ratio of the T1 upper bound to the RB column: {worst_t1[0]:.2f} (J' = {worst_t1[1]})")
