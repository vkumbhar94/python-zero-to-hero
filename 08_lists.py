# Lesson 8: Lists

# --- Creating Lists ---
print("=== Creating Lists ===")
empty = []
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", 3.14, True, None]  # can mix types
nested = [[1, 2], [3, 4], [5, 6]]

print(numbers)
print(mixed)
print(nested)

# --- Indexing and Slicing (same as strings) ---
print("\n=== Indexing & Slicing ===")
fruits = ["apple", "banana", "cherry", "date", "elderberry"]

print(fruits[0])     # apple
print(fruits[-1])    # elderberry
print(fruits[1:3])   # ['banana', 'cherry']
print(fruits[::2])   # ['apple', 'cherry', 'elderberry']
print(fruits[::-1])  # reversed

# --- Modifying Lists (mutable!) ---
print("\n=== Modifying ===")
nums = [1, 2, 3, 4, 5]

# Change single item
nums[0] = 10
print(nums)  # [10, 2, 3, 4, 5]

# Change a slice
nums[1:3] = [20, 30]
print(nums)  # [10, 20, 30, 4, 5]

# Delete items
del nums[0]
print(nums)  # [20, 30, 4, 5]

# --- Adding Items ---
print("\n=== Adding Items ===")
lst = [1, 2, 3]

lst.append(4)          # add to end
print(lst)             # [1, 2, 3, 4]

lst.insert(0, 0)       # insert at index
print(lst)             # [0, 1, 2, 3, 4]

lst.extend([5, 6, 7])  # add multiple items
print(lst)             # [0, 1, 2, 3, 4, 5, 6, 7]

# + creates a NEW list (doesn't modify in place)
new = lst + [8, 9]
print(new)             # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# * repeats
print([0] * 5)         # [0, 0, 0, 0, 0]

# --- Removing Items ---
print("\n=== Removing Items ===")
items = ["a", "b", "c", "b", "d"]

items.remove("b")     # removes FIRST occurrence
print(items)          # ['a', 'c', 'b', 'd']

popped = items.pop()  # removes and returns last item
print(popped, items)  # d ['a', 'c', 'b']

popped = items.pop(0) # removes at index
print(popped, items)  # a ['c', 'b']

items.clear()         # remove all
print(items)          # []

# --- Searching ---
print("\n=== Searching ===")
nums = [10, 20, 30, 20, 40]

print(20 in nums)        # True (membership test)
print(99 not in nums)    # True
print(nums.index(20))    # 1 (first occurrence)
print(nums.count(20))    # 2 (how many times)

# index() raises ValueError if not found — check with 'in' first
if 30 in nums:
    print(f"30 is at index {nums.index(30)}")

# --- Sorting ---
print("\n=== Sorting ===")
nums = [3, 1, 4, 1, 5, 9, 2, 6]

# sorted() — returns NEW sorted list (original unchanged)
print(sorted(nums))              # [1, 1, 2, 3, 4, 5, 6, 9]
print(sorted(nums, reverse=True))  # [9, 6, 5, 4, 3, 2, 1, 1]
print(nums)                      # [3, 1, 4, 1, 5, 9, 2, 6] (unchanged)

# .sort() — sorts in place (returns None!)
nums.sort()
print(nums)  # [1, 1, 2, 3, 4, 5, 6, 9]

# Sort with key function
words = ["banana", "apple", "cherry", "date"]
print(sorted(words))                    # alphabetical
print(sorted(words, key=len))           # by length
print(sorted(words, key=lambda w: w[-1]))  # by last character

# .reverse() — reverses in place
nums.reverse()
print(nums)  # [9, 6, 5, 4, 3, 2, 1, 1]

# --- Copying Lists ---
print("\n=== Copying ===")
original = [1, 2, 3]

# Assignment does NOT copy — both point to same list!
not_a_copy = original
not_a_copy.append(4)
print(original)  # [1, 2, 3, 4] — original modified!

# Shallow copy (3 ways)
original = [1, 2, 3]
copy1 = original.copy()
copy2 = original[:]
copy3 = list(original)

copy1.append(99)
print(original)  # [1, 2, 3] — safe!
print(copy1)     # [1, 2, 3, 99]

# CAUTION: shallow copy doesn't copy nested objects
nested = [[1, 2], [3, 4]]
shallow = nested.copy()
shallow[0][0] = 99
print(nested)   # [[99, 2], [3, 4]] — inner list was shared!

# Deep copy for nested structures
import copy
nested = [[1, 2], [3, 4]]
deep = copy.deepcopy(nested)
deep[0][0] = 99
print(nested)  # [[1, 2], [3, 4]] — safe!
print(deep)    # [[99, 2], [3, 4]]

# --- Useful Patterns ---
print("\n=== Useful Patterns ===")

# Unpack a list
first, second, *rest = [1, 2, 3, 4, 5]
print(f"first={first}, second={second}, rest={rest}")
# first=1, second=2, rest=[3, 4, 5]

head, *middle, tail = [1, 2, 3, 4, 5]
print(f"head={head}, middle={middle}, tail={tail}")
# head=1, middle=[2, 3, 4], tail=5

# Check if list is empty
items = []
if not items:
    print("List is empty")

# Flatten a 2D list
matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
flat = [item for row in matrix for item in row]
print(flat)  # [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Remove duplicates (preserving order)
nums = [1, 3, 2, 3, 1, 4, 2]
unique = list(dict.fromkeys(nums))
print(unique)  # [1, 3, 2, 4]

# --- List as Stack (LIFO) ---
print("\n=== Stack (LIFO) ===")
stack = []
stack.append("a")  # push
stack.append("b")
stack.append("c")
print(stack)        # ['a', 'b', 'c']
print(stack.pop())  # c (last in, first out)
print(stack)        # ['a', 'b']

# --- List as Queue (FIFO) — use deque for performance ---
print("\n=== Queue (FIFO) ===")
from collections import deque

queue = deque(["a", "b", "c"])
queue.append("d")       # add to right
print(queue.popleft())  # a (first in, first out)
print(queue)            # deque(['b', 'c', 'd'])
