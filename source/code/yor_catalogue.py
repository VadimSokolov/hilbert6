#!/usr/bin/env python3
"""Checks for the catalogue of Yor identities with algorithm boxes.

Book: On Hilbert's 6th Problem (Polson and Sokolov), Chapter on Brownian motion,
section on Yor's identities as algorithms, file chapters/ext/ch04_yor.tex.

For each exact sampler of the catalogue the script prints the Kolmogorov Smirnov
distance to the exact distribution function, and the same distance for an Euler
discretization of the path functional at the step sizes 2^-6, 2^-8, 2^-10, 2^-12.
The four Euler schemes of one functional share the same Brownian paths (the coarse
path is the fine path read on a coarser grid), so their errors are comparable.
It also repeats every exact sampler with fresh seeds (calibration of the test), checks
the Kent series for the exit time, the identity of Matsumoto and Yor for opposite drifts,
the moments of Biane, Pitman and Yor, and the horseshoe mixing variable, and times the
exact samplers against the Euler schemes.

Run:   python3 yor_catalogue.py [--fast] [--out DIR]
Needs: numpy (default_rng) and scipy.
Writes only into DIR (default ./yor_out): yor_results.json (every printed number).
Fixed seeds; the full run takes about two minutes on one core.  --fast uses
ten times fewer samples and is for testing only.
"""
import os
import sys
import time
import json

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")

import numpy as np
import scipy
from scipy import special, stats, integrate

FAST = "--fast" in sys.argv
OUT = "yor_out"
if "--out" in sys.argv:
    OUT = sys.argv[sys.argv.index("--out") + 1]

SEED = 20261007
N = 10_000 if FAST else 100_000          # sample size of every Kolmogorov Smirnov test
LEVELS = (6, 8, 10, 12)                   # Euler step sizes h = 2^-j
JMAX = max(LEVELS)
RES = {}                                  # everything printed is also stored here


def say(key, **kw):
    """Print one result line and store it."""
    RES[key] = kw
    print(key, " ".join("%s=%s" % (k, ("%.6g" % v) if isinstance(v, float) else v) for k, v in kw.items()), flush=True)


def ks_stat(x, cdf):
    """One sample Kolmogorov Smirnov statistic sup |F_n - F| (ties handled)."""
    x = np.sort(np.asarray(x, dtype=float))
    n = x.size
    F = cdf(x)
    i = np.arange(1, n + 1)
    return float(max((i / n - F).max(), (F - (i - 1) / n).max()))


def ks_crit(n, level=0.05):
    """Critical value of the one sample test at the given level."""
    return float(stats.kstwo.ppf(1.0 - level, n))


# ----------------------------------------------------------------------------
# 1. The exact samplers (the algorithm boxes of the book)
# ----------------------------------------------------------------------------
def sample_perpetuity(mu, n, rng):
    """Algorithm Dufresne: 1/(2G), G ~ Gamma(mu, 1).  One variate."""
    return 1.0 / (2.0 * rng.gamma(mu, 1.0, n))


def sample_bougerol(t, n, rng):
    """Algorithm Bougerol: sinh(sqrt(t) Z), Z ~ N(0,1).  One variate."""
    return np.sinh(np.sqrt(t) * rng.standard_normal(n))


def sample_bm_max(t, n, rng):
    """Algorithm maximum: (B_t, M_t) from one normal and one uniform variate."""
    z = rng.standard_normal(n)
    u = 1.0 - rng.random(n)                # uniform on (0, 1]
    b = np.sqrt(t) * z
    m = 0.5 * (b + np.sqrt(b * b - 2.0 * t * np.log(u)))
    return b, m


def sample_bm_max_pitman(t, n, rng):
    """Second exact route (Pitman): R = sqrt(t) chi_3, M = R V, B = 2M - R."""
    r = np.sqrt(2.0 * t * rng.gamma(1.5, 1.0, n))      # chi_3 = sqrt(2 Gamma(3/2))
    m = r * rng.random(n)
    return 2.0 * m - r, m


def sample_ig_msh(a, nu, n, rng):
    """Algorithm passage time (the box of the book): Michael, Schucany and Haas for the first passage
    time of B_t + nu t to the level a, that is IG(a/nu, a^2).  Two variates per draw."""
    y = rng.standard_normal(n) ** 2
    x = a / nu + (y - np.sqrt(y * y + 4.0 * a * nu * y)) / (2.0 * nu * nu)     # the root below a/nu
    u = rng.random(n)
    return np.where(u <= a / (a + nu * x), x, a * a / (nu * nu * x))


def sample_ig_msh_stable(a, nu, n, rng):
    """Same law with the smaller root computed as mu^2 / (larger root), which avoids the cancellation
    of the box formula when Z^2 is very large (used to show that both forms agree)."""
    mu, lam = a / nu, a * a
    y = rng.standard_normal(n) ** 2
    big = mu + mu * mu * y / (2.0 * lam) + (mu / (2.0 * lam)) * np.sqrt(4.0 * mu * lam * y + mu * mu * y * y)
    x = mu * mu / big
    u = rng.random(n)
    return np.where(u <= mu / (mu + x), x, mu * mu / x)


# ----------------------------------------------------------------------------
# 2. Exact distribution functions (independent of the samplers)
# ----------------------------------------------------------------------------
def cdf_perpetuity(x, mu):
    return special.gammaincc(mu, 1.0 / (2.0 * x))


def cdf_bougerol(x, t):
    return special.ndtr(np.arcsinh(x) / np.sqrt(t))


def cdf_max(m, t):
    return special.erf(np.maximum(m, 0.0) / np.sqrt(2.0 * t))


def cdf_ig(x, mu, lam):
    s = np.sqrt(lam / x)
    return special.ndtr(s * (x / mu - 1.0)) + np.exp(2.0 * lam / mu) * special.ndtr(-s * (x / mu + 1.0))


def cdf_exit_time(t):
    """P(T <= t) for the exit time of Brownian motion from (-1, 1): two convergent series."""
    t = np.asarray(t, dtype=float)
    k = np.arange(0, 60)[:, None]
    direct = 1.0 - (4.0 / np.pi) * np.sum((-1.0) ** k / (2 * k + 1) * np.exp(-((2 * k + 1) ** 2) * np.pi ** 2 * t[None, :] / 8.0), axis=0)
    dual = 2.0 * np.sum((-1.0) ** k * special.erfc((2 * k + 1) / np.sqrt(2.0 * t[None, :])), axis=0)
    return np.where(t > 0.4, direct, dual)


# ----------------------------------------------------------------------------
# 3. Nested Euler engine: paths on the finest grid, read on coarser grids
# ----------------------------------------------------------------------------
def bm_chunks(rng, n_paths, n_fine, h_fine, chunk_elems=3_000_000):
    """Yield blocks of Brownian paths on the grid k h_fine, k = 0..n_fine."""
    c = max(1, chunk_elems // (n_fine + 1))
    done = 0
    while done < n_paths:
        m = min(c, n_paths - done)
        inc = rng.standard_normal((m, n_fine))
        inc *= np.sqrt(h_fine)
        B = np.empty((m, n_fine + 1))
        B[:, 0] = 0.0
        np.cumsum(inc, axis=1, out=B[:, 1:])
        yield B
        done += m


def euler_integral_levels(rng, n_paths, horizon, drift, levels=LEVELS, extra=None):
    """Left endpoint Riemann sums of exp(2 (B_s + drift s)) on [0, horizon] for every step 2^-j,
    all computed on the same paths.  Returns {j: array}, and the end value B_horizon.
    `extra` is an optional per path array of independent normals returned unchanged (for Bougerol)."""
    n_fine = int(round(horizon * 2 ** JMAX))
    h_fine = 2.0 ** -JMAX
    out = {j: np.empty(n_paths) for j in levels}
    bend = np.empty(n_paths)
    pos = 0
    for B in bm_chunks(rng, n_paths, n_fine, h_fine):
        m = B.shape[0]
        for j in levels:
            s = 2 ** (JMAX - j)
            idx = np.arange(0, n_fine, s)
            tk = idx * h_fine
            out[j][pos:pos + m] = (2.0 ** -j) * np.exp(2.0 * (B[:, idx] + drift * tk)).sum(axis=1)
        bend[pos:pos + m] = B[:, -1]
        pos += m
    return out, bend


def euler_bougerol_and_max(rng, n_paths, t, levels=LEVELS):
    """Bougerol and the maximum on the same paths of B on [0, t]: for every j
    S_j = sqrt(A_j) G with A_j the left endpoint sum and G an independent normal (shared by all j),
    M_j = max of B on the grid, plus the exact end point B_t."""
    n_fine = int(round(t * 2 ** JMAX))
    h_fine = 2.0 ** -JMAX
    S = {j: np.empty(n_paths) for j in levels}
    A = {j: np.empty(n_paths) for j in levels}
    M = {j: np.empty(n_paths) for j in levels}
    bend = np.empty(n_paths)
    pos = 0
    for B in bm_chunks(rng, n_paths, n_fine, h_fine):
        m = B.shape[0]
        G = rng.standard_normal(m)
        for j in levels:
            s = 2 ** (JMAX - j)
            idx = np.arange(0, n_fine, s)
            a = (2.0 ** -j) * np.exp(2.0 * B[:, idx]).sum(axis=1)
            A[j][pos:pos + m] = a
            S[j][pos:pos + m] = np.sqrt(a) * G
            M[j][pos:pos + m] = B[:, ::s].max(axis=1)
        bend[pos:pos + m] = B[:, -1]
        pos += m
    return S, A, M, bend


def euler_passage_levels(rng, n_paths, a, nu, tcap, levels=LEVELS, block=4096, chunk=1500, jfine=None):
    """First grid time at which X_k = k h nu + B_{kh} reaches a, for every step 2^-j, same paths.
    Paths that have not reached a at time tcap get the value tcap + 1.  Returns {j: array}.
    The paths are simulated on the grid 2^-jfine (default: the finest level)."""
    jfine = JMAX if jfine is None else jfine
    h = 2.0 ** -jfine
    sq = np.sqrt(h)
    tau = {j: np.full(n_paths, np.nan) for j in levels}
    jc = min(levels)                                    # coarsest level, the last to cross
    X0 = np.zeros(n_paths)                              # fine walk at the start of the block
    active = np.arange(n_paths)
    nblocks = int(np.ceil(tcap / (block * h)))
    for b in range(nblocks):
        if active.size == 0:
            break
        start = b * block                               # fine index at the start of the block
        for lo in range(0, active.size, chunk):
            ids = active[lo:lo + chunk]
            m = ids.size
            X = rng.standard_normal((m, block))
            X *= sq
            X += nu * h
            np.cumsum(X, axis=1, out=X)
            X += X0[ids][:, None]
            for j in levels:
                s = 2 ** (jfine - j)
                need = np.isnan(tau[j][ids])
                if not need.any():
                    continue
                vals = X[:, s - 1::s]
                cross = vals >= a
                has = cross.any(axis=1)
                first = cross.argmax(axis=1)
                hit = need & has
                tau[j][ids[hit]] = (start + (first[hit] + 1) * s) * h
            X0[ids] = X[:, -1]
        active = active[np.isnan(tau[jc][active])]
    for j in levels:
        tau[j][np.isnan(tau[j])] = tcap + 1.0
    return tau


# ----------------------------------------------------------------------------
# 4. The checks
# ----------------------------------------------------------------------------
def main():
    t0 = time.time()
    print("numpy", np.__version__, "scipy", scipy.__version__,
          "python", sys.version.split()[0], "N", N, "seed", SEED, "fast", FAST, flush=True)
    crit = ks_crit(N)
    say("ks_critical_5pct", N=N, value=crit, expected_distance_exact_sample=0.8687 / np.sqrt(N))

    # ---- (a) Dufresne perpetuity ------------------------------------------------
    MU, TD = 2.0, 6.0
    rng = np.random.default_rng(SEED + 1)
    d = ks_stat(sample_perpetuity(MU, N, rng), lambda x: cdf_perpetuity(x, MU))
    say("dufresne_exact", mu=MU, N=N, KS=d)
    rngE = np.random.default_rng(SEED + 2)
    t1 = time.time()
    A_lv, _ = euler_integral_levels(rngE, N, TD, -MU)
    for j in LEVELS:
        say("dufresne_euler", mu=MU, horizon=TD, h="2^-%d" % j, N=N, KS=ks_stat(1.0 * A_lv[j], lambda x: cdf_perpetuity(x, MU)),
            mean=float(A_lv[j].mean()), mean_exact_euler=(2.0 ** -j) / (1.0 - np.exp(-2.0 * (MU - 1.0) * 2.0 ** -j)) * (1.0 - np.exp(-2.0 * (MU - 1.0) * TD)),
            mean_exact_limit=1.0 / (2.0 * (MU - 1.0)),
            rel_bias_exact_mean=((2.0 ** -j) / (1.0 - np.exp(-2.0 * (MU - 1.0) * 2.0 ** -j)) * (1.0 - np.exp(-2.0 * (MU - 1.0) * TD))) * 2.0 * (MU - 1.0) - 1.0)
    say("dufresne_euler_time", seconds=time.time() - t1)
    # truncation at the horizon: E[A_inf - A_T] = exp(-2 (mu-1) T) / (2 (mu-1))
    say("dufresne_truncation", mean_missing=float(np.exp(-2.0 * (MU - 1.0) * TD) / (2.0 * (MU - 1.0))))

    # ---- (b) Bougerol and (c) the maximum --------------------------------------
    TB = 1.0
    rng = np.random.default_rng(SEED + 3)
    sb = sample_bougerol(TB, N, rng)
    say("bougerol_exact", t=TB, N=N, KS=ks_stat(sb, lambda x: cdf_bougerol(x, TB)))
    rng = np.random.default_rng(SEED + 4)
    bb, mm = sample_bm_max(TB, N, rng)
    say("max_exact", t=TB, N=N, KS_M=ks_stat(mm, lambda m: cdf_max(m, TB)), KS_B=ks_stat(bb, lambda b: special.ndtr(b / np.sqrt(TB))))
    rng = np.random.default_rng(SEED + 5)
    bp, mp = sample_bm_max_pitman(TB, N, rng)
    # Pitman route vs the formula P(M >= m | B = b) = exp(-2 m (m - b) / t): probability integral transform
    v = np.exp(-2.0 * mp * (mp - bp) / TB)
    say("max_pitman_route", N=N, KS_M=ks_stat(mp, lambda m: cdf_max(m, TB)), KS_B=ks_stat(bp, lambda b: special.ndtr(b / np.sqrt(TB))),
        KS_conditional_PIT=ks_stat(v, lambda x: np.clip(x, 0.0, 1.0)))
    say("max_two_routes_2sample", N=N, KS_M=float(stats.ks_2samp(mm, mp).statistic), KS_B=float(stats.ks_2samp(bb, bp).statistic),
        crit_2sample_5pct=1.358 * np.sqrt(2.0 / N))
    rngE = np.random.default_rng(SEED + 6)
    t1 = time.time()
    S_lv, A_lv2, M_lv, bend = euler_bougerol_and_max(rngE, N, TB)
    exact_mean_A = (np.exp(2 * TB) - 1.0) / 2.0
    for j in LEVELS:
        h = 2.0 ** -j
        mean_euler_A = h * (np.exp(2 * TB) - 1.0) / (np.exp(2 * h) - 1.0)     # exact mean of the left endpoint sum
        say("bougerol_euler", t=TB, h="2^-%d" % j, N=N, KS=ks_stat(S_lv[j], lambda x: cdf_bougerol(x, TB)),
            meanA=float(A_lv2[j].mean()), meanA_euler_exact=float(mean_euler_A), meanA_limit=float(exact_mean_A),
            rel_bias_euler=float(mean_euler_A / exact_mean_A - 1.0))
        vv = np.exp(-2.0 * M_lv[j] * (M_lv[j] - bend) / TB)
        n_steps = int(round(TB / h))
        spitzer = np.sqrt(h / (2.0 * np.pi)) * np.sum(1.0 / np.sqrt(np.arange(1, n_steps + 1)))
        p0 = float(np.exp(special.gammaln(2 * n_steps + 1) - 2.0 * special.gammaln(n_steps + 1) - 2.0 * n_steps * np.log(2.0)))   # C(2n,n) 4^-n
        say("max_euler", t=TB, h="2^-%d" % j, N=N, KS_M=ks_stat(M_lv[j], lambda m: cdf_max(m, TB)),
            mean_M=float(M_lv[j].mean()), mean_M_grid_exact=float(spitzer), mean_M_limit=float(np.sqrt(2.0 * TB / np.pi)),
            P_M_equals_0=float(np.mean(M_lv[j] == 0.0)), P_M_equals_0_exact=p0)
    say("bougerol_max_euler_time", seconds=time.time() - t1)
    # Bougerol vs the finest Euler scheme, two sample
    say("bougerol_exact_vs_euler12_2sample", KS=float(stats.ks_2samp(sb, S_lv[JMAX]).statistic), crit_2sample_5pct=1.358 * np.sqrt(2.0 / N))
    say("max_exact_vs_euler12_2sample", KS=float(stats.ks_2samp(mm, M_lv[JMAX]).statistic), crit_2sample_5pct=1.358 * np.sqrt(2.0 / N))

    # ---- (d) first passage time with drift (Michael, Schucany and Haas) -----------
    AP, NU, TCAP = 1.0, 1.0, 24.0
    mu_ig, lam_ig = AP / NU, AP * AP
    rng = np.random.default_rng(SEED + 7)
    xs = sample_ig_msh(AP, NU, N, rng)
    say("passage_exact", a=AP, nu=NU, N=N, KS=ks_stat(xs, lambda x: cdf_ig(x, mu_ig, lam_ig)))
    rng = np.random.default_rng(SEED + 8)
    xt = sample_ig_msh_stable(AP, NU, N, rng)
    say("passage_exact_stable_form", KS=ks_stat(xt, lambda x: cdf_ig(x, mu_ig, lam_ig)))
    say("passage_tail_beyond_cap", tcap=TCAP, survival=float(1.0 - cdf_ig(np.array([TCAP]), mu_ig, lam_ig)[0]))
    # the fact behind the algorithm: (nu T - a)^2 / T has the chi squared law with one degree of freedom.
    # P((nu T - a)^2 / T <= y) = F(t2) - F(t1), with t1 < t2 the roots of (nu t - a)^2 = y t; exact, no sampling.
    yy = np.linspace(0.01, 30.0, 3000)
    disc = np.sqrt(yy * yy + 4.0 * AP * NU * yy)
    t1 = AP / NU + (yy - disc) / (2.0 * NU * NU)
    t2 = AP / NU + (yy + disc) / (2.0 * NU * NU)
    say("passage_chi2_fact", max_abs_difference=float(np.max(np.abs(cdf_ig(t2, mu_ig, lam_ig) - cdf_ig(t1, mu_ig, lam_ig) - special.erf(np.sqrt(yy / 2.0))))))
    rngE = np.random.default_rng(SEED + 9)
    t1 = time.time()
    tau = euler_passage_levels(rngE, N, AP, NU, TCAP)
    for j in LEVELS:
        say("passage_euler", a=AP, nu=NU, h="2^-%d" % j, N=N, KS=ks_stat(tau[j], lambda x: cdf_ig(x, mu_ig, lam_ig)), mean=float(tau[j].mean()),
            mean_exact=AP / NU)
    say("passage_euler_time", seconds=time.time() - t1)
    say("passage_exact_vs_euler12_2sample", KS=float(stats.ks_2samp(xs, tau[JMAX]).statistic), crit_2sample_5pct=1.358 * np.sqrt(2.0 / N))

    # ---- calibration of the exact samplers: R fresh replicates of N draws each ----------------------
    R = 20 if FAST else 40
    exact = {
        "perpetuity": (lambda r: sample_perpetuity(MU, N, r), lambda x: cdf_perpetuity(x, MU)),
        "bougerol": (lambda r: sample_bougerol(TB, N, r), lambda x: cdf_bougerol(x, TB)),
        "maximum_M": (lambda r: sample_bm_max(TB, N, r)[1], lambda m: cdf_max(m, TB)),
        "maximum_B": (lambda r: sample_bm_max(TB, N, r)[0], lambda b: special.ndtr(b / np.sqrt(TB))),
        "maximum_pitman_route_M": (lambda r: sample_bm_max_pitman(TB, N, r)[1], lambda m: cdf_max(m, TB)),
        "passage": (lambda r: sample_ig_msh(AP, NU, N, r), lambda x: cdf_ig(x, mu_ig, lam_ig)),
    }
    for k, (name, (draw, cdf)) in enumerate(exact.items()):
        ds = np.array([ks_stat(draw(np.random.default_rng(SEED + 1000 + 100 * k + r)), cdf) for r in range(R)])
        say("calibration", sampler=name, replicates=R, N=N, mean_KS=float(ds.mean()), max_KS=float(ds.max()), n_above_crit5=int((ds > crit).sum()))

    # the two exact routes to (B_t, M_t) against each other: R fresh two sample comparisons
    c2 = 1.358 * np.sqrt(2.0 / N)
    dM, dB = [], []
    for r in range(R):
        b1, m1 = sample_bm_max(TB, N, np.random.default_rng(SEED + 2000 + 2 * r))
        b2, m2 = sample_bm_max_pitman(TB, N, np.random.default_rng(SEED + 2001 + 2 * r))
        dM.append(float(stats.ks_2samp(m1, m2).statistic))
        dB.append(float(stats.ks_2samp(b1, b2).statistic))
    say("two_routes_replicates", replicates=R, N=N, crit_2sample_5pct=c2, mean_KS_M=float(np.mean(dM)), mean_KS_B=float(np.mean(dB)),
        n_above_M=int(np.sum(np.array(dM) > c2)), n_above_B=int(np.sum(np.array(dB) > c2)))

    # ---- (e) Kent series for the exit time, Ciesielski and Taylor ---------------
    tt = np.array([0.4])
    say("exit_cdf_two_series_at_0.4", direct=float(1.0 - (4 / np.pi) * sum((-1) ** n / (2 * n + 1) * np.exp(-((2 * n + 1) ** 2) * np.pi ** 2 * 0.4 / 8) for n in range(60))),
        dual=float(2 * sum((-1) ** k * special.erfc((2 * k + 1) / np.sqrt(0.8)) for k in range(60))))
    rng = np.random.default_rng(SEED + 10)
    for K in (1, 2, 4, 8, 16):
        n = np.arange(1, K + 1)
        c = 8.0 / ((2 * n - 1) ** 2 * np.pi ** 2)
        E = rng.standard_exponential((N, K))
        base = E @ c
        mrem = (special.polygamma(1, K + 0.5) / 4.0) * 8.0 / np.pi ** 2
        vrem = (special.polygamma(3, K + 0.5) / 96.0) * 64.0 / np.pi ** 4
        corr = base + rng.gamma(mrem ** 2 / vrem, vrem / mrem, N)
        say("kent_series", K=K, N=N, KS_truncated=ks_stat(base, cdf_exit_time), KS_with_gamma_remainder=ks_stat(corr, cdf_exit_time),
            remainder_mean=float(mrem), approx_2_over_pi2K=float(2.0 / (np.pi ** 2 * K)))
    # Laplace transform 1/cosh(sqrt(2 lam)) from the series, and the occupation time identity (radial ODE solution)
    for lam in (0.5, 2.0):
        k = np.sqrt(2 * lam)
        prod = np.prod(1.0 / (1.0 + 8.0 * lam / ((2 * np.arange(1, 200000) - 1) ** 2 * np.pi ** 2)))
        a_ = 1.0 / (k * np.cosh(k))
        u0 = a_ * k
        c_ = a_ * (k * np.cosh(k) - np.sinh(k))
        say("exit_laplace", lam=lam, product=float(prod), one_over_cosh=float(1.0 / np.cosh(k)), abs_difference=float(abs(prod - 1.0 / np.cosh(k))), occupation_u0=float(u0),
            continuity_at_1=float(a_ * np.sinh(k) - (1.0 - c_)))

    # ---- (f) Dufresne and Matsumoto and Yor, opposite drifts --------------------------
    MUY, TY, NY, JY = 1.0, 1.0, (4000 if FAST else 50_000), 10
    nf = int(round(TY * 2 ** JY))
    hY = 2.0 ** -JY
    tk = np.arange(0, nf) * hY
    def a_levels(seed, drift):
        r = np.random.default_rng(seed)
        out = np.empty(NY)
        pos = 0
        for B in bm_chunks(r, NY, nf, hY):
            out[pos:pos + B.shape[0]] = hY * np.exp(2.0 * (B[:, :-1] + drift * tk)).sum(axis=1)
            pos += B.shape[0]
        return out
    Aneg = a_levels(SEED + 11, -MUY)
    Apos = a_levels(SEED + 12, +MUY)
    rg = np.random.default_rng(SEED + 13)
    V = 1.0 / Aneg
    W = 1.0 / Apos + 2.0 * rg.gamma(MUY, 1.0, NY)
    say("my_opposite_drifts", mu=MUY, t=TY, h="2^-%d" % JY, N=NY, KS_2sample=float(stats.ks_2samp(V, W).statistic), crit_2sample_5pct=1.358 * np.sqrt(2.0 / NY),
        mean_V=float(V.mean()), se_V=float(V.std() / np.sqrt(NY)), mean_W=float(W.mean()), se_W=float(W.std() / np.sqrt(NY)),
        mean_difference_V_minus_1_over_Apos=float(V.mean() - (1.0 / Apos).mean()), expected_2mu=2.0 * MUY)

    # ---- (g) Biane, Pitman and Yor: E Y^s = 2 xi(s) --------------------------------------
    def cdf_exc_max(x):
        x = np.asarray(x, dtype=float)
        out = np.empty_like(x)
        lo = x <= 1.2
        xl = x[lo]
        kk = np.arange(1, 40)[:, None]
        out[lo] = np.sqrt(2.0) * np.pi ** 2.5 / xl ** 3 * np.sum(kk ** 2 * np.exp(-np.pi ** 2 * kk ** 2 / (2.0 * xl[None, :] ** 2)), axis=0)
        xh = x[~lo]
        nn = np.arange(-60, 61)[:, None]
        out[~lo] = np.sum((1.0 - 4.0 * nn ** 2 * xh[None, :] ** 2) * np.exp(-2.0 * nn ** 2 * xh[None, :] ** 2), axis=0)
        return out
    say("excursion_max_cdf_two_series_at_1.2", dual=float(cdf_exc_max(np.array([1.2]))[0]),
        direct=float(np.sum((1 - 4 * np.arange(-60, 61) ** 2 * 1.44) * np.exp(-2 * np.arange(-60, 61) ** 2 * 1.44))))
    def xi(s):
        if s == 1.0:
            return 0.5                                     # limit of (s - 1) zeta(s)
        return s * (s - 1.0) / 2.0 * np.pi ** (-s / 2.0) * special.gamma(s / 2.0) * special.zeta(s)
    for s in (1.0, 2.0, 3.0, 4.0):
        # E[m^s] = int s x^(s-1) (1 - F(x)) dx
        val = integrate.quad(lambda x: s * x ** (s - 1) * (1.0 - float(cdf_exc_max(np.array([x]))[0])), 0.0, 12.0, limit=400, epsabs=1e-13, epsrel=1e-12)[0]
        Ys = (2.0 / np.pi) ** (s / 2.0) * val
        say("bpy_moment", s=s, E_Ys_from_cdf=float(Ys), two_xi_s=float(2 * xi(s)), abs_difference=float(abs(Ys - 2 * xi(s))))
    # Monte Carlo: maximum of the excursion as the maximum of the norm of a 3 dimensional Brownian bridge on a grid
    NB, nb = (2000 if FAST else 20_000), 2 ** 10
    r = np.random.default_rng(SEED + 15)
    mx = np.empty(NB)
    pos = 0
    kgrid = np.arange(0, nb + 1) / nb
    chunk = max(1, 600_000 // (nb + 1))
    pos = 0
    while pos < NB:
        m = min(chunk, NB - pos)
        W = r.standard_normal((m, 3, nb)) * np.sqrt(1.0 / nb)
        P = np.concatenate([np.zeros((m, 3, 1)), np.cumsum(W, axis=2)], axis=2)
        Bb = P - kgrid[None, None, :] * P[:, :, -1:][:, :, :]
        mx[pos:pos + m] = np.sqrt((Bb ** 2).sum(axis=1)).max(axis=1)
        pos += m
    say("excursion_max_mc", N=NB, grid=nb, KS=ks_stat(mx, cdf_exc_max), mean=float(mx.mean()), mean_exact=float(np.sqrt(np.pi / 2.0)))

    # ---- (h) horseshoe mixing variable ----------------------------------------------------
    NH = 200_000 if FAST else 1_000_000
    r = np.random.default_rng(SEED + 16)
    lam2 = r.gamma(0.5, 1.0, NH) / r.gamma(0.5, 1.0, NH)
    cauchy2 = r.standard_cauchy(NH) ** 2
    say("horseshoe_ks_critical_5pct", N=NH, value=ks_crit(NH))
    say("horseshoe_two_routes", N=NH, KS_ratio_of_gammas=ks_stat(lam2, lambda x: 2.0 / np.pi * np.arctan(np.sqrt(x))),
        KS_cauchy_squared=ks_stat(cauchy2, lambda x: 2.0 / np.pi * np.arctan(np.sqrt(x))))
    for s in (0.1, 1.0, 10.0):
        est = np.exp(-s * lam2)
        say("horseshoe_laplace", s=s, monte_carlo=float(est.mean()), mc_se=float(est.std() / np.sqrt(NH)), exact_exp_s_erfc_sqrt_s=float(special.erfcx(np.sqrt(s))),
            abs_difference=float(abs(est.mean() - special.erfcx(np.sqrt(s)))), z=float((est.mean() - special.erfcx(np.sqrt(s))) / (est.std() / np.sqrt(NH))),
            exact_by_quadrature=float(integrate.quad(lambda u: np.exp(-s * u) / (np.pi * np.sqrt(u) * (1.0 + u)), 0, np.inf, limit=400)[0]))
    # Thorin mass: Phi(s) = -s - log erfc(sqrt s) and Phi(s) - (1/2) log(pi s) -> 0
    for s in (1e2, 1e4, 1e6):
        Phi = -float(np.log(special.erfcx(np.sqrt(s))))     # -s - log erfc(sqrt s), written with erfcx to avoid underflow
        say("horseshoe_thorin_mass", s=s, Phi=Phi, half_log_pi_s=0.5 * float(np.log(np.pi * s)), difference=Phi - 0.5 * float(np.log(np.pi * s)), Phi_over_log_s=Phi / float(np.log(s)))
    # Thorin density by Stieltjes inversion: u(x) = exp(x) / (pi^(3/2) sqrt(x) (1 + erfi(sqrt x)^2)).
    # Written with Dawson's integral, erfi(y) = (2/sqrt(pi)) exp(y^2) dawsn(y), so that nothing overflows.
    def thorin_density(x):
        d = special.dawsn(np.sqrt(x))
        return np.exp(-x) / (np.pi ** 1.5 * np.sqrt(x) * (np.exp(-2.0 * x) + (4.0 / np.pi) * d * d))
    mass = integrate.quad(thorin_density, 0, 400, limit=800, epsabs=1e-14, epsrel=1e-13)[0]
    errs = []
    for s in (0.01, 0.1, 1.0, 10.0, 100.0):
        phi_int = integrate.quad(lambda x: np.log1p(s / x) * thorin_density(x), 0, 400, limit=800, epsabs=1e-14, epsrel=1e-13)[0]
        phi_ex = -float(np.log(special.erfcx(np.sqrt(s))))
        errs.append(abs(phi_int - phi_ex))
        say("horseshoe_thorin_density_check", s=s, integral_log1p_s_over_x_times_u=float(phi_int), Phi_exact=phi_ex, abs_error=float(abs(phi_int - phi_ex)))
    say("horseshoe_thorin_mass_from_density", mass=float(mass), max_abs_error_laplace_exponent=float(max(errs)))

    # ---- timing: exact samplers against Euler at h = 2^-10 --------------------------------------
    # CPU time of this process (time.process_time), best of several repetitions, scaled to 10^5 draws.
    def cpu_best(f, reps):
        best = np.inf
        for _ in range(reps):
            t1 = time.process_time()
            f()
            best = min(best, time.process_time() - t1)
        return best

    def euler_sums(T_, drift, nfine_paths, seed):
        nfine = int(T_ * 2 ** 10)
        tk = np.arange(0, nfine) * 2.0 ** -10
        for B in bm_chunks(np.random.default_rng(seed), nfine_paths, nfine, 2.0 ** -10):
            _ = (2.0 ** -10) * np.exp(2.0 * (B[:, :-1] + drift * tk)).sum(axis=1)

    def euler_max(T_, nfine_paths, seed):
        nfine = int(T_ * 2 ** 10)
        for B in bm_chunks(np.random.default_rng(seed), nfine_paths, nfine, 2.0 ** -10):
            _ = B.max(axis=1)

    NT, NE, NEP = 1_000_000, 400, 2000
    timing = {}
    rr = np.random.default_rng(SEED + 20)
    timing["perpetuity_exact_per_1e5"] = cpu_best(lambda: sample_perpetuity(MU, NT, rr), 5) * 1e5 / NT
    timing["bougerol_exact_per_1e5"] = cpu_best(lambda: sample_bougerol(1.0, NT, rr), 5) * 1e5 / NT
    timing["maximum_exact_per_1e5"] = cpu_best(lambda: sample_bm_max(1.0, NT, rr), 5) * 1e5 / NT
    timing["passage_exact_per_1e5"] = cpu_best(lambda: sample_ig_msh(1.0, 1.0, NT, rr), 5) * 1e5 / NT
    timing["perpetuity_euler2^-10_per_1e5"] = cpu_best(lambda: euler_sums(6.0, -MU, NE, SEED + 21), 3) * 1e5 / NE
    timing["bougerol_euler2^-10_per_1e5"] = cpu_best(lambda: euler_sums(1.0, 0.0, NE, SEED + 21), 3) * 1e5 / NE
    timing["maximum_euler2^-10_per_1e5"] = cpu_best(lambda: euler_max(1.0, NE, SEED + 21), 3) * 1e5 / NE
    timing["passage_euler2^-10_per_1e5"] = cpu_best(
        lambda: euler_passage_levels(np.random.default_rng(SEED + 22), NEP, 1.0, 1.0, 24.0, levels=(10,), jfine=10), 3) * 1e5 / NEP
    for name in ("perpetuity", "bougerol", "maximum", "passage"):
        timing[name + "_speedup"] = timing[name + "_euler2^-10_per_1e5"] / timing[name + "_exact_per_1e5"]
    say("timing_cpu_seconds_per_1e5_draws", **{k: float(v) for k, v in timing.items()})
    say("total_seconds", seconds=time.time() - t0)

    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "yor_results.json"), "w") as fh:
        json.dump(RES, fh, indent=1, default=float)


if __name__ == "__main__":
    main()
