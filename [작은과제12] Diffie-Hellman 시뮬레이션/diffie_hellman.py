p = 23

Alice_x = 3

R1 = (7 ** Alice_x) % p

Bob_y = 6

R2 = (7 ** Bob_y) % 23

BobReceived = R1

AliceReceived = R2

Alice_K = (AliceReceived ** Alice_x) % p
Bob_K = (BobReceived ** Bob_y) % p

if Alice_K == Bob_K:
    print("Alice와 Bob은 동일한 값을 획득하였습니다.")
else:
    print("Alice와 Bob은 동일한 값을 획득하지 못하였습니다.")


    