#WAP to implement MD5 to generate message digest from file and for password
#hello.txt
#101001011

import hashlib
def file_check(filename):
    hash1 = hashlib.md5()
    with open(filename,'rb') as open_file:
        content = open_file.read()
        hash1.update(content)
    print(hash1.hexdigest())

def pass_check(pw):
    hash1 = hashlib.md5(pw.encode('utf-8'))
    print("Your MD5 password is ", hash1.hexdigest())

while True:
    choice = int(input("""Choose an option:
1. Hash From File
2. Hash User Input
3. Exit
"""))
    if choice == 1:
        filename = input("Enter file name: ")
        file_check(filename)
    elif choice == 2:
        pw = input("Enter your password: ")
        pass_check(pw)
    elif choice == 3:
        print("Program finished.")
        break
    else:
        print("Invalid choice")
