import hashlib, random
def mod_exp(base, exp, mod):
    return pow(base, exp, mod)
def hash_func(data):
    return int(hashlib.sha256(data.encode()).hexdigest(), 16)
def sign(p, q, a, s, M):
    r = random.randint(1, q-1)
    X = mod_exp(a, r, p)
    e = hash_func(M + str(X)) % q
    y = (r + s * e) % q
    return X, e, y
def verify(p, q, a, v, M, X, e, y):
    X_prime = (mod_exp(a, y, p) * mod_exp(v, e, p)) % p
    return e == hash_func(M + str(X_prime)) % q
p = int(input("Enter prime number p: "))
q = int(input(f"Enter factor q of {p-1}: "))
a = int(input(f"Enter base asuch as that a^{q} = 1 mode {p} : "))
s = int(input(f"Enter private key s (0 < s <{q}): "))
M = input("Enter a message to be signed: ")
v = mod_exp(a, q - s, p)
X, e, y = sign(p, q, a, s, M)
print(f"Signature: X={X}, e={e}, y={y}")
print(f"Valid Signature: {verify(p, q, a, v, M, X, e, y)}")
