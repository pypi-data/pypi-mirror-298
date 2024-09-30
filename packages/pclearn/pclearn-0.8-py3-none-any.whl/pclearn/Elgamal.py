#Elgamel Algorithm
from sympy import primitive_root,mod_inverse
from hashlib import sha256
def hash_message(msg):
    h=sha256(msg.encode()).hexdigest()
    return int(h,16)
p=int(input("Enter a prime number p: "))
x=int(input(f"Enter a private key x (1<x<{p-1}): "))
g=primitive_root(p)
print(f"Using the primitive root g={g} ")
#public key
y=pow(g,x,p) 
print(f"Public Key: (p={p},g={g},y={y})")
print(f"Private Key: x={x}")
msg=input("Enter the message to sign: ")
m=hash_message(msg)%(p-1)
while True:
    k=int(input(f"Enter the random integer k (1<k<{p-1} and gcd(k,{p-1})=1):"))
    if mod_inverse(k,p-1) is not None:
        break
s1=pow(g,k,p)
k_inv=mod_inverse(k,p-1)
s2=(k_inv * (m-x*s1))%(p-1)
sign=(s1,s2)
print(f"Signature: s1={s1} , s2={s2}")
v1=pow(g,m,p)
v2=(pow(y,s1,p)* pow(s1,s2,p))%p
print(f"v1={v1} and v2={v2}")
if v1==v2:
    print("Signature is valid.")
else:
    print("Signature is invalid.")


