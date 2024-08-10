import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from scipy.special import expi

# Defining the Prim approximation with actual which is pi(x), li(x), and x/logx

# Counting the real number of primes using the sieve of eratosthenes
def sieve_of_eratosthenes(limit):
  sieve= np.ones(limit,dtype=bool)
  sieve[:2] = False
  for i in range(2,int(limit**0.5)+1):
      if(sieve[i]):
          sieve[i*i:limit:i] = False
          
  return sieve
        
    
    # get the count of prime numbers up to a limit
def prim_acutal(limit):
    sieve = sieve_of_eratosthenes(limit)
    count = 0
    result = [0 for i in range(limit)]
    for i in range(limit):
        if(sieve[i] == True ):
            count += 1
            result[i] = count
        else:
            result[i] = count

    return result
    
# get the logrithmic estimation of prime numbers to a limit
def logarithmic_primes(limit):
    res = [0 for i in range(limit)] 
    res[0] = res[1] = 0
    for i in range(2,limit):
            
        res[i] = int( i / np.log(i))
            
    return res
     
# get the li function approximation    
def Li_function(limit):
    
    res = [0 for i in range(limit)] 
    res[0] = res[1] = 0
    for i in range(2,limit):
            
        res[i] = expi(np.log(i))
            
    return res
        





# standard 2D Zeta function with a t
def standard_riemann_zeta(s, n_terms=1000):
    return sum(1/n**s for n in range(1, n_terms + 1))


sigma = np.linspace(0.5, 1.5, 400)
t = 14.134725
s = sigma + t * 1j

zeta_values = np.array([standard_riemann_zeta(sigma + t * 1j) for sigma in sigma])



import numpy as np

def zeta(s, num_terms=1000):
    """
    Approximate the Riemann zeta function for a complex input s (which can be an array)
    using a truncated Dirichlet series.

    Args:
        s (complex or numpy.ndarray): The complex number input (or array of complex numbers) for the zeta function.
        num_terms (int): The number of terms to use in the series approximation.

    Returns:
        complex or numpy.ndarray: The approximated value of the zeta function at s.
    """
    # Create an array of integers from 1 to num_terms
    n = np.arange(1, num_terms + 1).reshape(-1, 1, 1)

    # Compute the zeta function element-wise for the grid of s values
    z = np.sum(1 / np.power(n, s), axis=0)

    return z

# Zeta function with complex numbers in a 2D space , showing critical path

def calculate_zeta_function(x_min, x_max, y_min, y_max, resolution=100):
    """
    Calculate the Riemann zeta function values over a grid defined by x_min, x_max, y_min, y_max.

    Args:
        x_min (float): Minimum x value (real part).
        x_max (float): Maximum x value (real part).
        y_min (float): Minimum y value (imaginary part).
        y_max (float): Maximum y value (imaginary part).
        resolution (int): Number of points in each direction.

    Returns:
        x (numpy.ndarray): Real parts.
        y (numpy.ndarray): Imaginary parts.
        z (numpy.ndarray): Zeta function values.
    """
    # Create a grid of complex numbers
    real_parts = np.linspace(x_min, x_max, resolution)
    imaginary_parts = np.linspace(y_min, y_max, resolution)
    x, y = np.meshgrid(real_parts, imaginary_parts)
    complex_input = x + 1j * y

    # Calculate zeta function values
    z = zeta(complex_input)

    return x, y, z
