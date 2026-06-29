# Lesson 15: Modules & Packages

# A module = a .py file
# A package = a directory with modules (and optionally __init__.py)

# --- Importing Modules ---
print("=== Import Styles ===")

# 1. Import the whole module
import math
print(math.sqrt(16))    # 4.0
print(math.pi)          # 3.14159...

# 2. Import specific items
from math import sqrt, pi
print(sqrt(25))         # 5.0
print(pi)               # 3.14159...

# 3. Import with alias
import math as m
print(m.ceil(3.2))      # 4

from math import factorial as fact
print(fact(5))           # 120

# 4. Import everything (avoid this — pollutes namespace)
# from math import *

# --- What's in a module? ---
print("\n=== Module Inspection ===")
import string
print(dir(string)[:10])         # list all names in module
print(string.ascii_lowercase)   # abcdefghijklmnopqrstuvwxyz
print(string.digits)            # 0123456789

# help(math.sqrt)  # detailed docs (try in REPL)

# --- Creating Your Own Module ---
print("\n=== Custom Module ===")

# Let's create a module file
import pathlib
pathlib.Path("myutils.py").write_text('''\
"""My utility module."""

PI = 3.14159

def greet(name):
    """Return a greeting string."""
    return f"Hello, {name}!"

def add(a, b):
    """Add two numbers."""
    return a + b

def _private_helper():
    """Convention: underscore prefix = private."""
    return "internal"

class Calculator:
    """Simple calculator class."""
    def __init__(self):
        self.history = []

    def compute(self, expr):
        result = eval(expr)
        self.history.append(f"{expr} = {result}")
        return result
''')

# Now import and use it
import myutils
print(myutils.greet("Alice"))
print(myutils.add(3, 5))
print(myutils.PI)

calc = myutils.Calculator()
print(calc.compute("2 + 3 * 4"))

from myutils import greet, Calculator
print(greet("Bob"))

# --- __name__ and __main__ ---
print("\n=== __name__ ===")
print(f"This module's __name__: {__name__}")
print(f"myutils's __name__: {myutils.__name__}")

# When a file is run directly: __name__ == "__main__"
# When a file is imported: __name__ == module name
#
# Common pattern at bottom of a module:
#
# def main():
#     ... do stuff ...
#
# if __name__ == "__main__":
#     main()
#
# This lets the file work as BOTH a module AND a script

# Let's create one
pathlib.Path("runnable.py").write_text('''\
"""A module that can also be run as a script."""

def process(data):
    return [x * 2 for x in data]

def main():
    result = process([1, 2, 3, 4, 5])
    print(f"Result: {result}")

if __name__ == "__main__":
    main()
''')

# Import uses it as a module (main() doesn't run)
import runnable
print(runnable.process([10, 20]))  # [20, 40]

# --- Packages (directories of modules) ---
print("\n=== Packages ===")

# Create a package structure:
# mypackage/
#   __init__.py
#   math_utils.py
#   string_utils.py
#   sub/
#     __init__.py
#     advanced.py

import os
os.makedirs("mypackage/sub", exist_ok=True)

pathlib.Path("mypackage/__init__.py").write_text('''\
"""My package — this file makes the directory a package."""

# What gets exported with "from mypackage import *"
__all__ = ["math_utils", "string_utils"]

# Package-level imports for convenience
from .math_utils import add, multiply
from .string_utils import capitalize_words

# Package metadata
__version__ = "1.0.0"
''')

pathlib.Path("mypackage/math_utils.py").write_text('''\
"""Math utility functions."""

def add(a, b):
    return a + b

def multiply(a, b):
    return a * b

def square(x):
    return x ** 2
''')

pathlib.Path("mypackage/string_utils.py").write_text('''\
"""String utility functions."""

def capitalize_words(text):
    return " ".join(w.capitalize() for w in text.split())

def reverse(text):
    return text[::-1]
''')

pathlib.Path("mypackage/sub/__init__.py").write_text("")

pathlib.Path("mypackage/sub/advanced.py").write_text('''\
"""Advanced utilities in a sub-package."""

def fibonacci(n):
    a, b = 0, 1
    result = []
    for _ in range(n):
        result.append(a)
        a, b = b, a + b
    return result
''')

# Import from package
import mypackage
print(f"Package version: {mypackage.__version__}")
print(mypackage.add(3, 5))              # from __init__ convenience import
print(mypackage.capitalize_words("hello world"))

# Import specific module
from mypackage import math_utils
print(math_utils.square(7))

# Import from sub-package
from mypackage.sub.advanced import fibonacci
print(f"Fibonacci: {fibonacci(8)}")

# --- Standard Library Highlights ---
print("\n=== Standard Library Highlights ===")

# os — operating system interface
import os
print(f"cwd: {os.getcwd()}")
print(f"CPU count: {os.cpu_count()}")

# sys — system-specific parameters
import sys
print(f"Python version: {sys.version_info.major}.{sys.version_info.minor}")
print(f"Platform: {sys.platform}")
# sys.argv — command line arguments
# sys.path — module search paths
# sys.exit() — exit program

# datetime — dates and times
from datetime import datetime, timedelta
now = datetime.now()
print(f"Now: {now.strftime('%Y-%m-%d %H:%M')}")
tomorrow = now + timedelta(days=1)
print(f"Tomorrow: {tomorrow.strftime('%Y-%m-%d')}")

# random
import random
print(f"Random int: {random.randint(1, 100)}")
print(f"Random choice: {random.choice(['a', 'b', 'c'])}")
print(f"Shuffled: {random.sample(range(10), 5)}")

# re — regular expressions
import re
text = "Contact us at support@example.com or admin@test.org"
emails = re.findall(r'[\w.]+@[\w.]+', text)
print(f"Emails found: {emails}")

# collections (covered in lesson 8b)
# itertools (covered in lesson 8b)

# functools
from functools import lru_cache

@lru_cache(maxsize=128)
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

print(f"fib(30): {fib(30)}")

# dataclasses (preview — full coverage in OOP lesson)
from dataclasses import dataclass

@dataclass
class Point:
    x: float
    y: float

p = Point(3.0, 4.0)
print(f"Point: {p}")

# typing
from typing import Optional

def find_user(user_id: int) -> Optional[dict]:
    users = {1: {"name": "Alice"}, 2: {"name": "Bob"}}
    return users.get(user_id)

print(f"User 1: {find_user(1)}")
print(f"User 9: {find_user(9)}")

# --- Installing Third-Party Packages ---
print("\n=== Third-Party Packages ===")
print("""
# pip — Python's package installer
pip install requests          # install a package
pip install requests==2.31.0  # specific version
pip install -r requirements.txt  # from file
pip list                      # list installed
pip freeze > requirements.txt # save dependencies
pip uninstall requests

# uv — modern, fast alternative (recommended)
uv pip install requests
uv add requests              # if using pyproject.toml

# Virtual environments (isolate project dependencies)
python -m venv .venv         # create
source .venv/bin/activate    # activate (macOS/Linux)
# .venv\\Scripts\\activate    # activate (Windows)
deactivate                   # deactivate

# uv for venv
uv venv                     # create .venv
uv pip install requests     # install into .venv

# Popular packages:
# requests     — HTTP requests
# flask/django — web frameworks
# pandas       — data analysis
# numpy        — numerical computing
# pytest       — testing
# sqlalchemy   — database ORM
# pydantic     — data validation
# click/typer  — CLI tools
""")

# --- Module Search Path ---
print("=== Module Search Path ===")
# Python searches for modules in this order:
# 1. Current directory
# 2. PYTHONPATH environment variable
# 3. Standard library
# 4. Site-packages (pip installed)
print("First 3 sys.path entries:")
for p in sys.path[:3]:
    print(f"  {p}")

# --- Cleanup ---
import shutil
pathlib.Path("myutils.py").unlink(missing_ok=True)
pathlib.Path("runnable.py").unlink(missing_ok=True)
shutil.rmtree("mypackage", ignore_errors=True)
# Clean up __pycache__
shutil.rmtree("__pycache__", ignore_errors=True)
print("\nCleaned up demo files.")
