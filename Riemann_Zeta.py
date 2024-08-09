import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from scipy.special import expi

# Defining the Prim approximation with actual which is pi(x), li(x), and x/logx

def sieve_of_eratosthenes(limit):
  sieve= np.ones(limit,dtype=bool)
  sieve[:2] = False
  for i in range(2,int(limit**0.5)+1):
      if(sieve[i]):
          sieve[i*i:limit:i] = False
          
  return sieve
        
    
    
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
    

def logarithmic_primes(limit):
    res = [0 for i in range(limit)] 
    res[0] = res[1] = 0
    for i in range(2,limit):
            
        res[i] = int( i / np.log(i))
            
    return res
        
def Li_function(limit):
    
    res = [0 for i in range(limit)] 
    res[0] = res[1] = 0
    for i in range(2,limit):
            
        res[i] = expi(np.log(i))
            
    return res
        






def riemann_zeta(s, n_terms=1000):
    return sum(1/n**s for n in range(1, n_terms + 1))


sigma = np.linspace(0.5, 1.5, 400)
t = 14.134725
s = sigma + t * 1j

zeta_values = np.array([riemann_zeta(sigma + t * 1j) for sigma in sigma])
