"""Posterior of the initial vorticity of the two dimensional Navier Stokes equations (Chapter 12).

Unknown: omega_0 on the torus (2 pi periodic), a Fourier series with |k|_inf <= K and a Gaussian prior,
E|c_k|^2 = TAU2 (1 + |k|^2)^(-(1 + ALPHA)).  Data: omega(T) at an NS x NS grid of sensors plus N(0, DELTA^2) noise.
Forward map: vorticity equation, dealiased pseudospectral method on an N x N grid, RK4 (jax, float64).
Truth: five Gaussian vortices projected on the prior's mode set; the data are computed on a 64 x 64 grid with half the
time step, so the posterior (32 x 32 grid) is not computed with the discretization that made the data.
Sampler: Hamiltonian Monte Carlo, four chains started from independent prior draws, mass matrix equal to the Gauss Newton
(Laplace) Hessian at the maximum a posteriori estimate, step size by dual averaging in the warmup only.
Run: python3 ns2d_posterior.py          (about 20 minutes with three processes; the cache of intermediate results is in the system temporary folder unless --cache is given)
Output: ../figures/ns2d_posterior.pdf and the numbers quoted in the text, printed as lines starting with RESULT.
Options: --quick (short chains, for testing), --plot-only (reuse the cache), --cache DIR, --checks (gradient check and a test of the sampler on the linear problem)."""
import os
os.environ.setdefault("XLA_FLAGS", "--xla_cpu_multi_thread_eigen=false --xla_cpu_parallel_codegen_split_count=1")
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "VECLIB_MAXIMUM_THREADS"):
    os.environ.setdefault(_v, "1")
import sys
import time
import argparse
import functools
import tempfile
import numpy as np
from scipy.special import j1, ndtri
import jax
import jax.numpy as jnp
jax.config.update("jax_enable_x64", True)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "figures")

# configuration
N, K = 32, 6                         # model grid; prior mode set |k|_inf <= K, so D = (2K+1)^2 - 1 = 168 real unknowns
NU, T, DT = 0.01, 3.0, 0.025         # viscosity, observation time, time step of the model
NS = 16                              # sensors on a regular NS x NS grid (every second point of the model grid)
ALPHA, TAU2 = 1.0, 1.0               # prior variance of c_k: TAU2 (1 + |k|^2)^(-(1 + ALPHA))
DELTA = 0.25                         # noise standard deviation at one sensor
NF, DTF = 64, 0.0125                 # grid and time step used to generate the data
R_DISC = 0.8                         # radius of the discs on which circulations are computed
A_WIDTH = 0.5                        # vortices of the truth: A exp(-r^2 / A_WIDTH)
VORT = [(1.6, 3.4, 6.0), (2.9, 3.4, -2.5), (5.0, 1.5, 4.0), (5.2, 4.9, -4.0), (2.2, 0.8, 3.0)]   # (x, y, A)
SEED_NOISE, SEED_START, SEED_HMC, SEED_LM = 2026, 7, 11, 1
DELTAS = [0.0625, 0.125, 0.25, 0.5, 1.0]   # noise levels of the contraction experiment (HMC for the middle three)
N_CHAINS, N_WARM, N_SAMP = 4, 400, 1000
N_WARM_SWEEP, N_SAMP_SWEEP = 300, 600     # chains of the contraction experiment (noise levels other than DELTA)


# forward model
def make_solver(n, nu, t_end, dt, nonlin=1.0):
    """Dealiased pseudospectral solver (rfft2 layout, RK4) for omega_t + nonlin u.grad omega = nu Laplace omega; psi_hat = omega_hat / |k|^2.
    nonlin = 0 gives the heat equation, used only in the checks."""
    nsteps = int(round(t_end / dt))
    kx = np.fft.fftfreq(n, 1.0 / n)[:, None] * np.ones((1, n // 2 + 1))
    ky = np.fft.rfftfreq(n, 1.0 / n)[None, :] * np.ones((n, 1))
    k2 = kx ** 2 + ky ** 2
    k2i = np.where(k2 == 0, 0.0, 1.0 / np.where(k2 == 0, 1.0, k2))
    da = ((np.abs(kx) < n / 3) & (np.abs(ky) < n / 3)).astype(float)
    KX, KY, K2, K2I, DA = map(jnp.asarray, (kx, ky, k2, k2i, da))

    def rhs(wh):
        psi = wh * K2I
        u = jnp.fft.irfft2(1j * KY * psi, s=(n, n)); v = jnp.fft.irfft2(-1j * KX * psi, s=(n, n))
        wx = jnp.fft.irfft2(1j * KX * wh, s=(n, n)); wy = jnp.fft.irfft2(1j * KY * wh, s=(n, n))
        return -nonlin * jnp.fft.rfft2(u * wx + v * wy) * DA - nu * K2 * wh

    def step(wh, _):
        k1 = rhs(wh); k2_ = rhs(wh + 0.5 * dt * k1); k3 = rhs(wh + 0.5 * dt * k2_); k4 = rhs(wh + dt * k3)
        return wh + dt / 6.0 * (k1 + 2 * k2_ + 2 * k3 + k4), None

    def solve(wh0):
        return jax.lax.scan(step, wh0, None, length=nsteps)[0]
    return solve


class Problem:
    """Unknowns: theta = (Re c_k, Im c_k) for k in a half plane (ky > 0, or ky = 0 and kx > 0), |k|_inf <= K, omega_0 = sum 2 Re(c_k e^{ik.x}).
    Prior: Re c_k, Im c_k independent N(0, lambda_k / 2), lambda_k = TAU2 (1 + |k|^2)^(-(1 + ALPHA)); z = theta / s are the whitened coordinates."""

    def __init__(self, delta=DELTA, n=N, k=K, nu=NU, t_end=T, dt=DT, ns=NS, alpha=ALPHA, tau2=TAU2, radius=R_DISC, nonlin=1.0):
        self.n, self.K, self.nu, self.T, self.dt, self.ns, self.delta, self.R = n, k, nu, t_end, dt, ns, delta, radius
        ks = [(kx, ky) for ky in range(0, k + 1) for kx in range(-k, k + 1) if (ky > 0 or kx > 0)]
        self.ks = np.array(ks); self.nH = len(ks); self.D = 2 * self.nH
        self.k2 = (self.ks[:, 0] ** 2 + self.ks[:, 1] ** 2).astype(float)
        self.kn = np.sqrt(self.k2)
        self.lam = tau2 * (1.0 + self.k2) ** (-(1.0 + alpha))
        self.s = np.sqrt(np.concatenate([self.lam, self.lam]) / 2.0)
        self.axis = np.where(self.ks[:, 1] == 0)[0]
        self.solve = make_solver(n, nu, t_end, dt, nonlin)
        self.sensor = np.arange(0, n, n // ns)
        self.lin = self.linear_functionals()

    def hat0(self, theta, n=None):
        n = n or self.n
        c = theta[: self.nH] + 1j * theta[self.nH:]
        wh = jnp.zeros((n, n // 2 + 1), dtype=complex)
        wh = wh.at[np.mod(self.ks[:, 0], n), self.ks[:, 1]].set(n ** 2 * c)
        return wh.at[np.mod(-self.ks[self.axis, 0], n), 0].set(n ** 2 * jnp.conj(c[self.axis]))

    def G(self, theta):
        """Noise free data: omega(T) at the sensors."""
        w = jnp.fft.irfft2(self.solve(self.hat0(theta)), s=(self.n, self.n))
        return w[self.sensor][:, self.sensor].ravel()

    def field0(self, theta, n=64):
        return jnp.fft.irfft2(self.hat0(theta, n), s=(n, n))

    def linear_functionals(self):
        """Circulation on the disc of radius R around each vortex and the point value at its center: both linear in theta."""
        kx, ky = self.ks[:, 0], self.ks[:, 1]
        out = {}
        for j, (cx, cy, _) in enumerate(VORT):
            ph = np.exp(1j * (kx * cx + ky * cy))
            b = ph * 2 * np.pi * self.R * j1(self.R * self.kn) / self.kn      # integral of e^{ik.x} over the disc
            out[f"circ{j + 1}"] = 2 * np.concatenate([b.real, -b.imag])
            out[f"peak{j + 1}"] = 2 * np.concatenate([ph.real, -ph.imag])
        return out

    def energy0(self, theta):
        """E = (1/2) int |u|^2 dx = (2 pi)^2 sum over the half plane of |c_k|^2 / |k|^2."""
        c2 = theta[: self.nH] ** 2 + theta[self.nH:] ** 2
        return (2 * np.pi) ** 2 * jnp.sum(c2 / self.k2)

    def energyT(self, theta):
        wh = self.solve(self.hat0(theta)) / self.n ** 2
        kx = np.fft.fftfreq(self.n, 1.0 / self.n)[:, None] * np.ones((1, self.n // 2 + 1))
        ky = np.fft.rfftfreq(self.n, 1.0 / self.n)[None, :] * np.ones((self.n, 1))
        k2 = kx ** 2 + ky ** 2; wgt = np.where(ky > 0, 2.0, 1.0) / np.where(k2 == 0, 1.0, k2) * (k2 > 0)
        return 0.5 * (2 * np.pi) ** 2 * jnp.sum(wgt * jnp.abs(wh) ** 2)


def truth_theta(p, nt=256, vort=None):
    """Fourier coefficients of the Gaussian vortices on the mode set (zero mean, as the mean of omega is not an unknown)."""
    x = np.arange(nt) * 2 * np.pi / nt; X, Y = np.meshgrid(x, x, indexing="ij")
    w = np.zeros((nt, nt))
    for cx, cy, a in (VORT if vort is None else vort):
        w += a * np.exp(-(np.angle(np.exp(1j * (X - cx))) ** 2 + np.angle(np.exp(1j * (Y - cy))) ** 2) / A_WIDTH)
    c = (np.fft.fft2(w) / nt ** 2)[np.mod(p.ks[:, 0], nt), p.ks[:, 1]]
    return np.concatenate([c.real, c.imag])


def fine_solution(p, theta):
    """omega(T) on the fine model (NF x NF grid, time step DTF) for the initial condition theta."""
    solve = make_solver(NF, p.nu, p.T, DTF)
    wh = jnp.zeros((NF, NF // 2 + 1), dtype=complex)
    c = theta[: p.nH] + 1j * theta[p.nH:]
    wh = wh.at[np.mod(p.ks[:, 0], NF), p.ks[:, 1]].set(NF ** 2 * c)
    wh = wh.at[np.mod(-p.ks[p.axis, 0], NF), 0].set(NF ** 2 * jnp.conj(c[p.axis]))
    return np.asarray(jnp.fft.irfft2(solve(wh), s=(NF, NF)))


def fine_data(p, theta):
    """Noise free data from the fine model: the fine solution at the sensors."""
    r = NF // p.ns
    return fine_solution(p, theta)[::r, ::r].ravel()


def make_data(delta):
    """Truth, noise free data and data at noise level delta (the same standard normal noise for every delta)."""
    p = Problem(delta=delta)
    th = truth_theta(p)
    yclean = fine_data(p, th)
    eps = np.random.default_rng(SEED_NOISE).standard_normal(yclean.shape)
    return p, th, yclean, yclean + delta * eps


# posterior, maximum a posteriori estimate, Laplace approximation
def objectives(p, y):
    s = jnp.asarray(p.s); yj = jnp.asarray(y); d2 = p.delta ** 2
    def U(z):                                  # minus log posterior in the whitened coordinates z
        r = yj - p.G(s * z)
        return 0.5 * jnp.sum(z ** 2) + 0.5 * jnp.sum(r ** 2) / d2
    return U, jax.jit(jax.value_and_grad(U)), jax.jit(jax.jacfwd(lambda z: p.G(s * z)))


def lm_map(p, Ug, Jfun, z0, iters=25, gtol=1e-2):
    """Levenberg Marquardt for the minimizer of U. Returns z, U(z), Gauss Newton Hessian I + J'J/delta^2 at z, iterations."""
    z = np.asarray(z0, float).copy()
    Uz, gz = Ug(jnp.asarray(z)); Uz = float(Uz); gz = np.asarray(gz)
    mu, it = 1.0, 0
    for it in range(iters):
        if np.linalg.norm(gz) < gtol:
            break
        J = np.asarray(Jfun(jnp.asarray(z)))
        H = np.eye(p.D) + J.T @ J / p.delta ** 2
        while mu < 1e12:
            step = np.linalg.solve(H + mu * np.eye(p.D), -gz)
            Un, gn = Ug(jnp.asarray(z + step)); Un = float(Un)
            if Un < Uz:
                z = z + step; gz = np.asarray(gn); Uz = Un; mu = max(mu / 5.0, 1e-9); break
            mu *= 5.0
        if mu >= 1e12:
            break
    J = np.asarray(Jfun(jnp.asarray(z)))
    return z, Uz, np.eye(p.D) + J.T @ J / p.delta ** 2, it


# Hamiltonian Monte Carlo (chains advance together, one batched gradient per leapfrog step)
def build_hmc(p, y, zstar, H):
    s = jnp.asarray(p.s); yj = jnp.asarray(y); d2 = p.delta ** 2
    Lc = np.linalg.cholesky(H)
    A = np.linalg.inv(Lc).T                    # z = zstar + A u; under the Laplace approximation u ~ N(0, I)
    Aj, zs = jnp.asarray(A), jnp.asarray(zstar)

    def U(u):
        z = zs + Aj @ u
        r = yj - p.G(s * z)
        return 0.5 * jnp.sum(z ** 2) + 0.5 * jnp.sum(r ** 2) / d2
    vg = jax.jit(jax.vmap(jax.value_and_grad(U)))

    @jax.jit
    def trajectory(u, mom, eps, nsteps):
        U0, g0 = vg(u)
        m1 = mom - 0.5 * eps * g0

        def body(i, st):
            uu, mm, _, _ = st
            uu = uu + eps * mm
            Uu, gg = vg(uu)
            return uu, mm - eps * gg, Uu, gg
        uL, mL, UL, gL = jax.lax.fori_loop(0, nsteps, body, (u, m1, U0, g0))
        mL = mL + 0.5 * eps * gL
        return uL, UL, U0 + 0.5 * jnp.sum(mom ** 2, axis=1), UL + 0.5 * jnp.sum(mL ** 2, axis=1)
    return dict(A=A, Lc=Lc, vg=vg, traj=trajectory)


def run_hmc(hm, zstar, z0s, n_warm, n_samp, seed, lam=1.5, target=0.75, max_steps=100):
    """Warmup: step size by dual averaging (Hoffman and Gelman) to the mean acceptance of the chains; then n_samp draws with the final step size.
    The trajectory has a random number of steps, round(lam * U(0.5, 1.5) / eps), the same for all chains."""
    nc, D = z0s.shape
    rng = np.random.default_rng(seed)
    u = jnp.asarray((hm["Lc"].T @ (z0s - zstar).T).T)
    def accept_one(e):                         # mean acceptance of a one step trajectory with step size e
        _, _, H0_, H1_ = hm["traj"](u, jnp.asarray(rng.standard_normal((nc, D))), e, 1)
        return float(np.nanmean(np.minimum(1.0, np.exp(np.minimum(np.asarray(H0_ - H1_), 0.0)))))
    eps = 0.1                                  # initial step size as in Hoffman and Gelman: double or halve until the acceptance crosses one half
    sgn = 1.0 if accept_one(eps) > 0.5 else -1.0
    for _ in range(30):
        e2 = eps * 2.0 ** sgn
        a2 = accept_one(e2)
        if (sgn > 0 and a2 < 0.5) or (sgn < 0 and a2 > 0.5) or not (1e-6 < e2 < 2.0):
            break
        eps = e2
    mu_da, hbar, leps_bar, t0_da, gamma, kappa = np.log(10 * eps), 0.0, 0.0, 10, 0.05, 0.75
    out_z = np.zeros((nc, n_samp, D)); out_U = np.zeros((nc, n_samp)); acc = np.zeros(n_warm + n_samp); eps_hist = np.zeros(n_warm + n_samp)
    grads, t_start = 0, time.time()
    for it in range(n_warm + n_samp):
        mom = jnp.asarray(rng.standard_normal((nc, D)))
        nsteps = int(np.clip(round(lam * rng.uniform(0.5, 1.5) / eps), 1, max_steps))
        uL, UL, H0, H1 = hm["traj"](u, mom, eps, nsteps)
        grads += nsteps + 1
        dH = np.asarray(H0 - H1)
        a = np.where(np.isfinite(dH), np.minimum(1.0, np.exp(np.minimum(dH, 0.0))), 0.0)
        ok = rng.uniform(size=nc) < a
        Uold = np.asarray(H0) - 0.5 * np.sum(np.asarray(mom) ** 2, axis=1)
        u = jnp.where(jnp.asarray(ok)[:, None], uL, u)
        Ucur = np.where(ok, np.asarray(UL), Uold)
        acc[it] = a.mean(); eps_hist[it] = eps
        if it < n_warm:
            m = it + 1
            hbar = (1 - 1 / (m + t0_da)) * hbar + (target - a.mean()) / (m + t0_da)
            leps = mu_da - np.sqrt(m) / gamma * hbar
            w = m ** (-kappa); leps_bar = w * leps + (1 - w) * leps_bar
            eps = float(np.exp(leps_bar)) if it == n_warm - 1 else float(np.exp(leps))
        else:
            out_z[:, it - n_warm] = zstar + (hm["A"] @ np.asarray(u).T).T
            out_U[:, it - n_warm] = Ucur
        if it % 100 == 0 or it == n_warm + n_samp - 1:
            print(f"  hmc it {it:5d} eps {eps_hist[it]:.3f} steps {nsteps:3d} acc {acc[max(0, it - 99):it + 1].mean():.2f} U {np.round(Ucur, 1)} grads {grads} t {time.time() - t_start:.0f}s", flush=True)
    return dict(z=out_z, U=out_U, acc=acc, eps=eps_hist, eps_final=eps, grads=grads, seconds=time.time() - t_start, Uburn=None)


# convergence diagnostics (split R-hat, effective sample size; Vehtari et al. 2021)
def _split(x):
    n = x.shape[1] // 2
    return np.concatenate([x[:, :n], x[:, n:2 * n]], axis=0)


def _rhat_ess(x):
    xs = _split(np.asarray(x, float)); m, n = xs.shape
    W = xs.var(axis=1, ddof=1).mean(); B = n * xs.mean(axis=1).var(ddof=1)
    vp = (n - 1) / n * W + B / n
    xc = xs - xs.mean(axis=1, keepdims=True)
    f = np.fft.rfft(xc, n=2 * n, axis=1)
    ac = np.fft.irfft(f * np.conj(f), axis=1)[:, :n] / n * n / (n - 1)
    rho = 1.0 - (W - ac.mean(axis=0)) / vp; rho[0] = 1.0
    pairs = rho[: 2 * (n // 2)].reshape(-1, 2).sum(axis=1)
    neg = np.where(pairs < 0)[0]
    if neg.size:
        pairs = pairs[: neg[0]]
    pairs = np.minimum.accumulate(pairs) if pairs.size else pairs
    tau = max(-1.0 + 2.0 * pairs.sum(), 1.0 / np.log10(m * n)) if pairs.size else 1.0
    return np.sqrt(vp / W), m * n / tau


def _rank_normal(x):
    r = np.argsort(np.argsort(x.ravel())).reshape(x.shape) + 1.0
    return ndtri((r - 0.375) / (x.size + 0.25))


def diagnostics(x):
    """x: (chains, draws), one scalar. Rank normalized split R-hat (the larger of bulk and folded), bulk effective sample size."""
    r1, e1 = _rhat_ess(_rank_normal(np.asarray(x, float)))
    r2, _ = _rhat_ess(_rank_normal(np.abs(x - np.median(x))))
    return max(r1, r2), e1


def diag_all(X):
    d = np.array([diagnostics(X[:, :, j]) for j in range(X.shape[2])])
    return d[:, 0], d[:, 1]


# linear benchmark and shell summaries
def heat_benchmark(p, delta):
    """Posterior sd (theta units) if the nonlinear term is dropped (heat equation, same prior, sensors and noise): diagonal, exact."""
    kn = np.concatenate([p.kn, p.kn])
    snr = p.ns ** 2 * p.s ** 2 * 2.0 * np.exp(-2 * p.nu * kn ** 2 * p.T) / delta ** 2   # p.s^2 * 2 = lambda_k
    return p.s / np.sqrt(1.0 + snr)


def shell_ratio(p, sd_post, shells=range(1, 9)):
    kn = np.concatenate([p.kn, p.kn]); sh = np.rint(kn)
    return np.array([np.sqrt(np.sum(sd_post[sh == m] ** 2) / np.sum(p.s[sh == m] ** 2)) for m in shells])


def functional_draws(p, th):
    """Functionals of the initial field for draws th (rows): circulations, peaks, energy; returns a dict of arrays."""
    out = {name: th @ a for name, a in p.lin.items()}
    out["energy0"] = (2 * np.pi) ** 2 * np.sum((th[:, : p.nH] ** 2 + th[:, p.nH:] ** 2) / p.k2, axis=1)
    return out


def laplace_functional_sd(p, z, H):
    """Posterior sd of the functionals under the Laplace approximation (energy by the delta method)."""
    C = np.linalg.inv(H); S = p.s
    Cth = S[:, None] * C * S[None, :]
    out = {name: float(np.sqrt(a @ Cth @ a)) for name, a in p.lin.items()}
    q = (2 * np.pi) ** 2 / np.concatenate([p.k2, p.k2]); g = 2 * q * (S * z)
    out["energy0"] = float(np.sqrt(g @ Cth @ g))
    return out, np.sqrt(np.diag(Cth))


# tasks run in separate processes
def task_chains(delta, n_warm, n_samp, cache, tag):
    """MAP and Laplace approximation from one prior draw, then HMC with four chains started from other prior draws."""
    p, th_true, yclean, y = make_data(delta)
    U, Ug, Jfun = objectives(p, y)
    t0 = time.time()
    z0 = np.random.default_rng(SEED_LM).standard_normal(p.D)
    zstar, Ustar, H, nit = lm_map(p, Ug, Jfun, z0)
    t_map = time.time() - t0
    print(f"[{tag}] MAP: U {Ustar:.4f} after {nit} iterations, {t_map:.0f}s", flush=True)
    hm = build_hmc(p, y, zstar, H)
    z0s = np.random.default_rng(SEED_START).standard_normal((N_CHAINS, p.D))
    res = run_hmc(hm, zstar, z0s, n_warm, n_samp, SEED_HMC)
    np.savez(os.path.join(cache, f"chains_{tag}.npz"), zstar=zstar, Ustar=Ustar, H=H, seconds_map=t_map, y=y, th_true=th_true, delta=delta, **res)
    return tag, res["seconds"]


def task_laplace(delta, cache, tag):
    p, th_true, yclean, y = make_data(delta)
    U, Ug, Jfun = objectives(p, y)
    z, Ustar, H, nit = lm_map(p, Ug, Jfun, np.zeros(p.D), iters=40)
    np.savez(os.path.join(cache, f"laplace_{tag}.npz"), zstar=z, Ustar=Ustar, H=H, delta=delta, nit=nit)
    return tag, Ustar


def task_multistart(seed, cache):
    p, th_true, yclean, y = make_data(DELTA)
    U, Ug, Jfun = objectives(p, y)
    z, Ustar, H, nit = lm_map(p, Ug, Jfun, np.random.default_rng(seed).standard_normal(p.D), iters=30)
    np.savez(os.path.join(cache, f"multistart_{seed}.npz"), zstar=z, Ustar=Ustar, nit=nit)
    return seed, Ustar


def task_importance(cache, tag, n_draws=2000, seed=5):
    """Importance weights of draws from the Laplace approximation: effective sample size fraction (1 means exactly Gaussian)."""
    d = np.load(os.path.join(cache, f"chains_{tag}.npz"))
    p, th_true, yclean, y = make_data(float(d["delta"]))
    U, Ug, Jfun = objectives(p, y)
    Uv = jax.jit(jax.vmap(U))
    H, zstar = d["H"], d["zstar"]
    Lc = np.linalg.cholesky(H); A = np.linalg.inv(Lc).T
    u = np.random.default_rng(seed).standard_normal((n_draws, p.D))
    z = zstar + u @ A.T
    logw = -np.concatenate([np.asarray(Uv(jnp.asarray(z[i:i + 250]))) for i in range(0, n_draws, 250)]) + 0.5 * np.sum(u ** 2, axis=1)
    w = np.exp(logw - logw.max())
    np.savez(os.path.join(cache, f"importance_{tag}.npz"), logw=logw, ess_fraction=float(w.sum() ** 2 / np.sum(w ** 2) / n_draws))
    return tag, float(w.sum() ** 2 / np.sum(w ** 2) / n_draws)


def task_energyT(cache, tag, n_use=1000):
    """Energy at the observation time for thinned posterior draws (needs one forward solve per draw)."""
    d = np.load(os.path.join(cache, f"chains_{tag}.npz"))
    p, th_true, yclean, y = make_data(float(d["delta"]))
    z = d["z"].reshape(-1, p.D); idx = np.linspace(0, z.shape[0] - 1, n_use).astype(int)
    f = jax.jit(jax.vmap(p.energyT))
    eT = np.concatenate([np.asarray(f(jnp.asarray(p.s * z[idx[i:i + 100]]))) for i in range(0, n_use, 100)])
    np.savez(os.path.join(cache, f"energyT_{tag}.npz"), energyT=eT, truth=float(p.energyT(jnp.asarray(th_true))))
    return tag, float(eT.std())


def task_fields(cache, tag, nplot=64):
    """Pointwise posterior mean and sd of omega_0 on an nplot x nplot grid (chunked over draws), truth, and two draws for the figure."""
    d = np.load(os.path.join(cache, f"chains_{tag}.npz"))
    p = Problem(delta=float(d["delta"]))
    z = d["z"]; th = (p.s * z.reshape(-1, p.D))
    f = jax.jit(jax.vmap(lambda t: p.field0(t, nplot)))
    s1 = np.zeros((nplot, nplot)); s2 = np.zeros((nplot, nplot))
    for i in range(0, th.shape[0], 250):
        w = np.asarray(f(jnp.asarray(th[i:i + 250]))); s1 += w.sum(axis=0); s2 += (w ** 2).sum(axis=0)
    m = s1 / th.shape[0]; sd = np.sqrt(np.maximum(s2 / th.shape[0] - m ** 2, 0.0))
    draws = np.stack([np.asarray(p.field0(jnp.asarray(p.s * z[c, -1]), nplot)) for c in range(z.shape[0])])
    truth = np.asarray(p.field0(jnp.asarray(d["th_true"]), nplot))
    np.savez(os.path.join(cache, f"fields_{tag}.npz"), mean=m, sd=sd, draws=draws, truth=truth, truthT=fine_solution(p, d["th_true"]), data=d["y"].reshape(p.ns, p.ns))
    return tag, float(sd.mean())


def disc_masks(R, nf=128):
    """Grid coordinates and the masks of the discs of radius R around the vortices of the truth."""
    x = np.arange(nf) * 2 * np.pi / nf; X, Y = np.meshgrid(x, x, indexing="ij")
    return X, Y, [(np.angle(np.exp(1j * (X - cx))) ** 2 + np.angle(np.exp(1j * (Y - cy))) ** 2 <= R ** 2) for cx, cy, _ in VORT]


def extrema(w, X, Y, masks):
    """w: (draws, nf, nf) -> (draws, vortices, 2) positions of the extremum of w in each disc (maximum for a positive vortex, minimum for a negative one),
    and the distance of that position from the center of the disc."""
    out = np.zeros((w.shape[0], len(VORT), 2)); dist = np.zeros((w.shape[0], len(VORT)))
    for j, (cx, cy, a) in enumerate(VORT):
        v = np.where(masks[j][None], np.sign(a) * w, -np.inf).reshape(w.shape[0], -1)
        k = v.argmax(axis=1); out[:, j, 0] = X.ravel()[k]; out[:, j, 1] = Y.ravel()[k]
        dist[:, j] = np.hypot(np.angle(np.exp(1j * (out[:, j, 0] - cx))), np.angle(np.exp(1j * (out[:, j, 1] - cy))))
    return out, dist


def task_positions(cache, tag, n_use=1000, nf=128):
    """Position of the extremum of omega_0 in the disc of radius R around each vortex, for thinned draws."""
    d = np.load(os.path.join(cache, f"chains_{tag}.npz"))
    p = Problem(delta=float(d["delta"]))
    z = d["z"].reshape(-1, p.D); idx = np.linspace(0, z.shape[0] - 1, n_use).astype(int)
    X, Y, masks = disc_masks(p.R, nf)
    f = jax.jit(jax.vmap(lambda t: p.field0(t, nf)))
    res = [extrema(np.asarray(f(jnp.asarray(p.s * z[idx[i:i + 100]]))), X, Y, masks) for i in range(0, n_use, 100)]
    pos = np.concatenate([r[0] for r in res]); dist = np.concatenate([r[1] for r in res])
    pt, _ = extrema(np.asarray(f(jnp.asarray(d["th_true"])[None])), X, Y, masks)
    np.savez(os.path.join(cache, f"positions_{tag}.npz"), pos=pos, dist=dist, pos_truth=pt[0])
    return tag, float(np.std(pos))


def prior_positions(p, th_true, n_draws=2000, nf=128, seed=6):
    """The same position error under the prior: rms distance between the extremum of omega_0 in each disc for prior draws and the extremum of the truth."""
    X, Y, masks = disc_masks(p.R, nf)
    f = jax.jit(jax.vmap(lambda t: p.field0(t, nf)))
    th = p.s * np.random.default_rng(seed).standard_normal((n_draws, p.D))
    pos = np.concatenate([extrema(np.asarray(f(jnp.asarray(th[i:i + 100]))), X, Y, masks)[0] for i in range(0, n_draws, 100)])
    pt = extrema(np.asarray(f(jnp.asarray(th_true)[None])), X, Y, masks)[0][0]
    dx = np.angle(np.exp(1j * (pos[:, :, 0] - pt[:, 0]))); dy = np.angle(np.exp(1j * (pos[:, :, 1] - pt[:, 1])))
    return np.sqrt(np.mean(dx ** 2 + dy ** 2, axis=0))


@functools.lru_cache(maxsize=None)
def vortex_pieces():
    """Each vortex of the truth advected separately (on the fine model: NF x NF grid, time step DTF) by the velocity of the whole field.  The vorticity equation is linear in omega
    for a given velocity, so the five pieces add up to omega(T); they show where each vortex has gone.  Returns the pieces and the whole field at t = 0 and at t = T."""
    p = Problem(); n = NF
    th = [truth_theta(p)] + [truth_theta(p, vort=[v]) for v in VORT]
    kx = np.fft.fftfreq(n, 1.0 / n)[:, None] * np.ones((1, n // 2 + 1)); ky = np.fft.rfftfreq(n, 1.0 / n)[None, :] * np.ones((n, 1))
    k2 = kx ** 2 + ky ** 2; k2i = np.where(k2 == 0, 0.0, 1.0 / np.where(k2 == 0, 1.0, k2)); da = ((np.abs(kx) < n / 3) & (np.abs(ky) < n / 3)).astype(float)
    KX, KY, K2, K2I, DA = map(jnp.asarray, (kx, ky, k2, k2i, da))

    def hat(theta):
        c = theta[: p.nH] + 1j * theta[p.nH:]
        wh = jnp.zeros((n, n // 2 + 1), dtype=complex)
        wh = wh.at[np.mod(p.ks[:, 0], n), p.ks[:, 1]].set(n ** 2 * c)
        return wh.at[np.mod(-p.ks[p.axis, 0], n), 0].set(n ** 2 * jnp.conj(c[p.axis]))

    def rhs(S):                                # S[0]: the whole field; S[1:]: the pieces, advected by the velocity of S[0]
        psi = S[0] * K2I
        u = jnp.fft.irfft2(1j * KY * psi, s=(n, n)); v = jnp.fft.irfft2(-1j * KX * psi, s=(n, n))
        def one(w):
            wx = jnp.fft.irfft2(1j * KX * w, s=(n, n)); wy = jnp.fft.irfft2(1j * KY * w, s=(n, n))
            return -jnp.fft.rfft2(u * wx + v * wy) * DA - p.nu * K2 * w
        return jax.vmap(one)(S)

    def step(S, _):
        k1 = rhs(S); k2_ = rhs(S + 0.5 * DTF * k1); k3 = rhs(S + 0.5 * DTF * k2_); k4 = rhs(S + DTF * k3)
        return S + DTF / 6.0 * (k1 + 2 * k2_ + 2 * k3 + k4), None

    S0 = jnp.stack([hat(t) for t in th])
    ST = jax.lax.scan(step, S0, None, length=int(round(p.T / DTF)))[0]
    back = jax.vmap(lambda h: jnp.fft.irfft2(h, s=(n, n)))
    return np.asarray(back(S0)), np.asarray(back(ST))


def elongation(c, X, Y):
    """Ratio of the principal axes of the second moments of |c| over the cells where |c| exceeds a fifth of its maximum (coordinates taken around the circular mean)."""
    w = np.abs(c); w = np.where(w > 0.2 * w.max(), w, 0.0)
    cx = np.angle((w * np.exp(1j * X)).sum()); cy = np.angle((w * np.exp(1j * Y)).sum())
    dx = np.angle(np.exp(1j * (X - cx))); dy = np.angle(np.exp(1j * (Y - cy)))
    W = w.sum(); mx = (w * dx).sum() / W; my = (w * dy).sum() / W
    C = np.array([[(w * (dx - mx) ** 2).sum(), (w * (dx - mx) * (dy - my)).sum()], [(w * (dx - mx) * (dy - my)).sum(), (w * (dy - my) ** 2).sum()]]) / W
    ev = np.linalg.eigvalsh(C)
    return float(np.sqrt(ev[1] / ev[0]))


def checks():
    """Two tests that are not part of the default run (python3 ns2d_posterior.py --checks, about ten minutes on one core).
    (a) The jax gradient of minus log posterior against central differences.
    (b) The sampler on the linear problem (nonlinear term dropped: heat equation, same prior, sensors and noise), whose posterior is exactly Gaussian
        with the diagonal covariance of heat_benchmark; HMC from prior draws must reproduce it."""
    p, th_true, yclean, y = make_data(DELTA)
    U, Ug, Jfun = objectives(p, y)
    rng = np.random.default_rng(99); z = rng.standard_normal(p.D) * 0.5; v = rng.standard_normal(p.D); v /= np.linalg.norm(v)
    g = np.asarray(Ug(jnp.asarray(z))[1]); h = 1e-5
    fd = (float(U(jnp.asarray(z + h * v))) - float(U(jnp.asarray(z - h * v)))) / (2 * h)
    print(f"RESULT check gradient: directional derivative by jax {g @ v:.6f}, by central differences {fd:.6f}, relative difference {abs(g @ v - fd) / abs(fd):.1e}")
    pl = Problem(delta=DELTA, nonlin=0.0)
    yl = np.asarray(pl.G(jnp.asarray(th_true))) + DELTA * np.random.default_rng(SEED_NOISE).standard_normal(p.ns ** 2)
    Ul, Ugl, Jl = objectives(pl, yl)
    J = np.asarray(Jl(jnp.zeros(pl.D)))                     # the problem is linear: G(z) = J z
    H = np.eye(pl.D) + J.T @ J / DELTA ** 2                 # exact posterior precision in the whitened coordinates
    zs = np.linalg.solve(H, J.T @ yl / DELTA ** 2)          # exact posterior mean
    sd_exact = heat_benchmark(pl, DELTA)
    sd_gn = pl.s * np.sqrt(np.diag(np.linalg.inv(H)))
    print(f"RESULT check linear problem: posterior sd from the jax Jacobian against the closed form of heat_benchmark: largest relative difference {np.max(np.abs(sd_gn / sd_exact - 1)):.1e}; "
          f"largest |off diagonal| of the precision {np.abs(H - np.diag(np.diag(H))).max():.1e}; gradient of U at the exact mean {np.linalg.norm(np.asarray(Ugl(jnp.asarray(zs))[1])):.1e}")
    hm = build_hmc(pl, yl, zs, H)
    z0s = np.random.default_rng(SEED_START).standard_normal((N_CHAINS, pl.D))
    res = run_hmc(hm, zs, z0s, 300, 600, SEED_HMC)
    th = pl.s * res["z"].reshape(-1, pl.D); sdh = th.std(axis=0)
    rh, ess = diag_all(res["z"])
    zmean = (th.mean(axis=0) - pl.s * zs) / sd_exact
    rat = sdh / sd_exact
    print(f"RESULT check linear problem, HMC against the exact Gaussian posterior: final step size {float(res['eps_final']):.2f}, mean acceptance {res['acc'][-600:].mean():.2f}, max R-hat {rh.max():.3f}, min ESS {ess.min():.0f}; "
          f"sd ratio HMC / exact: min {rat.min():.3f}, median {np.median(rat):.3f}, max {rat.max():.3f}; rms of (HMC mean - exact mean) / exact sd {np.sqrt(np.mean(zmean ** 2)):.3f}, "
          f"expected rms from the effective sample size {np.sqrt(np.mean(1.0 / ess)):.3f}")


def worker(job):
    name, args = job
    return globals()[name](*args)


def run_all(cache, quick):
    """Three worker processes, jobs in decreasing cost. Laplace approximations at the other noise levels come from the chain jobs."""
    from concurrent.futures import ProcessPoolExecutor
    import multiprocessing as mp
    nw, ns_, nw2, ns2 = (60, 60, 60, 60) if quick else (N_WARM, N_SAMP, N_WARM_SWEEP, N_SAMP_SWEEP)
    jobs1 = [("task_chains", (DELTA, nw, ns_, cache, "main")), ("task_chains", (DELTAS[1], nw2, ns2, cache, "lo")), ("task_chains", (DELTAS[3], nw2, ns2, cache, "hi")),
             ("task_laplace", (DELTAS[0], cache, "d0.0625")), ("task_laplace", (DELTAS[4], cache, "d1.0"))] + [("task_multistart", (sd, cache)) for sd in (101, 102, 103)]
    jobs2 = [("task_importance", (cache, "main")), ("task_energyT", (cache, "main")), ("task_fields", (cache, "main")), ("task_positions", (cache, "main"))]
    t0 = time.time()
    with ProcessPoolExecutor(max_workers=3, mp_context=mp.get_context("spawn")) as ex:
        futs = [ex.submit(worker, j) for j in jobs1]
        print("done:", futs[0].result(), f"{time.time() - t0:.0f}s elapsed", flush=True)      # the main chains; the jobs that need them follow
        futs += [ex.submit(worker, j) for j in jobs2]
        for f in futs[1:]:
            print("done:", f.result(), f"{time.time() - t0:.0f}s elapsed", flush=True)


# summary and figure
def derived_missing(cache):
    """Derived results that are computed from the main chains; computed here (in this process) if the files are missing."""
    for name, fn in (("importance_main", task_importance), ("energyT_main", task_energyT), ("fields_main", task_fields), ("positions_main", task_positions)):
        if not os.path.exists(os.path.join(cache, name + ".npz")):
            print("computing", name, fn(cache, "main"), flush=True)


def load(cache, tag):
    return dict(np.load(os.path.join(cache, tag + ".npz"), allow_pickle=True))


def summarize(cache):
    p, th_true, yclean, y = make_data(DELTA)
    zt = th_true / p.s
    ch = load(cache, "chains_main"); z = ch["z"]; nc, ns_, D = z.shape
    th = p.s * z.reshape(-1, D)
    print(f"RESULT model: grid {N}x{N}, dt {DT}, nu {NU}, T {T}, K {K} (D = {p.D}), sensors {NS}x{NS} = {NS ** 2}, delta {DELTA}, alpha {ALPHA}, tau2 {TAU2}")
    d = np.sqrt(np.mean((p.G(jnp.asarray(th_true)) - yclean) ** 2)); dmax = np.abs(np.asarray(p.G(jnp.asarray(th_true))) - yclean).max()
    print(f"RESULT discretization: 32 grid versus 64 grid at the truth: rms {d:.4f}, max {dmax:.4f}; rms of the signal {np.sqrt(np.mean(yclean ** 2)):.3f}; delta {DELTA}")
    w0 = np.asarray(p.field0(jnp.asarray(th_true), 64))
    print(f"RESULT truth: max |omega_0| {np.abs(w0).max():.3f}, rms {w0.std():.3f}, prior pointwise sd {np.sqrt(2 * p.lam.sum()):.3f}, truth standardized rms {np.sqrt(np.mean(zt ** 2)):.3f}")
    # maximum a posteriori
    ms = [load(cache, f"multistart_{s}") for s in (101, 102, 103)]
    zstar = ch["zstar"]
    print(f"RESULT map: U at MAP {float(ch['Ustar']):.4f}; U at truth {float(objectives(p, y)[1](jnp.asarray(zt))[0]):.2f}; multistart U {[round(float(m['Ustar']), 4) for m in ms]}, distance to the first MAP {[float(np.linalg.norm(m['zstar'] - zstar)) for m in ms]}")
    ev = np.linalg.eigvalsh(ch["H"])
    print(f"RESULT hessian: eigenvalues above 2: {(ev > 2).sum()}, above 10: {(ev > 10).sum()}, largest {ev.max():.0f}")
    # sampler diagnostics
    rh, ess = diag_all(z)
    Ur, Ue = diagnostics(ch["U"])
    print(f"RESULT negative log posterior over the draws: mean {ch['U'].mean():.2f}, sd {ch['U'].std():.2f}; a Gaussian posterior with the same maximum would give {float(ch['Ustar']) + D / 2:.2f} and {np.sqrt(D / 2):.2f}")
    print(f"RESULT hmc: chains {nc}, draws {ns_} each after {len(ch['acc']) - ns_} warmup, final step size {float(ch['eps_final']):.3f}, mean acceptance {ch['acc'][-ns_:].mean():.2f}, gradients per chain {int(ch['grads'])}, seconds {float(ch['seconds']):.0f}")
    print(f"RESULT hmc diagnostics over {D} coordinates: max R-hat {rh.max():.3f}, min bulk ESS {ess.min():.0f}, median bulk ESS {np.median(ess):.0f}; log posterior R-hat {Ur:.3f}, ESS {Ue:.0f}")
    fd = functional_draws(p, th)
    fdc = {k: v.reshape(nc, ns_) for k, v in fd.items()}
    frh = {k: diagnostics(v) for k, v in fdc.items()}
    print("RESULT functionals R-hat and ESS:", {k: (round(float(a), 3), int(b)) for k, (a, b) in frh.items()})
    # posterior versus prior and linear benchmark by shell
    sd_post = th.std(axis=0)
    lap_sd_f, lap_sd = laplace_functional_sd(p, zstar, ch["H"])
    lin = heat_benchmark(p, DELTA)
    r_h, r_l, r_b = shell_ratio(p, sd_post), shell_ratio(p, lap_sd), shell_ratio(p, lin)
    print("RESULT shell ratio posterior sd / prior sd, shells 1 to 8: HMC", np.round(r_h, 3), "Laplace", np.round(r_l, 3), "heat equation", np.round(r_b, 3))
    rc = sd_post / p.s
    print(f"RESULT coefficient sd ratios: below 0.5 for {int((rc < 0.5).sum())} of {D}, below 0.9 for {int((rc < 0.9).sum())}, above 0.95 for {int((rc > 0.95).sum())}; smallest {rc.min():.3f}, largest {rc.max():.3f}")
    zscore = (th_true - th.mean(axis=0)) / sd_post
    lo, hi = np.percentile(th, [5, 95], axis=0)
    print(f"RESULT coefficients: truth inside the central 90 percent interval for {int(np.sum((th_true >= lo) & (th_true <= hi)))} of {D}; rms z-score {np.sqrt(np.mean(zscore ** 2)):.2f}; "
          f"by shell, rms z for shells 1-3 {np.sqrt(np.mean(zscore[np.rint(np.concatenate([p.kn, p.kn])) <= 3] ** 2)):.2f}, shells 4-8 {np.sqrt(np.mean(zscore[np.rint(np.concatenate([p.kn, p.kn])) > 3] ** 2)):.2f}")
    # residuals at the posterior mean field
    Gm = np.mean([np.asarray(p.G(jnp.asarray(t))) for t in th[:: max(1, th.shape[0] // 200)]], axis=0)
    print(f"RESULT residual rms of the mean of G over draws {np.sqrt(np.mean((y - Gm) ** 2)):.3f} (delta {DELTA}); at the truth {np.sqrt(np.mean((y - np.asarray(p.G(jnp.asarray(th_true)))) ** 2)):.3f}")
    # functionals
    truth_f = {name: float(a @ th_true) for name, a in p.lin.items()}; truth_f["energy0"] = float(p.energy0(jnp.asarray(th_true)))
    prior_sd = {name: float(np.sqrt(a @ (p.s ** 2 * a))) for name, a in p.lin.items()}
    rng = np.random.default_rng(3); zp = rng.standard_normal((20000, D)); fp = functional_draws(p, p.s * zp)
    prior_sd["energy0"] = float(fp["energy0"].std()); prior_mean_E = float(fp["energy0"].mean())
    print(f"RESULT prior energy0 mean {prior_mean_E:.2f} sd {prior_sd['energy0']:.2f}")
    heat_sd = {name: float(np.sqrt(np.sum((a * lin) ** 2))) for name, a in p.lin.items()}
    print("RESULT functionals: name | truth | HMC mean | HMC sd | prior sd | ratio | Laplace sd | heat equation sd | z of truth | 90% interval covers")
    for name in list(p.lin) + ["energy0"]:
        v = fd[name]; l, h = np.percentile(v, [5, 95])
        print(f"RESULT  {name:8s} {truth_f[name]:9.3f} {v.mean():9.3f} {v.std():8.3f} {prior_sd[name]:8.3f} {v.std() / prior_sd[name]:7.3f} {lap_sd_f[name]:8.3f} {heat_sd.get(name, float('nan')):8.3f} {(truth_f[name] - v.mean()) / v.std():7.2f} {int(l <= truth_f[name] <= h)}")
    sk = {k: float(np.mean(((v - v.mean()) / v.std()) ** 3)) for k, v in fd.items()}
    ku = {k: float(np.mean(((v - v.mean()) / v.std()) ** 4) - 3) for k, v in fd.items()}
    print("RESULT skewness", {k: round(sk[k], 2) for k in ("energy0", "circ1", "circ2", "peak1", "peak2")}, "excess kurtosis", {k: round(ku[k], 2) for k in ("energy0", "circ1", "circ2", "peak1", "peak2")})
    eT = load(cache, "energyT_main")
    print(f"RESULT energy at T: truth {float(eT['truth']):.3f}, HMC mean {eT['energyT'].mean():.3f}, sd {eT['energyT'].std():.4f}")
    im = load(cache, "importance_main")
    print(f"RESULT importance weights of Laplace draws: effective sample size fraction {float(im['ess_fraction']):.3f}")
    # the posterior is not diagonal: correlations between coefficients (all zero for the prior and for the heat equation)
    cm = np.corrcoef(th.T); off = np.abs(cm[np.triu_indices(D, 1)])
    print(f"RESULT correlations: largest |corr| between two coefficients {off.max():.2f}; pairs with |corr| above 0.3: {int((off > 0.3).sum())}, above 0.5: {int((off > 0.5).sum())} of {off.size}; "
          f"mean over coefficients of the largest |corr| with another one {np.mean(np.abs(cm - np.eye(D)).max(axis=0)):.2f}")
    ps = load(cache, "positions_main")
    print("RESULT positions of the extremum of omega_0 in each disc: vortex | truth (x, y) | posterior mean (x, y) | sd x, sd y | rms distance to the truth | draws whose extremum lies on the disc edge")
    for j in range(len(VORT)):
        q = ps["pos"][:, j]; dx = np.angle(np.exp(1j * (q[:, 0] - ps["pos_truth"][j, 0]))); dy = np.angle(np.exp(1j * (q[:, 1] - ps["pos_truth"][j, 1])))
        print(f"RESULT  {j + 1} | ({ps['pos_truth'][j, 0]:.2f}, {ps['pos_truth'][j, 1]:.2f}) | ({ps['pos_truth'][j, 0] + dx.mean():.2f}, {ps['pos_truth'][j, 1] + dy.mean():.2f}) | {dx.std():.3f}, {dy.std():.3f} | {np.sqrt(np.mean(dx ** 2 + dy ** 2)):.3f} | {np.mean(ps['dist'][:, j] > p.R - 0.07):.3f}")
    ppr = prior_positions(p, th_true)
    print("RESULT position error under the prior (rms distance from the extremum of the truth over 2000 prior draws), vortices 1 to 5:", np.round(ppr, 3))
    # where each vortex of the truth has gone by time T
    w0p, wTp = vortex_pieces(); fl = load(cache, "fields_main")
    xg = np.arange(NF) * 2 * np.pi / NF; Xg, Yg = np.meshgrid(xg, xg, indexing="ij")
    print(f"RESULT vortex pieces add up to the truth: at t=0 max difference {np.abs(w0p[1:].sum(axis=0) - fl['truth']).max():.1e}, at t=T {np.abs(wTp[1:].sum(axis=0) - fl['truthT']).max():.1e} (the field itself has max {np.abs(fl['truthT']).max():.2f})")
    print("RESULT vortex pieces, each vortex advected separately by the velocity of the whole field: vortex | elongation at t=0 | at t=T | extremum at t=0 | at t=T | location of the extremum at t=T")
    for j, (cx, cy, a) in enumerate(VORT):
        c0, cT = w0p[1 + j], wTp[1 + j]; k = np.abs(cT).argmax()
        print(f"RESULT  {j + 1} | {elongation(c0, Xg, Yg):.2f} | {elongation(cT, Xg, Yg):.2f} | {(c0.max() if a > 0 else c0.min()):.2f} | {(cT.max() if a > 0 else cT.min()):.2f} | ({Xg.ravel()[k]:.2f}, {Yg.ravel()[k]:.2f})")
    # contraction with delta
    print("RESULT contraction: delta | sd energy0 (HMC, Laplace) | sd circ1 | sd circ2 | sd peak1 | min ESS | max R-hat  (data: same noise draw scaled)")
    for tag, dl in (("lo", DELTAS[1]), ("main", DELTAS[2]), ("hi", DELTAS[3])):
        c2 = load(cache, "chains_" + tag); zz = c2["z"]; pp = Problem(delta=dl); tt = pp.s * zz.reshape(-1, D)
        f2 = functional_draws(pp, tt); lsd, _ = laplace_functional_sd(pp, c2["zstar"], c2["H"]); r2, e2 = diag_all(zz)
        print(f"RESULT  {dl:6.4f} | {f2['energy0'].std():.3f} {lsd['energy0']:.3f} | {f2['circ1'].std():.3f} | {f2['circ2'].std():.3f} | {f2['peak1'].std():.3f} | {e2.min():.0f} | {r2.max():.3f} | acc {c2['acc'][-ns_:].mean():.2f} seconds {float(c2['seconds']):.0f}")
    sds = {}
    for tag, dl in (("lo", DELTAS[1]), ("main", DELTAS[2]), ("hi", DELTAS[3])):
        c2 = load(cache, "chains_" + tag); tt = Problem(delta=dl).s * c2["z"].reshape(-1, D); f2 = functional_draws(Problem(delta=dl), tt)
        sds[tag] = {k: f2[k].std() for k in ("energy0", "circ1", "circ2", "circ3", "circ4", "circ5", "peak1")}
        dg = [diagnostics(f2[k].reshape(c2["z"].shape[:2])) for k in sds[tag]]
        print(f"RESULT functionals in the contraction runs, delta {dl:6.4f}: max R-hat {max(a for a, _ in dg):.3f}, min bulk ESS {min(b for _, b in dg):.0f}, "
              f"so the relative Monte Carlo error of each sd is at most {1 / np.sqrt(2 * min(b for _, b in dg)):.3f}")
    print("RESULT slope of log sd against log delta between delta 0.125 and 0.5 (HMC):", {k: round(float(np.log(sds["hi"][k] / sds["lo"][k]) / np.log(4.0)), 2) for k in sds["lo"]})
    for dl, tagf in zip(DELTAS, ("laplace_d0.0625", "chains_lo", "chains_main", "chains_hi", "laplace_d1.0")):
        l2 = load(cache, tagf); pp = Problem(delta=dl); lsd, _ = laplace_functional_sd(pp, l2["zstar"], l2["H"])
        print(f"RESULT  Laplace delta {dl:6.4f}: sd energy0 {lsd['energy0']:.4f} circ1 {lsd['circ1']:.4f} circ2 {lsd['circ2']:.4f} circ3 {lsd['circ3']:.4f} circ4 {lsd['circ4']:.4f} circ5 {lsd['circ5']:.4f} peak1 {lsd['peak1']:.4f}; U at MAP {float(l2['Ustar']):.2f}")
    return dict(p=p, th_true=th_true, sd_post=sd_post, r_h=r_h, r_l=r_l, r_b=r_b)


def make_figure(cache, S):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "serif", "font.size": 8, "axes.linewidth": 0.6, "lines.linewidth": 1.0, "savefig.bbox": "tight", "pdf.fonttype": 42})
    f = load(cache, "fields_main"); p = S["p"]
    vm = float(np.abs(f["truth"]).max()); prior_sd = float(np.sqrt(2 * p.lam.sum()))
    print(f"RESULT figure: color scale +- {vm:.3f}; posterior sd map from {f['sd'].min():.3f} to {f['sd'].max():.3f}, mean {f['sd'].mean():.3f}; prior pointwise sd {prior_sd:.3f}")
    W_, H_ = 4.6, 3.55
    fig = plt.figure(figsize=(W_, H_))
    def axin(l, b, w, h):
        return fig.add_axes([l / W_, b / H_, w / W_, h / H_])
    ms, gx, left, rowy = 1.12, 0.10, 0.40, (0.82, 2.16)
    ext = [0, 2 * np.pi, 0, 2 * np.pi]
    ticks = [0, np.pi, 2 * np.pi]; tl = ["0", r"$\pi$", r"$2\pi$"]
    def style(ax, col, row, title):
        ax.set_title(title, fontsize=7.5, pad=2)
        ax.set_xticks(ticks); ax.set_xticklabels(tl if row == 0 else [])
        ax.set_yticks(ticks); ax.set_yticklabels(tl if col == 0 else [])
        ax.tick_params(labelsize=6.5, length=2, width=0.5, pad=1.5)
    for name, fld, col, row in [("truth", f["truth"], 0, 1), ("posterior mean", f["mean"], 1, 1), ("posterior draw 1", f["draws"][0], 0, 0), ("posterior draw 2", f["draws"][1], 1, 0)]:
        ax = axin(left + col * (ms + gx), rowy[row], ms, ms)
        im = ax.imshow(fld.T, origin="lower", cmap="RdBu_r", vmin=-vm, vmax=vm, extent=ext, interpolation="bicubic")
        style(ax, col, row, name)
        if name == "truth":
            th = np.linspace(0, 2 * np.pi, 100)
            for j, (cx, cy, _) in enumerate(VORT):
                ax.plot(cx + p.R * np.cos(th), cy + p.R * np.sin(th), color="0.25", lw=0.4)
                ax.text(cx + 0.95, cy + 0.55, str(j + 1), fontsize=6, ha="center", va="center", color="0.1")
    cax = axin(left, 0.40, 2 * ms + gx, 0.07)
    cb = fig.colorbar(im, cax=cax, orientation="horizontal")
    cb.set_ticks([-vm, 0, vm]); cb.set_ticklabels([f"\u2212{vm:.1f}", "0", f"{vm:.1f}"])
    cb.set_label("vorticity", fontsize=7, labelpad=1); cb.ax.tick_params(labelsize=6.5, length=2, width=0.5, pad=1.5)
    # posterior sd map with its own color bar
    ax = axin(left + 2 * (ms + gx) + 0.06, rowy[1], ms, ms)
    im2 = ax.imshow(f["sd"].T, origin="lower", cmap="viridis", vmin=0, vmax=prior_sd, extent=ext, interpolation="bicubic")
    style(ax, 1, 1, "posterior sd"); ax.set_yticklabels([])
    cax2 = axin(left + 2 * (ms + gx) + 0.06 + ms + 0.07, rowy[1], 0.07, ms)
    cb2 = fig.colorbar(im2, cax=cax2); cb2.set_ticks([0, 0.5, 1.0, 1.5]); cb2.ax.tick_params(labelsize=6.5, length=2, width=0.5, pad=1.5)
    cb2.set_label("sd (prior sd %.2f)" % prior_sd, fontsize=6.5, labelpad=2)
    # ratio of posterior to prior sd by wavenumber shell
    ax = axin(left + 2 * (ms + gx) + 0.50, rowy[0] + 0.12, ms - 0.28, ms - 0.12)
    sh = np.arange(1, 9)
    ax.plot(sh, S["r_h"], "o-", color="#1b4f9c", ms=3, lw=1.0, label="Navier Stokes")
    ax.plot(sh, S["r_b"], "--", color="#d1495b", lw=1.0, label="heat equation")
    ax.axhline(1.0, color="0.6", lw=0.5, ls=":")
    ax.set_ylim(0, 1.08); ax.set_xlim(0.5, 8.5); ax.set_xticks([1, 2, 4, 6, 8])
    ax.set_xlabel("wavenumber shell $|k|$", fontsize=7, labelpad=1); ax.set_title("sd ratio, posterior / prior", fontsize=7.5, pad=2)
    ax.tick_params(labelsize=6.5, length=2, width=0.5, pad=1.5); 
    ax.text(1.0, 0.95, "Navier\nStokes", color="#1b4f9c", fontsize=6.3, ha="left", va="top", linespacing=1.0)
    ax.text(8.3, 0.10, "heat\nequation", color="#d1495b", fontsize=6.3, ha="right", va="bottom", linespacing=1.0)
    fig.suptitle("Posterior of the initial vorticity", fontsize=8.5, y=0.995, va="bottom")
    return fig, plt


def make_figure_data(cache):
    """Short diagnostic: the truth at time 0 and at time T (fine model) and the data (T, sensors, noise)."""
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    plt.rcParams.update({"font.family": "serif", "font.size": 8, "axes.linewidth": 0.6, "lines.linewidth": 1.0, "savefig.bbox": "tight", "pdf.fonttype": 42})
    f = load(cache, "fields_main")
    vm = float(np.abs(f["truth"]).max())
    print(f"RESULT data figure: truth at 0 in [{f['truth'].min():.2f}, {f['truth'].max():.2f}]; truth at T in [{f['truthT'].min():.2f}, {f['truthT'].max():.2f}]; data in [{f['data'].min():.2f}, {f['data'].max():.2f}]")
    W_, H_ = 4.6, 1.75
    fig = plt.figure(figsize=(W_, H_))
    ms, gx, left = 1.14, 0.12, 0.40
    ticks = [0, np.pi, 2 * np.pi]; tl = ["0", r"$\pi$", r"$2\pi$"]
    for i, (name, fld, interp) in enumerate([("truth, $t=0$", f["truth"], "bicubic"), (f"truth, $t={T:g}$", f["truthT"], "bicubic"), (f"data, $t={T:g}$", f["data"], "nearest")]):
        ax = fig.add_axes([(left + i * (ms + gx)) / W_, 0.42 / H_, ms / W_, ms / H_])
        im = ax.imshow(fld.T, origin="lower", cmap="RdBu_r", vmin=-vm, vmax=vm, extent=[0, 2 * np.pi, 0, 2 * np.pi], interpolation=interp)
        ax.set_title(name, fontsize=7.5, pad=2)
        if i == 0:
            for j, (cx, cy, _) in enumerate(VORT):
                ax.text(cx + 0.95, cy + 0.55, str(j + 1), fontsize=6, ha="center", va="center", color="0.1")
        if i == 1:                             # where each vortex of the truth has gone: the extremum of the piece advected separately
            import matplotlib.patheffects as pe
            wTp = vortex_pieces()[1]; xg = np.arange(NF) * 2 * np.pi / NF; Xg, Yg = np.meshgrid(xg, xg, indexing="ij")
            for j in range(len(VORT)):
                k = np.abs(wTp[1 + j]).argmax()
                ax.text(Xg.ravel()[k], Yg.ravel()[k], str(j + 1), fontsize=6, ha="center", va="center", color="0.1", path_effects=[pe.withStroke(linewidth=1.3, foreground="white")])
        ax.set_xticks(ticks); ax.set_xticklabels(tl); ax.set_yticks(ticks); ax.set_yticklabels(tl if i == 0 else [])
        ax.tick_params(labelsize=6.5, length=2, width=0.5, pad=1.5)
    cax = fig.add_axes([(left + 3 * ms + 3 * gx - 0.02) / W_, 0.42 / H_, 0.07 / W_, ms / H_])
    cb = fig.colorbar(im, cax=cax); cb.set_ticks([-vm, 0, vm]); cb.set_ticklabels([f"\u2212{vm:.1f}", "0", f"{vm:.1f}"])
    cb.set_label("vorticity", fontsize=7, labelpad=1); cb.ax.tick_params(labelsize=6.5, length=2, width=0.5, pad=1.5)
    return fig, plt


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--quick", action="store_true"); ap.add_argument("--plot-only", action="store_true"); ap.add_argument("--cache", default=None)
    ap.add_argument("--checks", action="store_true", help="gradient check and linear test of the sampler, then exit")
    a = ap.parse_args()
    t_main = time.time()
    if a.checks:
        checks()
        return
    cache = a.cache or os.path.join(tempfile.gettempdir(), "ns2d_posterior_cache" + ("_quick" if a.quick else ""))
    os.makedirs(cache, exist_ok=True); os.makedirs(OUT, exist_ok=True)
    import scipy, matplotlib
    print(f"RESULT versions: python {sys.version.split()[0]}, numpy {np.__version__}, scipy {scipy.__version__}, jax {jax.__version__}, matplotlib {matplotlib.__version__}")
    if not a.plot_only:
        run_all(cache, a.quick)
        print(f"RESULT run time of the sampling jobs, three processes: {time.time() - t_main:.0f} s", flush=True)
    derived_missing(cache)
    S = summarize(cache)
    fig, plt = make_figure(cache, S)
    plt.savefig(os.path.join(OUT, "ns2d_posterior.pdf"), dpi=300); plt.close()
    fig, plt = make_figure_data(cache)
    plt.savefig(os.path.join(OUT, "ns2d_posterior_data.pdf"), dpi=300); plt.close()
    print("figures written to", os.path.abspath(OUT), f"; total {time.time() - t_main:.0f} s")


if __name__ == "__main__":
    main()
