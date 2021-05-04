import scipy.integrate as inte
import scipy.special as sc

def fun(a, b):
    def iner(y):
        if y == 0:
            return 0.
        if y == 1:
            return 0.
        return y**(a - 1) * (1-y)**(b-1)
    return iner

def Tstudent_beta(k):
    return sc.beta(k/2., .5)

def Tstudent_beta_incomplete(k, t):
    f = fun(k/2., 1/2.)
    return inte.romberg(f, 0., k/(t**2+k), divmax=50, tol=10**(-8), show=True)

def Tstudent_CDF(k,t):
    romb = 0.5 * Tstudent_beta_incomplete(k,t)/Tstudent_beta(k)
    if t < 0:
        return romb
    else:
        return 1 - romb

print(Tstudent_CDF(1,0))
