from itertools import accumulate
from math import comb as c

# Blotkarz
# Wszystkie możliwości 
blotkarz_all = c(36, 5)
blotkarz = [
    # Poker
    c(5, 1) * c(4, 1),
    # Kareta
    c(4, 1) * c(9, 1) * c(4, 4) * c(8, 1),
    # Full
    c(9, 1) * c(4, 3) * c(8, 1) * c(4, 2),
    # Kolor
    c(9, 5) * c(4, 1)-c(5, 1) * c(4, 1),
    # Strit
    c(5, 1) * (c(4, 1)**5) - c(5, 1) * c(4, 1),
    # 3
    c(9, 1) * c(4, 3) * c(8, 2)*(c(4, 1)**2),
    # 2x2
    c(9, 2) * (c(4, 2)**2) * c(7, 1) * c(4, 1),
    # 2
    c(9, 1) * c(4, 2) * c(8, 3)*(c(4, 1)**3),
    # Najwyższa
    blotkarz_all - (
        c(5, 1) * c(4, 1)  # Poker
        + c(4, 1) * c(9, 1) * c(32, 1)  # Kareta
        + c(9, 1) * c(4, 3) * c(8, 1) * c(4, 2)  # Full
        + c(9, 5) * c(4, 1)  # Kolor
        + (c(5, 1) * (c(4, 1)**5) - c(5, 1) * c(4, 1))  # Strit
        + c(9, 1) * c(4, 3) * c(8, 2)*(c(4, 1)**2)  # 3
        + c(9, 2) * (c(4, 2)**2) * c(7, 1) * c(4, 1)  # 2x2
        + c(9, 1) * c(4, 2) * c(8, 3)*(c(4, 1)**3)  # 2
    )
]
# Prawdopodobieństwa uzyskania danego układu
bp = list(map(lambda x:  (float(x) / blotkarz_all), blotkarz))

# Figurant
# Wszystkie kombinacje
figurant_all = c(16, 5)  
figurant = [
    # Poker (tylko 4 dostępne figury)
    0,
    # Kareta
    c(4, 1) * c(4, 4) * c(12, 1),
    # Full
    c(4, 1) * c(4, 3) * c(3, 1) * c(4, 2),  
    # Kolor
    0,    
    # Strit
    0,
     # 3
    c(4, 1) * c(4, 3) * c(3, 2)*(c(4, 1)**2),
    # 2x2
    c(4, 2)*(c(4, 2)**2) * c(2, 1) * c(4, 1),
    # 2
    c(4, 1) * c(4, 2) * c(3, 3)*(c(4, 1)**3), 
    # Najwyższa
    0
]
# Prawdopodobieństwo uzyskania danego układu
fp = list(map(lambda x: float(x) / figurant_all, figurant))


def all_pair(arr):
    return list(accumulate(arr))

bps = bp[:-2][::-1]
fps = all_pair(fp[1:-1][::-1])

bps_prime = list(map(lambda x: x, bps))
fps_prime = list(map(lambda x: x, fps))

s = list(map(lambda x: x[0] * x[1], zip(bps_prime, fps_prime)))

print(sum(s))