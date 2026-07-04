# Lesson 19: Context Managers

# Context managers manage setup and teardown of resources
# using the 'with' statement. Guarantees cleanup even on errors.

import time
import os
import functools
from contextlib import contextmanager, suppress, redirect_stdout, ExitStack

# --- Why Context Managers? ---
print("=== The Problem ===")

# Without context manager — error-prone
f = open("test.txt", "w")
try:
    f.write("hello")
    # What if an error happens here?
finally:
    f.close()  # must remember to close!

# With context manager — clean and safe
with open("test.txt", "w") as f:
    f.write("hello")
    # auto-closed when block exits, even on error

# --- The Protocol: __enter__ and __exit__ ---
print("\n=== Class-based Context Manager ===")

class ManagedFile:
    def __init__(self, filename, mode="r"):
        self.filename = filename
        self.mode = mode
        self.file = None

    def __enter__(self):
        """Called when entering 'with' block. Returns the resource."""
        print(f"  Opening {self.filename}")
        self.file = open(self.filename, self.mode)
        return self.file  # this is what 'as f' receives

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Called when exiting 'with' block. Handles cleanup.

        Args:
            exc_type: exception class (or None)
            exc_val:  exception instance (or None)
            exc_tb:   traceback (or None)
        Returns:
            True to suppress the exception, False/None to propagate
        """
        print(f"  Closing {self.filename}")
        if self.file:
            self.file.close()
        if exc_type:
            print(f"  Exception occurred: {exc_type.__name__}: {exc_val}")
        return False  # don't suppress exceptions

with ManagedFile("test.txt", "w") as f:
    f.write("Hello from context manager!\n")

with ManagedFile("test.txt", "r") as f:
    print(f"  Content: {f.read().strip()}")

# --- Exception Handling in __exit__ ---
print("\n=== Exception Handling ===")

class SuppressErrors:
    """Context manager that optionally suppresses exceptions."""
    def __init__(self, *exceptions):
        self.exceptions = exceptions

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type and issubclass(exc_type, self.exceptions):
            print(f"  Suppressed: {exc_type.__name__}: {exc_val}")
            return True  # suppress the exception
        return False

with SuppressErrors(ValueError, TypeError):
    int("not a number")  # ValueError suppressed
print("  Continued after suppressed error!")

# Built-in equivalent: contextlib.suppress
with suppress(FileNotFoundError):
    os.remove("nonexistent.txt")  # silently ignored
print("  suppress() works the same way")

# --- Generator-based Context Managers ---
print("\n=== @contextmanager ===")

@contextmanager
def timer(label):
    """Time a block of code."""
    start = time.perf_counter()
    yield  # --- code inside 'with' block runs here ---
    elapsed = time.perf_counter() - start
    print(f"  {label}: {elapsed:.4f}s")

with timer("sum computation"):
    total = sum(range(1_000_000))
    print(f"  total = {total}")

# yield can pass a value to 'as'
@contextmanager
def temp_file(filename, mode="w"):
    """Create a temp file, auto-delete on exit."""
    f = open(filename, mode)
    try:
        yield f  # 'as f' receives this
    finally:
        f.close()
        os.unlink(filename)
        print(f"  Cleaned up {filename}")

with temp_file("scratch.txt") as f:
    f.write("temporary data")
    print(f"  Wrote to {f.name}")

# --- Handling Errors in @contextmanager ---
print("\n=== Error Handling with @contextmanager ===")

@contextmanager
def managed_resource(name):
    print(f"  Acquiring {name}")
    resource = {"name": name, "active": True}
    try:
        yield resource
    except Exception as e:
        print(f"  Error with {name}: {e}")
        raise  # re-raise (or don't, to suppress)
    finally:
        resource["active"] = False
        print(f"  Released {name}")

with managed_resource("db-connection") as res:
    print(f"  Using {res['name']}, active={res['active']}")

print()
try:
    with managed_resource("db-connection") as res:
        raise RuntimeError("Query failed!")
except RuntimeError:
    print("  Error propagated to caller")

# --- Practical Context Managers ---
print("\n=== Practical: Change Directory ===")

@contextmanager
def cd(path):
    """Temporarily change directory, restore on exit."""
    old_dir = os.getcwd()
    os.chdir(path)
    try:
        yield os.getcwd()
    finally:
        os.chdir(old_dir)

with cd("/tmp") as path:
    print(f"  In: {path}")
print(f"  Back to: {os.getcwd()}")

# --- Practical: Database Transaction ---
print("\n=== Practical: Transaction ===")

class FakeDB:
    def __init__(self):
        self.data = {}
        self.committed = False

    @contextmanager
    def transaction(self):
        """Auto-commit on success, rollback on error."""
        snapshot = self.data.copy()
        try:
            yield self
            self.committed = True
            print("  Transaction committed")
        except Exception as e:
            self.data = snapshot
            self.committed = False
            print(f"  Transaction rolled back: {e}")
            raise

db = FakeDB()

# Successful transaction
with db.transaction():
    db.data["user"] = "Alice"
    db.data["age"] = 30
print(f"  Data: {db.data}")

# Failed transaction — rolls back
try:
    with db.transaction():
        db.data["user"] = "HACKED"
        raise ValueError("Validation error!")
except ValueError:
    pass
print(f"  Data after rollback: {db.data}")  # still Alice

# --- Practical: Indented Logger ---
print("\n=== Practical: Indented Logger ===")

class IndentLogger:
    def __init__(self):
        self._level = 0

    @contextmanager
    def indent(self, label=""):
        if label:
            self.log(label)
        self._level += 1
        try:
            yield
        finally:
            self._level -= 1

    def log(self, msg):
        print("  " + "  " * self._level + msg)

logger = IndentLogger()
logger.log("Starting process")
with logger.indent("Phase 1: Setup"):
    logger.log("Loading config")
    logger.log("Connecting to DB")
    with logger.indent("Sub-step: Migrations"):
        logger.log("Running migration 001")
        logger.log("Running migration 002")
    logger.log("Setup complete")
with logger.indent("Phase 2: Processing"):
    logger.log("Processing data")
logger.log("Done!")

# --- Nested Context Managers ---
print("\n=== Nested Context Managers ===")

# Multiple context managers in one 'with'
with open("test.txt", "r") as src, open("test_copy.txt", "w") as dst:
    dst.write(src.read())
    print("  Copied file with multiple context managers")

# Parenthesized form (Python 3.10+)
with (
    open("test.txt", "r") as src,
    open("test_copy2.txt", "w") as dst,
):
    dst.write(src.read())
    print("  Parenthesized context managers (3.10+)")

# --- ExitStack: Dynamic Context Managers ---
print("\n=== ExitStack ===")

# When you don't know how many context managers you need at write time
filenames = ["test.txt", "test_copy.txt", "test_copy2.txt"]

with ExitStack() as stack:
    files = [stack.enter_context(open(f)) for f in filenames]
    for f in files:
        print(f"  {f.name}: {f.read().strip()[:30]}")

# ExitStack with callbacks
@contextmanager
def cleanup_demo():
    with ExitStack() as stack:
        # Register cleanup callbacks
        stack.callback(print, "  Cleanup 3 (last registered, runs first)")
        stack.callback(print, "  Cleanup 2")
        stack.callback(print, "  Cleanup 1 (first registered, runs last)")
        yield

with cleanup_demo():
    print("  Inside the block")

# --- redirect_stdout ---
print("\n=== redirect_stdout ===")
import io

f = io.StringIO()
with redirect_stdout(f):
    print("This goes to the string buffer")
    print("So does this")

captured = f.getvalue()
print(f"  Captured: {captured.strip()}")

# --- Async Context Managers (preview) ---
print("\n=== Async Context Managers (preview) ===")
print("""
# Same protocol but async:
class AsyncDB:
    async def __aenter__(self):
        await self.connect()
        return self

    async def __aexit__(self, *exc):
        await self.disconnect()

# Usage:
async with AsyncDB() as db:
    await db.query("SELECT ...")

# Or with @asynccontextmanager:
from contextlib import asynccontextmanager

@asynccontextmanager
async def async_timer(label):
    start = time.perf_counter()
    yield
    print(f"{label}: {time.perf_counter() - start:.4f}s")
""")

# --- Summary ---
print("=== When to Use What ===")
print("""
| Approach              | When to Use                          |
|-----------------------|--------------------------------------|
| Class (__enter/exit__) | Need state, reusability, complex logic|
| @contextmanager       | Simple setup/teardown, most common   |
| suppress()            | Ignore specific exceptions           |
| ExitStack             | Dynamic/variable number of resources |
| redirect_stdout       | Capture print output                 |
""")

# Cleanup
for f in ["test.txt", "test_copy.txt", "test_copy2.txt"]:
    with suppress(FileNotFoundError):
        os.unlink(f)
