import timeit as t


def pierwsze_imperatywna(n):
    ret = []
    for i in range(2, n):
        prime = True
        for j in range(2, i):
            if i % j == 0:
                prime = False
                break
        if prime:
            ret.append(i)
    return ret


def pierwsze_skladana(n):
    return [i for i in range(2, n) if all(i % j != 0 for j in range(2, i))]


def pierwsze_funkcyjna(n):
    return list(filter(lambda i: all(i % j != 0 for j in range(2, i)), range(2, n)))


print(
    f"Imperatywna: {t.timeit(lambda: pierwsze_imperatywna(10000), number=30)}")
print(f"Składana: {t.timeit(lambda: pierwsze_skladana(10000), number=30)}")
print(f"Funkcyjna: {t.timeit(lambda: pierwsze_funkcyjna(10000), number=30)}")

# Console output:
# Imperatywna: 5.380140919005498
# Składana: 7.337528437026776
# Funkcyjna: 7.277449943998363
