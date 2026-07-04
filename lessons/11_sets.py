# Lesson 11: Sets

# Sets are unordered collections of UNIQUE elements (like HashSet in Java)

# --- Creating Sets ---
print("=== Creating Sets ===")
empty = set()         # NOT {} — that's an empty dict!
numbers = {1, 2, 3, 4, 5}
mixed = {1, "hello", 3.14, True}  # Note: True == 1, so only one kept
print(mixed)  # {1, 'hello', 3.14} — True/1 deduplicated

# From other iterables
from_list = set([1, 2, 2, 3, 3, 3])
print(from_list)  # {1, 2, 3}

from_string = set("mississippi")
print(from_string)  # {'m', 'i', 's', 'p'} — unique chars

# Set comprehension
evens = {x for x in range(20) if x % 2 == 0}
print(evens)

# --- Adding & Removing ---
print("\n=== Adding & Removing ===")
s = {1, 2, 3}

s.add(4)          # add single element
print(s)          # {1, 2, 3, 4}

s.add(3)          # already exists — no effect
print(s)          # {1, 2, 3, 4}

s.update([5, 6, 7])  # add multiple elements
print(s)              # {1, 2, 3, 4, 5, 6, 7}

s.remove(7)       # remove — raises KeyError if missing
print(s)

s.discard(99)     # discard — no error if missing
print(s)          # same as before

popped = s.pop()  # remove and return arbitrary element
print(f"popped: {popped}, remaining: {s}")

s.clear()         # remove all
print(s)          # set()

# --- Set Operations (the real power!) ---
print("\n=== Set Operations ===")
a = {1, 2, 3, 4, 5}
b = {4, 5, 6, 7, 8}

# Union (all elements from both)
print(f"a | b  = {a | b}")          # {1, 2, 3, 4, 5, 6, 7, 8}
print(f"union  = {a.union(b)}")

# Intersection (elements in both)
print(f"a & b  = {a & b}")          # {4, 5}
print(f"inter  = {a.intersection(b)}")

# Difference (in a but not in b)
print(f"a - b  = {a - b}")          # {1, 2, 3}
print(f"diff   = {a.difference(b)}")

# Symmetric difference (in either but not both)
print(f"a ^ b  = {a ^ b}")          # {1, 2, 3, 6, 7, 8}
print(f"sym_diff = {a.symmetric_difference(b)}")

# --- In-place Operations ---
print("\n=== In-place Operations ===")
s = {1, 2, 3, 4, 5}

s |= {6, 7}       # union update
print(s)           # {1, 2, 3, 4, 5, 6, 7}

s &= {2, 4, 6, 8}  # intersection update
print(s)            # {2, 4, 6}

s -= {4}           # difference update
print(s)           # {2, 6}

# --- Subset / Superset / Disjoint ---
print("\n=== Relationships ===")
a = {1, 2, 3}
b = {1, 2, 3, 4, 5}
c = {6, 7, 8}

print(a <= b)          # True — a is subset of b
print(a.issubset(b))   # True

print(b >= a)          # True — b is superset of a
print(b.issuperset(a)) # True

print(a < b)           # True — a is PROPER subset (not equal)
print(a < a)           # False — not proper subset of itself

print(a.isdisjoint(c)) # True — no common elements
print(a.isdisjoint(b)) # False — have common elements

# --- Frozen Sets (immutable sets) ---
print("\n=== frozenset ===")
fs = frozenset([1, 2, 3, 4])
print(fs)         # frozenset({1, 2, 3, 4})
# fs.add(5)      # AttributeError! — immutable

# Can be used as dict keys or set members (hashable)
seen_groups = {frozenset({1, 2}), frozenset({3, 4})}
print(frozenset({1, 2}) in seen_groups)  # True

# --- Practical Examples ---
print("\n=== Practical Examples ===")

# 1. Remove duplicates (preserving order with dict trick)
items = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]
unique_ordered = list(dict.fromkeys(items))
unique_unordered = list(set(items))
print(f"ordered:   {unique_ordered}")    # [3, 1, 4, 5, 9, 2, 6]
print(f"unordered: {unique_unordered}")  # order not guaranteed

# 2. Find common/different elements
enrolled_math = {"Alice", "Bob", "Charlie", "Diana"}
enrolled_science = {"Bob", "Diana", "Eve", "Frank"}

both = enrolled_math & enrolled_science
print(f"Both classes: {both}")           # {'Bob', 'Diana'}

only_math = enrolled_math - enrolled_science
print(f"Only math: {only_math}")         # {'Alice', 'Charlie'}

either = enrolled_math | enrolled_science
print(f"Any class: {either}")

# 3. Fast membership testing (O(1) vs O(n) for list)
valid_codes = {"US", "UK", "CA", "AU", "DE", "FR", "JP"}
code = "CA"
if code in valid_codes:  # O(1) lookup
    print(f"{code} is valid")

# 4. Find duplicates
nums = [1, 2, 3, 2, 4, 5, 3, 6]
seen = set()
duplicates = set()
for n in nums:
    if n in seen:
        duplicates.add(n)
    seen.add(n)
print(f"Duplicates: {duplicates}")  # {2, 3}

# One-liner for duplicates
dupes = {x for x in nums if nums.count(x) > 1}
print(f"Duplicates: {dupes}")  # {2, 3}

# 5. Set as a visited tracker (BFS/DFS)
def find_connected(graph, start):
    visited = set()
    queue = [start]
    while queue:
        node = queue.pop(0)
        if node not in visited:
            visited.add(node)
            queue.extend(graph.get(node, []))
    return visited

graph = {
    "A": ["B", "C"],
    "B": ["A", "D"],
    "C": ["A", "D"],
    "D": ["B", "C", "E"],
    "E": ["D"],
}
print(f"Connected to A: {find_connected(graph, 'A')}")

# 6. Compare lists efficiently
list1 = [1, 2, 3, 4, 5]
list2 = [3, 4, 5, 6, 7]
added = set(list2) - set(list1)
removed = set(list1) - set(list2)
print(f"Added: {added}, Removed: {removed}")

# --- Performance Comparison ---
print("\n=== Performance ===")
print("""
| Operation          | set    | list   |
|--------------------|--------|--------|
| x in collection    | O(1)   | O(n)   |
| add/append         | O(1)   | O(1)   |
| remove             | O(1)   | O(n)   |
| union (a | b)      | O(n+m) | —      |
| intersection       | O(min) | —      |

Rule: if you only need membership checks and don't
care about order or duplicates, use a set!
""")
