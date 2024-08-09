from Riemann_Zeta import *
import numpy as np
# Create the figure
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.2)  # Adjust the plot to make room for the button


global plotstate
plotstate = 0



DICT_PLOTSTATE = {
    'PRIM_APPROX' : 0,
    'ZETA_STANDARD' : 1
}

 


def show_prim_approx(limit):
    xdata = range(0,limit)
    
    ydata_actual_primes = prim_acutal(limit)
    plot2 = ax.plot(xdata,ydata_actual_primes,label =r"Actual Prime numbers",color = 'blue')
    
    ydata_logarithmic_primes = logarithmic_primes(limit)
    plot2 = ax.plot(xdata,ydata_logarithmic_primes,label =r"$\ frac{x}{log{x}}$ Apprxomation",color = 'red')
    ax.set_xlabel('x')
    ax.set_ylabel('Number of primes up to x') 
    ax.set_title('Comparison of Prime approximations')
    ax.legend()
    plt.draw()  # Redraw the plot




# Show standrad zeta function 
def show_standard_zeta():
    plot1 = ax.plot(sigma,np.abs(zeta_values),label =r"Zetafunction",color = 'black')
    ax.set_xlabel(r'$σ$')
    ax.set_ylabel(r'$|ζ(σ+it)|$')
    ax.set_title(r'Magnitude of the Riemann Zeta Function for $t=14.134725$')
    ax.axvline(1, color='red', linestyle='--')
    ax.legend()
    plt.draw()  # Redraw the plot

# Function to switch plots
def switch(event):
    global plotstate
    
    
    if (plotstate == DICT_PLOTSTATE['ZETA_STANDARD']):
 # Switch back to the original zeta plot
        show_standard_zeta()   
        plotstate = 0
  
    if(plotstate == DICT_PLOTSTATE['PRIM_APPROX']):
        show_prim_approx(100000)
        plotstate = 1
       
        
        
        

# Create the button
ax_button = plt.axes([0.7, 0.05, 0.1, 0.075])  # Position of the button
button = Button(ax_button, 'Switch Plot')

# Assign the switch function to the button
button.on_clicked(switch)

show_standard_zeta()
    
plt.show()

    

    
    