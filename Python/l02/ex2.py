def pierwiastek(n):
    if n == 1:
        return 1
    k = 0
    for i in range(1, n+1):
        if k >= n:
            return i-1
        k += 2*i - 1


print(pierwiastek(9))
print(pierwiastek(4))
print(pierwiastek(16))
print(pierwiastek(81))
print(pierwiastek(33*33))
print(pierwiastek(1))
