import scipy.special

def binom_coef(P,p):
    F = [1,1]
    INV = [1,1]
    INV_F = [1,1]
    n_max = 1
    for (n,k) in P:
        if n > n_max:
            for i in range (n_max+1, n+1):
                F.append((F[i-1]*i) % p)
                INV.append((p - (p//i) * INV[p%i]) %p)
                INV_F.append((INV[i] * INV_F[i-1]) %p)
            n_max = n
        print(F)
        print((F[n] * INV_F[k] * INV_F[n-k]) %p)

binom_coef([(2,1), (4,3), (6,5)], 7)
print(scipy.special.binom(2,1))
print(scipy.special.binom(4,3))
print(scipy.special.binom(6,5))