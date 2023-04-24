from random import randint


def gcd(a: int, b: int) -> int:
    if a == 0:
        return b
    if b == 0:
        return a
    return gcd(b, a % b)


# returns a tuple (d,s,t) such that d = gcd(a,b) and d == a*s + b*t
def ext_gcd(a: int, b: int) -> int:
    if b == 0:
        return (a, 1, 0)

    (d1, s1, t1) = ext_gcd(b, a % b)
    d, s = d1, t1
    t = s1 - (a // b) * t1
    return (d, s, t)


for _ in range(1000):
    x = randint(0, 1000)
    y = randint(0, 1000)
    assert(gcd(x, y) == ext_gcd(x, y)[0])
