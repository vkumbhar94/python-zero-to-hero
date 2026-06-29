# Lesson 23: Design Patterns in Python

# Design patterns are reusable solutions to common problems.
# Python's dynamic nature makes many patterns simpler than in Java/C++.

from __future__ import annotations
import functools
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Protocol


# ============================================================
# CREATIONAL PATTERNS
# ============================================================
print("=" * 60)
print("CREATIONAL PATTERNS")
print("=" * 60)

# --- Singleton ---
print("\n=== Singleton ===")

# Approach 1: Module-level variable (most Pythonic!)
# Just put your instance in a module — import gives you the same object.
# db = Database()  # in db.py
# from db import db  # everywhere else — same instance

# Approach 2: Decorator
def singleton(cls):
    instances = {}
    @functools.wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    return get_instance

@singleton
class DatabaseConnection:
    def __init__(self):
        self.connected = True
        print("  Creating DB connection (only once)")

db1 = DatabaseConnection()
db2 = DatabaseConnection()
print(f"  Same instance? {db1 is db2}")  # True

# Approach 3: __new__
class Logger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.logs = []
        return cls._instance

    def log(self, msg):
        self.logs.append(msg)

log1 = Logger()
log2 = Logger()
log1.log("Hello")
print(f"  Same? {log1 is log2}, logs: {log2.logs}")


# --- Factory ---
print("\n=== Factory ===")

class Serializer(Protocol):
    def serialize(self, data: dict) -> str: ...

class JSONSerializer:
    def serialize(self, data: dict) -> str:
        return json.dumps(data)

class XMLSerializer:
    def serialize(self, data: dict) -> str:
        items = "".join(f"<{k}>{v}</{k}>" for k, v in data.items())
        return f"<data>{items}</data>"

class CSVSerializer:
    def serialize(self, data: dict) -> str:
        return ",".join(f"{k}={v}" for k, v in data.items())

# Factory function (simplest approach)
def create_serializer(format: str) -> Serializer:
    serializers = {
        "json": JSONSerializer,
        "xml": XMLSerializer,
        "csv": CSVSerializer,
    }
    cls = serializers.get(format)
    if cls is None:
        raise ValueError(f"Unknown format: {format}")
    return cls()

data = {"name": "Alice", "age": 30}
for fmt in ("json", "xml", "csv"):
    s = create_serializer(fmt)
    print(f"  {fmt}: {s.serialize(data)}")

# Registry pattern (extensible factory)
class SerializerRegistry:
    _registry: dict[str, type] = {}

    @classmethod
    def register(cls, name: str):
        def decorator(serializer_cls):
            cls._registry[name] = serializer_cls
            return serializer_cls
        return decorator

    @classmethod
    def create(cls, name: str) -> Serializer:
        return cls._registry[name]()

@SerializerRegistry.register("yaml")
class YAMLSerializer:
    def serialize(self, data: dict) -> str:
        return "\n".join(f"{k}: {v}" for k, v in data.items())

print(f"  yaml: {SerializerRegistry.create('yaml').serialize(data)}")


# --- Builder ---
print("\n=== Builder ===")

@dataclass
class Query:
    table: str = ""
    conditions: list[str] = field(default_factory=list)
    columns: list[str] = field(default_factory=lambda: ["*"])
    order_by: str | None = None
    limit_val: int | None = None

class QueryBuilder:
    def __init__(self):
        self._query = Query()

    def table(self, name: str) -> QueryBuilder:
        self._query.table = name
        return self

    def select(self, *columns: str) -> QueryBuilder:
        self._query.columns = list(columns)
        return self

    def where(self, condition: str) -> QueryBuilder:
        self._query.conditions.append(condition)
        return self

    def order(self, column: str) -> QueryBuilder:
        self._query.order_by = column
        return self

    def limit(self, n: int) -> QueryBuilder:
        self._query.limit_val = n
        return self

    def build(self) -> str:
        cols = ", ".join(self._query.columns)
        sql = f"SELECT {cols} FROM {self._query.table}"
        if self._query.conditions:
            sql += " WHERE " + " AND ".join(self._query.conditions)
        if self._query.order_by:
            sql += f" ORDER BY {self._query.order_by}"
        if self._query.limit_val:
            sql += f" LIMIT {self._query.limit_val}"
        return sql

query = (
    QueryBuilder()
    .table("users")
    .select("name", "email")
    .where("age > 18")
    .where("active = true")
    .order("name")
    .limit(10)
    .build()
)
print(f"  {query}")


# ============================================================
# STRUCTURAL PATTERNS
# ============================================================
print("\n" + "=" * 60)
print("STRUCTURAL PATTERNS")
print("=" * 60)

# --- Decorator Pattern (not Python decorators — wrapping objects) ---
print("\n=== Decorator Pattern ===")

class TextProcessor(Protocol):
    def process(self, text: str) -> str: ...

class PlainText:
    def process(self, text: str) -> str:
        return text

class UpperCase:
    def __init__(self, wrapped: TextProcessor):
        self._wrapped = wrapped

    def process(self, text: str) -> str:
        return self._wrapped.process(text).upper()

class AddBorder:
    def __init__(self, wrapped: TextProcessor, char: str = "*"):
        self._wrapped = wrapped
        self._char = char

    def process(self, text: str) -> str:
        result = self._wrapped.process(text)
        border = self._char * (len(result) + 4)
        return f"{border}\n{self._char} {result} {self._char}\n{border}"

class TrimWhitespace:
    def __init__(self, wrapped: TextProcessor):
        self._wrapped = wrapped

    def process(self, text: str) -> str:
        return self._wrapped.process(text).strip()

# Stack decorators
processor = AddBorder(UpperCase(TrimWhitespace(PlainText())))
print(processor.process("  hello world  "))


# --- Adapter ---
print("\n=== Adapter ===")

# Existing classes with incompatible interfaces
class OldPaymentGateway:
    def make_payment(self, amount_cents: int, currency: str) -> dict:
        return {"paid": amount_cents, "cur": currency}

class NewPaymentGateway:
    def charge(self, amount: float, currency: str = "USD") -> dict:
        return {"charged": amount, "currency": currency}

# Unified interface
class PaymentAdapter:
    def __init__(self, gateway):
        self._gateway = gateway

    def pay(self, amount: float, currency: str = "USD") -> dict:
        if isinstance(self._gateway, OldPaymentGateway):
            return self._gateway.make_payment(int(amount * 100), currency)
        elif isinstance(self._gateway, NewPaymentGateway):
            return self._gateway.charge(amount, currency)
        raise TypeError(f"Unknown gateway: {type(self._gateway)}")

old = PaymentAdapter(OldPaymentGateway())
new = PaymentAdapter(NewPaymentGateway())
print(f"  Old: {old.pay(19.99)}")
print(f"  New: {new.pay(19.99)}")


# --- Proxy ---
print("\n=== Proxy ===")

class ExpensiveResource:
    def __init__(self, name: str):
        print(f"  Loading {name}... (expensive!)")
        self.name = name
        self.data = f"data for {name}"

    def get_data(self) -> str:
        return self.data

class LazyProxy:
    """Delays creation of expensive resource until first use."""
    def __init__(self, name: str):
        self._name = name
        self._resource: ExpensiveResource | None = None

    def get_data(self) -> str:
        if self._resource is None:
            self._resource = ExpensiveResource(self._name)
        return self._resource.get_data()

proxy = LazyProxy("big_dataset")
print("  Proxy created (resource NOT loaded yet)")
print(f"  First access: {proxy.get_data()}")  # loads here
print(f"  Second access: {proxy.get_data()}")  # cached


# ============================================================
# BEHAVIORAL PATTERNS
# ============================================================
print("\n" + "=" * 60)
print("BEHAVIORAL PATTERNS")
print("=" * 60)

# --- Observer ---
print("\n=== Observer ===")

class EventEmitter:
    def __init__(self):
        self._listeners: dict[str, list] = {}

    def on(self, event: str, callback):
        self._listeners.setdefault(event, []).append(callback)
        return self  # chainable

    def off(self, event: str, callback):
        self._listeners.get(event, []).remove(callback)

    def emit(self, event: str, *args, **kwargs):
        for callback in self._listeners.get(event, []):
            callback(*args, **kwargs)

class Store(EventEmitter):
    def __init__(self):
        super().__init__()
        self._items: list[str] = []

    def add(self, item: str):
        self._items.append(item)
        self.emit("item_added", item)

    def remove(self, item: str):
        self._items.remove(item)
        self.emit("item_removed", item)

store = Store()
store.on("item_added", lambda item: print(f"  Added: {item}"))
store.on("item_removed", lambda item: print(f"  Removed: {item}"))
store.on("item_added", lambda item: print(f"  Logging: {item} added to store"))

store.add("Apple")
store.add("Banana")
store.remove("Apple")


# --- Strategy ---
print("\n=== Strategy ===")

# In Python, strategies are often just functions (no class hierarchy needed)

def sort_by_name(items: list[dict]) -> list[dict]:
    return sorted(items, key=lambda x: x["name"])

def sort_by_price(items: list[dict]) -> list[dict]:
    return sorted(items, key=lambda x: x["price"])

def sort_by_rating(items: list[dict]) -> list[dict]:
    return sorted(items, key=lambda x: x["rating"], reverse=True)

class ProductCatalog:
    def __init__(self, products: list[dict]):
        self.products = products

    def display(self, strategy=sort_by_name):
        sorted_products = strategy(self.products)
        for p in sorted_products:
            print(f"  {p['name']}: ${p['price']}, ★{p['rating']}")

products = [
    {"name": "Widget", "price": 25.99, "rating": 4.5},
    {"name": "Gadget", "price": 15.99, "rating": 4.8},
    {"name": "Doohickey", "price": 35.99, "rating": 4.2},
]

catalog = ProductCatalog(products)
print("By price:")
catalog.display(sort_by_price)
print("By rating:")
catalog.display(sort_by_rating)


# --- Chain of Responsibility ---
print("\n=== Chain of Responsibility ===")

class Handler(ABC):
    def __init__(self):
        self._next: Handler | None = None

    def set_next(self, handler: Handler) -> Handler:
        self._next = handler
        return handler

    def handle(self, request: dict) -> str | None:
        result = self.process(request)
        if result is not None:
            return result
        if self._next:
            return self._next.handle(request)
        return None

    @abstractmethod
    def process(self, request: dict) -> str | None: ...

class AuthHandler(Handler):
    def process(self, request: dict) -> str | None:
        if not request.get("token"):
            return "Error: No auth token"
        print("  ✓ Auth passed")
        return None

class RateLimitHandler(Handler):
    def __init__(self):
        super().__init__()
        self._count = 0

    def process(self, request: dict) -> str | None:
        self._count += 1
        if self._count > 5:
            return "Error: Rate limited"
        print(f"  ✓ Rate limit OK ({self._count}/5)")
        return None

class ValidationHandler(Handler):
    def process(self, request: dict) -> str | None:
        if not request.get("data"):
            return "Error: No data"
        print("  ✓ Validation passed")
        return None

# Build chain
auth = AuthHandler()
rate = RateLimitHandler()
validation = ValidationHandler()
auth.set_next(rate).set_next(validation)

# Process requests
request = {"token": "abc123", "data": {"key": "value"}}
result = auth.handle(request)
print(f"  Result: {result or 'Success!'}")

bad_request = {"data": {"key": "value"}}  # no token
result = auth.handle(bad_request)
print(f"  Result: {result}")


# --- Command ---
print("\n=== Command ===")

@dataclass
class Command:
    execute: object  # callable
    undo: object     # callable

class TextEditor:
    def __init__(self):
        self.content = ""
        self._history: list[Command] = []
        self._redo_stack: list[Command] = []

    def _do(self, cmd: Command):
        cmd.execute()
        self._history.append(cmd)
        self._redo_stack.clear()

    def insert(self, text: str, position: int | None = None):
        pos = position if position is not None else len(self.content)
        def execute():
            self.content = self.content[:pos] + text + self.content[pos:]
        def undo():
            self.content = self.content[:pos] + self.content[pos + len(text):]
        self._do(Command(execute, undo))

    def delete(self, start: int, length: int):
        deleted = self.content[start:start + length]
        def execute():
            self.content = self.content[:start] + self.content[start + length:]
        def undo():
            self.content = self.content[:start] + deleted + self.content[start:]
        self._do(Command(execute, undo))

    def undo(self):
        if self._history:
            cmd = self._history.pop()
            cmd.undo()
            self._redo_stack.append(cmd)

    def redo(self):
        if self._redo_stack:
            cmd = self._redo_stack.pop()
            cmd.execute()
            self._history.append(cmd)

editor = TextEditor()
editor.insert("Hello World")
print(f"  After insert: '{editor.content}'")
editor.insert(", Python", 5)
print(f"  After insert at 5: '{editor.content}'")
editor.delete(5, 8)
print(f"  After delete: '{editor.content}'")
editor.undo()
print(f"  After undo: '{editor.content}'")
editor.undo()
print(f"  After undo: '{editor.content}'")
editor.redo()
print(f"  After redo: '{editor.content}'")


# --- Iterator Pattern (built into Python!) ---
print("\n=== Iterator (Python's built-in) ===")
print("""  Python's for loop, generators, and __iter__/__next__
  ARE the iterator pattern. See Lesson 17.

  # Custom iterable
  class Range:
      def __init__(self, n): self.n = n
      def __iter__(self):
          for i in range(self.n): yield i
""")


# --- State Machine ---
print("=== State Machine ===")

class State(ABC):
    @abstractmethod
    def handle(self, context: "TrafficLight") -> None: ...

class RedState(State):
    def handle(self, context):
        print("  🔴 Red → Green")
        context.state = GreenState()

class GreenState(State):
    def handle(self, context):
        print("  🟢 Green → Yellow")
        context.state = YellowState()

class YellowState(State):
    def handle(self, context):
        print("  🟡 Yellow → Red")
        context.state = RedState()

class TrafficLight:
    def __init__(self):
        self.state: State = RedState()

    def change(self):
        self.state.handle(self)

light = TrafficLight()
for _ in range(6):
    light.change()


# ============================================================
# PYTHON-SPECIFIC PATTERNS
# ============================================================
print("\n" + "=" * 60)
print("PYTHON-SPECIFIC PATTERNS")
print("=" * 60)

# --- Mixin ---
print("\n=== Mixin ===")

class JsonMixin:
    def to_json(self) -> str:
        return json.dumps(self.__dict__, default=str)

    @classmethod
    def from_json(cls, json_str: str):
        return cls(**json.loads(json_str))

class TimestampMixin:
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        from datetime import datetime
        original_init = cls.__init__
        @functools.wraps(original_init)
        def new_init(self, *args, **kwargs):
            original_init(self, *args, **kwargs)
            self.created_at = datetime.now().isoformat()
        cls.__init__ = new_init

@dataclass
class User(JsonMixin):
    name: str
    email: str

u = User("Alice", "alice@example.com")
json_str = u.to_json()
print(f"  JSON: {json_str}")
u2 = User.from_json(json_str)
print(f"  From JSON: {u2}")


# --- Descriptor ---
print("\n=== Descriptor ===")

class Validated:
    """Descriptor that validates on assignment."""
    def __init__(self, validator, error_msg="Invalid value"):
        self.validator = validator
        self.error_msg = error_msg

    def __set_name__(self, owner, name):
        self.name = f"_{name}"

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.name, None)

    def __set__(self, obj, value):
        if not self.validator(value):
            raise ValueError(f"{self.name[1:]}: {self.error_msg} (got {value!r})")
        setattr(obj, self.name, value)

class Employee:
    name = Validated(lambda x: isinstance(x, str) and len(x) > 0, "must be non-empty string")
    age = Validated(lambda x: isinstance(x, int) and 18 <= x <= 100, "must be 18-100")
    salary = Validated(lambda x: isinstance(x, (int, float)) and x >= 0, "must be non-negative")

    def __init__(self, name, age, salary):
        self.name = name
        self.age = age
        self.salary = salary

emp = Employee("Alice", 30, 75000)
print(f"  {emp.name}, age {emp.age}, ${emp.salary}")

try:
    emp.age = 15
except ValueError as e:
    print(f"  Validation: {e}")


# --- Summary ---
print("\n" + "=" * 60)
print("PATTERN SUMMARY")
print("=" * 60)
print("""
| Pattern          | Python Approach                     | When                    |
|------------------|-------------------------------------|-------------------------|
| Singleton        | Module variable or decorator        | Shared resources        |
| Factory          | Dict of classes + function          | Dynamic object creation |
| Builder          | Chained methods returning self      | Complex construction    |
| Decorator (obj)  | Wrapper classes                     | Add behavior to objects |
| Adapter          | Wrapper translating interface       | Integrate old/new code  |
| Proxy            | Lazy wrapper                        | Expensive init, caching |
| Observer         | EventEmitter / callbacks            | Event-driven systems    |
| Strategy         | Pass functions (no class needed!)   | Swappable algorithms    |
| Chain of Resp.   | Linked handlers                     | Middleware, validation  |
| Command          | Callable objects with undo          | Undo/redo, queuing      |
| State Machine    | State classes with transitions      | Workflow, protocols     |
| Mixin            | Multiple inheritance                | Reusable behavior       |
| Descriptor       | __get__/__set__/__set_name__        | Attribute validation    |
| Iterator         | __iter__/yield (built-in!)          | Traversal               |

Key Python insight: many patterns that need classes in Java
are just functions, decorators, or generators in Python.
""")
