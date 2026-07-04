# Lesson 9: Tuples

# Tuples are like lists but IMMUTABLE (can't change after creation)

# --- Creating Tuples ---
print("=== Creating Tuples ===")
empty = ()
single = (42,)         # NOTE: comma is required for single item!
not_a_tuple = (42)     # this is just an int in parentheses
pair = (1, 2)
mixed = (1, "hello", 3.14, True)

print(type(single))      # <class 'tuple'>
print(type(not_a_tuple)) # <class 'int'> — gotcha!

# Parentheses are optional
t = 1, 2, 3
print(t)         # (1, 2, 3)
print(type(t))   # <class 'tuple'>

# tuple() constructor
from_list = tuple([1, 2, 3])
from_str = tuple("hello")
print(from_list)   # (1, 2, 3)
print(from_str)    # ('h', 'e', 'l', 'l', 'o')

# --- Indexing & Slicing (same as lists) ---
print("\n=== Indexing & Slicing ===")
t = (10, 20, 30, 40, 50)
print(t[0])      # 10
print(t[-1])     # 50
print(t[1:3])    # (20, 30)
print(t[::-1])   # (50, 40, 30, 20, 10)

# --- Immutability ---
print("\n=== Immutability ===")
t = (1, 2, 3)
# t[0] = 10     # TypeError! Can't modify
# t.append(4)   # AttributeError! No append

# BUT: if a tuple contains a mutable object, that object CAN change
t = ([1, 2], [3, 4])
t[0].append(99)
print(t)  # ([1, 2, 99], [3, 4]) — the list inside changed!

# --- Tuple Methods (only 2!) ---
print("\n=== Methods ===")
t = (1, 2, 3, 2, 4, 2)
print(t.count(2))  # 3
print(t.index(3))  # 2 (first occurrence)

# --- Unpacking ---
print("\n=== Unpacking ===")

# Basic unpacking
x, y, z = (1, 2, 3)
print(x, y, z)  # 1 2 3

# Swap (actually tuple packing/unpacking)
a, b = 1, 2
a, b = b, a
print(a, b)  # 2 1

# Star unpacking
first, *rest = (1, 2, 3, 4, 5)
print(first, rest)  # 1 [2, 3, 4, 5]

*beginning, last = (1, 2, 3, 4, 5)
print(beginning, last)  # [1, 2, 3, 4] 5

# Ignore values with _
_, y, _ = (1, 2, 3)
print(y)  # 2

# Nested unpacking
(a, b), (c, d) = (1, 2), (3, 4)
print(a, b, c, d)  # 1 2 3 4

# --- Tuples as Dictionary Keys ---
print("\n=== Tuples as Dict Keys ===")
# Lists can't be dict keys (mutable), but tuples can (immutable)
locations = {
    (40.7128, -74.0060): "New York",
    (51.5074, -0.1278): "London",
    (35.6762, 139.6503): "Tokyo",
}
print(locations[(40.7128, -74.0060)])  # New York

# Grid/matrix coordinates
grid = {}
grid[(0, 0)] = "start"
grid[(2, 3)] = "treasure"

# --- Named Tuples (revisited, better than plain tuples) ---
print("\n=== namedtuple vs tuple ===")
from collections import namedtuple

# Plain tuple — what does each position mean?
person = ("Alice", 30, "NYC")
print(person[0])  # Alice — not clear what index means

# Named tuple — self-documenting
Person = namedtuple("Person", ["name", "age", "city"])
alice = Person("Alice", 30, "NYC")
print(alice.name)  # Alice — clear!
print(alice)       # Person(name='Alice', age=30, city='NYC')

# Still a tuple — indexing, unpacking, immutability all work
print(alice[0])          # Alice
name, age, city = alice  # unpacking
print(isinstance(alice, tuple))  # True

# --- When to Use Tuple vs List ---
print("\n=== Tuple vs List ===")

# Tuple: fixed structure, heterogeneous data
point = (3.5, 7.2)          # x, y coordinates
rgb = (255, 128, 0)          # color
record = ("Alice", 30, True) # database row

# List: variable length, homogeneous data
scores = [85, 92, 78, 90]    # collection of same type
names = ["Alice", "Bob"]     # can grow/shrink

# Tuple is faster and uses less memory
import sys
lst = [1, 2, 3, 4, 5]
tpl = (1, 2, 3, 4, 5)
print(f"List size:  {sys.getsizeof(lst)} bytes")
print(f"Tuple size: {sys.getsizeof(tpl)} bytes")

# --- Practical Examples ---
print("\n=== Practical Examples ===")

# 1. Multiple return values from functions
def divide(a, b):
    return a // b, a % b  # returns a tuple

quotient, remainder = divide(17, 5)
print(f"17 / 5 = {quotient} remainder {remainder}")

# 2. Iterating with enumerate (returns tuples)
for i, fruit in enumerate(["apple", "banana", "cherry"]):
    print(f"  {i}: {fruit}")

# 3. Tuple as a record / struct
from typing import NamedTuple

class Employee(NamedTuple):
    name: str
    department: str
    salary: float

emp = Employee("Alice", "Engineering", 95000)
print(f"{emp.name} in {emp.department} earns ${emp.salary:,.0f}")

# 4. Comparing tuples (lexicographic)
print((1, 2, 3) < (1, 2, 4))   # True (compares element by element)
print((1, 2) < (1, 2, 0))      # True (shorter is "less")

# Sort by multiple keys using tuples
students = [("Alice", "B", 85), ("Bob", "A", 92), ("Charlie", "A", 78)]
by_grade_then_score = sorted(students, key=lambda s: (s[1], -s[2]))
print(by_grade_then_score)
# A students first (sorted by score desc), then B students
