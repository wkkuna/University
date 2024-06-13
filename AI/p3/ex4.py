def B(i, j):
    return 'B_%d_%d' % (i, j)


# Constraint on a 2x2 square.
# (i, j) - left top corner of the square
# Allowed squares:
# - with one pixel set,
# - with all pixels set,
# - with no pixels set
def square(i, j):
    return '{0} + {1} + {2} + {3} #= 1 #\/ {4} + {5} #= {6} + {7}' \
        .format(B(i, j), B(i, j+1), B(i+1, j), B(i+1, j+1),
                B(i, j), B(i+1, j+1), B(i, j+1), B(i+1, j))


def get_squares(R, C):
    return ',\n'.join([square(i, j) for i in range(R-1) for j in range(C-1)])


# Constraint on the triples given on the input
def triple(t):
    return B(t[0], t[1]) + ' #= ' + str(t[2])


def get_triples(triples):
    return ',\n'.join([triple(t) for t in triples])


# Constraint on the sum of the row
def sum_row(i, cols, K):
    return ' + '.join([B(i, j) for j in range(cols)]) + ' #= ' + str(K)


# Constraint on the sum of the column
def sum_column(j, rows, K):
    return ' + '.join([B(i, j) for i in range(rows)]) + ' #= ' + str(K)


def get_sums(rows, cols, R, C):
    return ',\n'.join([sum_row(i, C, r) for i, r in enumerate(rows)]) + ",\n" \
        + ',\n'.join([sum_column(j, R, c) for j, c in enumerate(cols)])


# Constraint  on the domains (pixel is either 0 or 1)
def get_domains(bs):
    return ', '.join([b + " in 0..1" for b in bs])


# Constraint on the 1x3(3x1) rectangle: A + 2B + 3C != 2
# (the middle pixel is not set when  the rest is not)
def get_1x3_rec(i, cols):
    return ', '.join(['{0} + 2*{1} + 3*{2} #\= 2'.format(B(i, j), B(i, j+1), B(i, j+2)) for j in range(cols-2)])


def get_3x1_rec(j, rows):
    return ', '.join(['{0} + 2*{1} + 3*{2} #\= 2'.format(B(i, j), B(i+1, j), B(i+2, j)) for i in range(rows-2)])


def get_threes(R, C):
    return ', \n'.join([get_1x3_rec(i, C) for i in range(R)]) \
        + ',\n' + ', \n'.join([get_3x1_rec(j, R) for j in range(C)])


def storms(rows, cols, triples):
    writeln(':- use_module(library(clpfd)).')

    R = len(rows)
    C = len(cols)

    bs = [B(i, j) for i in range(R) for j in range(C)]

    writeln('solve([' + ', '.join(bs) + ']) :- ')

    # Constrain the domains
    writeln(get_domains(bs) + ',')
    # Constrain the sums of each row and column
    writeln(get_sums(rows, cols, R, C) + ',')
    # Constrain that the storm is at least 2x2 square
    writeln(get_squares(R, C) + ',')
    # Constrain the storms on allowed 1x3 (3x1) rectangles (lecture)
    writeln(get_threes(R, C) + ', ')
    # Constrain the triples given on input
    writeln(get_triples(triples) + ',')

    writeln('    labeling([ff], [' + ', '.join(bs) + ']).')
    writeln('')
    writeln(":- tell('prolog_result.txt'), solve(X), write(X), nl, told.")


def writeln(s):
    output.write(s + '\n')


txt = open('zad_input.txt').readlines()
output = open('zad_output.txt', 'w')

rows = list(map(int, txt[0].split()))
cols = list(map(int, txt[1].split()))
triples = []

for i in range(2, len(txt)):
    if txt[i].strip():
        triples.append(list(map(int, txt[i].split())))

storms(rows, cols, triples)
