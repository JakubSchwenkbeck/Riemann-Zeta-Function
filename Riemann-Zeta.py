import numpy as np
import matplotlib.pyplot as plt


def riemann_zeta(s, n_terms=1000):
    return sum(1/n**s for n in range(1, n_terms + 1))

sigma = np.linspace(0.5, 1.5, 400)
t = 14.134725
s = sigma + t * 1j

zeta_values = np.array([riemann_zeta(sigma + t*1j) for sigma in sigma])

plt.figure(figsize=(10, 6))
plt.plot(sigma, np.abs(zeta_values), label=r'$|ζ(σ+it)|$')
plt.axhline(0, color='black', linewidth=0.5)
plt.axvline(1, color='red', linestyle='--', label='Critical Line $σ=1$')

plt.xlabel(r'$σ$')
plt.ylabel(r'$|ζ(σ+it)|$')
plt.title(r'Magnitude of the Riemann Zeta Function for $t=14.134725$')
plt.legend()
plt.grid(True)
plt.show()