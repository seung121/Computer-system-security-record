Bob_b = [7, 11, 19, 39, 79, 157, 313]
Bob_n = 900
Bob_r = 37
Bob_rd = 73


def permute(a):
    a[0], a[1], a[2], a[3], a[4], a[5], a[6] = \
        a[3], a[1], a[4], a[2], a[0], a[6], a[5]


def calc_t(n, r, b):
    t = [0 for i in range(len(b))]
    for i in range(0, len(b)):
        t[i] = (b[i] * r) % n
    return t


def KnapsackSum(a, x):
    s = 0
    for i in range(len(a)):
        s = s + a[i] * x[i]
    return s


def KnapsackSum_inv(s, a, n):
    result = [0 for j in range(len(a))]
    for i in range(n - 1, -1, -1):
        if s >= a[i]:
            result[i] = 1
            s = s - a[i]
    return result


Bob_t = calc_t(Bob_n, Bob_r, Bob_b)

permute(Bob_t)

Alice_data = [1, 1, 0, 0, 1, 1, 1]

Alice_s = KnapsackSum(Bob_t, Alice_data)

Bob_s = Alice_s * Bob_rd % Bob_n

print('s\''' : ', Bob_s)

Bob_result = KnapsackSum_inv(Bob_s, Bob_b, len(Bob_t))

print('x\' : ', Bob_result)

permute(Bob_result)

print('x  : ', Bob_result)
