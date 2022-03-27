import timeit as t


def doskonale_imperatywna(n):
    ret = []
    for i in range(1, n):
        sum = 0
        for j in range(1, int(i/2) + 1):
            if i % j == 0:
                sum += j
        if sum == i:
            ret.append(i)
    return ret


def doskonale_skladana(n):
    return [i for i in range(1, n) if sum([j for j in range(1, int(i/2) + 1) if i % j == 0]) == i]


def doskonale_funkcyjna(n):
    return list(filter(lambda i: sum(filter(lambda j: i % j == 0, range(1, int(i/2) + 1))) == i, range(1, n)))


print(
    f"Imperatywna: {t.timeit(lambda: doskonale_imperatywna(10000), number=30)}")
print(f"Skladana: {t.timeit(lambda: doskonale_skladana(10000), number=30)}")
print(f"Funkcyjna: {t.timeit(lambda: doskonale_funkcyjna(10000), number=30)}")

# Console output
# Imperatywna: 21.654849015001673
# Skladana: 21.765698980016168
# Funkcyjna: 36.86763408099068
