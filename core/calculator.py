import sympy
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

class CalculatorEngine:
    """
    Handles math evaluation with support for Degrees/Radians, 
    implicit multiplication, and safe parsing.
    """
    def __init__(self):
        self.mode = 'RAD'  # Default mode
        
        # Base allowed functions (Standard SymPy objects)
        self.allowed_names = {
            'sqrt': sympy.sqrt, 'log': sympy.log, 'ln': sympy.ln,
            'exp': sympy.exp, 'pi': sympy.pi, 'e': sympy.E, 'abs': sympy.Abs,
            'sin': sympy.sin, 'cos': sympy.cos, 'tan': sympy.tan,
            'asin': sympy.asin, 'acos': sympy.acos, 'atan': sympy.atan
        }

    def set_mode(self, mode):
        self.mode = mode

    def evaluate(self, expression_str):
        if not expression_str.strip():
            return ""

        try:
            # 1. Pre-processing: Fix common calculator syntax
            # Replace UI power symbol '^' with Python's '**'
            expr_cleaned = expression_str.replace('^', '**')
            # Handle 'ln' (SymPy uses log for base e)
            expr_cleaned = expr_cleaned.replace('ln(', 'log(')

            # 2. Parse (Always parse as standard SymPy first to avoid SyntaxErrors)
            # This enables things like "2sin(30)" or "2pi" to work
            transformations = (standard_transformations + (implicit_multiplication_application,))
            expr = parse_expr(expr_cleaned, local_dict=self.allowed_names, transformations=transformations, evaluate=False)

            # 3. Apply Degree Mode Conversions (Post-Parsing)
            if self.mode == 'DEG':
                conv = sympy.pi / 180
                
                # --- Step A: Forward Trig (sin/cos/tan) ---
                # We use temporary functions to avoid infinite recursion loops 
                # (e.g., replacing sin(x) with sin(x*c) repeatedly)
                sin_d = sympy.Function('sin_d')
                cos_d = sympy.Function('cos_d')
                tan_d = sympy.Function('tan_d')
                
                # Swap standard trig to temp functions
                expr = expr.replace(sympy.sin, sin_d)
                expr = expr.replace(sympy.cos, cos_d)
                expr = expr.replace(sympy.tan, tan_d)
                
                # Swap temp functions back to standard trig with conversion applied
                expr = expr.replace(sin_d, lambda arg: sympy.sin(arg * conv))
                expr = expr.replace(cos_d, lambda arg: sympy.cos(arg * conv))
                expr = expr.replace(tan_d, lambda arg: sympy.tan(arg * conv))
                
                # --- Step B: Inverse Trig (asin/acos/atan) ---
                # Inverse functions return an angle, so we multiply the RESULT by (180/pi)
                # These don't loop recursively, so we can replace directly.
                expr = expr.replace(sympy.asin, lambda arg: sympy.asin(arg) / conv)
                expr = expr.replace(sympy.acos, lambda arg: sympy.acos(arg) / conv)
                expr = expr.replace(sympy.atan, lambda arg: sympy.atan(arg) / conv)

            # 4. Numerical Evaluation
            result = expr.evalf(15)
            
            # 5. Format Output
            result_val = float(result)
            if result_val.is_integer():
                return str(int(result_val))
            else:
                return f"{result_val:.10f}".rstrip('0').rstrip('.')

        except (sympy.SympifyError, TypeError, ValueError, SyntaxError):
            return "Error: Invalid syntax"
        except ZeroDivisionError:
            return "Error: Division by zero"
        except Exception as e:
            return f"Error: {str(e)}"