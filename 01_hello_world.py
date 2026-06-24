# Lesson 1: Hello World & Basics

# print() outputs text to the console
print("Hello, World!")

# Python uses indentation (not braces) to define blocks
# Comments start with #

# You can print multiple things
print("My name is", "Python")  # separates with space
print("Version:", 3.14)        # can mix types

# input() reads from the user
name = input("What is your name? ")
print("Hello,", name)

# --- print() options ---
# print(*objects, sep=' ', end='\n', file=sys.stdout, flush=False)

# sep: separator between multiple arguments (default: space)
print("a", "b", "c")              # a b c
print("a", "b", "c", sep="-")    # a-b-c
print("a", "b", "c", sep="")     # abc
print("a", "b", "c", sep=" | ")  # a | b | c

# end: what to print at the end (default: newline)
print("Loading", end="")
print("...", end="")
print(" Done!")   # Loading... Done! (all on one line)

# Useful for progress-style output
for i in range(5):
    print(i, end=" ")  # 0 1 2 3 4
print()  # just a newline to finish the line

# file: redirect output to a file
import sys
print("This is an error!", file=sys.stderr)

# Write to a file
# with open("output.txt", "w") as f:
#     print("Hello file!", file=f)

# flush: force immediate output (useful in loops/progress bars)
# print("Processing...", flush=True)

# --- Other useful built-in functions ---
print("\n--- Built-in Functions ---")

# len() — length of strings, lists, dicts, etc.
print(len("hello"))       # 5
print(len([1, 2, 3]))     # 3

# type() — check the type
print(type(42))           # <class 'int'>

# int(), float(), str(), bool() — type conversion
print(int("42"))          # 42
print(float("3.14"))      # 3.14
print(str(100))           # "100"
print(bool(0))            # False

# abs(), round(), min(), max(), sum()
print(abs(-7))            # 7
print(round(3.14159, 2))  # 3.14
print(min(3, 1, 4, 1))   # 1
print(max(3, 1, 4, 1))   # 4
print(sum([1, 2, 3, 4]))  # 10

# sorted() — returns a new sorted list
print(sorted([3, 1, 4, 1, 5]))          # [1, 1, 3, 4, 5]
print(sorted("python"))                  # ['h', 'n', 'o', 'p', 't', 'y']
print(sorted([3, 1, 2], reverse=True))   # [3, 2, 1]

# reversed() — returns reversed iterator
print(list(reversed([1, 2, 3])))  # [3, 2, 1]

# isinstance() — check type (better than type() for checks)
print(isinstance(42, int))        # True
print(isinstance("hi", (str, int)))  # True (multiple types)

# id() — memory address of an object
a = [1, 2]
b = a
print(id(a) == id(b))  # True (same object)

# help() — interactive help (try in REPL)
# help(print)
# help(str.split)
