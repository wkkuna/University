# Buble - with each traverse we want to push the biggest element to the right by
# swapping the adjacment elements that are not in order

from random import randint


def bubble_sort(A: list[int]) -> None:
    def swap(i, j):
        A[i], A[j] = A[j], A[i]
    for i in range(len(A)):
        for j in range(0, len(A) - i-1):
            if A[j] > A[j+1]:
                swap(j, j+1)


for _ in range(1000):
    array_len = randint(0, 1000)
    A = [randint(-2**16, 2**16) for _ in range(array_len)]
    A_expected = A.copy()
    A_expected.sort()
    bubble_sort(A)
    assert(A == A_expected)
