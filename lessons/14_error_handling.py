# Lesson 14: Error Handling (Exceptions)

# --- Basic try/except ---
print("=== Basic try/except ===")

try:
    result = 10 / 0
except ZeroDivisionError:
    print("Can't divide by zero!")

# Without handling, this would crash the program

# --- Catching the exception object ---
print("\n=== Exception Object ===")

try:
    num = int("hello")
except ValueError as e:
    print(f"Error: {e}")          # invalid literal for int()...
    print(f"Type: {type(e)}")     # <class 'ValueError'>

# --- Multiple except blocks ---
print("\n=== Multiple Except ===")

def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        print("Division by zero!")
        return None
    except TypeError:
        print("Invalid types!")
        return None

print(safe_divide(10, 3))     # 3.333...
print(safe_divide(10, 0))     # None
print(safe_divide("10", 3))   # None

# Catch multiple exceptions in one block
try:
    x = int("hello")
except (ValueError, TypeError) as e:
    print(f"Conversion error: {e}")

# --- else and finally ---
print("\n=== else / finally ===")

def read_number(text):
    try:
        num = int(text)
    except ValueError:
        print(f"  '{text}' is not a number")
        return None
    else:
        # Runs ONLY if no exception occurred
        print(f"  Successfully parsed: {num}")
        return num
    finally:
        # Runs ALWAYS — whether exception or not
        print(f"  Finished processing '{text}'")

read_number("42")
print()
read_number("abc")

# finally is guaranteed to run — even with return!
print("\n--- finally with return ---")
def demo():
    try:
        return "from try"
    finally:
        print("finally still runs!")

result = demo()
print(f"result: {result}")

# --- Exception Hierarchy ---
print("\n=== Exception Hierarchy ===")
print("""
BaseException
├── SystemExit              # sys.exit()
├── KeyboardInterrupt       # Ctrl+C
├── GeneratorExit
└── Exception               # ← catch this, not BaseException
    ├── ValueError           # wrong value ("int('abc')")
    ├── TypeError            # wrong type (1 + "a")
    ├── KeyError             # missing dict key
    ├── IndexError           # list index out of range
    ├── AttributeError       # obj.nonexistent_attr
    ├── NameError            # undefined variable
    ├── FileNotFoundError    # open("nope.txt")
    ├── IOError / OSError    # file/network issues
    ├── ImportError          # import nonexistent
    ├── StopIteration        # iterator exhausted
    ├── ArithmeticError
    │   └── ZeroDivisionError
    ├── LookupError
    │   ├── IndexError
    │   └── KeyError
    └── RuntimeError
        └── RecursionError
""")

# Catch parent catches all children
try:
    d = {}
    print(d["missing"])
except LookupError as e:  # catches both KeyError and IndexError
    print(f"LookupError caught: {type(e).__name__}: {e}")

# --- Raising Exceptions ---
print("\n=== Raising Exceptions ===")

def validate_age(age):
    if not isinstance(age, int):
        raise TypeError(f"Age must be int, got {type(age).__name__}")
    if age < 0:
        raise ValueError(f"Age cannot be negative, got {age}")
    if age > 150:
        raise ValueError(f"Age too large: {age}")
    return age

try:
    validate_age(-5)
except ValueError as e:
    print(f"Validation failed: {e}")

try:
    validate_age("twenty")
except TypeError as e:
    print(f"Type error: {e}")

# --- Re-raising Exceptions ---
print("\n=== Re-raising ===")

def process_data(data):
    try:
        return int(data)
    except ValueError:
        print(f"Logging: failed to parse '{data}'")
        raise  # re-raise the same exception

try:
    process_data("bad")
except ValueError as e:
    print(f"Caller caught: {e}")

# --- Custom Exceptions ---
print("\n=== Custom Exceptions ===")

class AppError(Exception):
    """Base exception for our application."""
    pass

class ValidationError(AppError):
    """Raised when input validation fails."""
    def __init__(self, field, message):
        self.field = field
        self.message = message
        super().__init__(f"{field}: {message}")

class NotFoundError(AppError):
    """Raised when a resource is not found."""
    def __init__(self, resource, id):
        self.resource = resource
        self.id = id
        super().__init__(f"{resource} with id={id} not found")

# Using custom exceptions
def create_user(name, age):
    if not name:
        raise ValidationError("name", "cannot be empty")
    if age < 0:
        raise ValidationError("age", "must be non-negative")
    return {"name": name, "age": age}

try:
    create_user("", 25)
except ValidationError as e:
    print(f"Validation: {e}")
    print(f"  Field: {e.field}")

try:
    raise NotFoundError("User", 42)
except NotFoundError as e:
    print(f"Not found: {e}")
    print(f"  Resource: {e.resource}, ID: {e.id}")

# Catch parent catches all app errors
try:
    raise ValidationError("email", "invalid format")
except AppError as e:
    print(f"App error: {e}")

# --- Exception Chaining ---
print("\n=== Exception Chaining ===")

# 'from' — explicit chaining (shows the cause)
def connect_to_db():
    try:
        raise ConnectionError("Connection refused")
    except ConnectionError as e:
        raise RuntimeError("Database unavailable") from e

try:
    connect_to_db()
except RuntimeError as e:
    print(f"Error: {e}")
    print(f"Caused by: {e.__cause__}")

# 'from None' — suppress the chain
def parse_config(text):
    try:
        return int(text)
    except ValueError:
        raise ValueError(f"Invalid config value: '{text}'") from None

try:
    parse_config("abc")
except ValueError as e:
    print(f"Config error: {e}")
    print(f"Cause suppressed: {e.__cause__}")  # None

# --- Context-based Suppression ---
print("\n=== contextlib.suppress ===")
from contextlib import suppress

# Instead of try/except/pass:
d = {"a": 1}
with suppress(KeyError):
    print(d["b"])  # silently ignored
print("Continued after suppress")

# Equivalent to:
# try:
#     print(d["b"])
# except KeyError:
#     pass

# --- EAFP vs LBYL ---
print("\n=== EAFP vs LBYL ===")

data = {"name": "Alice", "age": 30}

# LBYL: Look Before You Leap (common in Java/C)
if "email" in data:
    email = data["email"]
else:
    email = "N/A"
print(f"LBYL: {email}")

# EAFP: Easier to Ask Forgiveness than Permission (Pythonic!)
try:
    email = data["email"]
except KeyError:
    email = "N/A"
print(f"EAFP: {email}")

# Even better for this case:
email = data.get("email", "N/A")
print(f"get(): {email}")

# --- Practical Patterns ---
print("\n=== Practical Patterns ===")

# 1. Retry pattern
import random
random.seed(42)

def unreliable_api():
    if random.random() < 0.7:
        raise ConnectionError("Server busy")
    return {"status": "ok"}

def call_with_retry(func, max_retries=5):
    for attempt in range(1, max_retries + 1):
        try:
            result = func()
            print(f"  Attempt {attempt}: success!")
            return result
        except ConnectionError as e:
            print(f"  Attempt {attempt}: {e}")
            if attempt == max_retries:
                raise
    return None

try:
    result = call_with_retry(unreliable_api)
    print(f"  Result: {result}")
except ConnectionError:
    print("  All retries failed!")

# 2. Cleanup with finally
print("\n--- Cleanup pattern ---")
class DatabaseConnection:
    def __init__(self, name):
        self.name = name
        print(f"  Connected to {name}")

    def query(self, sql):
        if "DROP" in sql:
            raise PermissionError("DROP not allowed!")
        return f"Results for: {sql}"

    def close(self):
        print(f"  Closed {self.name}")

db = DatabaseConnection("mydb")
try:
    print(f"  {db.query('SELECT * FROM users')}")
    print(f"  {db.query('DROP TABLE users')}")
except PermissionError as e:
    print(f"  Error: {e}")
finally:
    db.close()  # always closes, even on error

# 3. Collecting errors (don't fail on first error)
print("\n--- Collect errors ---")
items = ["10", "abc", "20", "xyz", "30"]
results = []
errors = []

for i, item in enumerate(items):
    try:
        results.append(int(item))
    except ValueError as e:
        errors.append(f"Item {i} ('{item}'): {e}")

print(f"  Parsed: {results}")
print(f"  Errors: {errors}")

# 4. Exception groups (Python 3.11+)
print("\n--- ExceptionGroup (Python 3.11+) ---")
errors = [
    ValueError("invalid email"),
    TypeError("age must be int"),
    KeyError("missing field 'name'"),
]

try:
    raise ExceptionGroup("Validation failed", errors)
except* ValueError as eg:
    print(f"  Value errors: {[str(e) for e in eg.exceptions]}")
except* TypeError as eg:
    print(f"  Type errors: {[str(e) for e in eg.exceptions]}")
except* KeyError as eg:
    print(f"  Key errors: {[str(e) for e in eg.exceptions]}")
