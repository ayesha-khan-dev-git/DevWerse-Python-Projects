# Calculator Project
# 5th Semester - Python Assignment
# This program does +, -, *, /, sin, cos
# It keeps running until user types "end"

import math

# main loop starts here
while True:

    choice = input("\nChoose an operation (+, -, *, /, sin, cos) or type 'end' to exit: ")
    choice = choice.strip()
    choice = choice.lower()

    # check if user wants to stop
    if choice == "end":
        print("Calculator shutting down...")
        break

    # addition
    if choice == "+":
        n1 = input("Enter first number: ")
        n2 = input("Enter second number: ")
        n1 = float(n1)
        n2 = float(n2)
        result = n1 + n2
        print("Result:", result)

    # subtraction
    elif choice == "-":
        n1 = input("Enter first number: ")
        n2 = input("Enter second number: ")
        n1 = float(n1)
        n2 = float(n2)
        result = n1 - n2
        print("Result:", result)

    # multiplication
    elif choice == "*":
        n1 = input("Enter first number: ")
        n2 = input("Enter second number: ")
        n1 = float(n1)
        n2 = float(n2)
        result = n1 * n2
        print("Result:", result)

    # division (with zero check)
    elif choice == "/":
        n1 = input("Enter first number: ")
        n2 = input("Enter second number: ")
        n1 = float(n1)
        n2 = float(n2)

        if n2 == 0:
            print("Error: cannot divide by zero")
        else:
            result = n1 / n2
            print("Result:", result)

    # sine function
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