N = 1000
fib_recursive_cache = [-1] * N
fib_recursive_cache[0] = 0
fib_recursive_cache[1] = 1


def fib_recursive(n: int) -> int:
    if fib_recursive_cache[n] > -1:
        return fib_recursive_cache[n]
    fib_recursive_cache[n] = fib_recursive(n-1) + fib_recursive(n-2)
    return fib_recursive_cache[n]


def fib_iter(n: int):
    f0, f1 = 0, 1
    if n == 0:
        return f0
    if n == 1:
        return f1
    for _ in range(2, n + 1):
        f2 = f0 + f1
        f0, f1 = f1, f2
    return f2

# |Fn+1  Fn|       |1  1|^n
# |Fn  Fn-1|  =    |1  0|
def fib_matrix(n: int):
    def mult_matrix(m1, m2):
        return [m1[0][0] * m2[0][0] + m1[0][1] * m2[1][0], m1[0][0] * m2[0][1] + m1[0][1] * m2[1][1]], [m1[1][0] * m2[0][0] + m1[1][1] * m2[1][0], m1[1][0] * m2[0][1] + m1[1][1] * m2[1][1]]

    def matrix_pow(matrix: list[list[int]], k: int):
        m = matrix.copy()
        for _ in range(k):
            m = mult_matrix(m, matrix)
        return m

    base_matrix = [[1, 1], [1, 0]]
    return matrix_pow(base_matrix, n)[1][1]


N = 2000000
fib_cache = [-1] * N
fib_cache[0], fib_cache[1], fib_cache[2] = 0, 1, 1


def fib_quick(n):
    sgn = -1 if n < 0 and n % 2 == 0 else 1
    n = abs(n)
    if fib_cache[n] > -1:
        return sgn * fib_cache[n]

    k = n // 2
    fk, fk1 = fib_quick(k), fib_quick(k+1)
    fib_cache[n] = fk1 ** 2 + fk ** 2 if n % 2 else fk * (2 * fk1 - fk)
    return sgn * fib_cache[n]


for i in range(1000):
    a = fib_recursive(i)
    b = fib_iter(i)
    c = fib_matrix(i)
    assert (a == b and b == c)
