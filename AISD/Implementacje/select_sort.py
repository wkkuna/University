# Each time we look through an array searching for a smallest element.
# First time we look at n elements, then n-1, n-2... When finished each overview
# of an array, we swap the smallest element with the element after most recent smallest element.
# So after n-k runs, we'd search an array begining at k-th element up to n and we swap the k-th
# with the smallest found. 
from random import randint

def select_sort(A: list[int]) -> None:
    def swap(i, j):
        A[i], A[j] = A[j], A[i]
    for i in range(len(A)):
        curr_min = i
        for j in range(i, len(A)):
            if A[curr_min] > A[j]:
                curr_min = j
        swap(i, curr_min)


for _ in range(1000):
    array_len = randint(0, 1000)
    A = [randint(-2**16, 2**16) for _ in range(array_len)]
    A_expected = A.copy()
    A_expected.sort()
    select_sort(A)
    assert(A == A_expected)