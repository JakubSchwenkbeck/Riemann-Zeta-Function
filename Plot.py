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
    
    def __init__(self): # init the window
        super().__init__()
        
        # Set the window title and icon
        self.setWindowTitle("My PyQt5 Application")
        self.setWindowIcon(QIcon('C:/Users/jakub/Python/rzeta.ico'))  # Specify the path to your icon file

    

        
        layout = QVBoxLayout()

        self.plot_buttons = [] # Buttons to switch between plots
        plots = [
            ("Prime Approximation", self.show_prim_approx),
            ("Standard Zeta 2D", self.show_standard_zeta),  # Add more plots as needed
        ]

        for plot_name, plot_func in plots: # init and add Buttons
            button = QPushButton(plot_name, self)
            button.clicked.connect(lambda checked, func=plot_func: func())
            layout.addWidget(button)
            self.plot_buttons.append(button)

        # Web view to display Plotly plots
        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)

        self.setLayout(layout)
        self.setWindowTitle('Riemann Hypothesis')

        # Start with the first plot
        self.show_prim_approx()
        
        # Function to show the prime number approximations
    def show_prim_approx(self):
        limit = 100000
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

    def display_plot(self, fig):
        # Write the Plotly figure to a temporary HTML file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.html') as tmpfile:
            fig.write_html(tmpfile.name)
            tmpfile.flush()
            self.web_view.setUrl(QUrl.fromLocalFile(tmpfile.name))

    
def main():
    app = QApplication(sys.argv)
    ex = RiemannZetaVisualizer()
    ex.show()  # Ensure the widget is shown
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
