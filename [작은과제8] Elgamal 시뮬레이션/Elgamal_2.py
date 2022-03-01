from math import gcd
import random


def primRoots(modulo):
    coprime_set = {num for num in range(1, modulo) if gcd(num, modulo) == 1}
    return [g for g in range(1, modulo) if coprime_set == {pow(g, powers, modulo)
                                                           for powers in range(1, modulo)}]


def ElGamal_Encryption(e1, e2, p, P):
    r = 4
    C1 = e1 ** r % p
    C2 = P * (e2 ** r) % p
    return C1, C2


def Elgamel_Decryption(d, p, C1, C2):
    P = (C2 * (C1 ** (p - d - 1))) % p
    return P


print('p, d, r, P : ')
p, d, r, P = input().split()

p = int(p)
d = int(d)
r = int(r)
P = int(P)

print('p :', p, ', d :', d, ', r :', r, ', Plaintext: ', P, '\n')

e_1 = int(random.choice(primRoots(p)))

e_2 = e_1 ** d

print("=> e1 : ", e_1, ", e2 : ", e_2, '\n')

C_1, C_2 = ElGamal_Encryption(e_1, e_2, p, P)

print("=> Cypher text : (C1 :", C_1, ",  C2 :", C_2, ')', '\n')

print("=> Plaintext : ", Elgamel_Decryption(d, p, C_1, C_2), '\n')
