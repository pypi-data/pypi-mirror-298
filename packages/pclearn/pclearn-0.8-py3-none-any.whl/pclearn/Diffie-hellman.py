from sympy import isprime, primitive_root
def diffie_hellman(q, x_a, x_b):
 if not isprime(q):
     raise Exception("Enter a prime number.")
 if not x_a < q:
     raise Exception(f"Enter x_a: {x_a} less than q: {q}")
 if not x_b < q:
     raise Exception(f"Enter x_b: {x_b} less than q: {q}")
 prim_root = primitive_root(q)
 print(f"Primitive root of {q} is {prim_root}")
 y_a = (prim_root**x_a) % q
 y_b = (prim_root**x_b) % q
 sender_key = (y_b**x_a) % q
 receiver_key = (y_a**x_b) % q
 return sender_key, receiver_key
q = int(input("Enter a prime number: "))
x_a = int(input("Enter value of x_a: "))
x_b = int(input("Enter value of x_b: "))
sk, rk = diffie_hellman(q, x_a, x_b)
print(f"The sender's key is {sk} and the receiver's key is {rk}")
