# Lesson 7: Functions

# --- Defining and Calling ---
print("=== Basic Functions ===")

def greet():
    print("Hello!")

greet()  # Hello!

def greet_person(name):
    print(f"Hello, {name}!")

greet_person("Alice")

# --- Return Values ---
print("\n=== Return Values ===")

def add(a, b):
    return a + b

result = add(3, 5)
print(result)  # 8

# Without return, function returns None
def no_return():
    x = 42

print(no_return())  # None

# Return multiple values (as a tuple)
def min_max(numbers):
    return min(numbers), max(numbers)

lo, hi = min_max([3, 1, 7, 2, 9])
print(f"min={lo}, max={hi}")

# Early return
def absolute(n):
    if n < 0:
        return -n
    return n

print(absolute(-5))  # 5

# --- Default Parameters ---
print("\n=== Default Parameters ===")

def power(base, exponent=2):
    return base ** exponent

print(power(3))      # 9 (uses default exponent=2)
print(power(3, 3))   # 27

def create_user(name, role="viewer", active=True):
    return {"name": name, "role": role, "active": active}

print(create_user("Alice"))
print(create_user("Bob", role="admin"))

# WARNING: Never use mutable default arguments!
# BAD:
def bad_append(item, lst=[]):
    lst.append(item)
    return lst

print(bad_append(1))  # [1]
print(bad_append(2))  # [1, 2] — BUG! Same list reused!

# GOOD: Use None as default
def good_append(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst

print(good_append(1))  # [1]
print(good_append(2))  # [2] — correct!

# --- Keyword Arguments ---
print("\n=== Keyword Arguments ===")

def describe(name, age, city):
    print(f"{name}, {age}, from {city}")

# Positional
describe("Alice", 30, "NYC")
# Keyword (any order)
describe(city="London", name="Bob", age=25)
# Mix (positional must come first)
describe("Charlie", city="Paris", age=35)

# --- *args and **kwargs ---
print("\n=== *args (variable positional) ===")

def total(*numbers):
    print(f"  Got: {numbers}")  # it's a tuple
    return sum(numbers)

print(total(1, 2, 3))       # 6
print(total(10, 20, 30, 40))  # 100

print("\n=== **kwargs (variable keyword) ===")

def build_profile(**info):
    print(f"  Got: {info}")  # it's a dict
    return info

profile = build_profile(name="Alice", age=30, lang="Python")
print(profile)

print("\n=== Combining all parameter types ===")

def example(required, default=10, *args, **kwargs):
    print(f"  required={required}")
    print(f"  default={default}")
    print(f"  args={args}")
    print(f"  kwargs={kwargs}")

example("hello", 20, 1, 2, 3, x=True, y="yes")

# --- Unpacking Arguments ---
print("\n=== Unpacking ===")

def add3(a, b, c):
    return a + b + c

nums = [1, 2, 3]
print(add3(*nums))  # unpack list as positional args

config = {"a": 10, "b": 20, "c": 30}
print(add3(**config))  # unpack dict as keyword args

# --- Lambda (anonymous functions) ---
print("\n=== Lambda ===")

# Regular function
def square(x):
    return x ** 2

# Same as lambda
square_l = lambda x: x ** 2

print(square(5))    # 25
print(square_l(5))  # 25

# Useful with sorted, map, filter
students = [("Alice", 85), ("Bob", 92), ("Charlie", 78)]
by_score = sorted(students, key=lambda s: s[1], reverse=True)
print(by_score)  # sorted by score descending

# map: apply function to each item
nums = [1, 2, 3, 4, 5]
doubled = list(map(lambda x: x * 2, nums))
print(doubled)  # [2, 4, 6, 8, 10]

# filter: keep items where function returns True
evens = list(filter(lambda x: x % 2 == 0, nums))
print(evens)  # [2, 4]

# --- Scope ---
print("\n=== Scope ===")

x = "global"

def outer():
    x = "outer"

    def inner():
        x = "inner"
        print(f"  inner: {x}")

    inner()
    print(f"  outer: {x}")

outer()
print(f"  global: {x}")

# global keyword — modify global variable from inside function
counter = 0

def increment():
    global counter
    counter += 1

increment()
increment()
print(f"counter = {counter}")  # 2

# nonlocal — modify enclosing (not global) variable
def make_counter():
    count = 0
    def inc():
        nonlocal count
        count += 1
        return count
    return inc

c = make_counter()
print(c())  # 1
print(c())  # 2
print(c())  # 3

# --- Functions are First-Class Objects ---
print("\n=== First-Class Functions ===")

def shout(text):
    return text.upper()

def whisper(text):
    return text.lower()

def speak(func, text):
    return func(text)

print(speak(shout, "hello"))    # HELLO
print(speak(whisper, "HELLO"))  # hello

# Store functions in a data structure
operations = {
    "add": lambda a, b: a + b,
    "sub": lambda a, b: a - b,
    "mul": lambda a, b: a * b,
}
print(operations["mul"](4, 5))  # 20

# --- Docstrings ---
print("\n=== Docstrings ===")

def calculate_bmi(weight_kg, height_m):
    """Calculate Body Mass Index from weight and height."""
    return weight_kg / (height_m ** 2)

print(calculate_bmi(70, 1.75))
print(calculate_bmi.__doc__)  # access the docstring

# --- Type Hints (documentation, not enforced) ---
print("\n=== Type Hints ===")

def greeting(name: str, times: int = 1) -> str:
    return (f"Hello, {name}! ") * times

print(greeting("Alice", 3))

# Hints don't prevent wrong types — they're for tooling/readability
print(greeting(42))  # works but IDE would warn
