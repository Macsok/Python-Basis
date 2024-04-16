import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import sympy

#konfiguracja matplotlib
matplotlib.use("pgf")
matplotlib.rcParams.update({
    "pgf.texsystem": "pdflatex",
    'font.family': 'serif',
    'text.usetex': True,
    'pgf.rcfonts': False,
})

#wyrazenie expr z sympy, argument wyrazenia x, przedzial (a,b), N czesci przedzialu, zapisz jako
def darboux_sums(expr, x, a, b, N, save_as):
    x = sympy.symbols(x)
    funkcja = expr(x)
    f = sympy.lambdify(x, funkcja)
    #ilosc przedzialow mnozymy razy n zeby wykres funkcji byl gladki
    n = 10
    x_axis = np.linspace(a,b,N+1)

    X_axis = np.linspace(a,b,n*N+1)
    Y_axis = f(X_axis)
    plt.plot(X_axis,Y_axis,'blue')
    dx = np.broadcast_to(np.linspace(0,(b-a)/N,n), (1,n)).T
    F = f(x_axis[:-1]+dx)
    y_upper = np.amax(F,0)
    y_lower = np.amin(F,0)
    suma_gorna=0
    suma_dolna=0
    delta_x = abs((a-b)/N)
    for i in range(0, len(x_axis)-1):
        suma_gorna += y_upper[i]*(delta_x)
        suma_dolna += y_lower[i]*(delta_x)
    plt.bar(x_axis[1:],y_upper,width=-(b-a)/N, alpha=0.3, align='edge',edgecolor='black', color='red')
    plt.bar(x_axis[1:],y_lower,width=-(b-a)/N, alpha=0.3, align='edge',edgecolor='black', color='green')
    plt.title('Darboux sums, N = {}'.format(N))
    #plt.fill_between(X_axis, Y_axis, where=[(x > a) and (x < b) for x in X_axis], color="white", alpha=0.5)

    #plt.legend(loc='upper right')

    plt.savefig('wykresy/' + save_as)
    plt.clf()
    
    #plt.show()
    return[suma_dolna, suma_gorna]

#print(darboux_sums(sympy.sin,'x',0,5,10000, 'test.pgf'))
    
def riemann_integral(expr, x, a, b, N, save_as):
    x = sympy.symbols(x)
    funkcja = expr(x)
    wartosc_calki = sympy.integrate(funkcja, (x, a, b))
    f = sympy.lambdify(x, funkcja)
    X_axis = np.linspace(a,b, N*10)
    Y_axis = f(X_axis)
    plt.plot(X_axis,Y_axis,'b')
    plt.axhline(color="black") 
    plt.fill_between(X_axis, Y_axis, where=[(x > a) and (x < b) for x in X_axis], alpha=0.3) 
    plt.title('Riemann integral')
    plt.savefig('wykresy/' + save_as)
    plt.clf()
    #plt.show()
    return [abs(sympy.N(wartosc_calki))]

#print(riemann_integral(sympy.sin, 'x', 0, 5, 100, 'test2.pgf'))

def trapezoid_rule(expr, x, a, b, N, save_as):
    x = sympy.symbols(x)
    funkcja = expr(x)
    f = sympy.lambdify(x, funkcja)
    #ilosc przedzialow mnozymy razy n zeby wykres funkcji byl gladki
    n = 100
    x_axis = np.linspace(a,b,N+1)
    #y_axis = f(x_axis)

    X = np.linspace(a,b,N*n+1)
    Y = f(X)
    plt.plot(X,Y)
    suma=0
    for i in range(N):
        xs = [x_axis[i],x_axis[i],x_axis[i+1],x_axis[i+1]]
        ys = [0,f(x_axis[i]),f(x_axis[i+1]),0]
        h = x_axis[i+1]-x_axis[i]
        a = f(x_axis[i])
        b = f(x_axis[i+1])
        podstawy = a + b
        suma += (podstawy*h)/2
        plt.fill(xs,ys,'b',edgecolor='b',alpha=0.3)

    plt.title('Trapezoid Rule, N = {}'.format(N))

    plt.savefig('wykresy/' + save_as)
    plt.clf()
    #plt.show()
    return [suma]

#print(trapezoid_rule(sympy.sin,'x',0,5,50, 'test3.pgf'))