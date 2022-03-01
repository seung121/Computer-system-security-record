from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

AlicePrivKey = RSA.generate(2048)
f = open('AlicePrivKey.pem', 'wb')
f.write(AlicePrivKey.export_key('PEM', passphrase="!@#$"))
f.close()
f=open('AlicePubKey.pem','wb')
f.write(AlicePrivKey.publickey().export_key('PEM'))
f.close()

BobPrivKey = RSA.generate(2048)
f = open('BobPrivKey.pem', 'wb')
f.write(BobPrivKey.export_key('PEM', passphrase="!@#$"))
f.close()
f=open('BobPubKey.pem','wb')
f.write(BobPrivKey.publickey().export_key('PEM'))
f.close()

f = open('AlicePrivKey.pem','r')
AlicePrivKey = RSA.import_key(f.read(), passphrase="!@#$")
f.close()
f = open('BobPubKey.pem','r')
BobPubKey = RSA.import_key(f.read())
f.close()

message = 'To be signed'
h = SHA256.new(message.encode('utf-8'))
signature = pkcs1_15.new(AlicePrivKey).sign(h)
print("Alice sent (", message, signature,") to Bob.")

f = open('BobPrivKey.pem', 'r')
BobPrivKey = RSA.import_key(f.read(), passphrase="!@#$")
f.close()
f = open('AlicePubKey.pem', 'r')
AlicePubKey = RSA.import_key(f.read())
f.close()
print("Bob received message (", message, signature, ")from Alice.")
h = SHA256.new(message.encode('utf-8'))
try:
    pkcs1_15.new(AlicePubKey).verify(h, signature)
    print("The signature is valid.")
except (ValueError, TypeError):
    print("The signature is not valid.")