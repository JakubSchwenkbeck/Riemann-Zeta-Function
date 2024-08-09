import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Button


# Defining the Prim approximation with actual which is pi(x), li(x), and x/logx

def sieve_of_eratosthenes(limit):
   prime = [True for i in range(limit)]
   prime[0]= prime[1] = False
   p = 2
   while(p*p <limit):
       
    if (prime[p] == True):
        
        for i in range(p*p,limit,p):
            prime[i] = False
            
        p+= 1 
     
    return prime
        
    
    
def prim_acutal(limit):
    res = sieve_of_eratosthenes(limit)
    count = 0
    
    for i in range(limit):
        if(res[i] == True ):
            count += 1
            res[i] = count
        else:
            res[i] = count

    return res
    

def logarithmic_primes(limit):
    res = [0 for i in range(limit)] 
    res[0] = res[1] = 0
    for i in range(2,limit):
            
        res[i] = int( i / np.log(i))
            
    return res
        







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

x = logarithmic_primes(1000000000)
print(x[999999999])