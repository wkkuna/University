def tabliczka(x1, x2, y1, y2):
    alignment = len(str(x2*y2)) + 1

    def printrow(fst, f):
        print(fst.rjust(alignment), end='')
        print(*(f(col).rjust(alignment) for col in range(x1, x2+1)))

    printrow("", lambda x: str(x))
    for row in range(y1, y2+1):
        printrow(str(row), lambda x: str(row*x))


tabliczka(300, 302, 2, 4)
print()
tabliczka(3, 5, 2, 4)
