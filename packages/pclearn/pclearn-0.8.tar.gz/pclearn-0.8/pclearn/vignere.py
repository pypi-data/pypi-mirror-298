chars = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
def encrypted(pt, k):
    ct = ""
    key_length = len(k)
    for i in range(len(pt)):
        ct += chars[(chars.index(pt[i].upper()) + chars.index(k[i % key_length].upper())) % 26]
    return ct
def decrypted(ct, k):
    pt = ""
    key_length = len(k)
    for i in range(len(ct)):
        pt += chars[(chars.index(ct[i].upper()) - chars.index(k[i % key_length].upper())) % 26]
    return pt
plaintext = input("Enter the plaintext: ")
keyword = input("Enter the keyword: ")
ciphertext = encrypted(plaintext, keyword)
print(f"Encrypted text: {ciphertext}")
decrypted_text = decrypted(ciphertext, keyword)
print(f"Decrypted text: {decrypted_text}")
