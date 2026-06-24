# Lesson 3: Operators

# --- Arithmetic Operators ---
print("=== Arithmetic ===")
print(10 + 3)   # 13  Addition
print(10 - 3)   # 7   Subtraction
print(10 * 3)   # 30  Multiplication
print(10 / 3)   # 3.333...  Division (always returns float)
print(10 // 3)  # 3   Floor division (rounds down to int)
print(10 % 3)   # 1   Modulo (remainder)
print(10 ** 3)  # 1000  Exponentiation (power)

# Floor division with negatives rounds toward negative infinity
print(-7 // 2)  # -4 (not -3!)

# --- Comparison Operators ---
print("\n=== Comparison ===")
print(5 == 5)   # True   Equal
print(5 != 3)   # True   Not equal
print(5 > 3)    # True   Greater than
print(5 < 3)    # False  Less than
print(5 >= 5)   # True   Greater or equal
print(5 <= 4)   # False  Less or equal

# Chained comparisons (unique to Python!)
x = 5
print(1 < x < 10)   # True — same as (1 < x) and (x < 10)
print(1 < x < 3)    # False

# --- Logical Operators ---
print("\n=== Logical ===")
print(True and False)   # False
print(True or False)    # True
print(not True)         # False

# Short-circuit evaluation
# 'and' returns first falsy value, or last value
# 'or' returns first truthy value, or last value
print(0 and 5)      # 0 (0 is falsy)
print(3 and 5)      # 5 (both truthy, returns last)
print(0 or 5)       # 5 (0 is falsy, returns 5)
print(3 or 5)       # 3 (3 is truthy, returns it)

# --- Assignment Operators ---
print("\n=== Assignment ===")
n = 10
n += 3   # n = n + 3
print(n)  # 13
n -= 5   # n = n - 5
print(n)  # 8
n *= 2   # n = n * 2
print(n)  # 16
n //= 3  # n = n // 3
print(n)  # 5
n **= 2  # n = n ** 2
print(n)  # 25

# --- Identity Operators ---
print("\n=== Identity (is / is not) ===")
a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a == b)     # True  (same value)
print(a is b)     # False (different objects in memory)
print(a is c)     # True  (same object)
print(a is not b) # True

# Use 'is' for None checks
val = None
print(val is None)      # True (correct way)
print(val == None)      # True (works but not Pythonic)

# --- Membership Operators ---
print("\n=== Membership (in / not in) ===")
fruits = ["apple", "banana", "cherry"]
print("banana" in fruits)      # True
print("grape" not in fruits)   # True
print("h" in "hello")          # True (works on strings too)

# --- Bitwise Operators (bonus) ---
print("\n=== Bitwise ===")
print(5 & 3)   # 1   AND  (0101 & 0011 = 0001)
print(5 | 3)   # 7   OR   (0101 | 0011 = 0111)
print(5 ^ 3)   # 6   XOR  (0101 ^ 0011 = 0110)
print(~5)      # -6  NOT  (inverts all bits)
print(5 << 1)  # 10  Left shift  (0101 -> 1010)
print(5 >> 1)  # 2   Right shift (0101 -> 0010)

# --- Operator Precedence (high to low) ---
# **  >  *, /, //, %  >  +, -  >  comparisons  >  not  >  and  >  or
# When in doubt, use parentheses!
print("\n=== Precedence ===")
print(2 + 3 * 4)       # 14 (not 20)
print((2 + 3) * 4)     # 20
print(2 ** 3 ** 2)     # 512 (** is right-associative: 2^(3^2) = 2^9)

# --- Truthy and Falsy Values ---
print("\n=== Truthy / Falsy ===")
# Falsy: 0, 0.0, "", [], {}, (), set(), None, False
# Everything else is truthy
print(bool(0))       # False
print(bool(""))      # False
print(bool([]))      # False
print(bool(42))      # True
print(bool("hi"))    # True
print(bool([1, 2]))  # True
