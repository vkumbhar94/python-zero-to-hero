# Lesson 2: Variables & Data Types

# Variables are created by assignment — no declaration needed
name = "Alice"
age = 30
height = 5.7
is_student = False

# Python has these basic types:
print(type(name))        # <class 'str'>
print(type(age))         # <class 'int'>
print(type(height))      # <class 'float'>
print(type(is_student))  # <class 'bool'>

# int: whole numbers (no size limit!)
big_number = 999_999_999_999_999_999_999_999_999_999  # underscores for readability
print(big_number)
print(type(big_number))

# float: decimal numbers
pi = 3.14159
print(pi)

# str: text (single or double quotes both work)
greeting = 'Hello'
message = "World"
multiline = """This is
a multiline
string"""
print(multiline)

# bool: True or False
is_active = True
is_empty = False

# NoneType: represents "nothing"
result = None
print(result)        # None
print(type(result))  # <class 'NoneType'>

# --- Type Conversion ---
x = "42"
print(x + "1")      # "421" (string concatenation)
print(int(x) + 1)   # 43   (integer addition)

y = 3.99
print(int(y))        # 3 (truncates, doesn't round)
print(str(y))        # "3.99"
print(float("2.5"))  # 2.5

# --- Multiple Assignment ---
a, b, c = 1, 2, 3
print(a, b, c)  # 1 2 3

# Swap variables (no temp needed!)
a, b = b, a
print(a, b)  # 2 1

# --- Naming Rules ---
# Must start with letter or underscore
# Can contain letters, digits, underscores
# Case-sensitive: Age and age are different
# Convention: use snake_case for variables
my_variable = "good"
# myVariable = "works but not Pythonic"
