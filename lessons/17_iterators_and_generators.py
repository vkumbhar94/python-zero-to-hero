# Lesson 17: Iterators & Generators

# --- What is an Iterator? ---
print("=== Iterator Protocol ===")

# Any object that implements __iter__() and __next__() is an iterator
# All for loops use iterators under the hood

# Behind the scenes of: for x in [1, 2, 3]
nums = [1, 2, 3]
it = iter(nums)       # calls nums.__iter__() → gets an iterator
print(next(it))       # 1 — calls it.__next__()
print(next(it))       # 2
print(next(it))       # 3
# next(it)            # StopIteration exception!

# Everything iterable: lists, tuples, dicts, strings, files, range...

# --- Building a Custom Iterator ---
print("\n=== Custom Iterator ===")

class Countdown:
    """Iterator that counts down from n to 1."""
    def __init__(self, n):
        self.n = n

    def __iter__(self):
        return self  # iterator returns itself

    def __next__(self):
        if self.n <= 0:
            raise StopIteration
        self.n -= 1
        return self.n + 1

for num in Countdown(5):
    print(num, end=" ")  # 5 4 3 2 1
print()

# --- Generators (the easy way to make iterators) ---
print("\n=== Generator Functions ===")

# 'yield' makes a function into a generator
# Each yield pauses the function and produces a value
# Next call resumes from where it left off

def countdown(n):
    while n > 0:
        yield n
        n -= 1

for num in countdown(5):
    print(num, end=" ")  # 5 4 3 2 1
print()

# Much simpler than writing a class with __iter__/__next__!

# --- How Generators Work ---
print("\n=== Generator Internals ===")

def simple_gen():
    print("  Start")
    yield 1
    print("  After first yield")
    yield 2
    print("  After second yield")
    yield 3
    print("  End")

gen = simple_gen()
print(type(gen))      # <class 'generator'>

print(next(gen))      # prints "Start", returns 1
print(next(gen))      # prints "After first yield", returns 2
print(next(gen))      # prints "After second yield", returns 3
# next(gen)           # prints "End", raises StopIteration

# --- Generator Expressions (one-liner generators) ---
print("\n=== Generator Expressions ===")

# List comprehension — builds entire list in memory
squares_list = [x**2 for x in range(1000000)]

# Generator expression — produces values lazily
squares_gen = (x**2 for x in range(1000000))

import sys
print(f"List size: {sys.getsizeof(squares_list):,} bytes")
print(f"Generator size: {sys.getsizeof(squares_gen)} bytes")  # ~200 bytes always!

# Use generators in any function that takes an iterable
print(sum(x**2 for x in range(10)))     # 285
print(max(x**2 for x in range(10)))     # 81
print(min(x**2 for x in range(10)))     # 0
print(sorted(x**2 for x in range(5)))   # [0, 1, 4, 9, 16]

# --- Practical Generator Patterns ---
print("\n=== Practical Patterns ===")

# 1. Infinite sequence
def naturals(start=1):
    n = start
    while True:
        yield n
        n += 1

# Take first 5 from infinite sequence
from itertools import islice
first_5 = list(islice(naturals(), 5))
print(f"First 5 naturals: {first_5}")

# 2. Fibonacci generator (infinite)
def fibonacci():
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b

fibs = list(islice(fibonacci(), 10))
print(f"Fibonacci: {fibs}")

# 3. Read large file lazily (line by line)
def read_lines(filename):
    with open(filename) as f:
        for line in f:
            yield line.strip()

# 4. Pipeline of generators (like Unix pipes)
def integers():
    n = 1
    while True:
        yield n
        n += 1

def evens(stream):
    for n in stream:
        if n % 2 == 0:
            yield n

def squares(stream):
    for n in stream:
        yield n ** 2

def take(n, stream):
    for _, val in zip(range(n), stream):
        yield val

# Pipeline: integers → filter evens → square → take 5
pipeline = take(5, squares(evens(integers())))
print(f"Pipeline: {list(pipeline)}")  # [4, 16, 36, 64, 100]

# 5. Flatten nested structure
def flatten(nested):
    for item in nested:
        if isinstance(item, (list, tuple)):
            yield from flatten(item)  # yield from = delegate to sub-generator
        else:
            yield item

data = [1, [2, 3], [4, [5, 6]], 7, [8, [9, [10]]]]
print(f"Flattened: {list(flatten(data))}")

# --- yield from (delegation) ---
print("\n=== yield from ===")

# Without yield from
def chain_manual(*iterables):
    for it in iterables:
        for item in it:
            yield item

# With yield from (cleaner)
def chain(*iterables):
    for it in iterables:
        yield from it

result = list(chain([1, 2], [3, 4], [5, 6]))
print(f"Chained: {result}")  # [1, 2, 3, 4, 5, 6]

# yield from with generator
def sub_gen():
    yield "a"
    yield "b"

def main_gen():
    yield 1
    yield from sub_gen()  # delegates to sub_gen
    yield 2

print(list(main_gen()))  # [1, 'a', 'b', 2]

# --- Sending Values to Generators ---
print("\n=== send() ===")

def accumulator():
    total = 0
    while True:
        value = yield total  # yield current total, receive new value
        if value is None:
            break
        total += value

acc = accumulator()
next(acc)          # prime the generator (advance to first yield)
print(acc.send(10))  # 10
print(acc.send(20))  # 30
print(acc.send(5))   # 35

# Running average
def running_average():
    total = 0
    count = 0
    average = None
    while True:
        value = yield average
        if value is None:
            break
        total += value
        count += 1
        average = total / count

avg = running_average()
next(avg)
print(f"avg after 10: {avg.send(10)}")    # 10.0
print(f"avg after 20: {avg.send(20)}")    # 15.0
print(f"avg after 30: {avg.send(30)}")    # 20.0

# --- Generator as Context Manager ---
print("\n=== Generator Context Manager ===")
from contextlib import contextmanager

@contextmanager
def timer(label):
    import time
    start = time.perf_counter()
    yield  # code inside 'with' block runs here
    elapsed = time.perf_counter() - start
    print(f"  {label}: {elapsed:.4f}s")

with timer("sum"):
    total = sum(range(1_000_000))
    print(f"  total = {total}")

# --- itertools Recipes with Generators ---
print("\n=== itertools + Generators ===")
from itertools import count, cycle, repeat, chain, tee

# count — infinite counter
print(f"count: {list(islice(count(10, 2), 5))}")  # [10, 12, 14, 16, 18]

# cycle — infinite cycling
print(f"cycle: {list(islice(cycle('ABC'), 7))}")  # ['A','B','C','A','B','C','A']

# repeat
print(f"repeat: {list(repeat('x', 3))}")  # ['x', 'x', 'x']

# tee — split one iterator into multiple independent copies
gen = (x**2 for x in range(5))
g1, g2 = tee(gen, 2)
print(f"tee g1: {list(g1)}")  # [0, 1, 4, 9, 16]
print(f"tee g2: {list(g2)}")  # [0, 1, 4, 9, 16] (independent copy)

# Pairwise (sliding window of 2)
def pairwise(iterable):
    a, b = tee(iterable)
    next(b, None)
    return zip(a, b)

print(f"pairwise: {list(pairwise([1, 2, 3, 4, 5]))}")
# [(1,2), (2,3), (3,4), (4,5)]

# --- Performance: Generator vs List ---
print("\n=== Performance ===")

import time

# List — builds everything in memory
start = time.perf_counter()
total = sum([x * x for x in range(5_000_000)])
list_time = time.perf_counter() - start

# Generator — lazy, constant memory
start = time.perf_counter()
total = sum(x * x for x in range(5_000_000))
gen_time = time.perf_counter() - start

print(f"List comp: {list_time:.3f}s")
print(f"Generator: {gen_time:.3f}s")
print(f"Generator is {'faster' if gen_time < list_time else 'slower'}")

print("""
=== When to Use What ===

| Use               | When                                      |
|--------------------|------------------------------------------|
| List               | Need random access, multiple iterations   |
| Generator function | Complex logic, state, infinite sequences  |
| Generator expr     | Simple transform/filter of large data     |
| Iterator class     | Need __len__, reversibility, or reset     |

Rule: if you only need to iterate ONCE through large data,
      use a generator. It saves memory and can be faster.
""")
