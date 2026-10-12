"""Pseudo-spectral 2D Navier-Stokes (vorticity form) on the 2pi-torus, and the
Bayesian initial-condition problem of Konen-Nickl."""
import numpy as np

class NS2D:
    def __init__(self, n=32, nu=0.02, T=0.5, nsteps=100):
        self.n, self.nu, self.T, self.nsteps = n, nu, T, nsteps
        self.dt = T/nsteps
        k = np.fft.fftfreq(n, 1.0/n)
        self.KX, self.KY = np.meshgrid(k, k, indexing='ij')
        self.K2 = self.KX**2 + self.KY**2
        self.K2inv = np.where(self.K2==0, 1.0, self.K2); self.K2inv = 1.0/self.K2inv
        self.K2inv[0,0]=0.0
        kmax = n//3                       # 2/3 dealiasing
        self.mask = (np.abs(self.KX)<=kmax)&(np.abs(self.KY)<=kmax)

    def rhs(self, wh):
        psih = wh*self.K2inv
        u  = np.real(np.fft.ifft2( 1j*self.KY*psih))
        v  = np.real(np.fft.ifft2(-1j*self.KX*psih))
        wx = np.real(np.fft.ifft2( 1j*self.KX*wh))
        wy = np.real(np.fft.ifft2( 1j*self.KY*wh))
        nl = np.fft.fft2(u*wx+v*wy)*self.mask
        return -nl - self.nu*self.K2*wh

    def solve(self, w0h, save_times=None):
        """RK2 (Heun) with exact viscous factor. Returns dict t -> velocity fields."""
        wh = w0h.copy(); out = {}
        ts = np.linspace(0, self.T, self.nsteps+1)
        if save_times is None: save_times = ts
        snaps = []
        for i,t in enumerate(ts):
            snaps.append(wh.copy())
            if i==self.nsteps: break
            k1 = self.rhs(wh); w1 = wh + self.dt*k1
            k2 = self.rhs(w1); wh = wh + 0.5*self.dt*(k1+k2)
        return np.array(snaps), ts

    def velocity(self, wh):
        psih = wh*self.K2inv
        u = np.real(np.fft.ifft2( 1j*self.KY*psih))
        v = np.real(np.fft.ifft2(-1j*self.KX*psih))
        return u, v

# --- parameterisation: real amplitudes of a few low vorticity modes ---
MODES = [(1,0),(0,1),(1,1),(1,-1),(2,0),(0,2)]   # 6 modes, cos and sin -> use cos only for realness
def theta_to_w0h(theta, ns):
    """theta: real coefficients of cos(k.x) vorticity modes."""
    n = ns.n; wh = np.zeros((n,n), dtype=complex)
    for a,(kx,ky) in zip(theta, MODES):
        wh[kx % n, ky % n]      += a*n*n/2
        wh[(-kx) % n, (-ky) % n]+= a*n*n/2
    return wh
