from pyDes import *
from aes_cipher import *
def aes():
    
    data=input("Enter a string : ")
    data_encrypter=DataEncrypter()
    data_encrypter.Encrypt(data,"test_pwd")
    enc_data=data_encrypter.GetEncryptedData()
    print("Encrypted Data :",enc_data)
    data_decrypter=DataDecrypter()
    data_decrypter.Decrypt(enc_data, "test_pwd")
    dec_data = data_decrypter.GetDecryptedData()
    print("Decrypted Data :",dec_data)
aes()
