from math import cos,atan, pi, sin, sqrt
import struct

def double_to_hex(f):
    return hex(struct.unpack('<Q', struct.pack('<d', f))[0])

def ex_1_a(x):
    return 4*cos(x)**2 - 3

def ex_1_a_better(x):
    return (-4)*sin(x-(pi/6))*sin(x+(pi/6))

def a(x):
    return 2*cos(2*x) - 1

def ex_1_b(x):
    return x**(-3)*(atan(x) - x)

def ex_1_b_better(x):
    return sum([(-1)**i * x**(2*(i-1)) / (2*i+1) for i  in range(1,10)])

def ex_2(a,b,c):
    d=b**2-4*a*c
    return [(-b-sqrt(d))/(2*a), (-b+sqrt(d))/(2*a)]

def ex_2_better(a,b,c):
    x1=0
    x2=0
    d=b**2-4*a*c

    if b<0:
        x1 = (-b + sqrt(d))/(2*a)
    if b>=0:
        x1 = (-b-sqrt(d))/(2*a)
    if x1==0:
        x2 = -(b/a)
    else:
        x2 = c/(a*x1)
    return [x1,x2]


def main():
    ## EX1 A:
    print("Zadanie 1A:")
    for i in range(15):
        m=pi/6 - 10**(-i)
        mm= -pi/6 + 10**(-i)

        x1=ex_1_a(m)
        x1b=ex_1_a_better(m)

        x2=ex_1_a(mm)
        x2b=ex_1_a_better(mm)

        print(f" pi/6 - 10^(-{i}): {x1} hex: {double_to_hex(x1)} {x1b} hex: {double_to_hex(x1b)}")
        print(f"-pi/6 + 10^(-{i}): {x2} hex: {double_to_hex(x2)} {x2b} hex: {double_to_hex(x2b)}")
    print("\n")

    ## EX1 B:
    print("Zadanie 1B:")
    for i in range(15):
        x = 10**(-i)
        print(f"{x}: {ex_1_b(x)} {ex_1_b_better(x)}")
    print("\n")
    ## EX2:
    print("Zadanie 2:")


    
    print("x^2 + 4x + 10^(-15): ")
    x12 = ex_2(1,4,10**(-15))
    x12alt = ex_2_better(1,4,10**(-15))
    print(f"Metoda szkolna: {x12}")
    print(f"Hex: {set(map(double_to_hex,x12))}")
    print(f"Zaproponowana metoda: {x12alt}")
    print(f"Hex: {set(map(double_to_hex,x12alt))}")

    print("\n")

    
    print("-4x^2 - 8x + 10^(-15): ")
    x12 = ex_2(-4,-8,10**(-15))
    x12alt = ex_2_better(-4,-8,10**(-15))
    print(f"Metoda szkolna: {x12}")
    print(f"Hex: {set(map(double_to_hex,x12))}")
    print(f"Zaproponowana metoda: {x12alt}")
    print(f"Hex: {set(map(double_to_hex,x12alt))}")

    print("\n")

    
    print("(10^-6)x^2 1000x - 1: ")
    x12 = ex_2(10**(-6),1000,-1)
    x12alt = ex_2_better(10**(-6),1000,-1)
    print(f"Metoda szkolna: {x12}")
    print(f"Hex: {set(map(double_to_hex,x12))}")
    print(f"Zaproponowana metoda: {x12alt}")
    print(f"Hex: {set(map(double_to_hex,x12alt))}")



main()