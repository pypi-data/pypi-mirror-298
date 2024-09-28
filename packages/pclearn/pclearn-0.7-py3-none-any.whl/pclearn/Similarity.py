f1=input("Enter a name of file1: ")
f2=input("Enter a name of file2: ")
with open(f1,'r') as f:
    f1=f.read().lower().split(' ')
with open(f2,'r') as f:
    f2=f.read().lower().split(' ')
a1 = set(f1)
a2 = set(f2)
ele_1 = sorted(list(a2))
ele_2 = sorted(list(a1.difference(a2)))
ele_1.extend(ele_2)
print(ele_1)
vec_1 = [0]*len(ele_1)
vec_2 = [0]*len(ele_1)
for i in range(len(ele_1)):
    if ele_1[i] in f2:
        vec_1[i] = f2.count(ele_1[i])
for i in range(len(ele_1)):
    if ele_1[i] in f1:
        vec_2[i] = f1.count(ele_1[i])
#cosine
num = 0
for i,j in zip(vec_1,vec_2):
    num+=(i*j)
d1 = 0
for i in vec_1:
    d1+=i**2
d1 = d1**(0.5)
d2 = 0
for i in vec_2:
    d2+=i**2
d2 = d2**(0.5)
print("The cosine similarity for given doc is: ",num/(d1*d2))
