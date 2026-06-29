# Lesson 18: Decorators

# A decorator is a function that wraps another function to extend its behavior
# without modifying it. Uses the @syntax sugar.

import time
import functools

# --- Foundations: Functions are objects ---
print("=== Functions are Objects ===")

def greet(name):
    return f"Hello, {name}!"

# Functions can be assigned to variables
say_hello = greet
print(say_hello("Alice"))

# Functions can be passed as arguments
def apply(func, value):
    return func(value)

print(apply(greet, "Bob"))

# Functions can return functions
def make_greeter(greeting):
    def greeter(name):
        return f"{greeting}, {name}!"
    return greeter

hi = make_greeter("Hi")
hey = make_greeter("Hey")
print(hi("Alice"))   # Hi, Alice!
print(hey("Bob"))    # Hey, Bob!

# --- First Decorator ---
print("\n=== First Decorator ===")

def my_decorator(func):
    def wrapper(*args, **kwargs):
        print(f"  Before {func.__name__}")
        result = func(*args, **kwargs)
        print(f"  After {func.__name__}")
        return result
    return wrapper

# Manual decoration
def say_hello(name):
    print(f"  Hello, {name}!")

say_hello = my_decorator(say_hello)
say_hello("Alice")

# @syntax does the same thing
@my_decorator
def say_goodbye(name):
    print(f"  Goodbye, {name}!")

say_goodbye("Bob")

# --- Preserving Function Metadata with functools.wraps ---
print("\n=== functools.wraps ===")

# Problem: decorator replaces the original function
def bad_decorator(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@bad_decorator
def add(a, b):
    """Add two numbers."""
    return a + b

print(f"Name: {add.__name__}")    # 'wrapper' — wrong!
print(f"Doc: {add.__doc__}")      # None — lost!

# Solution: use @functools.wraps
def good_decorator(func):
    @functools.wraps(func)  # copies metadata from func to wrapper
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@good_decorator
def multiply(a, b):
    """Multiply two numbers."""
    return a * b

print(f"Name: {multiply.__name__}")  # 'multiply' — correct!
print(f"Doc: {multiply.__doc__}")    # 'Multiply two numbers.'

# --- Practical Decorators ---
print("\n=== Practical: Timer ===")

def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"  {func.__name__} took {elapsed:.4f}s")
        return result
    return wrapper

@timer
def slow_function():
    total = sum(range(1_000_000))
    return total

result = slow_function()
print(f"  Result: {result}")

# --- Logger ---
print("\n=== Practical: Logger ===")

def log(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f"  Calling {func.__name__}({signature})")
        result = func(*args, **kwargs)
        print(f"  {func.__name__} returned {result!r}")
        return result
    return wrapper

@log
def add_numbers(a, b):
    return a + b

add_numbers(3, b=5)

# --- Retry ---
print("\n=== Practical: Retry ===")

def retry(max_attempts=3, exceptions=(Exception,)):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    print(f"  Attempt {attempt}/{max_attempts} failed: {e}")
                    if attempt == max_attempts:
                        raise
        return wrapper
    return decorator

call_count = 0

@retry(max_attempts=3, exceptions=(ValueError,))
def flaky_function():
    global call_count
    call_count += 1
    if call_count < 3:
        raise ValueError("Not ready yet!")
    return "Success!"

print(f"  Result: {flaky_function()}")

# --- Cache / Memoize ---
print("\n=== Practical: Memoize ===")

def memoize(func):
    cache = {}
    @functools.wraps(func)
    def wrapper(*args):
        if args not in cache:
            cache[args] = func(*args)
        return cache[args]
    return wrapper

@memoize
def fibonacci(n):
    if n < 2:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)

print(f"  fib(30) = {fibonacci(30)}")

# Built-in alternative: functools.lru_cache
@functools.lru_cache(maxsize=128)
def fib_cached(n):
    if n < 2:
        return n
    return fib_cached(n - 1) + fib_cached(n - 2)

print(f"  fib_cached(50) = {fib_cached(50)}")
print(f"  Cache info: {fib_cached.cache_info()}")

# Python 3.9+: @functools.cache (unlimited, simpler)
@functools.cache
def fib_simple(n):
    if n < 2:
        return n
    return fib_simple(n - 1) + fib_simple(n - 2)

print(f"  fib_simple(100) = {fib_simple(100)}")

# --- Decorators with Arguments ---
print("\n=== Decorators with Arguments ===")

# Three levels of nesting:
# 1. Outer function takes decorator arguments
# 2. Middle function takes the function being decorated
# 3. Inner function is the wrapper

def repeat(n):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(n):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def say(message):
    print(f"  {message}")

say("Hello!")  # prints 3 times

# Access control decorator
def require_role(role):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(user, *args, **kwargs):
            if user.get("role") != role:
                raise PermissionError(
                    f"Requires {role}, got {user.get('role')}"
                )
            return func(user, *args, **kwargs)
        return wrapper
    return decorator

@require_role("admin")
def delete_database(user):
    return f"Database deleted by {user['name']}"

admin = {"name": "Alice", "role": "admin"}
viewer = {"name": "Bob", "role": "viewer"}

print(f"  {delete_database(admin)}")
try:
    delete_database(viewer)
except PermissionError as e:
    print(f"  Permission denied: {e}")

# --- Stacking Decorators ---
print("\n=== Stacking Decorators ===")

@timer
@log
def compute(x, y):
    return x ** y

# Equivalent to: compute = timer(log(compute))
# Execution order: timer wraps log wraps compute
# So timer runs first (outermost), then log, then compute
result = compute(2, 10)
print(f"  Result: {result}")

# --- Class-based Decorators ---
print("\n=== Class-based Decorator ===")

class CountCalls:
    """Decorator that counts how many times a function is called."""
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        print(f"  Call #{self.count} to {self.func.__name__}")
        return self.func(*args, **kwargs)

@CountCalls
def greet(name):
    return f"Hello, {name}!"

print(greet("Alice"))
print(greet("Bob"))
print(greet("Charlie"))
print(f"  Total calls: {greet.count}")

# --- Decorating a Class ---
print("\n=== Decorating Classes ===")

def singleton(cls):
    """Ensures only one instance of a class exists."""
    instances = {}
    @functools.wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class Database:
    def __init__(self):
        print("  Creating database connection...")
        self.connected = True

db1 = Database()
db2 = Database()  # doesn't create new instance
print(f"  Same instance? {db1 is db2}")  # True

# --- Built-in Decorators You Already Know ---
print("\n=== Built-in Decorators ===")
print("""
| Decorator          | Purpose                              |
|--------------------|--------------------------------------|
| @property          | Getter method as attribute           |
| @staticmethod      | No self/cls parameter                |
| @classmethod       | Receives class as first arg          |
| @abstractmethod    | Must be overridden in subclass       |
| @functools.wraps   | Preserve function metadata           |
| @functools.cache   | Memoization (unlimited)              |
| @functools.lru_cache| Memoization (bounded)               |
| @dataclass         | Auto-generate class boilerplate      |
| @contextmanager    | Generator as context manager         |
""")

# --- Advanced: Decorator that works with and without arguments ---
print("=== Optional Arguments Decorator ===")

def debug(func=None, *, prefix="DEBUG"):
    """Can be used as @debug or @debug(prefix='INFO')."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            print(f"  [{prefix}] {func.__name__} called")
            return func(*args, **kwargs)
        return wrapper

    if func is not None:
        return decorator(func)  # called without arguments: @debug
    return decorator             # called with arguments: @debug(prefix='INFO')

@debug
def foo():
    return "foo"

@debug(prefix="INFO")
def bar():
    return "bar"

foo()
bar()
