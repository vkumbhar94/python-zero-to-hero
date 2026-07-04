# Lesson 16: Object-Oriented Programming (Classes & Inheritance)

# --- Basic Class ---
print("=== Basic Class ===")

class Dog:
    # Class variable (shared by all instances)
    species = "Canis familiaris"

    # Constructor (initializer)
    def __init__(self, name, age):
        # Instance variables (unique to each instance)
        self.name = name
        self.age = age

    # Instance method
    def bark(self):
        return f"{self.name} says Woof!"

    # String representation
    def __repr__(self):
        return f"Dog(name='{self.name}', age={self.age})"

    def __str__(self):
        return f"{self.name}, {self.age} years old"

rex = Dog("Rex", 5)
bella = Dog("Bella", 3)

print(rex.bark())          # Rex says Woof!
print(rex.name)            # Rex
print(Dog.species)         # Canis familiaris (class variable)
print(rex.species)         # same — accessed via instance too
print(repr(rex))           # Dog(name='Rex', age=5)
print(str(bella))          # Bella, 3 years old
print(rex)                 # uses __str__ when printing

# --- self explained ---
# 'self' is the instance itself (like 'this' in Java)
# Python passes it automatically when you call methods
# rex.bark() → Dog.bark(rex)

# --- Properties (getters/setters the Pythonic way) ---
print("\n=== Properties ===")

class Circle:
    def __init__(self, radius):
        self._radius = radius  # convention: _ prefix = "private"

    @property
    def radius(self):
        """Getter — accessed like an attribute."""
        return self._radius

    @radius.setter
    def radius(self, value):
        """Setter — with validation."""
        if value < 0:
            raise ValueError("Radius cannot be negative")
        self._radius = value

    @property
    def area(self):
        """Computed property — read only."""
        import math
        return math.pi * self._radius ** 2

c = Circle(5)
print(f"Radius: {c.radius}")  # uses getter
print(f"Area: {c.area:.2f}")

c.radius = 10                 # uses setter
print(f"New radius: {c.radius}")

try:
    c.radius = -1             # setter validates
except ValueError as e:
    print(f"Error: {e}")

# c.area = 100  # AttributeError — no setter defined

# --- Inheritance ---
print("\n=== Inheritance ===")

class Animal:
    def __init__(self, name, sound):
        self.name = name
        self.sound = sound

    def speak(self):
        return f"{self.name} says {self.sound}!"

    def __repr__(self):
        return f"{type(self).__name__}('{self.name}')"

class Cat(Animal):
    def __init__(self, name, indoor=True):
        super().__init__(name, "Meow")  # call parent constructor
        self.indoor = indoor

    def purr(self):
        return f"{self.name} purrs..."

class Dog2(Animal):
    def __init__(self, name, breed):
        super().__init__(name, "Woof")
        self.breed = breed

    def fetch(self, item):
        return f"{self.name} fetches the {item}!"

cat = Cat("Whiskers")
dog = Dog2("Max", "Labrador")

print(cat.speak())       # inherited method
print(cat.purr())        # Cat-specific method
print(dog.speak())       # inherited method
print(dog.fetch("ball")) # Dog-specific method

print(isinstance(cat, Cat))     # True
print(isinstance(cat, Animal))  # True (inheritance)
print(isinstance(dog, Cat))     # False

# --- Method Overriding ---
print("\n=== Method Overriding ===")

class Shape:
    def area(self):
        raise NotImplementedError("Subclasses must implement area()")

    def describe(self):
        return f"{type(self).__name__} with area {self.area():.2f}"

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

class Triangle(Shape):
    def __init__(self, base, height):
        self.base = base
        self.height = height

    def area(self):
        return 0.5 * self.base * self.height

shapes = [Rectangle(4, 5), Triangle(6, 3)]
for shape in shapes:
    print(f"  {shape.describe()}")

# --- Multiple Inheritance & MRO ---
print("\n=== Multiple Inheritance ===")

class Flyable:
    def fly(self):
        return f"{self.name} is flying!"

class Swimmable:
    def swim(self):
        return f"{self.name} is swimming!"

class Duck(Animal, Flyable, Swimmable):
    def __init__(self, name):
        super().__init__(name, "Quack")

duck = Duck("Donald")
print(duck.speak())  # from Animal
print(duck.fly())    # from Flyable
print(duck.swim())   # from Swimmable

# MRO (Method Resolution Order) — which class is checked first
print(f"MRO: {[c.__name__ for c in Duck.__mro__]}")

# --- Dunder (Magic) Methods ---
print("\n=== Dunder Methods ===")

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    # String representations
    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

    def __str__(self):
        return f"({self.x}, {self.y})"

    # Arithmetic operators
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar)

    # Comparison
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return self.magnitude() < other.magnitude()

    # Length / truthiness
    def __abs__(self):
        return self.magnitude()

    def __bool__(self):
        return self.x != 0 or self.y != 0

    # Container-like behavior
    def __len__(self):
        return 2

    def __getitem__(self, index):
        return (self.x, self.y)[index]

    def __iter__(self):
        yield self.x
        yield self.y

    # Callable
    def __call__(self, scalar):
        return self * scalar

    def magnitude(self):
        return (self.x ** 2 + self.y ** 2) ** 0.5

v1 = Vector(3, 4)
v2 = Vector(1, 2)

print(f"v1 = {v1}")           # __str__
print(f"repr: {repr(v1)}")    # __repr__
print(f"v1 + v2 = {v1 + v2}") # __add__
print(f"v1 - v2 = {v1 - v2}") # __sub__
print(f"v1 * 3 = {v1 * 3}")   # __mul__
print(f"v1 == v2: {v1 == v2}") # __eq__
print(f"|v1| = {abs(v1)}")     # __abs__
print(f"v1[0] = {v1[0]}")      # __getitem__
print(f"len(v1) = {len(v1)}")  # __len__
print(f"v1(2) = {v1(2)}")      # __call__
x, y = v1                       # __iter__ (unpacking)
print(f"unpacked: x={x}, y={y}")

# Common dunder methods reference:
print("""
| Method          | Triggered by           |
|-----------------|------------------------|
| __init__        | Constructor            |
| __repr__        | repr(), debugging      |
| __str__         | str(), print()         |
| __add__         | +                      |
| __sub__         | -                      |
| __mul__         | *                      |
| __eq__          | ==                     |
| __lt__          | <                      |
| __hash__        | hash(), dict keys      |
| __len__         | len()                  |
| __getitem__     | obj[key]               |
| __setitem__     | obj[key] = val         |
| __contains__    | 'in' operator          |
| __iter__        | for loop, unpacking    |
| __call__        | obj()                  |
| __enter/exit__  | with statement         |
""")

# --- Class Methods & Static Methods ---
print("=== Class & Static Methods ===")

class Employee:
    raise_rate = 1.05  # 5% raise
    _count = 0

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
        Employee._count += 1

    # Regular method — operates on instance (self)
    def apply_raise(self):
        self.salary *= self.raise_rate

    # Class method — operates on class (cls), not instance
    @classmethod
    def set_raise_rate(cls, rate):
        cls.raise_rate = rate

    # Class method as alternative constructor
    @classmethod
    def from_string(cls, emp_str):
        name, salary = emp_str.split(",")
        return cls(name, float(salary))

    @classmethod
    def get_count(cls):
        return cls._count

    # Static method — no access to instance or class
    @staticmethod
    def is_workday(day):
        return day.weekday() < 5

e1 = Employee("Alice", 50000)
e2 = Employee.from_string("Bob,60000")  # alternative constructor
print(f"{e1.name}: ${e1.salary}")
print(f"{e2.name}: ${e2.salary}")
print(f"Total employees: {Employee.get_count()}")

Employee.set_raise_rate(1.10)  # affects all instances
e1.apply_raise()
print(f"After 10% raise: {e1.name}: ${e1.salary}")

from datetime import date
print(f"Is today a workday? {Employee.is_workday(date.today())}")

# --- Abstract Base Classes ---
print("\n=== Abstract Classes ===")
from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    @abstractmethod
    def process(self, amount):
        """Subclasses MUST implement this."""
        pass

    @abstractmethod
    def refund(self, amount):
        pass

    # Concrete method (inherited as-is)
    def validate_amount(self, amount):
        if amount <= 0:
            raise ValueError("Amount must be positive")

class CreditCardProcessor(PaymentProcessor):
    def process(self, amount):
        self.validate_amount(amount)
        return f"Charged ${amount:.2f} to credit card"

    def refund(self, amount):
        return f"Refunded ${amount:.2f} to credit card"

class PayPalProcessor(PaymentProcessor):
    def process(self, amount):
        self.validate_amount(amount)
        return f"Charged ${amount:.2f} via PayPal"

    def refund(self, amount):
        return f"Refunded ${amount:.2f} via PayPal"

# Can't instantiate abstract class
try:
    p = PaymentProcessor()
except TypeError as e:
    print(f"Can't instantiate: {e}")

# Use concrete implementations
processors = [CreditCardProcessor(), PayPalProcessor()]
for proc in processors:
    print(f"  {proc.process(99.99)}")

# --- dataclass (modern Python classes) ---
print("\n=== dataclasses ===")
from dataclasses import dataclass, field

@dataclass
class Product:
    name: str
    price: float
    quantity: int = 0
    tags: list = field(default_factory=list)  # mutable default done right

    @property
    def total_value(self):
        return self.price * self.quantity

# Auto-generates: __init__, __repr__, __eq__
p1 = Product("Widget", 9.99, 100)
p2 = Product("Widget", 9.99, 100)
p3 = Product("Gadget", 19.99, 50, ["electronics", "new"])

print(p1)                     # auto __repr__
print(f"p1 == p2: {p1 == p2}")  # auto __eq__
print(f"Total value: ${p1.total_value}")
print(f"Tags: {p3.tags}")

# Frozen (immutable) dataclass
@dataclass(frozen=True)
class Coordinate:
    lat: float
    lon: float

coord = Coordinate(40.7128, -74.0060)
print(coord)
# coord.lat = 0  # FrozenInstanceError!

# Ordered dataclass
@dataclass(order=True)
class Version:
    major: int
    minor: int
    patch: int

versions = [Version(2, 1, 0), Version(1, 9, 5), Version(2, 0, 1)]
print(f"Sorted: {sorted(versions)}")

# --- Slots (memory optimization) ---
print("\n=== __slots__ ===")

class HeavyPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class LightPoint:
    __slots__ = ("x", "y")  # fixed attributes, no __dict__
    def __init__(self, x, y):
        self.x = x
        self.y = y

import sys
h = HeavyPoint(1, 2)
l = LightPoint(1, 2)
print(f"Without slots: {sys.getsizeof(h.__dict__)} bytes for __dict__")
# l.__dict__  # AttributeError — no __dict__ with slots!
# l.z = 3    # AttributeError — can't add new attributes

# dataclass with slots (Python 3.10+)
@dataclass(slots=True)
class FastPoint:
    x: float
    y: float

fp = FastPoint(1.0, 2.0)
print(f"dataclass slots: {fp}")
