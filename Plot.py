import sys
import numpy as np
import plotly.graph_objs as go
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon
import tempfile
import os



# Assuming Riemann_Zeta contains the required functions
from Riemann_Zeta import *  # Replace with your import paths

class RiemannZetaVisualizer(QWidget):
    PrimeApproxBuffer = 0 # Buffer for the values of the PrimeApproximation
    PrimeApproxLimit = 100000
    
    Zeta_3D_Buffer = None

    Zeta_3D_Buffer_zeros = None
    def __init__(self): # init the window
        super().__init__()
        
        # Set the window title and icon
        self.setWindowTitle("My PyQt5 Application")
        self.setWindowIcon(QIcon('C:/Users/jakub/Python/rzeta.ico'))  # Specify the path to your icon file

    

        
        layout = QVBoxLayout()

        self.plot_buttons = [] # Buttons to switch between plots
        plots = [
            ("Prime Approximation", self.show_prim_approx),
            ("Standard Zeta 2D", self.show_standard_zeta),
            ("complex Zeta 2D", self.plot_zeta_function),
            ("Complex Zeta 3D", self.show_Zeta_3D),
            ("Complex Zeta 3D with zeros", self.show_Zeta_3D_zeros),# Add more plots as needed
        ]

        for plot_name, plot_func in plots: # init and add Buttons
            button = QPushButton(plot_name, self)
            button.clicked.connect(lambda checked, func=plot_func: func())
            layout.addWidget(button)
            self.plot_buttons.append(button)


        # steps = []
        # for i in range(self.PrimeApproxLimit):
        #     step = dict(method = "restyle",args = ["visible", [False]*self.PrimeApproxLimit],)
            
        # step["args"][1][i] = True
        # steps.append(step)
        # sliders = [dict(active = 100000,steps = steps)]
        # layout.addWidget(sliders)
            
        




        # Web view to display Plotly plots
        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)
        
        self.resize(1200, 800)  # Width, Height in pixels

        self.setLayout(layout)
        self.setWindowTitle('Riemann Hypothesis')

        # Start with the first plot
        self.plot_zeta_function()
        
        # Function to show the prime number approximations
    def show_prim_approx(self):
        limit = self.PrimeApproxLimit
        # Generate x data
        xdata = np.arange(0, limit)

        # make usage of the buffer to lower calc times
        if(self.PrimeApproxBuffer == 0):
             # Generate y data for different approximations
            ydata_actual_primes = prim_acutal(limit)
            ydata_logarithmic_primes = logarithmic_primes(limit)
            ydata_LI = Li_function(limit)

        else:
            ydata_actual_primes = self.PrimeApproxBuffer[0]
            ydata_logarithmic_primes= self.PrimeApproxBuffer[1]
            ydata_LI= self.PrimeApproxBuffer[2]
        
       
       # Create plot traces
        trace1 = go.Scatter(x=xdata, y=ydata_actual_primes, mode='lines', name="Actual Primes", line=dict(color='blue', width=5))

        trace2 = go.Scatter(x=xdata, y=ydata_logarithmic_primes, mode='lines', name="Logarithmic Primes", line=dict(color='yellow', width=2))

        trace3 = go.Scatter(x=xdata, y=ydata_LI, mode='lines', name="Li Approximation", line=dict(color='red', width=2))

        # Create layout and figure
        layout = go.Layout(title="Comparison of Prime Approximations", xaxis_title="x", yaxis_title="Number of Primes", legend_title="Legend")
        fig = go.Figure(data=[trace1, trace2, trace3], layout=layout)
        
        # Render the plot and display it in the web view
        self.display_plot(fig)
        if(self.PrimeApproxBuffer == 0):
            self.PrimeApproxBuffer = [ydata_actual_primes,ydata_logarithmic_primes,ydata_LI]

    def show_standard_zeta(self):
        
        # Create trace for zeta function
        trace = go.Scatter(x=sigma, y=np.abs(zeta_values), mode='lines', name="Zeta Function", line=dict(color='black', width=2))

        # Create layout and figure
        layout = go.Layout(title="Magnitude of the Riemann Zeta Function for t=14.134725", xaxis_title="σ", yaxis_title="|ζ(σ+it)|", legend_title="Legend")
        fig = go.Figure(data=[trace], layout=layout)

        # Add a vertical line at σ = 1
        fig.add_shape(type="line", x0=1, y0=0, x1=1, y1=max(np.abs(zeta_values)), line=dict(color="red", width=2, dash="dash"))
        
        # Render the plot and display it in the web view
        self.display_plot(fig)

    def plot_zeta_function(self):
        # Parameters for the zeta function plot
        x_min = -10
        x_max = 2
        y_min = -10
        y_max = 10
        resolution = 40  # Increase for higher resolution

        # Calculate the zeta function over the grid
        x, y, z = calculate_zeta_function(x_min, x_max, y_min, y_max, resolution)

        #Plot the Riemann zeta function values.
        """"
        Args:
            x (numpy.ndarray): Real parts.
            y (numpy.ndarray): Imaginary parts.
            z (numpy.ndarray): Zeta function values.
        """
        magnitude = np.abs(z)
        angle = np.angle(z)

        # Plot the magnitude as a contour plot
        # magnitude_trace = go.Contour(
        #     x=x[0],
        #     y=y[:, 0],
        #     z=magnitude,
        #     colorscale='Viridis',
        #     colorbar=dict(title='Magnitude'),
        #    # contours=dict(showlabels=True),
        #     name='Magnitude'
        # )

      #  Plot the phase as another contour plot
        angle_trace = go.Contour(
            x=x[0],
            y=y[:, 0],
            z=angle,
            colorscale='Cividis',
            colorbar=dict(title='Phase'),
            #contours=dict(showlabels=True),
            name='Phase',
            opacity=0.5
        )

        fig = go.Figure(data=angle_trace)#[magnitude_trace, angle_trace])

        # Highlight the critical line (real part = 0.5)
        critical_line_y = np.linspace(y.min(), y.max(), 100)
        critical_line_x = np.full_like(critical_line_y, 0.5)
        fig.add_trace(go.Scatter(x=critical_line_x, y=critical_line_y, mode='lines', name='Critical Line',
                                line=dict(color='red', width=2)))

        # Highlight the trivial zeros (real part = -2, -4, -6, ...)
        trivial_zeros_x = np.array([-2, -4, -6, -8, -10])
        trivial_zeros_y = np.zeros_like(trivial_zeros_x)
        fig.add_trace(go.Scatter(x=trivial_zeros_x, y=trivial_zeros_y, mode='markers', name='Trivial Zeros',
                                marker=dict(color='blue', size=10)))

        fig.update_layout(
            title='Riemann Zeta Function',
            xaxis_title='Real Part',
            yaxis_title='Imaginary Part',
        )

        # Show the plot in a web browser
        self.display_plot(fig)
    def show_Zeta_3D(self):
        # Define the real and imaginary parts of s
        re_vals = np.linspace(0, 1, 200)
        im_vals = np.linspace(-30, 30, 400)

        # Create a meshgrid for the real and imaginary values
        Re, Im = np.meshgrid(re_vals, im_vals)
        s = Re + 1j * Im

        # Calculate the absolute value of the zeta function
     
        # Later in the code
        if self.Zeta_3D_Buffer is None:
            self.Zeta_3D_Buffer = np.abs(zeta(s))

        # Create a 3D surface plot
        fig = go.Figure(data=[go.Surface(z= self.Zeta_3D_Buffer, x=Re, y=Im)])

        # Update plot layout
        fig.update_layout(title='3D Plot of |ζ(s)|',
                        scene = dict(
                            xaxis_title='Re(s)',
                            yaxis_title='Im(s)',
                            zaxis_title='|ζ(s)|'))

        self.display_plot(fig)
    
    def show_Zeta_3D_zeros(self):
                # Define the real and imaginary parts of s
        re_vals = np.linspace(-8, 2, 300)  # Reduced number of points
        im_vals = np.linspace(-26, 26, 400) # Reduced range and number of points

        # Create a meshgrid for the real and imaginary values
        Re, Im = np.meshgrid(re_vals, im_vals)
        s = Re + 1j * Im

        # Calculate the absolute value of the zeta function
        if self.Zeta_3D_Buffer_zeros is None:
            self.Zeta_3D_Buffer_zeros = np.abs(zeta(s))

        # Create a 3D surface plot
        surface = go.Surface(z=self.Zeta_3D_Buffer_zeros, x=Re, y=Im, colorscale='Viridis', showscale=True)

        # Highlight Trivial Zeros (where Re(s) = -2, -4, -6,...)
        trivial_zeros_x = [-2, -4, -6, -8, -10]  # Known trivial zeros
        trivial_zeros_y = [0] * len(trivial_zeros_x)
        trivial_zeros_z = [0] * len(trivial_zeros_x)  # They should all be zero

        trivial_zeros = go.Scatter3d(x=trivial_zeros_x, y=trivial_zeros_y, z=trivial_zeros_z,
                                    mode='markers',
                                    marker=dict(size=5, color='red'),
                                    name='Trivial Zeros')

        # Highlight Non-Trivial Zeros (e.g., first few on the critical line Re(s) = 0.5)
        non_trivial_zeros_y = [-14.135, 14.135, -21.022, 21.022, -25.011, 25.011]  # First few non-trivial zeros
        non_trivial_zeros_x = [0.5] * len(non_trivial_zeros_y)
        non_trivial_zeros_z = [0] * len(non_trivial_zeros_y)  # They should all be zero

        non_trivial_zeros = go.Scatter3d(x=non_trivial_zeros_x, y=non_trivial_zeros_y, z=non_trivial_zeros_z,
                                        mode='markers',
                                        marker=dict(size=5, color='blue'),
                                        name='Non-Trivial Zeros')

        # Combine the surface plot with the highlighted zeros
        fig = go.Figure(data=[surface, trivial_zeros, non_trivial_zeros])

        # Update plot layout
        fig.update_layout(title='3D Plot of |ζ(s)| with Highlighted Zeros',
                        scene=dict(
                            xaxis_title='Re(s)',
                            yaxis_title='Im(s)',
                            zaxis_title='|ζ(s)|',
                            zaxis=dict(range=[0, 10])))
        
        self.display_plot(fig)
    
    def display_plot(self, fig):
        # Save the plot as an HTML file in a temporary directory
        with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as f:
            fig.write_html(f.name)
            url = QUrl.fromLocalFile(f.name)
            self.web_view.setUrl(url)

def main():
    app = QApplication(sys.argv)
    ex = RiemannZetaVisualizer()
    ex.show()  # Ensure the widget is shown
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
