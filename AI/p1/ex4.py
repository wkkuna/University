#!/usr/bin/python

def opt_dist(puzzle, D):
    puzzle.split()
    bits = list(map(int, puzzle))
    ones = [i for i in range(len(bits)) if bits[i] == 1]

    if not len(ones):
        return D

    n = len(bits)
    min_cost = len(bits)

    for fst in ones:
        if fst+D > n:
            break
        min_cost = min(D - sum(bits[fst:fst+D]) +
                       sum(bits[:fst]) + sum(bits[fst+D:]), min_cost)

    return str(min_cost)


if __name__ == "__main__":
    with open("zad4_input.txt") as f, open("zad4_output.txt", 'w') as out:
        for line in f.readlines():
            l, D = line.split(' ')
            output = opt_dist(l, int(D))
            out.write(output+"\n")
