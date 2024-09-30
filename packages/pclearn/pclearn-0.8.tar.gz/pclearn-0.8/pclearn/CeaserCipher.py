list1='abcdefghijklmnopqrstuvwxyz'
def encryption(pt,key):
    en=""
    for i in pt.lower():
        k=(list1.index(i)+key)%26
        en+=list1[k] 
    print('Encrypted text: ',en)
    return en
def decryption(pt,key):
    de=""
    for i in pt.lower():
        k=(list1.index(i)-key)%26
        de+=list1[k]
    print('Decrypted text: ',de)
pt=input("Enter plain text: ")
key=int(input("Enter key: "))
en=encryption(pt,key)
decryption(en,key)    
