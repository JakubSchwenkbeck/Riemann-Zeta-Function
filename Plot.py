from Riemann_Zeta import *

# Create the figure
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.2)  # Adjust the plot to make room for the button

# Initial plot (plot1: Magnitude of the Riemann Zeta Function)
plot1, = ax.plot(sigma, np.abs(zeta_values), label=r'$|ζ(σ+it)|$')
ax.axhline(0, color='black', linewidth=0.5)
critical_line = ax.axvline(1, color='red', linestyle='--', label='Critical Line $σ=1$')

ax.set_xlabel(r'$σ$')
ax.set_ylabel(r'$|ζ(σ+it)|$')
ax.set_title(r'Magnitude of the Riemann Zeta Function for $t=14.134725$')
ax.legend()
ax.grid(True)

# Store plot1 data for switching back
plot1_data = (sigma, np.abs(zeta_values), r'$|ζ(σ+it)|$', r'Magnitude of the Riemann Zeta Function for $t=14.134725$', r'$σ$', r'$|ζ(σ+it)|$')

# Function to switch plots
def switch(event):
    if plot1.get_xdata().all() == sigma.all():
        # Switch to sine plot
        plot1.set_xdata(x)
        plot1.set_ydata(y2)
        ax.set_xlabel('x')
        ax.set_ylabel('sin(x)')
        ax.set_title('Sine Wave')
        critical_line.set_visible(False)  # Hide the critical line
    else:
        # Switch back to the original zeta plot
        plot1.set_xdata(plot1_data[0])
        plot1.set_ydata(plot1_data[1])
        ax.set_xlabel(plot1_data[4])
        ax.set_ylabel(plot1_data[5])
        ax.set_title(plot1_data[3])
        critical_line.set_visible(True)  # Hide the critical line
    ax.legend()
    plt.draw()  # Redraw the plot

# Create the button
ax_button = plt.axes([0.7, 0.05, 0.1, 0.075])  # Position of the button
button = Button(ax_button, 'Switch Plot')

# Assign the switch function to the button
button.on_clicked(switch)

plt.show()

