from random import randint
import sys

# Simpliest a * b
def mult_addition(a: int, b: int) -> int:
    out = 0
    sign = a < 0 and b > 0 or a > 0 and b < 0
    a, b = abs(a), abs(b)
    for _ in range(a):
        out += b
    return out * -1 if sign else out


def long_mult(a: int, b: int) -> int:
    comps = ["" for _ in range(max(len(str(a)), len(str(b))) + 1)]
    out = 0
    sign = a < 0 and b > 0 or a > 0 and b < 0
    a, b = abs(a), abs(b)
    for i, y in enumerate(str(b)[::-1]):
        prev = 0
        y = int(y)
        for _, x in enumerate(str(a)[::-1]):
            x = int(x)
            prod = mult_addition(x, y)
            if prev:
                prod += prev
                prev = 0
            if prod >= 10:
                prev = prod // 10
                prod %= 10
            comps[i] += str(prod)
        if prev:
            comps[i] += str(prev)

    for i, comp in enumerate(comps):
        if comp:
            out += int(comp[::-1], 10) * (10 ** i)
    return out * -1 if sign else out


def russian_mult(a: int, b: int) -> int:
    out = 0
    sign = a < 0 and b > 0 or a > 0 and b < 0
    a, b = abs(a), abs(b)
    while b > 0:
        if b % 2:
            out += a
        a *= 2
        b //= 2
    return out * -1 if sign else out


for _ in range(10000):
    a = randint(-2**16, 2**16)
    b = randint(-2**16, 2**16)
    result0 = mult_addition(a, b)
    result1 = long_mult(a, b)
    result2 = russian_mult(a, b)
    expected = a*b
    assert(result0 == result1 == result2 == expected)
