import sys
import numpy as np
import plotly.graph_objs as go
from PyQt5.QtWidgets import QApplication, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import tempfile
import os

# Assuming Riemann_Zeta contains the required functions
from Riemann_Zeta import *  # Replace with your import paths

class RiemannZetaVisualizer(QWidget):
    def __init__(self):
        super().__init__()

        self.plotstate = 0
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Button to switch plots
        self.switch_button = QPushButton('Switch Plot', self)
        self.switch_button.clicked.connect(self.switch)
        layout.addWidget(self.switch_button)

        # Web view to display Plotly plots
        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)

        self.setLayout(layout)
        self.setWindowTitle('Riemann Hypothesis')

        # Start with the prime approximation plot
        self.show_prim_approx(100000)

    def show_prim_approx(self, limit):
        # Generate x data
        xdata = np.arange(0, limit)

        # Generate y data for different approximations
        ydata_actual_primes = prim_acutal(limit)
        trace1 = go.Scatter(x=xdata, y=ydata_actual_primes, mode='lines', name="Actual Primes", line=dict(color='blue', width=5))

        ydata_logarithmic_primes = logarithmic_primes(limit)
        trace2 = go.Scatter(x=xdata, y=ydata_logarithmic_primes, mode='lines', name="Logarithmic Primes", line=dict(color='yellow', width=2))

        ydata_LI = Li_function(limit)
        trace3 = go.Scatter(x=xdata, y=ydata_LI, mode='lines', name="Li Approximation", line=dict(color='red', width=2))

        # Create layout and figure
        layout = go.Layout(title="Comparison of Prime Approximations", xaxis_title="x", yaxis_title="Number of Primes", legend_title="Legend")
        fig = go.Figure(data=[trace1, trace2, trace3], layout=layout)
        
        # Render the plot and display it in the web view
        self.display_plot(fig)

    def show_standard_zeta(self):
        # Generate sigma data
       
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

    def switch(self):
        # Toggle between plots
        if self.plotstate == 0:
            self.show_standard_zeta()
            self.plotstate = 1
        else:
            self.show_prim_approx(100000)
            self.plotstate = 0

def main():
    app = QApplication(sys.argv)
    ex = RiemannZetaVisualizer()
    ex.show()  # Ensure the widget is shown
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
