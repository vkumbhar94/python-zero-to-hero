# Lesson 8b: Java-like Streams & Collections Module

# ============================================================
# PART 1: Chaining operations (Java Stream-like patterns)
# ============================================================

print("=== Java Streams vs Python ===")

# Java: list.stream().filter(...).map(...).collect(...)
# Python has several approaches:

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# --- Approach 1: Nested map/filter (not great readability) ---
print("\n--- map/filter (functional) ---")

# Get squares of even numbers
result = list(map(lambda x: x ** 2, filter(lambda x: x % 2 == 0, numbers)))
print(result)  # [4, 16, 36, 64, 100]

# Chain: filter → map → reduce
from functools import reduce

# Sum of squares of even numbers
result = reduce(
    lambda acc, x: acc + x,
    map(lambda x: x ** 2, filter(lambda x: x % 2 == 0, numbers))
)
print(result)  # 220

# Problem: reads inside-out, hard to follow

# --- Approach 2: List comprehensions (Pythonic!) ---
print("\n--- List comprehensions (preferred) ---")

# Same thing, much more readable
result = [x ** 2 for x in numbers if x % 2 == 0]
print(result)  # [4, 16, 36, 64, 100]

# Sum of squares of evens
result = sum(x ** 2 for x in numbers if x % 2 == 0)
print(result)  # 220

# --- Approach 3: Generator chaining (lazy, memory efficient) ---
print("\n--- Generator chaining (lazy) ---")

# Like Java streams, generators are lazy — process one item at a time
def stream_example():
    data = range(1, 11)
    evens = (x for x in data if x % 2 == 0)       # lazy filter
    squares = (x ** 2 for x in evens)               # lazy map
    big = (x for x in squares if x > 10)            # lazy filter
    return list(big)

print(stream_example())  # [16, 36, 64, 100]

# --- Approach 4: Build your own Stream class ---
print("\n--- Custom Stream class (Java-like chaining) ---")

class Stream:
    def __init__(self, data):
        self._data = iter(data)

    def filter(self, predicate):
        self._data = (x for x in self._data if predicate(x))
        return self  # enables chaining

    def map(self, func):
        self._data = (func(x) for x in self._data)
        return self

    def flat_map(self, func):
        self._data = (item for x in self._data for item in func(x))
        return self

    def peek(self, func):
        def _peek(x):
            func(x)
            return x
        self._data = (_peek(x) for x in self._data)
        return self

    def limit(self, n):
        from itertools import islice
        self._data = islice(self._data, n)
        return self

    def skip(self, n):
        from itertools import islice
        self._data = islice(self._data, n, None)
        return self

    def sorted(self, key=None, reverse=False):
        self._data = iter(sorted(self._data, key=key, reverse=reverse))
        return self

    def distinct(self):
        seen = set()
        def _unique(data):
            for x in data:
                if x not in seen:
                    seen.add(x)
                    yield x
        self._data = _unique(self._data)
        return self

    # Terminal operations
    def to_list(self):
        return list(self._data)

    def to_set(self):
        return set(self._data)

    def count(self):
        return sum(1 for _ in self._data)

    def first(self, default=None):
        return next(self._data, default)

    def reduce(self, func, initial=None):
        if initial is not None:
            return reduce(func, self._data, initial)
        return reduce(func, self._data)

    def for_each(self, func):
        for x in self._data:
            func(x)

    def any_match(self, predicate):
        return any(predicate(x) for x in self._data)

    def all_match(self, predicate):
        return all(predicate(x) for x in self._data)


# Now use it like Java streams!
result = (
    Stream(range(1, 21))
    .filter(lambda x: x % 2 == 0)
    .map(lambda x: x ** 2)
    .filter(lambda x: x > 50)
    .sorted(reverse=True)
    .limit(3)
    .to_list()
)
print(result)  # [400, 324, 256]

# More examples
words = ["hello", "world", "hi", "python", "hey", "help"]
result = (
    Stream(words)
    .filter(lambda w: w.startswith("h"))
    .map(str.upper)
    .sorted(key=len)
    .to_list()
)
print(result)  # ['HI', 'HEY', 'HELP', 'HELLO']

# distinct
result = Stream([1, 2, 2, 3, 3, 3, 4]).distinct().to_list()
print(result)  # [1, 2, 3, 4]

# reduce (sum)
total = Stream(range(1, 11)).reduce(lambda a, b: a + b)
print(total)  # 55

# any_match / all_match
print(Stream([1, 2, 3, 4]).any_match(lambda x: x > 3))  # True
print(Stream([1, 2, 3, 4]).all_match(lambda x: x > 0))  # True

# --- Approach 5: itertools (Python's stream toolkit) ---
print("\n--- itertools (standard library) ---")
import itertools

numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# chain — concatenate iterables
combined = list(itertools.chain([1, 2], [3, 4], [5, 6]))
print(f"chain: {combined}")  # [1, 2, 3, 4, 5, 6]

# islice — slice an iterator (like .limit/.skip)
first_5 = list(itertools.islice(range(100), 5))
print(f"islice: {first_5}")  # [0, 1, 2, 3, 4]

# takewhile / dropwhile — take/drop while condition is true
taken = list(itertools.takewhile(lambda x: x < 5, numbers))
print(f"takewhile: {taken}")  # [1, 2, 3, 4]

dropped = list(itertools.dropwhile(lambda x: x < 5, numbers))
print(f"dropwhile: {dropped}")  # [5, 6, 7, 8, 9, 10]

# accumulate — running totals (like scan in Java)
running = list(itertools.accumulate(numbers))
print(f"accumulate: {running}")  # [1, 3, 6, 10, 15, 21, 28, 36, 45, 55]

# product — cartesian product
pairs = list(itertools.product("AB", [1, 2]))
print(f"product: {pairs}")  # [('A', 1), ('A', 2), ('B', 1), ('B', 2)]

# groupby — group consecutive items (must be sorted first!)
data = sorted(["apple", "avocado", "banana", "blueberry", "cherry"], key=lambda x: x[0])
for key, group in itertools.groupby(data, key=lambda x: x[0]):
    print(f"  {key}: {list(group)}")

# combinations and permutations
print(f"combinations: {list(itertools.combinations([1,2,3], 2))}")
print(f"permutations: {list(itertools.permutations([1,2,3], 2))}")


# ============================================================
# PART 2: collections module
# ============================================================

print("\n" + "=" * 60)
print("=== collections module ===")
print("=" * 60)
from collections import (
    namedtuple, deque, Counter, OrderedDict,
    defaultdict, ChainMap
)

# --- namedtuple: lightweight immutable class ---
print("\n--- namedtuple ---")

Point = namedtuple("Point", ["x", "y"])
p = Point(3, 4)
print(p)        # Point(x=3, y=4)
print(p.x)     # 3 (access by name)
print(p[0])    # 3 (access by index)
# p.x = 5     # ERROR — immutable!

# Use like a struct/record
User = namedtuple("User", "name age email")
alice = User("Alice", 30, "alice@example.com")
print(f"{alice.name} is {alice.age}")

# Convert to dict
print(alice._asdict())

# Create from dict
data = {"name": "Bob", "age": 25, "email": "bob@ex.com"}
bob = User(**data)
print(bob)

# --- deque: double-ended queue ---
print("\n--- deque ---")

dq = deque([1, 2, 3, 4, 5])

# O(1) operations on both ends
dq.appendleft(0)     # add to left
dq.append(6)         # add to right
print(dq)            # deque([0, 1, 2, 3, 4, 5, 6])

dq.popleft()         # remove from left
dq.pop()             # remove from right
print(dq)            # deque([1, 2, 3, 4, 5])

# Rotate
dq.rotate(2)         # rotate right by 2
print(dq)            # deque([4, 5, 1, 2, 3])
dq.rotate(-2)        # rotate left by 2
print(dq)            # deque([1, 2, 3, 4, 5])

# maxlen — bounded deque (like a sliding window)
recent = deque(maxlen=3)
for i in range(5):
    recent.append(i)
    print(f"  append {i}: {list(recent)}")
# Only keeps last 3 items!

# --- Counter: count occurrences ---
print("\n--- Counter ---")

# Count from iterable
word = "mississippi"
c = Counter(word)
print(c)  # Counter({'s': 4, 'i': 4, 'p': 2, 'm': 1})

# Most common
print(c.most_common(2))  # [('s', 4), ('i', 4)]

# Count from list
colors = ["red", "blue", "red", "green", "blue", "red"]
color_count = Counter(colors)
print(color_count)  # Counter({'red': 3, 'blue': 2, 'green': 1})

# Arithmetic with Counters
c1 = Counter(a=3, b=1)
c2 = Counter(a=1, b=2)
print(c1 + c2)  # Counter({'a': 4, 'b': 3})
print(c1 - c2)  # Counter({'a': 2}) — drops zero/negative

# Total count
print(c1.total())  # 4

# --- defaultdict: dict with default factory ---
print("\n--- defaultdict ---")

# Regular dict raises KeyError for missing keys
# defaultdict provides a default value

# Group items
words = ["apple", "bat", "car", "apple", "bat", "apple"]
grouped = defaultdict(list)
for word in words:
    grouped[word].append(word)
print(dict(grouped))

# Count (like Counter but manual)
counts = defaultdict(int)  # default is 0
for word in words:
    counts[word] += 1
print(dict(counts))  # {'apple': 3, 'bat': 2, 'car': 1}

# Set as default
index = defaultdict(set)
data = [("color", "red"), ("color", "blue"), ("size", "large"), ("color", "red")]
for key, value in data:
    index[key].add(value)
print(dict(index))  # {'color': {'red', 'blue'}, 'size': {'large'}}

# Nested defaultdict (like Java's Map<String, Map<String, Integer>>)
tree = lambda: defaultdict(tree)
taxonomy = tree()
taxonomy["animal"]["mammal"]["dog"] = "woof"
taxonomy["animal"]["mammal"]["cat"] = "meow"
taxonomy["animal"]["bird"]["eagle"] = "screech"
print(taxonomy["animal"]["mammal"]["dog"])  # woof

# --- OrderedDict: remembers insertion order ---
print("\n--- OrderedDict ---")
# Note: regular dict preserves insertion order since Python 3.7
# OrderedDict is still useful for:

od = OrderedDict()
od["b"] = 2
od["a"] = 1
od["c"] = 3

# 1. move_to_end
od.move_to_end("b")       # move to end
print(list(od.keys()))    # ['a', 'c', 'b']
od.move_to_end("b", last=False)  # move to beginning
print(list(od.keys()))    # ['b', 'a', 'c']

# 2. Equality considers order
od1 = OrderedDict([("a", 1), ("b", 2)])
od2 = OrderedDict([("b", 2), ("a", 1)])
print(od1 == od2)  # False (order matters)

d1 = {"a": 1, "b": 2}
d2 = {"b": 2, "a": 1}
print(d1 == d2)  # True (regular dict ignores order)

# 3. LRU cache pattern
class LRU(OrderedDict):
    def __init__(self, capacity):
        super().__init__()
        self.capacity = capacity

    def get(self, key):
        if key in self:
            self.move_to_end(key)
            return self[key]
        return -1

    def put(self, key, value):
        if key in self:
            self.move_to_end(key)
        self[key] = value
        if len(self) > self.capacity:
            self.popitem(last=False)

cache = LRU(3)
cache.put("a", 1)
cache.put("b", 2)
cache.put("c", 3)
cache.get("a")      # moves 'a' to end
cache.put("d", 4)   # evicts 'b' (least recently used)
print(list(cache.keys()))  # ['c', 'a', 'd']

# --- ChainMap: combine multiple dicts ---
print("\n--- ChainMap ---")

defaults = {"color": "red", "size": "medium", "debug": False}
user_settings = {"color": "blue"}
cli_args = {"debug": True}

# ChainMap searches dicts in order (first match wins)
config = ChainMap(cli_args, user_settings, defaults)
print(config["color"])  # blue (from user_settings)
print(config["size"])   # medium (from defaults)
print(config["debug"])  # True (from cli_args)

# Great for layered configuration!
print(dict(config))  # merged view


# ============================================================
# PART 3: Quick comparison table
# ============================================================

print("\n" + "=" * 60)
print("=== When to use what ===")
print("=" * 60)
print("""
| Need                          | Use                    |
|-------------------------------|------------------------|
| Count occurrences             | Counter                |
| Dict with default values      | defaultdict            |
| Immutable struct/record       | namedtuple / dataclass |
| Fast append/pop both ends     | deque                  |
| Sliding window / bounded buf  | deque(maxlen=N)        |
| Order-aware dict comparison   | OrderedDict            |
| Layered config / scope chain  | ChainMap               |
| Lazy chained transforms       | generator expressions  |
| Java-like stream API          | custom Stream class    |
""")
