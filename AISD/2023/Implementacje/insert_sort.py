# We traverse an array n times and each of those n times we order the j lower elements.
from random import randint

def insert_sort(A: list[int]) -> None:
    def swap(i, j):
        A[i], A[j] = A[j], A[i]
    i, j = 0, 0
    while (i < len(A)):
        j = i
        while (j > 0 and A[j-1] > A[j]):
            swap(j-1, j)
            j -=1
        i +=1


for _ in range(1000):
    array_len = randint(0, 1000)
    A = [randint(-2**16, 2**16) for _ in range(array_len)]
    A_expected = A.copy()
    A_expected.sort()
    insert_sort(A)
    assert(A == A_expected)