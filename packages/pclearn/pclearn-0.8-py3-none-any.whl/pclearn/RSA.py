import math
def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(math.sqrt(num)) + 1):
        if num % i == 0:
            return False
    return True
def rc4(p, q, m):
    if not is_prime(p) or not is_prime(q):
        raise Exception("One or both of the numbers are not prime.")
    if m >= p * q:
        raise Exception("Plaintext must be less than the product of p and q.")
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 2
    while math.gcd(e, phi) != 1:
        e += 1
    d = 2
    while (d * e) % phi != 1:
        d += 1
    ct = pow(m, e, n)
    print("Ciphertext is:", ct)
    pt = pow(ct, d, n)
    print("Plaintext is:", pt)
try:
    p = int(input("Enter the 1st prime number: "))
    q = int(input("Enter the 2nd prime number: "))
    m = int(input("Enter the plaintext (must be less than the product of both prime numbers): "))
    rc4(p, q, m)
except ValueError:
    print("Invalid input. Please enter integer values.")
except Exception as e:
    print(e)
