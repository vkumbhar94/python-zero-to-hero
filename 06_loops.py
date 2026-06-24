# Lesson 6: Loops (for, while)

# --- for loop with range() ---
print("=== for with range() ===")
# range(stop) — 0 to stop-1
for i in range(5):
    print(i, end=" ")  # 0 1 2 3 4
print()

# range(start, stop)
for i in range(2, 6):
    print(i, end=" ")  # 2 3 4 5
print()

# range(start, stop, step)
for i in range(0, 20, 3):
    print(i, end=" ")  # 0 3 6 9 12 15 18
print()

# Counting down
for i in range(5, 0, -1):
    print(i, end=" ")  # 5 4 3 2 1
print()

# --- for loop with iterables ---
print("\n=== for with iterables ===")

# Iterating over a list
fruits = ["apple", "banana", "cherry"]
for fruit in fruits:
    print(fruit)

# Iterating over a string
for char in "Python":
    print(char, end="-")  # P-y-t-h-o-n-
print()

# Iterating over a dictionary
person = {"name": "Alice", "age": 30, "city": "NYC"}
for key in person:
    print(f"{key}: {person[key]}")

# Better: .items() gives key-value pairs
for key, value in person.items():
    print(f"{key} = {value}")

# --- enumerate() — get index + value ---
print("\n=== enumerate() ===")
colors = ["red", "green", "blue"]
for index, color in enumerate(colors):
    print(f"{index}: {color}")

# Start from a different number
for i, color in enumerate(colors, start=1):
    print(f"{i}. {color}")

# --- zip() — iterate multiple sequences together ---
print("\n=== zip() ===")
names = ["Alice", "Bob", "Charlie"]
scores = [85, 92, 78]

for name, score in zip(names, scores):
    print(f"{name}: {score}")

# zip stops at shortest
names2 = ["Alice", "Bob", "Charlie", "Diana"]
scores2 = [85, 92]

print("\nzip (stops at shortest):")
for name, score in zip(names2, scores2):
    print(f"  {name}: {score}")  # only Alice and Bob

# itertools.zip_longest pads the shorter with a fill value
from itertools import zip_longest

print("\nzip_longest (pads with default):")
for name, score in zip_longest(names2, scores2, fillvalue=0):
    print(f"  {name}: {score}")  # all 4 names, missing scores become 0

# --- while loop ---
print("\n=== while loop ===")
count = 0
while count < 5:
    print(count, end=" ")
    count += 1  # Don't forget this or infinite loop!
print()

# while with condition
password = ""
attempts = 0
while password != "secret" and attempts < 3:
    password = "wrong" if attempts < 2 else "secret"  # simulating input
    attempts += 1
    print(f"Attempt {attempts}: {'success' if password == 'secret' else 'failed'}")

# --- break — exit loop immediately ---
print("\n=== break ===")
for i in range(10):
    if i == 5:
        break
    print(i, end=" ")  # 0 1 2 3 4
print()

# Find first even number
numbers = [1, 3, 7, 8, 9, 10]
for n in numbers:
    if n % 2 == 0:
        print(f"First even: {n}")
        break

# --- continue — skip to next iteration ---
print("\n=== continue ===")
for i in range(10):
    if i % 2 == 0:
        continue  # skip even numbers
    print(i, end=" ")  # 1 3 5 7 9
print()

# --- else clause on loops (unique to Python!) ---
print("\n=== for/else ===")
# else runs ONLY if the loop completed without hitting break

# Case 1: no break hit — else runs
for n in [2, 4, 6]:
    if n % 2 != 0:
        print(f"Found odd: {n}")
        break
else:
    print("All numbers are even!")

# Case 2: break hit — else skipped
for n in [2, 3, 6]:
    if n % 2 != 0:
        print(f"Found odd: {n}")
        break
else:
    print("All numbers are even!")  # won't print

# Practical use: search pattern
def find_prime_factor(n):
    for i in range(2, n):
        if n % i == 0:
            print(f"{n} = {i} × {n // i}")
            break
    else:
        print(f"{n} is prime!")

find_prime_factor(15)
find_prime_factor(17)

# --- Nested Loops ---
print("\n=== Nested Loops ===")
for i in range(1, 4):
    for j in range(1, 4):
        print(f"{i}×{j}={i*j}", end="\t")
    print()

# --- Common Patterns ---
print("\n=== Common Patterns ===")

# Pattern 1: Accumulator
total = 0
for n in range(1, 11):
    total += n
print(f"Sum 1-10: {total}")

# Pattern 2: Building a list
squares = []
for n in range(1, 6):
    squares.append(n ** 2)
print(f"Squares: {squares}")

# Pattern 3: Filtering
numbers = [1, -2, 3, -4, 5, -6]
positives = []
for n in numbers:
    if n > 0:
        positives.append(n)
print(f"Positives: {positives}")

# Pattern 4: Finding max/min
values = [34, 67, 12, 89, 45]
maximum = values[0]
for v in values[1:]:
    if v > maximum:
        maximum = v
print(f"Max: {maximum}")

# --- Infinite loop with break (common pattern) ---
print("\n=== Loop until condition ===")
import random
random.seed(42)
attempts = 0
while True:
    num = random.randint(1, 10)
    attempts += 1
    if num == 7:
        print(f"Got 7 after {attempts} attempts!")
        break
