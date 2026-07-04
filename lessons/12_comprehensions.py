# Lesson 12: Comprehensions (List, Dict, Set, Generator)

# Comprehensions are Python's concise syntax for creating collections
# They replace verbose for-loop patterns with a single readable expression

# --- List Comprehensions ---
print("=== List Comprehensions ===")

# Basic: [expression for item in iterable]
squares = [x**2 for x in range(1, 11)]
print(squares)  # [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]

# With filter: [expression for item in iterable if condition]
even_squares = [x**2 for x in range(1, 11) if x % 2 == 0]
print(even_squares)  # [4, 16, 36, 64, 100]

# Equivalent loop form:
result = []
for x in range(1, 11):
    if x % 2 == 0:
        result.append(x**2)
print(result)  # same

# --- if/else in comprehension (ternary in expression) ---
print("\n=== if/else (ternary) ===")

# Note: if/else goes BEFORE for (it's part of the expression)
labels = ["even" if x % 2 == 0 else "odd" for x in range(1, 6)]
print(labels)  # ['odd', 'even', 'odd', 'even', 'odd']

# vs filter which goes AFTER for
only_evens = [x for x in range(1, 6) if x % 2 == 0]
print(only_evens)  # [2, 4]

# Combine both: transform + filter
result = [x**2 if x > 0 else 0 for x in [-2, -1, 0, 1, 2] if x != 0]
print(result)  # [0, 0, 1, 4] — filtered out 0; negatives become 0, positives squared

# --- Nested Loops in Comprehension ---
print("\n=== Nested Loops ===")

# Flatten 2D list
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [num for row in matrix for num in row]
print(flat)  # [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Equivalent:
# for row in matrix:
#     for num in row:
#         flat.append(num)

# Cartesian product
pairs = [(x, y) for x in range(3) for y in range(3)]
print(pairs)  # [(0,0), (0,1), (0,2), (1,0), ...]

# Nested with condition
pairs = [(x, y) for x in range(5) for y in range(5) if x != y]
print(f"Pairs where x != y: {len(pairs)} items")

# --- Nested List Comprehension (creating 2D structures) ---
print("\n=== Creating 2D Structures ===")

# 3x3 identity matrix
identity = [[1 if i == j else 0 for j in range(3)] for i in range(3)]
for row in identity:
    print(row)

# Transpose a matrix
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
transposed = [[row[i] for row in matrix] for i in range(3)]
print(f"\nOriginal:   {matrix}")
print(f"Transposed: {transposed}")

# --- Dict Comprehensions ---
print("\n=== Dict Comprehensions ===")

# {key_expr: value_expr for item in iterable}
squares_dict = {x: x**2 for x in range(1, 6)}
print(squares_dict)  # {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# Invert a dict
original = {"a": 1, "b": 2, "c": 3}
inverted = {v: k for k, v in original.items()}
print(inverted)  # {1: 'a', 2: 'b', 3: 'c'}

# Filter dict
scores = {"Alice": 85, "Bob": 92, "Charlie": 78, "Diana": 95}
passed = {k: v for k, v in scores.items() if v >= 80}
print(passed)  # {'Alice': 85, 'Bob': 92, 'Diana': 95}

# Transform keys/values
upper_scores = {k.upper(): v for k, v in scores.items()}
print(upper_scores)

# From two lists
keys = ["name", "age", "city"]
values = ["Alice", 30, "NYC"]
person = {k: v for k, v in zip(keys, values)}
print(person)  # {'name': 'Alice', 'age': 30, 'city': 'NYC'}

# --- Set Comprehensions ---
print("\n=== Set Comprehensions ===")

# {expression for item in iterable}
unique_lengths = {len(word) for word in ["hello", "world", "hi", "hey"]}
print(unique_lengths)  # {2, 3, 5}

# First letters
words = ["apple", "avocado", "banana", "blueberry", "cherry"]
first_chars = {w[0] for w in words}
print(first_chars)  # {'a', 'b', 'c'}

# --- Generator Expressions (lazy comprehension) ---
print("\n=== Generator Expressions ===")

# Use () instead of [] — doesn't build the whole list in memory
gen = (x**2 for x in range(1, 6))
print(gen)        # <generator object ...>
print(list(gen))  # [1, 4, 9, 16, 25] — consumed now

# Great for large data — only computes values as needed
big_sum = sum(x**2 for x in range(1_000_000))  # no list in memory!
print(f"Sum of squares 0..999999: {big_sum}")

# Can iterate once only
gen = (x for x in range(3))
print(next(gen))  # 0
print(next(gen))  # 1
print(next(gen))  # 2
# next(gen)       # StopIteration!

# Use directly in functions (no extra parentheses needed)
print(max(len(w) for w in ["hello", "world", "hi"]))  # 5
print(any(x > 100 for x in [1, 50, 200]))  # True
print(all(x > 0 for x in [1, 2, 3]))       # True
print(",".join(str(x) for x in range(5)))   # "0,1,2,3,4"

# --- When to Use What ---
print("\n=== Comprehension vs Generator ===")
print("""
| Use            | When                                    |
|----------------|-----------------------------------------|
| [list comp]    | Need the full list, or it's small       |
| (gen expr)     | Large/infinite data, only iterate once  |
| {set comp}     | Need unique values                      |
| {dict comp}    | Building a dict from transformation     |
""")

# --- Practical Examples ---
print("=== Practical Examples ===")

# 1. Parse CSV-like data
raw = "Alice:85,Bob:92,Charlie:78"
grades = {name: int(score) for name, score in
          (item.split(":") for item in raw.split(","))}
print(grades)  # {'Alice': 85, 'Bob': 92, 'Charlie': 78}

# 2. Flatten and filter in one step
data = [[1, -2, 3], [-4, 5, -6], [7, -8, 9]]
positives = [x for row in data for x in row if x > 0]
print(positives)  # [1, 3, 5, 7, 9]

# 3. Word frequency from text
text = "the cat sat on the mat the cat purred"
freq = {word: text.split().count(word) for word in set(text.split())}
print(freq)

# 4. File processing (generator for memory efficiency)
# lines = (line.strip() for line in open("file.txt"))
# non_empty = (line for line in lines if line)
# comments = (line for line in non_empty if line.startswith("#"))

# 5. Multiple transformations chained
names = ["  alice ", "BOB", " Charlie  "]
cleaned = [name.strip().title() for name in names]
print(cleaned)  # ['Alice', 'Bob', 'Charlie']

# 6. Create lookup table
words = ["hello", "world", "python", "code"]
by_length = {}
for word in words:
    by_length.setdefault(len(word), []).append(word)
# Same with comprehension (using itertools.groupby or this pattern):
from itertools import groupby
sorted_words = sorted(words, key=len)
by_length2 = {k: list(g) for k, g in groupby(sorted_words, key=len)}
print(by_length2)  # {4: ['code'], 5: ['hello', 'world'], 6: ['python']}

# --- Readability Guidelines ---
print("\n=== Readability Guidelines ===")
print("""
DO use comprehensions for:
  - Simple transforms: [x*2 for x in items]
  - Simple filters: [x for x in items if x > 0]
  - One level of nesting: [x for row in matrix for x in row]

DON'T use comprehensions when:
  - Logic is complex (use a regular loop)
  - More than 2 levels of nesting
  - Side effects are needed (printing, writing to file)
  - The line exceeds ~80 characters

Rule of thumb: if you can't read it in 5 seconds, use a loop.
""")
