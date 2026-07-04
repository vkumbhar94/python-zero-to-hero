# Lesson 5: Control Flow (if / elif / else)

# --- Basic if/else ---
print("=== Basic if/else ===")
age = 18

if age >= 18:
    print("You are an adult")
else:
    print("You are a minor")

# --- if / elif / else ---
print("\n=== if/elif/else ===")
score = 75

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
elif score >= 70:
    grade = "C"
elif score >= 60:
    grade = "D"
else:
    grade = "F"

print(f"Score: {score}, Grade: {grade}")

# --- Indentation matters! ---
# Python uses indentation (4 spaces) to define blocks
# No braces {} like C/Java/JS
if True:
    print("\n=== Indentation ===")
    print("This is inside the if block")
    print("So is this")
print("This is outside (always runs)")

# --- Multiple Conditions ---
print("\n=== Multiple Conditions ===")
age = 25
has_license = True

if age >= 18 and has_license:
    print("You can drive")

if age < 13 or age > 65:
    print("Discount available")
else:
    print("No discount")

# not operator
is_raining = False
if not is_raining:
    print("Go outside!")

# --- Nested if ---
print("\n=== Nested if ===")
num = 15

if num > 0:
    if num % 2 == 0:
        print(f"{num} is positive and even")
    else:
        print(f"{num} is positive and odd")
else:
    print(f"{num} is not positive")

# --- Ternary Expression (one-line if/else) ---
print("\n=== Ternary Expression ===")
age = 20
status = "adult" if age >= 18 else "minor"
print(f"Status: {status}")

x = 10
print("even" if x % 2 == 0 else "odd")

# --- Truthy/Falsy in Conditions ---
print("\n=== Truthy/Falsy ===")
name = ""
if name:
    print(f"Hello, {name}")
else:
    print("Name is empty!")

items = [1, 2, 3]
if items:
    print(f"List has {len(items)} items")

# This is more Pythonic than:
# if len(items) > 0:

# --- match/case (Python 3.10+) — like switch/case ---
print("\n=== match/case ===")
command = "quit"

match command:
    case "start":
        print("Starting...")
    case "stop":
        print("Stopping...")
    case "quit" | "exit":
        print("Goodbye!")
    case _:
        print(f"Unknown command: {command}")

# match with patterns
point = (0, 5)
match point:
    case (0, 0):
        print("Origin")
    case (0, y):
        print(f"On Y-axis at y={y}")
    case (x, 0):
        print(f"On X-axis at x={x}")
    case (x, y):
        print(f"Point at ({x}, {y})")

# --- Practical Example ---
print("\n=== Practical: FizzBuzz (1-20) ===")
for num in range(1, 21):
    if num % 3 == 0 and num % 5 == 0:
        print("FizzBuzz", end=" ")
    elif num % 3 == 0:
        print("Fizz", end=" ")
    elif num % 5 == 0:
        print("Buzz", end=" ")
    else:
        print(num, end=" ")
print()  # newline at end
