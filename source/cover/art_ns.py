import numpy as np, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from scipy.ndimage import zoom
rng = np.random.default_rng(1900)
N = 256; nu = 5e-4; dt = 1e-3
k1 = np.fft.fftfreq(N, 1.0 / N); KX, KY = np.meshgrid(k1, k1, indexing="ij")
K2 = KX**2 + KY**2; K2i = np.where(K2 == 0, 0, 1.0 / np.where(K2 == 0, 1, K2))
dealias = (np.abs(KX) < N/3) & (np.abs(KY) < N/3)
# random initial vorticity concentrated at wavenumbers 3..8
amp = np.exp(-((np.sqrt(K2) - 5.5)**2) / 4.0)
phase = np.exp(2j * np.pi * rng.random((N, N)))
wh = amp * phase * dealias
w = np.real(np.fft.ifft2(wh)); w *= 8.0 / w.std(); wh = np.fft.fft2(w); wh[0, 0] = 0
def rhs(wh):
    psi = wh * K2i
    u = np.real(np.fft.ifft2(1j * KY * psi)); v = np.real(np.fft.ifft2(-1j * KX * psi))
    wx = np.real(np.fft.ifft2(1j * KX * wh)); wy = np.real(np.fft.ifft2(1j * KY * wh))
    return -np.fft.fft2(u * wx + v * wy) * dealias - nu * K2 * wh
for step in range(4000):
    a = rhs(wh); b = rhs(wh + 0.5*dt*a); c = rhs(wh + 0.5*dt*b); d = rhs(wh + dt*c)
    wh = wh + dt/6*(a + 2*b + 2*c + d)
w = np.real(np.fft.ifft2(wh))
from scipy.ndimage import gaussian_filter
w = zoom(gaussian_filter(w, 0.8), 4, order=3)
vm = np.percentile(np.abs(w), 99.5)
cmap = LinearSegmentedColormap.from_list("ns", [
    (0.00, "#5ff2ff"), (0.22, "#0aa3d8"), (0.40, "#16305a"), (0.50, "#0f1b2d"),
    (0.60, "#5a2a1a"), (0.78, "#e8611a"), (1.00, "#ffd66b")])
fig = plt.figure(figsize=(6.4, 6.4)); ax = fig.add_axes([0, 0, 1, 1])
ax.imshow(w.T, origin="lower", cmap=cmap, vmin=-vm, vmax=vm, interpolation="bicubic")
ax.axis("off")
fig.savefig("art_ns.png", dpi=400, facecolor="#0f1b2d")
print("done", w.shape)
