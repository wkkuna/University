import sys 

def B(i,j):
    return 'B_%d_%d' % (i,j)

def square(i, j):
    """
    Constraint on a 2x2 square. (i, j) - left top corner of the square
    """
    return '{0} + {1} + {2} + {3} #= 1 #\/ {4} + {5} #= {6} + {7}' \
            .format(B(i, j), B(i, j+1), B(i+1, j), B(i+1, j+1), 
                    B(i, j), B(i+1, j+1), B(i, j+1), B(i+1, j))


def getSquares(R, C):
    return ',\n'.join([square(i, j) for i in range(R-1) for j in range(C-1)])

def triple(t):
    return B(t[0], t[1]) + ' #= ' + str(t[2])

def getTriples(triples):
    return ',\n'.join([triple(t) for t in triples])

def rowsum(i, cols, K):
    return ' + '.join([B(i, j) for j in range(cols)]) + ' #= ' + str(K)

def colsum(j, rows, K):
    return ' + '.join([B(i, j) for i in range(rows)]) + ' #= ' + str(K)

def getSums(rows, cols, R, C):
    return ',\n'.join([rowsum(i, C, r) for i, r in enumerate(rows)]) + ",\n" \
         + ',\n'.join([colsum(j, R, c) for j, c in enumerate(cols)])

def getDomains(bs):
    return ', '.join([b + " in 0..1" for b in bs])

def getRowThree(i, cols):
    return ', '.join(['{0} + 2*{1} + 3*{2} #\= 2'.format(B(i, j), B(i, j+1), B(i, j+2)) for j in range(cols-2)])

def getColThree(j, rows):
    return ', '.join(['{0} + 2*{1} + 3*{2} #\= 2'.format(B(i, j), B(i+1, j), B(i+2, j)) for i in range(rows-2)])

def getThrees(R, C):
    return ', \n'.join([getRowThree(i, C) for i in range(R)]) \
        + ',\n' + ', \n'.join([getColThree(j, R) for j in range(C)])


def storms(rows, cols, triples):
    writeln(':- use_module(library(clpfd)).')
    
    R = len(rows)
    C = len(cols)
    
    bs = [ B(i,j) for i in range(R) for j in range(C)]

 
    
    writeln('solve([' + ', '.join(bs) + ']) :- ')

    writeln(getDomains(bs) + ',')   
    writeln(getSums(rows, cols, R, C) + ',')
    writeln(getSquares(R,C) + ',')   
    writeln(getThrees(R, C) + ', ')
    writeln(getTriples(triples) + ',')

    writeln('    labeling([ff], [' +  ', '.join(bs) + ']).' )
    writeln('')
    writeln(":- tell('prolog_result.txt'), solve(X), write(X), nl, told.")

def writeln(s):
    output.write(s + '\n')

finput = 'zad_input.txt'

if len(sys.argv) == 2:
    finput = sys.argv[1]


txt = open(finput).readlines()
output = open('zad_output.txt', 'w')

rows = list(map(int, txt[0].split()))
cols = list(map(int, txt[1].split()))
triples = []

for i in range(2, len(txt)):
    if txt[i].strip():
        triples.append(tuple(map(int, txt[i].split())))

storms(rows, cols, triples)            
        

