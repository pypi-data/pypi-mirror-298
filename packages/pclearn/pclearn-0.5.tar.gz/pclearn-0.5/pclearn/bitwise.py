def bitwise(a, b):
    print("------------------")
    print("First number converted to binary:", bin(a))
    print("Second number converted to binary:", bin(b))
    print("------------------")

    print("Let's Perform some operation on Numbers")
    print("1. AND")
    print("2. OR")
    print("3. NOT for a")
    print("4. NOT for b")

    oper = int(input("Enter number to perform operation (1-4): "))

    if oper == 1:
        result = a & b
        print("Bitwise AND operation:", a, "&", b, "=", result, "(", bin(result), ")")
    elif oper == 2:
        result = a | b
        print("Bitwise OR operation:", a, "|", b, "=", result, "(", bin(result), ")")
    elif oper == 3:
        result = ~a
        print("Bitwise NOT operation (a):", "~", a, "=", result, "(", bin(result), ")") 
    
    elif oper == 4:
        	# NOT operation using bitwise ~ (inverts all bits)
        result = ~b
        print("Bitwise NOT operation (b):", "~", b, "=", result, "(", bin(result), ")")  # Corrected output for ~b
    
    else:
        print("Invalid operation choice.")

if __name__ == "__main__":
    a = int(input("Enter 1st number: "))
    b = int(input("Enter 2nd number: "))
    bitwise(a, b)
