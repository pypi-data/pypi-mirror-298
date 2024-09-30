def encryption(pt, k):
    pt = ("".join(pt.split())).upper()  # Remove spaces and convert to uppercase
    ct = ""
    for i in range(k):
        ct += pt[i::k]
        print(ct)
    print(f"Encrypted text: {ct}")
    return ct

def decryption(ct, k):
    pt = ""
    if len(ct) % k == 0:
        _k = int(len(ct) / k)
    else:
        _k = int(len(ct) / k + 1)
    print(f"Row length for decryption: {_k}")
    for i in range(_k):
        pt += ct[i::_k]
    print(f"Decrypted text: {pt}")
    return pt

plaintext = input("Enter the plaintext: ")
key = int(input("Enter the key (number of columns): "))

ciphertext = encryption(plaintext, key)
decryption(ciphertext, key)
