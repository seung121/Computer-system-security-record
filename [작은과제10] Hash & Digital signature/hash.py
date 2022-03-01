import hashlib
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

myStr = 'puppy'
salt = '0121'
prep_salt = str(myStr + salt).encode('utf-8')
myHash = hashlib.sha512(prep_salt).hexdigest()
print(myHash)
mymsg = [prep_salt, myHash]

key = get_random_bytes(16)
cipher = AES.new(key, AES.MODE_EAX)
nonce = cipher.nonce
ciphertext, tag = cipher.encrypt_and_digest(prep_salt)
print("Alice sent (Ciphertext, tag) to Bob.")
print("Bob received (ciphertext, tag) from Alice")
print("Assume that Bob has key (", key, ")")
cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
plaintext = cipher.decrypt(ciphertext)
try:
    cipher.verify(tag)
    print("The message (", plaintext, ") in authentic.")
except ValueError:
    print("Key incorrect or message corrupted")
