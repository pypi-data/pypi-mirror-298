from re import findall

# Alphabet array including 'j'
array = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

def datalist_normal(key):
    key = key.replace(" ", "").lower()
    list1 = []
    for char in key:
        if char not in list1:
            list1.append('j' if char == 'i' else char)
    for char in array:
        if char not in list1:
            list1.append(char)
    return list1

def matrix(list1):
    m = []
    index = 0
    for i in range(5):
        a = []
        for j in range(5):
            a.append(list1[index])
            index += 1
        m.append(a)
    print("Matrix:")
    for row in m:
        print(" ".join(row))
    return m

def plain(text):
    text = text.replace(" ", "").lower()
    p = []
    for char in text:
        if char == 'i':
            p.append('j')
        else:
            p.append(char)
    for i in range(0, len(p), 2):
        if i < len(p) - 1 and p[i] == p[i + 1]:
            p.insert(i + 1, 'x')
    if len(p) % 2 != 0:
        p.append('x')
    return p

def enc(p, m):
    encr = ""
    for i in range(0, len(p), 2):
        a = b = c = d = -1
        for j in range(5):
            for k in range(5):
                if p[i] == m[j][k]:
                    a, b = j, k
                if p[i + 1] == m[j][k]:
                    c, d = j, k
        if a == c:
            encr += m[a][(b + 1) % 5] + m[c][(d + 1) % 5]
        elif b == d:
            encr += m[(a + 1) % 5][b] + m[(c + 1) % 5][d]
        else:
            encr += m[a][d] + m[c][b]
    return encr

def dec(p, m):
    decr = ""
    for i in range(0, len(p), 2):
        a = b = c = d = -1
        for j in range(5):
            for k in range(5):
                if p[i] == m[j][k]:
                    a, b = j, k
                if p[i + 1] == m[j][k]:
                    c, d = j, k
        if a == c:
            decr += m[a][(b - 1) % 5] + m[c][(d - 1) % 5]
        elif b == d:
            decr += m[(a - 1) % 5][b] + m[(c - 1) % 5][d]
        else:
            decr += m[a][d] + m[c][b]
    # Replace 'j' with 'i' in the decrypted text
    decr = decr.replace('j', 'i')
    return decr

def playfair_cipher():
    key = input("Enter key: ")
    text = input("Enter text: ")
    list1 = datalist_normal(key)
    print("Datalist:", list1)
    matrix1 = matrix(list1)
    plaintext = plain(text)
    print("Plaintext:", plaintext)
    encrypt = enc(plaintext, matrix1)
    print("Encrypted:", encrypt)
    decrypt = dec(encrypt, matrix1)
    print("Decrypted:", decrypt)

# Run the Playfair Cipher
playfair_cipher()
