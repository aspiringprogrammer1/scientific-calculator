from PyQt6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np

# Set a modern style for Matplotlib plots
plt.style.use('seaborn-v0_8-darkgrid')

class MplCanvas(FigureCanvas):
    """Custom Matplotlib canvas for embedding in PyQt."""
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        super().__init__(self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self,
                                   self.sizePolicy().horizontalPolicy(),
                                   self.sizePolicy().verticalPolicy())
        self.updateGeometry()

class GraphWidget(QWidget):
    """
    Widget that contains the plot canvas and the interactive toolbar.
    Handles the logic for generating and displaying the graph.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def plot_function(self, func_str, x_min, x_max, num_points=500, mode='RAD'):
        """
        Generates data and plots a function. 
        Now accepts a 'mode' argument ('RAD' or 'DEG').
        """
        func_str = func_str.replace('^', '**')
        
        try:
            x = np.linspace(x_min, x_max, num_points)
            
            # Define safe environment
            safe_dict = {
                'x': x,
                'sqrt': np.sqrt, 'log': np.log, 'exp': np.exp,
                'pi': np.pi, 'e': np.e, 'np': np
            }

            # Handle Trig based on Mode
            if mode == 'RAD':
                safe_dict.update({
                    'sin': np.sin, 'cos': np.cos, 'tan': np.tan,
                    'asin': np.arcsin, 'acos': np.arccos, 'atan': np.arctan
                })
            else:
                # Degree Mode: Convert input x (degrees) to radians for calculation
                safe_dict.update({
                    'sin': lambda z: np.sin(np.deg2rad(z)),
                    'cos': lambda z: np.cos(np.deg2rad(z)),
                    'tan': lambda z: np.tan(np.deg2rad(z)),
                    'asin': lambda z: np.rad2deg(np.arcsin(z)),
                    'acos': lambda z: np.rad2deg(np.arccos(z)),
                    'atan': lambda z: np.rad2deg(np.arctan(z)),
                })
            
            y = eval(func_str, {"__builtins__": None}, safe_dict)
            
            self.canvas.axes.cla()
            # Update label to show mode
            self.canvas.axes.plot(x, y, label=f'f(x) [{mode}]', linewidth=2, color='#0078d4')
            self.canvas.axes.set_title(f"Function Graph ({mode})")
            self.canvas.axes.set_xlabel("x-axis")
            self.canvas.axes.set_ylabel("y-axis")
            self.canvas.axes.legend()
            self.canvas.axes.grid(True, linestyle='--', alpha=0.7)
            self.canvas.draw()
            return True, ""

        except Exception as e:
            return False, f"Plotting Error: {str(e)}"