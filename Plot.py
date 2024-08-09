from Riemann_Zeta import *

# Create the figure
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.2)  # Adjust the plot to make room for the button

# Initial plot (plot1: Magnitude of the Riemann Zeta Function)
plot1, = ax.plot(sigma, np.abs(zeta_values), label=r'$|ζ(σ+it)|$')
ax.axhline(0, color='black', linewidth=0.5)
AXVLINE = ax.axvline(1, color='red', linestyle='--', label='Critical Line $σ=1$')

global plotstate
plotstate = 0



DICT_PLOTSTATE = {
    'PRIM_APPROX' : 0,
    'ZETA_STANDARD' : 1
}

 

ax.set_xlabel(r'$σ$')
ax.set_ylabel(r'$|ζ(σ+it)|$')
ax.set_title(r'Magnitude of the Riemann Zeta Function for $t=14.134725$')
ax.legend()
ax.grid(True)



def show_prim_approx():
    5




# Show standrad zeta function 
def show_standard_zeta():
    plot1.set_xdata(sigma)
    plot1.set_ydata( np.abs(zeta_values))
    ax.set_xlabel(r'$σ$')
    ax.set_ylabel(r'$|ζ(σ+it)|$')
    ax.set_title(r'Magnitude of the Riemann Zeta Function for $t=14.134725$')
    AXVLINE.set_visible(True)
    
    
    

    
    
# Function to switch plots
def switch(event):
    global plotstate
    
    if plotstate == DICT_PLOTSTATE['ZETA_STANDARD']:
 # Switch back to the original zeta plot
        show_standard_zeta()   
        plotstate = plotstate+1
    else:
       
     # placeholder:
        # Switch to sine plot
        plot1.set_xdata(x)
        plot1.set_ydata(y2)
        ax.set_xlabel('x')
        ax.set_ylabel('sin(x)')
        ax.set_title('Sine Wave')
        AXVLINE.set_label = ' '
        AXVLINE.set_visible(False) # Hide the critical line    
        plotstate = plotstate-1
        
    ax.legend()
    plt.draw()  # Redraw the plot

# Create the button
ax_button = plt.axes([0.7, 0.05, 0.1, 0.075])  # Position of the button
button = Button(ax_button, 'Switch Plot')

# Assign the switch function to the button
button.on_clicked(switch)

plt.show()




    
    

    
    