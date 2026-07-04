# Python Zero to Hero

A comprehensive, self-contained Python course — from your first `print("Hello, World!")` to design patterns and async programming. Every lesson is a single, runnable `.py` file packed with examples, explanations, and practical patterns.

## Getting Started

```bash
# Clone the repo
git clone https://github.com/vkumbhar94/python-zero-to-hero.git
cd python-zero-to-hero

# Run any lesson
python3 lessons/01_hello_world.py
python3 lessons/16_oop.py

# Run the test suite (Lesson 22)
pip install pytest
pytest lessons/test_22_testing.py -v
```

**Requirements:** Python 3.10+ (some features use 3.11+ syntax with graceful fallbacks).

## Course Outline

### Phase 1: Foundations

| # | Lesson | Key Topics |
|---|--------|------------|
| 01 | [Hello World](lessons/01_hello_world.py) | `print()` options (`sep`, `end`, `file`, `flush`), `input()`, built-in functions (`len`, `type`, `sorted`, `min`, `max`, `sum`, `isinstance`) |
| 02 | [Variables & Data Types](lessons/02_variables_and_types.py) | `int`, `float`, `str`, `bool`, `None`, type conversion, multiple assignment, swap |
| 03 | [Operators](lessons/03_operators.py) | Arithmetic, comparison, logical (`and`/`or`/`not`), identity (`is`), membership (`in`), bitwise, operator precedence, truthy/falsy values |
| 04 | [Strings](lessons/04_strings.py) | Indexing, slicing, string methods, f-strings, formatting, escape characters, raw strings, immutability |
| 05 | [Control Flow](lessons/05_control_flow.py) | `if`/`elif`/`else`, ternary expressions, `match`/`case` (3.10+), nested conditions, FizzBuzz |
| 06 | [Loops](lessons/06_loops.py) | `for`, `while`, `range()`, `enumerate()`, `zip()`, `zip_longest()`, `break`/`continue`, `for`/`else`, nested loops |
| 07 | [Functions](lessons/07_functions.py) | Parameters, defaults, `*args`/`**kwargs`, unpacking, lambda, `map`/`filter`, scope, `global`/`nonlocal`, closures, first-class functions, docstrings, type hints |

### Phase 2: Data Structures

| # | Lesson | Key Topics |
|---|--------|------------|
| 08 | [Lists](lessons/08_lists.py) | CRUD operations, sorting (`sort` vs `sorted`), copying (shallow vs deep), unpacking with `*`, stack/queue patterns, `deque` |
| 08b | [Streams & Collections](lessons/08b_streams_and_collections.py) | Java-like stream chaining, custom `Stream` class, `itertools` (`chain`, `islice`, `takewhile`, `groupby`, `accumulate`), `collections` module (`Counter`, `defaultdict`, `deque`, `namedtuple`, `OrderedDict`, `ChainMap`) |
| 09 | [Tuples](lessons/09_tuples.py) | Immutability, unpacking, as dict keys, `namedtuple`, `NamedTuple`, tuple comparison, when to use tuple vs list |
| 10 | [Dictionaries](lessons/10_dictionaries.py) | CRUD, `.get()`, merge (`\|`), comprehensions, nested dicts, views, set operations on keys, dispatch tables, sorting by value |
| 11 | [Sets](lessons/11_sets.py) | Set operations (`\|`, `&`, `-`, `^`), subset/superset, `frozenset`, deduplication, membership testing, finding duplicates |
| 12 | [Comprehensions](lessons/12_comprehensions.py) | List, dict, set comprehensions, generator expressions, nested loops, flattening, lazy evaluation, readability guidelines |

### Phase 3: Intermediate

| # | Lesson | Key Topics |
|---|--------|------------|
| 13 | [File I/O](lessons/13_file_io.py) | `with` statement, read/write modes, `pathlib.Path`, CSV (`csv.DictReader`), JSON (`json.load`/`dump`), binary files, temp files |
| 14 | [Error Handling](lessons/14_error_handling.py) | `try`/`except`/`else`/`finally`, exception hierarchy, custom exceptions, chaining (`from`), `contextlib.suppress`, EAFP vs LBYL, retry pattern, `ExceptionGroup` (3.11+) |
| 15 | [Modules & Packages](lessons/15_modules_and_packages.py) | Import styles, `__name__`/`__main__`, package structure, `__init__.py`, standard library highlights (`os`, `sys`, `datetime`, `re`, `functools`, `dataclasses`), pip/uv, virtual environments |
| 16 | [OOP](lessons/16_oop.py) | Classes, `__init__`, properties, inheritance, `super()`, method overriding, multiple inheritance, MRO, dunder methods (`__add__`, `__eq__`, `__iter__`, `__call__`), `@classmethod`/`@staticmethod`, ABC, `@dataclass`, `__slots__` |
| 17 | [Iterators & Generators](lessons/17_iterators_and_generators.py) | Iterator protocol, `yield`, generator expressions, `yield from`, `send()`, pipeline pattern, infinite sequences, `@contextmanager`, `itertools` recipes, performance comparison |

### Phase 4: Advanced

| # | Lesson | Key Topics |
|---|--------|------------|
| 18 | [Decorators](lessons/18_decorators.py) | `@functools.wraps`, timer/logger/retry/memoize decorators, decorators with arguments, stacking, class-based decorators, `@singleton`, `@functools.cache`/`lru_cache` |
| 19 | [Context Managers](lessons/19_context_managers.py) | `__enter__`/`__exit__`, `@contextmanager`, exception suppression, `ExitStack`, `redirect_stdout`, practical patterns (timer, transaction, `cd`) |
| 20 | [Concurrency](lessons/20_concurrency.py) | `threading` (Thread, Lock, Event, Semaphore), `ThreadPoolExecutor`, GIL, `multiprocessing` (Process, Queue, `ProcessPoolExecutor`), `asyncio` (`async`/`await`, `gather`, `create_task`, `TaskGroup`, async generators, semaphore, timeouts, `run_in_executor`) |
| 21 | [Type Hints](lessons/21_type_hints.py) | Basic hints, `Optional`/`Union`/`\|`, `Callable`, generics (`TypeVar`), `Literal`, `TypedDict`, `Protocol`, `Annotated`, `Final`, `Self`, `TypeGuard`, mypy/pyright |
| 22 | [Testing](lessons/22_testing.py) | pytest (`assert`, fixtures, `@parametrize`, markers, mocking, `capsys`), `conftest.py`, project structure, pytest commands, `unittest` comparison |
| 23 | [Design Patterns](lessons/23_design_patterns.py) | Singleton, Factory, Builder, Decorator (object), Adapter, Proxy, Observer, Strategy, Chain of Responsibility, Command (undo/redo), State Machine, Mixin, Descriptor |

## How to Use This Course

1. **Read & run** each file in order — every file is self-contained with inline comments explaining each concept.
2. **Experiment** — modify the examples, break things, and see what happens.
3. **Use as reference** — come back to specific lessons when you need a refresher.

## Quick Reference

### Python Essentials Cheat Sheet

```python
# Variables & types
name: str = "Alice"
nums: list[int] = [1, 2, 3]
data: dict[str, int] = {"a": 1}

# List comprehension
squares = [x**2 for x in range(10) if x % 2 == 0]

# Generator (lazy, memory efficient)
gen = (x**2 for x in range(1_000_000))

# Unpacking
first, *rest, last = [1, 2, 3, 4, 5]

# Ternary
status = "adult" if age >= 18 else "minor"

# f-string formatting
print(f"{name:>10}")      # right-align
print(f"{3.14159:.2f}")   # 2 decimal places
print(f"{1000000:,}")     # thousands separator

# Context manager
with open("file.txt") as f:
    content = f.read()

# Decorator
@functools.cache
def fibonacci(n):
    if n < 2: return n
    return fibonacci(n-1) + fibonacci(n-2)

# Dataclass
@dataclass
class Point:
    x: float
    y: float

# Async
async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.json()
```

### When to Use What

| Need | Use |
|------|-----|
| Ordered, mutable collection | `list` |
| Immutable sequence / dict key | `tuple` |
| Key-value mapping | `dict` |
| Unique elements / fast lookup | `set` |
| Count occurrences | `collections.Counter` |
| Dict with default values | `collections.defaultdict` |
| Fast both-ends queue | `collections.deque` |
| I/O-bound concurrency | `asyncio` or `threading` |
| CPU-bound parallelism | `multiprocessing` |
| Iterate once over large data | Generator expression |

## License

This project is open source and available for learning purposes.

---

*Built with the help of [Claude Code](https://claude.ai/code).*
