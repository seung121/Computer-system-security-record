p = 11
e_1 = 2
d = 3
e_2 = 8
P = 7

def ElGamal_Encryption(e1, e2, p, P):
    r = 4
    C1 = e1 ** r % p
    C2 = P * (e2 ** r) % p
    return C1, C2


def Elgamel_Decryption(d, p, C1, C2):
    P = (C2 * (C1 ** (p-d-1))) % p
    return P


C_1, C_2 = ElGamal_Encryption(e_1, e_2, p, P)

print(Elgamel_Decryption(d, p, C_1, C_2))






from math import gcd

def primRoots(modulo):
    coprime_set = {num for num in range(1, modulo) if gcd(num, modulo) == 1}
    return [g for g in range(1, modulo) if coprime_set == {pow(g, powers, modulo)
                                                           for powers in range(1, modulo)}]

