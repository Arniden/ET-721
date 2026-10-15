"""
Arnaud Tadonkeng
Oct 5, 2026
lab 9 unit testing using Pytest
"""

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError(" cannot divide by zero")
    
    return a / b

# exercise 2
# create a function that validates a password: 8+ characters, contains at least one digit
def validate_password(password):
    if len(password) < 8:
        return False
    return any(char.isdigit() for char in password)

# exercise 3
# create a function that check if a number is even
def in_even(n):
    return n % 2 == 0 and n !=0
#for the git commit
