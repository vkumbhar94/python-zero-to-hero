# Lesson 10: Dictionaries

# Dicts are key-value pairs (like HashMap in Java, object in JS)

# --- Creating Dictionaries ---
print("=== Creating Dicts ===")
empty = {}
person = {"name": "Alice", "age": 30, "city": "NYC"}
print(person)

# dict() constructor
from_pairs = dict([("a", 1), ("b", 2), ("c", 3)])
from_kwargs = dict(name="Bob", age=25)
print(from_pairs)
print(from_kwargs)

# dict comprehension
squares = {x: x**2 for x in range(1, 6)}
print(squares)  # {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# --- Accessing Values ---
print("\n=== Accessing ===")
person = {"name": "Alice", "age": 30, "city": "NYC"}

print(person["name"])    # Alice
# print(person["email"])  # KeyError!

# .get() — safe access with default
print(person.get("name"))          # Alice
print(person.get("email"))         # None (no error)
print(person.get("email", "N/A")) # N/A (custom default)

# --- Adding / Updating ---
print("\n=== Adding / Updating ===")
d = {"a": 1, "b": 2}

d["c"] = 3          # add new key
d["a"] = 10         # update existing
print(d)            # {'a': 10, 'b': 2, 'c': 3}

# update() — merge another dict
d.update({"b": 20, "d": 4})
print(d)            # {'a': 10, 'b': 20, 'c': 3, 'd': 4}

# | operator (Python 3.9+) — merge dicts
defaults = {"color": "red", "size": "M", "debug": False}
overrides = {"color": "blue", "debug": True}
config = defaults | overrides
print(config)  # {'color': 'blue', 'size': 'M', 'debug': True}

# |= for in-place merge
defaults |= overrides
print(defaults)

# setdefault — set only if key doesn't exist
d = {"a": 1}
d.setdefault("a", 99)  # already exists, no change
d.setdefault("b", 99)  # doesn't exist, sets it
print(d)  # {'a': 1, 'b': 99}

# --- Removing ---
print("\n=== Removing ===")
d = {"a": 1, "b": 2, "c": 3, "d": 4}

# del
del d["a"]
print(d)  # {'b': 2, 'c': 3, 'd': 4}

# pop — remove and return value
val = d.pop("b")
print(val, d)  # 2 {'c': 3, 'd': 4}

# pop with default (no error if missing)
val = d.pop("z", None)
print(val)  # None

# popitem — remove last inserted pair
d = {"x": 1, "y": 2, "z": 3}
last = d.popitem()
print(last, d)  # ('z', 3) {'x': 1, 'y': 2}

# clear
d.clear()
print(d)  # {}

# --- Iterating ---
print("\n=== Iterating ===")
scores = {"Alice": 85, "Bob": 92, "Charlie": 78}

# Keys (default iteration)
for name in scores:
    print(f"  {name}")

# Values
for score in scores.values():
    print(f"  {score}")

# Key-value pairs
for name, score in scores.items():
    print(f"  {name}: {score}")

# --- Checking Membership ---
print("\n=== Membership ===")
d = {"a": 1, "b": 2, "c": 3}

print("a" in d)       # True (checks keys)
print(1 in d)         # False (doesn't check values)
print("z" not in d)   # True

# --- Dict Comprehensions ---
print("\n=== Comprehensions ===")

# Basic
squares = {n: n**2 for n in range(1, 6)}
print(squares)

# With condition
even_squares = {n: n**2 for n in range(1, 11) if n % 2 == 0}
print(even_squares)  # {2: 4, 4: 16, 6: 36, 8: 64, 10: 100}

# Invert a dict (swap keys and values)
original = {"a": 1, "b": 2, "c": 3}
inverted = {v: k for k, v in original.items()}
print(inverted)  # {1: 'a', 2: 'b', 3: 'c'}

# Filter a dict
scores = {"Alice": 85, "Bob": 92, "Charlie": 78, "Diana": 95}
top_scores = {k: v for k, v in scores.items() if v >= 90}
print(top_scores)  # {'Bob': 92, 'Diana': 95}

# Transform values
doubled = {k: v * 2 for k, v in scores.items()}
print(doubled)

# --- Nested Dicts ---
print("\n=== Nested Dicts ===")
users = {
    "alice": {
        "age": 30,
        "email": "alice@example.com",
        "hobbies": ["reading", "coding"],
    },
    "bob": {
        "age": 25,
        "email": "bob@example.com",
        "hobbies": ["gaming", "cooking"],
    },
}

print(users["alice"]["email"])
print(users["bob"]["hobbies"][0])

# Safe nested access
def get_nested(d, *keys, default=None):
    for key in keys:
        if isinstance(d, dict):
            d = d.get(key, default)
        else:
            return default
    return d

print(get_nested(users, "alice", "age"))          # 30
print(get_nested(users, "alice", "phone"))         # None
print(get_nested(users, "nobody", "email"))        # None

# --- Common Patterns ---
print("\n=== Common Patterns ===")

# 1. Counting (prefer Counter, but good to know)
words = "the cat sat on the mat the cat".split()
counts = {}
for word in words:
    counts[word] = counts.get(word, 0) + 1
print(counts)  # {'the': 3, 'cat': 2, 'sat': 1, 'on': 1, 'mat': 1}

# 2. Grouping
students = [
    ("Alice", "A"), ("Bob", "B"), ("Charlie", "A"),
    ("Diana", "B"), ("Eve", "A"),
]
groups = {}
for name, grade in students:
    groups.setdefault(grade, []).append(name)
print(groups)  # {'A': ['Alice', 'Charlie', 'Eve'], 'B': ['Bob', 'Diana']}

# 3. Dict as switch/dispatch
def add(a, b): return a + b
def sub(a, b): return a - b
def mul(a, b): return a * b

operations = {"+": add, "-": sub, "*": mul}
op = "+"
result = operations[op](10, 3)
print(f"10 {op} 3 = {result}")  # 13

# 4. Merge multiple dicts
d1 = {"a": 1, "b": 2}
d2 = {"c": 3, "d": 4}
d3 = {"e": 5}
merged = {**d1, **d2, **d3}  # unpack operator
print(merged)  # {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}

# 5. Sort dict by value
scores = {"Alice": 85, "Bob": 92, "Charlie": 78}
sorted_by_score = dict(sorted(scores.items(), key=lambda item: item[1], reverse=True))
print(sorted_by_score)  # {'Bob': 92, 'Alice': 85, 'Charlie': 78}

# --- Views are Dynamic ---
print("\n=== Views ===")
d = {"a": 1, "b": 2}
keys = d.keys()
print(keys)     # dict_keys(['a', 'b'])

d["c"] = 3     # modify the dict
print(keys)     # dict_keys(['a', 'b', 'c']) — view updated!

# Views support set operations
d1 = {"a": 1, "b": 2, "c": 3}
d2 = {"b": 2, "c": 4, "d": 5}
print(d1.keys() & d2.keys())   # {'b', 'c'} — common keys
print(d1.keys() - d2.keys())   # {'a'} — keys only in d1
print(d1.keys() | d2.keys())   # {'a', 'b', 'c', 'd'} — all keys

# --- Performance Notes ---
print("\n=== Performance ===")
print("""
| Operation      | Time Complexity |
|----------------|-----------------|
| d[key]         | O(1) average    |
| key in d       | O(1) average    |
| d[key] = val   | O(1) average    |
| del d[key]     | O(1) average    |
| for k in d     | O(n)            |
| len(d)         | O(1)            |
""")
