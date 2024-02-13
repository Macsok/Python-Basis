from matplotlib import pyplot as plt
import matplotlib
import numpy as np
import math
import sympy

#matplotlib configuration to save as pgf
matplotlib.use("pgf")
matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
})

#returns taylor series (n elements)
def TaylorSeries(func, n, x_0 = 0):
    out = ''
    last = func
    for i in range(0, n + 1):
        out = str(out) + ' + ' + str(getValue(last, x_0) * (x-x_0)**i / math.factorial(i))
        last = sympy.Derivative(last, 'x').doit()
    return (out)

#returns array of values from taylor series
def Taylor_values(func, n, array, x_0 = 0):
    taylor = str(TaylorSeries(func, n, x_0))
    return [getValue(taylor, x) for x in array]

#returns value from expression
def getValue(sympy_expr, x_0):
    x = sympy.symbols('x')
    func = sympy.lambdify(x, sympy_expr)
    return func(x_0)

#plots provided function and its Taylor series in point x_0
def generatePlot(func, n, a, b, x_0, save_as):
    arr = np.linspace(a, b)
    plt.plot(arr, [getValue(func, x) for x in arr])
    plt.plot(arr, Taylor_values(func, n, arr, x_0))
    plt.scatter(x_0, f(x_0), color = 'green')
    plt.annotate("common point", (x_0 - 1, f(x_0) - 1), color = 'green')
    plt.ylim(top=b, bottom=a)
    plt.savefig('plots/' + save_as)
    plt.close()

#generatePlot('x', 1, 1, 2, 0, 'test.pgf')