from skrypty import *

def correct_steps(func, var):
    #func1 = 'x**2 - x + sympy.exp(-x) + 1'
    kroki = get_steps(eval(str(func)), str(var))
    steps = steps_to_array(kroki)
    return steps


#print(correct_steps('x**2 - x + sympy.exp(-x) + 1', 'x'))
