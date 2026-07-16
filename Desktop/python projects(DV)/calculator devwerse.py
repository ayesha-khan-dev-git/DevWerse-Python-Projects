"""
Console Calculator
-------------------
A loop-driven calculator supporting +, -, *, /, sin, cos.
Runs until the user types 'end'.
"""

import math


def get_number(prompt):
    """Keep asking until the user enters a valid number."""
    while True:
        value = input(prompt)
        try:
            return float(value)
        except ValueError:
            print("Invalid input. Please enter a numeric value.")


def get_angle_unit():
    """Ask whether the trig input is in degrees or radians."""
    while True:
        unit = input("Is the number in degrees or radians? (deg/rad): ").strip().lower()
        if unit in ("deg", "degrees"):
            return "deg"
        elif unit in ("rad", "radians"):
            return "rad"
        else:
            print("Please type 'deg' or 'rad'.")


def main():
    print("=== Python Console Calculator ===")

    while True:
        operation = input(
            "\nChoose an operation (+, -, *, /, sin, cos) or type 'end' to exit: "
        ).strip().lower()

        if operation == "end":
            print("Calculator shutting down...")
            break

        if operation in ("+", "-", "*", "/"):
            num1 = get_number("Enter first number: ")
            num2 = get_number("Enter second number: ")

            if operation == "+":
                result = num1 + num2
            elif operation == "-":
                result = num1 - num2
            elif operation == "*":
                result = num1 * num2
            elif operation == "/":
                if num2 == 0:
                    print("Error: Division by zero is not allowed.")
                    continue
                result = num1 / num2

            print(f"Result: {result}")

        elif operation in ("sin", "cos"):
            unit = get_angle_unit()
            unit_label = "degrees" if unit == "deg" else "radians"
            number = get_number(f"Enter number (in {unit_label}): ")

            # Convert to radians if the user entered degrees
            angle = math.radians(number) if unit == "deg" else number

            if operation == "sin":
                result = math.sin(angle)
            else:
                result = math.cos(angle)

            print(f"Result: {result}")

        else:
            print("Invalid operation. Please choose from +, -, *, /, sin, cos, or 'end'.")


if __name__ == "__main__":
    main()