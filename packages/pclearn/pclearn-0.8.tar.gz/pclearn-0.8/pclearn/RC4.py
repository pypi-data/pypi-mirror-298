from Crypto.Cipher import ARC4
pt = bytes(input("Enter plain Text: "), 'utf-8')
key = bytes(input("Enter Key: "), 'utf-8')
arc4 = ARC4.new(key)
cipher = arc4.encrypt(pt)
print("Encrypted text: ", cipher)
arc4 = ARC4.new(key)
decipher = arc4.decrypt(cipher)
print("Decrypted text: ", decipher.decode())
