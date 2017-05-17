from sympy import *

x = symbols('x')
print integrate((0.001 * x ** 2) / exp(0.002 * x ** 2), x)
