def preprocess_text(text, key):
    text = text.lower().replace(" ", "")
    while len(text) % len(key) != 0:
        text += "x"
    return text
def create_matrix(text, key):
    rows = len(text) // len(key)
    return [text[i:i + len(key)] for i in range(0, len(text), len(key))]
def print_matrix(matrix):
    print("Matrix:")
    for row in matrix:
        print(" ".join(row))
    print()
def encrypt(text, key):
    text = preprocess_text(text, key)
    matrix = create_matrix(text, key)
    print("Encryption Matrix:")
    print_matrix(matrix)    
    sorted_key_indices = sorted(range(len(key)), key=lambda k: key[k])
    cipher = ''.join(matrix[i][j] for j in sorted_key_indices for i in range(len(matrix)))
    return cipher
def decrypt(cipher, key):
    cols = len(key)
    rows = len(cipher) // cols
    sorted_key_indices = sorted(range(len(key)), key=lambda k: key[k])
    matrix = [''] * cols
    index = 0
    for k in sorted_key_indices:
        for i in range(rows):
            matrix[k] += cipher[index]
            index += 1
    decryption_matrix = [matrix[i] for i in range(cols)]
    print("Decryption Matrix:")
    print_matrix(decryption_matrix)
    return ''.join(matrix[i][j] for j in range(rows) for i in range(cols)).rstrip('x')
if __name__ == "__main__":
    text = input("Enter plaintext: ")
    key = input("Enter key: ")    
    print("\nEncryption Process:")
    cipher = encrypt(text, key)
    print("Cipher text:", cipher)    
    print("\nDecryption Process:")
    plain = decrypt(cipher, key)
    print("Decrypted Plain text:", plain)
