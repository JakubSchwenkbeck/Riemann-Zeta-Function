import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

def riemann_zeta(s, n_terms=1000):
    return sum(1/n**s for n in range(1, n_terms + 1))

sigma = np.linspace(0.5, 1.5, 400)
t = 14.134725
s = sigma + t * 1j

zeta_values = np.array([riemann_zeta(sigma + t*1j) for sigma in sigma])

# Sample data for the second plot
x = np.linspace(0, 4*np.pi, 100)
y2 = np.sin(x)

# Need to add more variants 