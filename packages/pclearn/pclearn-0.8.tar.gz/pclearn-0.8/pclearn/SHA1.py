import hashlib
import hmac
def sha(m):
    hash1 = hashlib.sha1(m.encode())
    print("SHA-1 signature of your message is:", hash1.hexdigest())
pt = input("Enter message: ")
sha(pt)
