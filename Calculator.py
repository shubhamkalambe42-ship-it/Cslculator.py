Python 3.11.9 (tags/v3.11.9:de54cf5, Apr  2 2024, 10:12:12) [MSC v.1938 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license()" for more information.
# calculator_cli.py

# Step 1: Define functions for each operation
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return "Error! Division by zero."
    return a / b


# Step 2: Calculator function to handle user interaction
def calculator():
...     print("=== CLI Calculator ===")
...     print("Select an operation:")
...     print("1. Addition (+)")
...     print("2. Subtraction (-)")
...     print("3. Multiplication (*)")
...     print("4. Division (/)")
...     print("5. Exit")
... 
...     while True:  # Step 3: Loop until user chooses exit
...         choice = input("\nEnter choice (1/2/3/4/5): ")
... 
...         if choice == '5':
...             print("Exiting... Goodbye!")
...             break
... 
...         if choice not in ['1', '2', '3', '4']:
...             print("Invalid choice! Please select a valid option.")
...             continue
... 
...         try:
...             num1 = float(input("Enter first number: "))
...             num2 = float(input("Enter second number: "))
...         except ValueError:
...             print("Invalid input! Please enter numeric values.")
...             continue
... 
...         if choice == '1':
...             print(f"Result: {add(num1, num2)}")
...         elif choice == '2':
...             print(f"Result: {subtract(num1, num2)}")
...         elif choice == '3':
...             print(f"Result: {multiply(num1, num2)}")
...         elif choice == '4':
...             print(f"Result: {divide(num1, num2)}")
... 
... 
... # Step 4: Run the calculator
... if __name__ == "__main__":
...     calculator()
