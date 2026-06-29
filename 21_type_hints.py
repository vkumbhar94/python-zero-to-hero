# Lesson 21: Type Hints

# Type hints are OPTIONAL annotations for documentation & tooling
# Python does NOT enforce them at runtime — they're for:
# 1. IDEs (autocomplete, error highlighting)
# 2. Static type checkers (mypy, pyright)
# 3. Documentation (self-documenting code)

# --- Basic Type Hints ---
print("=== Basic Hints ===")

# Variables
name: str = "Alice"
age: int = 30
height: float = 5.7
active: bool = True

# Functions
def greet(name: str) -> str:
    return f"Hello, {name}!"

def add(a: int, b: int) -> int:
    return a + b

def say_hello(name: str) -> None:
    print(f"Hello, {name}")

print(greet("Alice"))
print(add(3, 5))

# Python doesn't enforce types — this runs fine!
print(add("hello", " world"))  # "hello world" — no error

# --- Common Types ---
print("\n=== Common Types ===")
from typing import Optional, Union

# Collections (Python 3.9+: use built-in types directly)
names: list[str] = ["Alice", "Bob"]
scores: dict[str, int] = {"Alice": 85, "Bob": 92}
coords: tuple[float, float] = (3.14, 2.71)
unique: set[int] = {1, 2, 3}

# Variable-length tuple
values: tuple[int, ...] = (1, 2, 3, 4, 5)

# Nested
matrix: list[list[int]] = [[1, 2], [3, 4]]
registry: dict[str, list[int]] = {"scores": [85, 92]}

print(f"names: {names}")
print(f"scores: {scores}")
print(f"matrix: {matrix}")

# --- Optional and Union ---
print("\n=== Optional & Union ===")

# Optional[X] = X | None
def find_user(user_id: int) -> Optional[dict]:
    users = {1: {"name": "Alice"}, 2: {"name": "Bob"}}
    return users.get(user_id)

print(find_user(1))   # {'name': 'Alice'}
print(find_user(99))  # None

# Union[X, Y] = X | Y
def process(value: Union[str, int]) -> str:
    return str(value)

# Python 3.10+: use | syntax instead
def process_modern(value: str | int) -> str:
    return str(value)

def divide(a: float, b: float) -> float | None:
    if b == 0:
        return None
    return a / b

print(process(42))
print(process("hello"))
print(divide(10, 3))
print(divide(10, 0))

# --- Type Aliases ---
print("\n=== Type Aliases ===")

# Simple alias
Vector = list[float]
Matrix = list[list[float]]

def dot_product(v1: Vector, v2: Vector) -> float:
    return sum(a * b for a, b in zip(v1, v2))

print(dot_product([1.0, 2.0, 3.0], [4.0, 5.0, 6.0]))

# Python 3.12+: type statement
# type UserId = int
# type UserMap = dict[UserId, str]

# Complex aliases
JSON = dict[str, "JSON"] | list["JSON"] | str | int | float | bool | None
Headers = dict[str, str]
Callback = "Callable[[int], str]"

# --- Callable ---
print("\n=== Callable ===")
from typing import Callable

def apply(func: Callable[[int, int], int], a: int, b: int) -> int:
    return func(a, b)

def multiply(x: int, y: int) -> int:
    return x * y

print(apply(multiply, 3, 4))  # 12

# Function that returns a function
def make_adder(n: int) -> Callable[[int], int]:
    def adder(x: int) -> int:
        return x + n
    return adder

add5 = make_adder(5)
print(add5(10))  # 15

# --- Generics ---
print("\n=== Generics ===")
from typing import TypeVar

T = TypeVar("T")

def first(items: list[T]) -> T:
    return items[0]

print(first([1, 2, 3]))       # int
print(first(["a", "b", "c"])) # str

# Bounded TypeVar
from typing import Sequence

N = TypeVar("N", int, float)

def total(values: Sequence[N]) -> N:
    return sum(values)

print(total([1, 2, 3]))       # 6
print(total([1.5, 2.5]))      # 4.0

# Python 3.12+ syntax (simpler):
# def first[T](items: list[T]) -> T:
#     return items[0]

# --- Literal ---
print("\n=== Literal ===")
from typing import Literal

def set_color(color: Literal["red", "green", "blue"]) -> str:
    return f"Color set to {color}"

print(set_color("red"))
# set_color("purple")  # mypy would flag this

def open_file(path: str, mode: Literal["r", "w", "a"] = "r") -> str:
    return f"Opening {path} in {mode} mode"

print(open_file("test.txt", "w"))

# --- TypedDict ---
print("\n=== TypedDict ===")
from typing import TypedDict

class UserProfile(TypedDict):
    name: str
    age: int
    email: str

class UserProfileOptional(TypedDict, total=False):
    name: str       # all fields optional when total=False
    age: int
    email: str

# Required + optional fields
class Config(TypedDict):
    host: str              # required
    port: int              # required

class FullConfig(Config, total=False):
    debug: bool            # optional
    timeout: float         # optional

def create_profile(data: UserProfile) -> str:
    return f"{data['name']} ({data['email']})"

profile: UserProfile = {"name": "Alice", "age": 30, "email": "alice@ex.com"}
print(create_profile(profile))

config: FullConfig = {"host": "localhost", "port": 8080}
print(config)

# --- Protocol (structural typing / duck typing) ---
print("\n=== Protocol ===")
from typing import Protocol

class Drawable(Protocol):
    def draw(self) -> str: ...

class Circle:
    def draw(self) -> str:
        return "Drawing circle"

class Square:
    def draw(self) -> str:
        return "Drawing square"

def render(shape: Drawable) -> None:
    print(f"  {shape.draw()}")

# No inheritance needed — just matching method signatures!
render(Circle())
render(Square())

# Protocol with properties
class Sized(Protocol):
    @property
    def size(self) -> int: ...

class MyList:
    @property
    def size(self) -> int:
        return 42

def print_size(obj: Sized) -> None:
    print(f"  Size: {obj.size}")

print_size(MyList())

# --- dataclass with Type Hints ---
print("\n=== dataclass + Types ===")
from dataclasses import dataclass, field

@dataclass
class Product:
    name: str
    price: float
    tags: list[str] = field(default_factory=list)
    in_stock: bool = True

    def display_price(self) -> str:
        return f"${self.price:.2f}"

p = Product("Widget", 9.99, ["sale", "new"])
print(f"{p.name}: {p.display_price()}, tags={p.tags}")

# --- Annotated (attach metadata to types) ---
print("\n=== Annotated ===")
from typing import Annotated

# Annotated lets you attach validation metadata
PositiveInt = Annotated[int, "must be > 0"]
Email = Annotated[str, "valid email format"]

def create_user(name: str, age: PositiveInt, email: Email) -> dict:
    return {"name": name, "age": age, "email": email}

# Metadata is accessible but not enforced by Python
# Frameworks like Pydantic and FastAPI use it for validation
print(create_user("Alice", 30, "alice@example.com"))

# --- Type Guards ---
print("\n=== Type Guards ===")
from typing import TypeGuard

def is_string_list(val: list[object]) -> TypeGuard[list[str]]:
    return all(isinstance(x, str) for x in val)

data: list[object] = ["hello", "world"]
if is_string_list(data):
    # mypy now knows data is list[str]
    print(f"  String list: {[s.upper() for s in data]}")

# --- Final (constants) ---
print("\n=== Final ===")
from typing import Final

MAX_RETRIES: Final = 3
API_URL: Final[str] = "https://api.example.com"
# MAX_RETRIES = 5  # mypy would flag this

print(f"  MAX_RETRIES: {MAX_RETRIES}")
print(f"  API_URL: {API_URL}")

# --- Self type (Python 3.11+) ---
print("\n=== Self ===")
from typing import Self

class Builder:
    def __init__(self) -> None:
        self.parts: list[str] = []

    def add(self, part: str) -> Self:
        self.parts.append(part)
        return self

    def build(self) -> str:
        return " + ".join(self.parts)

result = Builder().add("A").add("B").add("C").build()
print(f"  Built: {result}")

# --- Practical Example: API Client ---
print("\n=== Practical: Typed API Client ===")

@dataclass
class APIResponse:
    status: int
    data: dict[str, str | int | list[str]]
    error: str | None = None

    @property
    def ok(self) -> bool:
        return 200 <= self.status < 300

class APIClient:
    def __init__(self, base_url: str, timeout: float = 30.0) -> None:
        self.base_url = base_url
        self.timeout = timeout

    def get(self, path: str, params: dict[str, str] | None = None) -> APIResponse:
        return APIResponse(
            status=200,
            data={"message": "success", "path": path},
        )

client = APIClient("https://api.example.com")
response = client.get("/users", params={"page": "1"})
print(f"  Status: {response.status}, OK: {response.ok}")
print(f"  Data: {response.data}")

# --- Running mypy ---
print("\n=== Using mypy ===")
print("""
# Install: pip install mypy
# Run:     mypy your_file.py

# Configuration in pyproject.toml:
# [tool.mypy]
# strict = true
# warn_return_any = true
# warn_unused_configs = true

# Common mypy flags:
# mypy --strict file.py          # strictest checking
# mypy --ignore-missing-imports  # skip untyped libraries
# mypy --check-untyped-defs      # check functions without hints

# Inline overrides:
# x: int = "hello"  # type: ignore  ← suppress specific error
# reveal_type(x)    # mypy prints the inferred type

# Alternative: pyright (faster, VS Code default)
# pip install pyright
# pyright your_file.py
""")

# --- Summary ---
print("=== Quick Reference ===")
print("""
| Type              | Example                              |
|-------------------|--------------------------------------|
| Basic             | str, int, float, bool, None          |
| List              | list[str]                            |
| Dict              | dict[str, int]                       |
| Tuple (fixed)     | tuple[int, str]                      |
| Tuple (variable)  | tuple[int, ...]                      |
| Set               | set[str]                             |
| Optional          | str | None  (or Optional[str])       |
| Union             | str | int   (or Union[str, int])      |
| Callable          | Callable[[int], str]                 |
| TypeVar           | T = TypeVar("T")                     |
| Literal           | Literal["a", "b"]                    |
| TypedDict         | class Config(TypedDict): ...         |
| Protocol          | class Drawable(Protocol): ...        |
| Final             | MAX: Final = 100                     |
| Self              | def method(self) -> Self: ...        |
| Annotated         | Annotated[int, "positive"]           |
""")
