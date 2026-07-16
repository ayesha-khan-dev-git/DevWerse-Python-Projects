#  Continous Calculator Project
#  For Internship task
# This program does +, -, *, /, sin, cos
# It keeps running until user types "end"

import math   #ya math ky funcution perfom krny ky liya use krty hn

# main loop starts here
while True:

    choice = input("\nChoose an operation (+, -, *, /, sin, cos) or type 'end' to exit: ")
    choice = choice.strip()   #if any extra space occur then use this to set automatically
    choice = choice.lower()   #if upper case alphabet use then use this to set them

    # check if user wants to stop
    if choice == "end":
        print("Calculator shutting down...")
        break

    # Perform add operator
    if choice == "+":
        n1 = input("Enter first number: ")
        n2 = input("Enter second number: ")
        n1 = float(n1)
        n2 = float(n2)
        result = n1 + n2
        print("Result:", result)

    # perfom sub operator
    elif choice == "-":
        n1 = input("Enter first number: ")
        n2 = input("Enter second number: ")
        n1 = float(n1)
        n2 = float(n2)
        result = n1 - n2
        print("Result:", result)

    # perfom mult operator
    elif choice == "*":
        n1 = input("Enter first number: ")
        n2 = input("Enter second number: ")
        n1 = float(n1)
        n2 = float(n2)
        result = n1 * n2
        print("Result:", result)

    # perfom div operator
    elif choice == "/":
        n1 = input("Enter first number: ")
        n2 = input("Enter second number: ")
        n1 = float(n1)
        n2 = float(n2)
    #check if denominator has value 0
        if n2 == 0:
            print("Error: cannot divide by zero")
        else:
            result = n1 / n2
            print("Result:", result)

    # Perfom the sine function
    elif choice == "sin":
        unit = input("Is the number in degrees or radians? (deg/rad): ")
        unit = unit.strip().lower()
        num = input("Enter number: ")
        num = float(num)

        # if degrees, convert to radians first because
        # math.sin only understands radians
        if unit == "deg":
            num = math.radians(num)

        result = math.sin(num)
        print("Result:", result)

    # cosine function
    elif choice == "cos":
        unit = input("Is the number in degrees or radians? (deg/rad): ")
        unit = unit.strip().lower()
        num = input("Enter number: ")
        num = float(num)

        if unit == "deg":
            num = math.radians(num)

        result = math.cos(num)
        print("Result:", result)

    # if user types something else that is not valid
    else:
        print("Invalid operation, please try again")

        #The endcd