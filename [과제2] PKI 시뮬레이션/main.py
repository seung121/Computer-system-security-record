from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
import pickle

# 1) 인증서를 만드는 함수 genCertificate
def genCertificate(myPubKey, CAPrivKey):
    h = SHA256.new(str(myPubKey.export_key('PEM')).encode('utf-8'))
    S = pkcs1_15.new(CAPrivKey).sign(h)
    return [myPubKey.export_key('PEM'), S]

# 2) 인증서로 인증서를 검증하는 함수 veriCertificate
def veriCertificate(aCertificate, CACertificate):
    CA = RSA.import_key(CACertificate[0])
    try:
        pkcs1_15.new(CA).verify(SHA256.new(str(aCertificate[0]).encode('utf-8')), aCertificate[1])
        print("인증서 검증에 성공 하였습니다!")
    except (ValueError, TypeError):
        print("인증서 검증에 실패 하였습니다.")
        exit()


# a) CA의 개인키를 만들어 CAPriv.pem에 저장한다.
CAPriv = RSA.generate(2048)
f = open('CAPriv.pem', 'wb')
f.write(CAPriv.export_key('PEM', passphrase="!@#$"))
f.close()

# b) CA의 RSA 개인키에서 공개키 CA_pub를 추출한다. 이를 파일 CAPub.pem에 저장한다.
f = open('CAPub.pem', 'wb')
f.write(CAPriv.publickey().export_key('PEM'))
f.close()

# c) CA는 자신의 공개키에 SAH256을 적용하고, 자신의 개인키로 서명하여 서명 S_CA를 만들고,
# 이를 이용하여 자신의 root 인증서 [CA_pub, S_CA]를 만들어 CACertCA.plk 파일에 저장한다.
# 인증서의 저장은 pickle.dump()를 쓰고, 인증서를 읽는 것은 pickle.load()를 쓴다.
f = open('CAPub.pem', 'r')
CAPub = RSA.import_key(f.read())
f.close()
f = open('CAPriv.pem', 'r')
CAPriv = RSA.import_key(f.read(), passphrase="!@#$")
f.close()

# 공개키에 SHA256 적용, 개인키 서명으로 S_CA를 만듬
root = genCertificate(CAPub, CAPriv)

f = open('CACertCA.plk', 'wb')
pickle.dump(root, f)
f.close()


# d) Bob은 자신의 RSA 개인키를 만든다. 이를 파일 BobPriv.pem에 저장한다.
BobPriv = RSA.generate(2048)
f = open('BobPriv.pem', 'wb')
f.write(BobPriv.export_key('PEM', passphrase="!@#$"))
f.close()

# e) Bob은 개인키에서 공개키 Bob_pub를 추출하여 파일 BobPub.pem에 저장한다.
f = open('BobPub.pem', 'wb')
f.write(BobPriv.publickey().export_key('PEM'))
f.close()

# f) CA는 자신의 개인키로 서명한 Bob의 공개키 인증서[Bob_pub, S_Bob_CA] 를 만들어 BobCertCA.plk에 저장한다.
f = open('BobPub.pem', 'r')          # Bob의 공개키 불러오기
BobPub = RSA.import_key(f.read())
f.close()

BobCertCA = genCertificate(BobPub, CAPriv)

f = open('BobCertCA.plk', 'wb')
pickle.dump(BobCertCA, f)
f.close()

# g) Bob은 M = "I bought 100 doge coins." 메시지에 SHA256을 적용한 후
# 자신의 개인키로 서명한 서명 S, 메시지 M, 그리고 공개키 인증서 [Bob_pub, S_Bob_CA]를
# Alice에게 보낸다. (보냈다고 가정하고 print로 출력한다.)
M = SHA256.new('I bought 100 doge coins'.encode('utf-8'))
S = pkcs1_15.new(BobPriv).sign(M)
print("Bob sent (", M, S, BobCertCA, ") to Bob.")

# h) Alice는 메시지 [M, S, [Bob_pub, S_Bob_CA]]를 받는다.
print("Alice received message (", M, S, BobCertCA, ")from Alice.")

# i) Alice는 Bob의 공개키 인증서를 검증하기 위해 CA의 root 인증서 [CA_pub, S_CA]를 파일 CACertCA.plk에서 읽는다.
f = open('CACertCA.plk', 'rb')
rootRead = pickle.load(f)
f.close()

# j)  CA의 root 인증서를 CA의 root 인증서로 검증한다. 검증 실패의 경우 오류 메시지를 출력하고 종료한다.
veriCertificate(rootRead, rootRead)
# k) Bob의 인증서를 CA의 root 인증서로 검증한다. 검증 실패의 경우 오류 메시지를 출력하고 종료한다.
veriCertificate(BobCertCA, rootRead)

# l) 메시지 [M, S]를 Bob의 인증서에 있는 공개키로 검증한다. 검증 실패의 경우 오류 메시지를 출력하고 종료한다.
try:
    pkcs1_15.new(BobPub).verify(M, S)
    print("메세지를 공개키로 검증하는 것을 성공하였습니다!")
except (ValueError, TypeError):
    print("메세지를 공개키로 검증하는 것을 실패하였습니다.")
    exit()
# m) 여기까지 정상적으로 오면 "Good job. Well done!"을 출력하고 종료한다.
print("Good job. Well done! :)")
