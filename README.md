PyScientific Calculator
A feature-rich, desktop scientific calculator built with Python and PyQt6. This application is designed to solve real-world mathematical problems, providing standard and scientific calculation capabilities along with advanced function graphing and history management.

Project Objective
The goal of this project is to design, develop, and deploy a complete Python-based desktop application that demonstrates proficiency in GUI development, data processing with Pandas, mathematical computation with NumPy and SymPy, and data visualization with Matplotlib.

Features
Modern GUI: Clean, aesthetically pleasing user interface modeled after modern calculator apps.

Scientific Calculations: Supports arithmetic operations, trigonometric functions (sin, cos, tan, and their inverses), logarithms (log, ln), exponentials, square roots, and constants like pi and e.

Symbolic Computation: Utilizes the SymPy library for robust and accurate expression evaluation.

Graphing Capability: An interactive graphing tab allows users to plot mathematical functions f(x) over a specified range using Matplotlib and NumPy. The plot includes zoom and pan tools.

History Management: A dedicated panel tracks calculation history. Users can view past calculations, clear the history, and save/load it to/from a CSV file using Pandas.

Requirements
Python 3.8+

PyQt6

NumPy

Pandas

Matplotlib

SymPy

Installation & Usage
Clone the repository:

Bash

git clone https://github.com/yourusername/pyscientific-calculator.git
cd pyscientific-calculator
Install dependencies: It is recommended to use a virtual environment.

Bash

pip install -r requirements.txt
Run the application:

Bash

python main.py