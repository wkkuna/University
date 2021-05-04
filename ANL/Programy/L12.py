from scipy.integrate import newton_cotes
from scipy.interpolate import lagrange
import numpy as np
import matplotlib.pyplot as plt



a = -3
b = 3
exact = 2 * np.arctan(3)
step = 10000
xDraw = np.linspace(a, b, step)


def f(x):
    return 1/(1 + (x*x))


def nc(x,N):
    an, B = newton_cotes(N, 1)
    quad = ((b - a) / N) * np.sum(an * f(x))
    error = abs(quad - exact)
    perc = error/exact * 100
    print('{:2d}  {:10.9f}  {:.5e} {:10.2f}%'.format(N, quad, error, perc))
    
    return error


def plot(i,x,N,error):
    L = lagrange(x, f(x))
    plt.subplot(3, 2, i+1)
    plt.yticks(np.linspace(-0.5, 1.5, 9))
    plt.ylim(-0.5, 1.5)
    plt.title("N = {}, błąd = {:.5e}".format(N, error))
    plt.grid(b=None, which='major', axis='y')
    
    
    plt.plot(xDraw, f(xDraw), color="black")
    plt.plot(xDraw, L(xDraw), color="red")


def main():
    for i, N in enumerate([2, 4, 6, 8, 10, 12]):
        x = np.linspace(a, b, N + 1)
        error = nc(x,N)

        plot(i,x,N,error)

    fig = plt.gcf()
    fig.set_size_inches(18.5, 10.5)
    plt.savefig("res.png", dpi=200)
    
   
main()
