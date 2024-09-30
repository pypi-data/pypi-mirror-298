def ver(pt,key):
    pt=pt.replace(" "," ")
    al='abcdefghijklmnopqrstuvwxyz'
    en=''
    de=''
    i=0
    j=0
    n=0
    a=[]
    b=[]
    for x in range(0,len(pt)):
        a.append(0)
        b.append(0)
    for l1 in pt.lower():
        a[i]=al.index(l1)
        i+=1
    for l2 in key.lower():
        b[j]=al.index(l2)
        j+=1
    for k in range(0,len(pt)):
        s1=(a[k]+b[k])%26
        en+=al[s1]
    print("Encrypted text is: ",en)
    for k in range(0,len(pt)):
        n=n+1
        s2=al.index(en[k])-al.index(key[n-1])
        de=de+al[s2%26]
    print("Decrypted text: ",de)
pt=input("Enter Plain Text : ")
key=input("Enter a key of same no of letters as that of plain text : ")
ver(pt,key)
