"""Two checks of the Henon Heiles section drawn by figures.py (Figure fig:hh, file henon_heiles.pdf).

Run from this folder: python3 hh_checks.py   (prints one table and a summary; writes no file, draws no random
numbers; two to three minutes on a laptop).

The fifteen orbits are those of figures.py: energy E = 1/8, start at x = 0 with p_y = 0 and y equally spaced
from -0.25 to 0.45, p_x > 0 fixed by the energy, integrated to time 2500; the section points are the crossings
of x = 0 with p_x > 0.

1. Sensitivity to the integrator. Every orbit is integrated a second time with the relative tolerance 1e-10
   (absolute 1e-12) in place of the 1e-9 (absolute 1e-11) of figures.py, a stand in for a change of machine or
   library, and the points of the two sections are compared crossing by crossing.
2. Largest Lyapunov exponent along every orbit, from the tangent flow integrated together with the orbit
   (tolerances of figures.py) and renormalized every 5 time units up to the time 2500.
"""
import numpy as np
from scipy.integrate import solve_ivp

E, T_END = 1.0 / 8.0, 2500.0
Y0 = np.linspace(-0.25, 0.45, 15)
show = lambda y: round(float(y), 2) + 0.0                     # display of an initial y (the sixth start is -2.8e-17)


def hh(t, s):
    x, y, px, py = s
    return [px, py, -x - 2 * x * y, -y - x * x + y * y]


def start(y0, py0=0.0):
    rest = 2 * E - py0 ** 2 - y0 ** 2 + (2.0 / 3.0) * y0 ** 3
    return [0.0, y0, np.sqrt(rest), py0]


def section(y0, rtol, atol):
    ev = lambda t, s: s[0]
    ev.direction = 1
    sol = solve_ivp(hh, [0, T_END], start(y0), events=ev, rtol=rtol, atol=atol)
    return sol.y_events[0][:, [1, 3]]                      # (y, p_y) at the crossings


def tangent(t, u):
    x, y, px, py = u[:4]
    J = np.array([[0, 0, 1, 0], [0, 0, 0, 1], [-1 - 2 * y, -2 * x, 0, 0], [-2 * x, -1 + 2 * y, 0, 0]])
    return np.concatenate((hh(t, u[:4]), J @ u[4:]))


def lyapunov(y0, dt=5.0):
    u = np.concatenate((start(y0), [1.0, 0.0, 0.0, 0.0]))
    total = 0.0
    for _ in range(int(T_END / dt)):
        u = solve_ivp(tangent, [0, dt], u, rtol=1e-9, atol=1e-11).y[:, -1]
        n = np.linalg.norm(u[4:])
        total += np.log(n)
        u[4:] /= n
    return total / T_END


print("initial y   crossings (1e-9, 1e-10)   first crossing with a difference above 0.01   "
      "largest difference over the first 100 crossings   largest Lyapunov exponent", flush=True)
rows = []
for y0 in Y0:
    a = section(y0, 1e-9, 1e-11)
    b = section(y0, 1e-10, 1e-12)
    n = min(len(a), len(b))
    d = np.abs(a[:n] - b[:n]).max(axis=1)
    bad = np.where(d > 0.01)[0]
    first = int(bad[0]) + 1 if len(bad) else None
    lam = lyapunov(y0)
    rows.append((show(y0), first, d[:100].max(), lam))
    print(f"{show(y0):+10.2f}   {len(a):9d} {len(b):5d}   {first if first else 'never':>12}   {d[:100].max():12.2e}   {lam:12.5f}",
          flush=True)

regular = [r for r in rows if r[3] < 0.01]
chaotic = [r for r in rows if r[3] >= 0.01]
print(f"exponent below 0.01: {len(regular)} orbits, initial y from {min(r[0] for r in regular):+.2f} to "
      f"{max(r[0] for r in regular):+.2f}, largest exponent {max(r[3] for r in regular):.5f}, "
      f"largest difference over the first 100 crossings {max(r[2] for r in regular):.1e}, "
      f"difference above 0.01: {'never' if all(r[1] is None for r in regular) else 'yes'}")
if chaotic:
    firsts = [r[1] for r in chaotic if r[1] is not None]
    print(f"exponent 0.01 or more: {len(chaotic)} orbits, initial y from {min(r[0] for r in chaotic):+.2f} to "
          f"{max(r[0] for r in chaotic):+.2f}, exponents from {min(r[3] for r in chaotic):.4f} to "
          f"{max(r[3] for r in chaotic):.4f}, first difference above 0.01 at crossings "
          f"{min(firsts) if firsts else 'none'} to {max(firsts) if firsts else 'none'} "
          f"({len(firsts)} of {len(chaotic)} orbits)")
