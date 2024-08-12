import sys

import numpy as np

import plotly.graph_objs as go # Plotly for graphs and plots

from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton, QLabel  , QDesktopWidget # PyWt5 for GUI and widgets
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon


import tempfile

from Riemann_Zeta import *  # own zeta function


# Class handeling the Plots
class RiemannZetaVisualizer(QWidget):
    PrimeApproxBuffer = 0 # Buffer for the values of the PrimeApproximation
    PrimeApproxLimit = 100000
    
    Zeta_3D_Buffer = None # buffer to decrease loading times
    Zeta_3D_Buffer_zeros = None
    
    def __init__(self): # init the window
        super().__init__()
        
        # Set the window title and icon
        self.setWindowTitle("My PyQt5 Application")
        self.setWindowIcon(QIcon('C:/Users/jakub/Python/rzeta.ico'))  # Specify the path to your icon file

    

        
        layout = QVBoxLayout()

        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)

        self.info_label = QLabel("")  # Label for info card
        self.info_label.setStyleSheet("""
            background-color: lightyellow;
            padding: 5px;
            font-size: 11pt;
            max-height: 60px;
        """)
        layout.addWidget(self.info_label)
        self.info_label.hide()  # Start with the info label hidden

        plots = [
            ("Prime Approximation Comparison", self.show_prim_approx, "This plot delves into the comparison of actual prime numbers with mathematical approximations like the logarithmic prime number approximation and the Li function."),
            ("2D Zeta Function", self.show_standard_zeta, "This plot illustrates the magnitude of the Riemann zeta function, exploring its behavior across different values of the real and imaginary components."),
            ("2D Complex Zeta Function", self.plot_zeta_function, "Visualizing the Riemann zeta function across the complex plane, this plot reveals the intricate relationship between the real and imaginary parts."),
            ("3D Zeta Function", self.show_Zeta_3D, "A 3D representation of the Riemann zeta function's magnitude, highlighting the function's behavior in three-dimensional space."),
            ("Critical Strip Zeta 3D", self.show_Zeta_3D_critical_strip, "This 3D plot focuses on the critical strip of the Riemann zeta function, an area of deep mathematical interest due to its connection with the Riemann Hypothesis."),
            ("Dirichlet L-function", self.show_dirichlet, "The Dirichlet L-functions for residues modulo 4 are visualized in this plot, revealing the periodic properties and zero distributions of these important functions.")
        ]


        for plot_name, plot_func, info_text in plots:
            button = QPushButton(plot_name, self)
            button.clicked.connect(lambda checked, func=plot_func, text=info_text: self.display_plot_and_info(func, text))
            layout.addWidget(button)

        # Info toggle button
        self.toggle_button = QPushButton("Show Info", self)
        self.toggle_button.clicked.connect(self.toggle_info)
        layout.addWidget(self.toggle_button)

        self.setLayout(layout)
        self.setWindowTitle('Riemann Hypothesis')

        # Start with the first plot
        self.show_prim_approx()

    def display_plot_and_info(self, plot_func, info_text):
        plot_func()
        self.info_label.setText(info_text)
        self.toggle_button.setText("Hide Info")
        self.info_label.show()

    def toggle_info(self):
        if self.info_label.isVisible():
            self.info_label.hide()
            self.toggle_button.setText("Show Info")
        else:
            self.info_label.show()
            self.toggle_button.setText("Hide Info")

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
        # Define the range of σ (real part of s)
        sigma = np.linspace(0.5, 1.5, 400)

        # Define a range for t (imaginary part of s) for the slider
        t_values = np.linspace(0.1, 50, 50)  # Slider will range from 0.1 to 50

        # Initial value of t
        initial_t = t_values[0]

        # Calculate the initial zeta values for the initial t
        zeta_values = np.array([standard_riemann_zeta(sigma + initial_t * 1j) for sigma in sigma])

        #  Create the initial trace for the zeta function plot
        trace = go.Scatter(x=sigma, y=np.abs(zeta_values), mode='lines', name="Zeta Function", line=dict(color='black', width=2))

        # Add a vertical line at σ = 1
        line = go.layout.Shape(type="line", x0=1, y0=0, x1=1, y1=max(np.abs(zeta_values)),
                            line=dict(color="red", width=2, dash="dash"))

        # Create the layout and figure
        layout = go.Layout(title="Magnitude of the Riemann Zeta Function with Variable t",
                        xaxis_title="σ", yaxis_title="|ζ(σ+it)|", legend_title="Legend",
                        shapes=[line])

        fig = go.Figure(data=[trace], layout=layout)

        # Add a slider to adjust t
        steps = []
        for t in t_values:
            # Update the zeta values for each t
            zeta_values = np.array([standard_riemann_zeta(sigma + t * 1j) for sigma in sigma])
            
            step = dict(
                method="update",
                args=[{"y": [np.abs(zeta_values)]},  # Update the y-data
                    {"shapes[0].y1": max(np.abs(zeta_values))}],  # Update the height of the vertical line
                label=f't = {t:.2f}'
            )
            steps.append(step)

        sliders = [dict(
            active=0,
            currentvalue={"prefix": "t: "},
            pad={"t": 50},
            steps=steps
        )]

    # Add the slider to the layout
        fig.update_layout(sliders=sliders)

    # Render the plot and display it in the web view
        self.display_plot(fig)

    # plot the zeta function with complex numbers in 2D
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

    #plot the zeta function with complex inputs in 3D
    def show_Zeta_3D(self):
        # Define the real and imaginary parts of s
        re_vals = np.linspace(-1, 1, 200)
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
    # plot the zeta function in 3D with emphasis on the critical strip
    def show_Zeta_3D_critical_strip(self):
                # Define the real and imaginary parts of s, focusing on the critical strip
        re_vals = np.linspace(0, 1, 200)  # Focus on 0 < Re(s) < 1
        im_vals = np.linspace(-30, 30, 400)  # Retain range for Im(s)

        # Create a meshgrid for the real and imaginary values
        Re, Im = np.meshgrid(re_vals, im_vals)
        s = Re + 1j * Im

        # Calculate the logarithm of the absolute value of the zeta function to manage large values
        if self.Zeta_3D_Buffer_zeros is None:
            self.Zeta_3D_Buffer_zeros = np.abs(zeta(s))

        # Create a 3D surface plot with a color scale suitable for highlighting small variations
        surface = go.Surface(z=self.Zeta_3D_Buffer_zeros, x=Re, y=Im, colorscale='Viridis', showscale=True)

        # Highlight Trivial Zeros (Note: Trivial zeros occur outside the critical strip)
        trivial_zeros_x = []
        trivial_zeros_y = []
        trivial_zeros_z = []

        # Highlight Non-Trivial Zeros (first few on the critical line Re(s) = 0.5)
        non_trivial_zeros_y = [-14.135, 14.135, -21.022, 21.022, -25.011, 25.011]  # First few non-trivial zeros
        non_trivial_zeros_x = [0.5] * len(non_trivial_zeros_y)
        non_trivial_zeros_z = [0] * len(non_trivial_zeros_y)  # They should all be zero on the critical line

        non_trivial_zeros = go.Scatter3d(x=non_trivial_zeros_x, y=non_trivial_zeros_y, z=non_trivial_zeros_z,
                                        mode='markers',
                                        marker=dict(size=5, color='blue'),
                                        name='Non-Trivial Zeros')
        # Add the critical line at Re(s) = 0.5
        critical_line = go.Scatter3d(x=[0.5] * len(im_vals), y=im_vals, z=[0] * len(im_vals),
                             mode='lines',
                             line=dict(color='red', width=3),
                             name='Critical Line Re(s) = 0.5')

        # Combine the surface plot with the highlighted zeros
        fig = go.Figure(data=[surface, non_trivial_zeros,critical_line])

        # Update plot layout
        fig.update_layout(title='3D Plot of log(|ζ(s)|) in the Critical Strip with Highlighted Zeros',
                        scene=dict(
                            xaxis_title='Re(s)',
                            yaxis_title='Im(s)',
                            zaxis_title='log(|ζ(s)|)'))
    

        self.display_plot(fig)
    
     # New method to visualize Dirichlet L-functions
    def show_dirichlet(self):
        # Define the range for s = σ + it
        sigma = np.linspace(0, 1, 400)  # Real part
        t = np.linspace(-30, 30, 400)    # Imaginary part

        # Create a meshgrid for the values of s
        S_sigma, S_t = np.meshgrid(sigma, t)
        s = S_sigma + 1j * S_t

        # Calculate the Dirichlet L-functions for residues 1 and 3
        L_residue_1 = np.array([[dirichlet_L_function(1, val) for val in row] for row in s])
        L_residue_3 = np.array([[dirichlet_L_function(3, val) for val in row] for row in s])

        # Create traces for both residues
        trace1 = go.Surface(z=np.abs(L_residue_1), x=S_sigma, y=S_t, colorscale='Viridis', name='|L(s)| for 4k + 1')
        trace2 = go.Surface(z=np.abs(L_residue_3), x=S_sigma, y=S_t, colorscale='Cividis', name='|L(s)| for 4k + 3', opacity=0.8)

        # Create layout for the plot
        layout = go.Layout(
            title='Dirichlet L-functions for Residues Modulo 4',
            scene=dict(
                xaxis_title='Re(s)',
                yaxis_title='Im(s)',
                zaxis_title='|L(s)|'
            )
        )

        # Create a figure and add the traces
        fig = go.Figure(data=[trace1, trace2], layout=layout)

        # Display the plot
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
