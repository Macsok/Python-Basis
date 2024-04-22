import sympy
import re
from sympy import sin, cos, tan, exp, log, integrate, atan
from sympy.integrals.manualintegrate import manualintegrate
from sympy.abc import x, y
from sympy.integrals.manualintegrate import integral_steps
from sympy import print_latex
from sympy import init_printing

x = sympy.symbols('x')
# x = sympy.symbols('x')
# expr = sympy.sqrt(3) * x**3

# funkcja = x**2 - x + sympy.exp(-x) + 1
# #funkcja = sympy.atan(x)

# calka = sympy.integrate(funkcja, x)

# kroki = integral_steps(funkcja, x)

#---------------------------------------

#print(str(kroki), '\n')

def get_steps(func, var):
    f = sympy.sympify(eval(str(func)))
    x = sympy.symbols(str(var))
    odp = integral_steps(f, x)
    odp = repr(odp)
    return odp

def steps_to_array(kroki):
    #tworzymy krotke z listy krokow, tup[0] - nazwa kroku, tup[1] - tresc
    kroki = str(kroki)

    #oddzielamy pierwszy segment do momentu napotkania 'Rule'
    steps = re.split('Rule', kroki)

    #utworzenie tablic keys, values
    keys = []
    #zebranie nazw krokow, od 0 do n-1
    for el in range(0, len(steps) - 1):
        keys.append(steps[el][steps[el].rfind(' ') + 1:])

    #zebranie tresci krokow, od 1 do n-1
    values = []
    for el in range(1, len(steps) - 1):
        values.append(steps[el][:steps[el].rfind(' ')])
    #ostatni krok w calosci
    values.append(steps[-1][:steps[-1].rfind(')')])

    steps = []
    for i in range(len(keys)):
        steps.append([keys[i], values[i]])
    #steps = [(k, v) for (k, v) in zip(keys, values)]
    
    return steps

#----------------------------
#     integrand - funkcja podcalkowa

def current_int(step_context):
#aktualne wyrazenie podcalkowe
    buff = ''
    copy = step_context
    #Wycinamy interesujacy nas fragment
    if step_context.find('integrand=') >= 0:
        buff += step_context[step_context.find('integrand=') + 10 : step_context.find(',')]
    elif step_context.find('context=') >= 0:
        buff += step_context[step_context.find('context=') + 8 : step_context.find(',')]
    else: return ['', '']
    #buff += ','
    if copy.find('variable=') >= 0:
        copy = copy[copy.find('variable=') + 9 : ]
        copy = copy[ : copy.find(',')]
    if copy.find('symbol=') >= 0:
        copy = copy[copy.find('symbol=') + 7 : ]
        copy = copy[ : copy.find(',')]
    #czyszczenie
    while copy[-1] == ")" or copy[-1] == ']':
        copy = copy[ : -1]
    #buff += copy
    return [buff, copy]

def printing(one_step_array):
#Zwraca opracowanie tresci kroku
    step_type = str(one_step_array[0])
    step_context = str(one_step_array[1])

    #usuwamy rodzaj kroku
    if step_type.find('='):
        step_type = step_type[step_type.find('=') + 1 : ]
    if step_type[0] == '[':
        step_type = step_type[1 : ]

    odp = []
    #print(step_type)
    if step_type == 'Parts':
        odp.append('Całkowanie przez części. ')
        odp.append('Podstawiamy: ')
        odp.append(f'u = {step_context[step_context.find("u=") + 2 : -1]}')
    
    if step_type == 'Constant':
        odp.append('Całkowanie funkcji stałej. ')
        odp.append('Wyciągamy stałą przed nawias.')
        odp.append(f'')

    if step_type == 'U':
        odp.append('Całkowanie przez podstawienie. ')
        odp.append('Podstawiamy pod zmienną u: ')
        odp.append(f'u = {step_context[step_context.find("u_func=") + 7 : -1]}')

    if step_type == 'ConstantTimes':
        odp.append('Wyciągamy stałą przed całkę. ')
        con = step_context[step_context.find("constant=") + 9 : ]
        odp.append(f'Mnożymy całkę przez {con[ : con.find(",")]}: ')
        odp.append(f'Wtedy pod całką zostaje: {step_context[step_context.find("other=") + 6 : - 1]}')

    if step_type == 'Reciprocal':
        odp.append('Całka funkcji odwrotnej. ')
        odp.append(f'Podstawiamy pod zmienną {step_context[step_context.find("variable=") + 9 : step_context.find("variable=") + 11]}: ')
        odp.append(f'u = {step_context[step_context.find("u=") + 2 : - 1]}')

    if step_type == 'Add':
        odp.append('Rozbijamy całkę na sumę całek. ')
        odp.append('')
        odp.append(f'')

    if step_type == 'Power':
        odp.append('Całkowanie funkcji x**n. ')
        odp.append('')
        odp.append(f'n = {step_context[step_context.find("exp=") + 4 : - 1]}')
        #obcinanie ogona
        while odp[-1][-1] == ")": odp[-1] = odp[-1][:-1]

    if step_type == 'Exp':
        odp.append('Całkowanie funkcji wykładniczej. ')
        odp.append('Wyrażenie ma postać typu: a**x. ')
        baza = step_context[step_context.find("base=") + 5 : ]
        if baza[0] == 'E': baza = 'e'
        else: baza = baza[ : baza.find(',')]
        odp.append(f'Nasze wyrażenie przyjmuje postać: {baza}**{step_context[step_context.find("exp=") + 4 : -1]}')

    #Wzrór
    if step_type == 'typ':
        odp.append('tytul...')
        odp.append('opis')
        odp.append(f'u = {step_context[step_context.find("u=") + 2 : - 1]}')

    if odp == []: return 'skip'

    return str(odp[0] + odp[1] + odp[2])

def is_substep(step_vector):
    print(step_vector[0])
    if step_vector[0].find('substep=') > -1:
        return True
    else: return False

def steps_to_file(func, var, file_name):
    f = sympy.sympify(eval(str(func)))
    x = sympy.symbols(str(var))
    odp = integral_steps(f, x)
    with open(str(file_name), "w") as text_file:
        text_file.write(str(odp))
#-----------


#steps = steps_to_array(kroki)

#print(steps)

#for step in steps:
    #print(sympy.latex(printing(step)))
    #print(printing(step)[:])
    #print('')
    #print(current_int(step[1]))

# for step in steps:
#     print(step, '\n')

# from sympy.integrals.manualintegrate import integral_steps
# funkcja = x**2 - x + sympy.exp(-x) + 1
# #funkcja = sympy.atan(x) * x
# #funkcja = sympy.atan(x)
# #---------------------------------------
# calka = sympy.integrate(funkcja, x)

# kroki = integral_steps(funkcja, x)

# steps = steps_to_array(kroki)
# for step in steps:
#     #print(sympy.latex(current_int(step[1])[0]))
#     print('$\int_{}^{}', sympy.latex(current_int(step[1])[0]), '$\n')
    
#print(get_steps('x**2 - x + sympy.exp(-x) + 1', 'x'))
        
#steps_to_file('x**2 - x + sympy.exp(-x) + 1', 'x', 'kroki.txt')