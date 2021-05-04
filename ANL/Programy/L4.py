from math import cos
def sgn(x):
    if x>0:
        return 1
    elif x==0:
        return 0
    else:
        return -1

def abs_err(x,x_aprox):
    return abs(x-x_aprox)

# f:(x:number)-> number, [a:number,b:number] -> False, [a,(a+b)/2] | False, [(a+b)/2,b] | True ,[a,a] | True ,[(a+b)/2,(a+b)/2] | True ,[b,b]
def bisection(f,vec2):
    a,b = vec2
    mid = (a+b)/2
    s_f_a = sgn(f(a))
    s_f_b = sgn(f(b))
    s_f_mid = sgn(f(mid))
    
    if s_f_a == 0:
        return True, [a,a]
    if s_f_b == 0:
        return True, [b,b]
    if s_f_mid == 0:
        return True, [mid,mid]
    elif s_f_a != s_f_mid:
        return False, [a,mid]
    else:
        return False, [mid,b]


# ex3
def ex3():
    f = lambda x: x - 0.49
    f_root = 0.49
    sets = [0,1]
    found = False
    for i in range(1,6):
        found, sets = bisection(f,sets)
        if found:
            break
        print(f"I:[{i}] set {sets} e_n {abs_err(f_root,(sets[0]+sets[1])/2)}")
    if found:
        print(f"Zero found at x ={sets[0]}")

print("ZADANIE 3:")
ex3()


class Warning(Exception):
    """Base class for exceptions in this module."""
    pass
def m(sets):
    return (sets[0]+sets[1])/2

# ex4
def ex4(sets):
    f = lambda x: x**2 - 2*cos(3*x+1)
    max_iter = 100
    epsilon = 10**(-5)
    found = False
    for i in range(0,max_iter+1):
        found, sets =  bisection(f,sets)
        if found or abs(f(m(sets))) < epsilon:
            break
    print(f"Root x  ≈ {m(sets)}")

print("ZADANIE 4:")
ex4([0,0.5])
ex4([-1,0])

a = 3

def ex6(_x):
    g = lambda x: x*(3- a*(x**2))/2
    f = lambda x: (x**(-2)-a)
    x = _x
    epsilon = 10**(-5)
    i = 0
    while  abs(f(x)) >= epsilon:
        x = g(x)
 #       print(x)
        i+=1

    print(f"ITER: [{i}] {x}")

print("ZADANIE 6:")
print("1: x = 2/(3 * sqrt(a))")
try:
    x = 2/(3*a**(1/2))
    ex6(x)
except Exception as identifier:
    pass

print("2: x = -9/(3 * sqrt(a))")
try:
    x =  -9/(3*a**(1/2))
    ex6(x)
except Exception as identifier:
    pass

print("3: x = (sqrt(5) + 4)/(3 * sqrt(a))")
try:
    x = (5**(1/2)+4)/(3*a**(1/2))
    ex6(x)
except Exception as identifier:
    pass

print("4: x = (sqrt(5)+5)/(3 * sqrt(a))")
try:
    x = (5**(1/2)+5)/(3*a**(1/2))
    ex6(x)
except Exception as identifier:
    pass
