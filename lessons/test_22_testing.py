# Test file for Lesson 22
# Run with: pytest test_22_testing.py -v

# pytest discovers tests automatically:
# - Files named test_*.py or *_test.py
# - Functions named test_*
# - Classes named Test*

import pytest
from unittest.mock import Mock, patch, MagicMock
from io import StringIO

import sys
sys.path.insert(0, ".")
from importlib import import_module
_mod = import_module("22_testing")
Calculator = _mod.Calculator
is_palindrome = _mod.is_palindrome
fizzbuzz = _mod.fizzbuzz
BankAccount = _mod.BankAccount


# ============================================================
# PART 1: Basic Tests (assert)
# ============================================================

# --- Simple function tests ---
class TestIsPalindrome:
    def test_simple_palindrome(self):
        assert is_palindrome("racecar")

    def test_not_palindrome(self):
        assert not is_palindrome("hello")

    def test_palindrome_with_spaces(self):
        assert is_palindrome("race car")

    def test_case_insensitive(self):
        assert is_palindrome("Racecar")

    def test_empty_string(self):
        assert is_palindrome("")

    def test_single_char(self):
        assert is_palindrome("a")


# --- Class method tests ---
class TestCalculator:
    # setup runs before EACH test method
    def setup_method(self):
        self.calc = Calculator()

    def test_add(self):
        assert self.calc.add(2, 3) == 5

    def test_add_negative(self):
        assert self.calc.add(-1, -1) == -2

    def test_add_float(self):
        assert self.calc.add(0.1, 0.2) == pytest.approx(0.3)

    def test_subtract(self):
        assert self.calc.subtract(10, 3) == 7

    def test_multiply(self):
        assert self.calc.multiply(4, 5) == 20

    def test_multiply_by_zero(self):
        assert self.calc.multiply(100, 0) == 0

    def test_divide(self):
        assert self.calc.divide(10, 3) == pytest.approx(3.333, rel=1e-2)

    def test_divide_by_zero(self):
        with pytest.raises(ValueError, match="Cannot divide by zero"):
            self.calc.divide(10, 0)


# ============================================================
# PART 2: Fixtures
# ============================================================

# Fixtures provide reusable test setup/teardown

@pytest.fixture
def account():
    """Create a fresh bank account for each test."""
    return BankAccount("Alice", 1000)

@pytest.fixture
def empty_account():
    return BankAccount("Bob")


class TestBankAccount:
    def test_initial_balance(self, account):
        assert account.balance == 1000

    def test_deposit(self, account):
        account.deposit(500)
        assert account.balance == 1500

    def test_withdraw(self, account):
        account.withdraw(300)
        assert account.balance == 700

    def test_withdraw_insufficient(self, account):
        with pytest.raises(ValueError, match="Insufficient funds"):
            account.withdraw(2000)

    def test_negative_deposit(self, account):
        with pytest.raises(ValueError, match="Deposit must be positive"):
            account.deposit(-100)

    def test_negative_withdraw(self, account):
        with pytest.raises(ValueError, match="Withdrawal must be positive"):
            account.withdraw(-50)

    def test_empty_account(self, empty_account):
        assert empty_account.balance == 0
        empty_account.deposit(100)
        assert empty_account.balance == 100

    def test_repr(self, account):
        assert repr(account) == "BankAccount('Alice', 1000)"


# Fixture with teardown
@pytest.fixture
def temp_file(tmp_path):
    """Create a temp file that's auto-cleaned up."""
    file = tmp_path / "test.txt"
    file.write_text("test data")
    yield file  # test runs here
    # teardown: tmp_path is auto-cleaned by pytest


def test_temp_file(temp_file):
    assert temp_file.read_text() == "test data"


# Fixture with scope (shared across tests)
@pytest.fixture(scope="module")
def shared_calculator():
    """Created once, shared by all tests in this module."""
    print("\n  Creating shared calculator")
    return Calculator()

def test_shared_add(shared_calculator):
    assert shared_calculator.add(1, 1) == 2

def test_shared_subtract(shared_calculator):
    assert shared_calculator.subtract(5, 3) == 2


# ============================================================
# PART 3: Parametrize (run same test with different data)
# ============================================================

@pytest.mark.parametrize("input_str, expected", [
    ("racecar", True),
    ("hello", False),
    ("madam", True),
    ("", True),
    ("a", True),
    ("ab", False),
    ("aba", True),
])
def test_palindrome_parametrize(input_str, expected):
    assert is_palindrome(input_str) == expected


@pytest.mark.parametrize("n, expected", [
    (1, "1"),
    (3, "Fizz"),
    (5, "Buzz"),
    (15, "FizzBuzz"),
    (7, "7"),
    (9, "Fizz"),
    (10, "Buzz"),
    (30, "FizzBuzz"),
])
def test_fizzbuzz(n, expected):
    assert fizzbuzz(n) == expected


@pytest.mark.parametrize("a, b, expected", [
    (2, 3, 5),
    (-1, 1, 0),
    (0, 0, 0),
    (100, 200, 300),
    (-5, -3, -8),
])
def test_add_parametrize(a, b, expected):
    calc = Calculator()
    assert calc.add(a, b) == expected


# ============================================================
# PART 4: Markers (skip, xfail, custom)
# ============================================================

@pytest.mark.skip(reason="Feature not implemented yet")
def test_future_feature():
    assert False

@pytest.mark.skipif(
    not hasattr(str, "removeprefix"),
    reason="Requires Python 3.9+"
)
def test_removeprefix():
    assert "HelloWorld".removeprefix("Hello") == "World"

@pytest.mark.xfail(reason="Known bug — fix in next sprint")
def test_known_bug():
    assert 0.1 + 0.2 == 0.3  # fails due to float precision


# ============================================================
# PART 5: Mocking
# ============================================================

# Mock external dependencies (APIs, databases, file system)

class UserService:
    def __init__(self, api_client):
        self.api = api_client

    def get_user_name(self, user_id: int) -> str:
        response = self.api.get(f"/users/{user_id}")
        return response["name"]

    def create_user(self, name: str) -> dict:
        return self.api.post("/users", data={"name": name})


class TestUserService:
    def test_get_user_name(self):
        # Create a mock API client
        mock_api = Mock()
        mock_api.get.return_value = {"name": "Alice", "id": 1}

        service = UserService(mock_api)
        name = service.get_user_name(1)

        assert name == "Alice"
        mock_api.get.assert_called_once_with("/users/1")

    def test_create_user(self):
        mock_api = Mock()
        mock_api.post.return_value = {"id": 42, "name": "Bob"}

        service = UserService(mock_api)
        result = service.create_user("Bob")

        assert result == {"id": 42, "name": "Bob"}
        mock_api.post.assert_called_once_with("/users", data={"name": "Bob"})

    def test_api_failure(self):
        mock_api = Mock()
        mock_api.get.side_effect = ConnectionError("API down")

        service = UserService(mock_api)
        with pytest.raises(ConnectionError):
            service.get_user_name(1)


# patch — replace objects in the module being tested
import time as time_module

def get_greeting() -> str:
    hour = time_module.localtime().tm_hour
    if hour < 12:
        return "Good morning"
    elif hour < 18:
        return "Good afternoon"
    return "Good evening"

class TestGreeting:
    @patch("time.localtime")
    def test_morning(self, mock_time):
        mock_time.return_value = Mock(tm_hour=9)
        assert get_greeting() == "Good morning"

    @patch("time.localtime")
    def test_afternoon(self, mock_time):
        mock_time.return_value = Mock(tm_hour=14)
        assert get_greeting() == "Good afternoon"

    @patch("time.localtime")
    def test_evening(self, mock_time):
        mock_time.return_value = Mock(tm_hour=20)
        assert get_greeting() == "Good evening"


# ============================================================
# PART 6: Testing Exceptions and Warnings
# ============================================================

def test_raises_type_error():
    with pytest.raises(TypeError):
        "hello" + 42

def test_raises_with_message():
    with pytest.raises(ValueError) as exc_info:
        int("not_a_number")
    assert "invalid literal" in str(exc_info.value)

def test_warning():
    import warnings
    with pytest.warns(DeprecationWarning):
        warnings.warn("old function", DeprecationWarning)


# ============================================================
# PART 7: Capturing Output
# ============================================================

def loud_function():
    print("Hello, World!")
    print("Processing...")
    return 42

def test_capture_stdout(capsys):
    result = loud_function()
    captured = capsys.readouterr()

    assert result == 42
    assert "Hello, World!" in captured.out
    assert "Processing..." in captured.out


# ============================================================
# PART 8: conftest.py and Project Structure
# ============================================================

# conftest.py — shared fixtures across test files
# pytest automatically discovers it (no import needed)

# Example conftest.py:
"""
# conftest.py
import pytest

@pytest.fixture(scope="session")
def db_connection():
    conn = create_connection()
    yield conn
    conn.close()

@pytest.fixture
def sample_data():
    return {"users": [{"name": "Alice"}, {"name": "Bob"}]}
"""

# Project structure:
"""
my_project/
├── src/
│   └── my_app/
│       ├── __init__.py
│       ├── models.py
│       └── services.py
├── tests/
│   ├── conftest.py          ← shared fixtures
│   ├── test_models.py
│   ├── test_services.py
│   └── integration/
│       ├── conftest.py      ← integration-specific fixtures
│       └── test_api.py
├── pyproject.toml
└── pytest.ini / pyproject.toml  ← pytest config
"""


# ============================================================
# PART 9: pytest Configuration & Commands
# ============================================================

# pyproject.toml configuration:
"""
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
addopts = "-v --strict-markers"
markers = [
    "slow: marks tests as slow",
    "integration: integration tests",
]
"""

# Common pytest commands:
"""
pytest                          # run all tests
pytest test_file.py             # run specific file
pytest test_file.py::test_func  # run specific test
pytest test_file.py::TestClass  # run specific class
pytest -v                       # verbose output
pytest -x                       # stop on first failure
pytest -s                       # show print output
pytest -k "palindrome"          # run tests matching name
pytest -k "not slow"            # exclude tests by name
pytest --tb=short               # shorter tracebacks
pytest --lf                     # rerun last failures only
pytest --ff                     # run failures first
pytest -n auto                  # parallel (pip install pytest-xdist)
pytest --cov=src                # coverage (pip install pytest-cov)
pytest --cov=src --cov-report=html  # HTML coverage report
"""


# ============================================================
# PART 10: unittest (standard library alternative)
# ============================================================

import unittest

class TestCalculatorUnittest(unittest.TestCase):
    def setUp(self):
        """Runs before each test (like setup_method in pytest)."""
        self.calc = Calculator()

    def test_add(self):
        self.assertEqual(self.calc.add(2, 3), 5)

    def test_subtract(self):
        self.assertEqual(self.calc.subtract(10, 3), 7)

    def test_divide_by_zero(self):
        with self.assertRaises(ValueError):
            self.calc.divide(10, 0)

    def test_float_approx(self):
        self.assertAlmostEqual(self.calc.add(0.1, 0.2), 0.3, places=5)

    # unittest assertion methods:
    # assertEqual, assertNotEqual
    # assertTrue, assertFalse
    # assertIs, assertIsNot
    # assertIsNone, assertIsNotNone
    # assertIn, assertNotIn
    # assertRaises, assertWarns
    # assertAlmostEqual


# Run with: python -m pytest test_22_testing.py -v
# Or:       python -m unittest test_22_testing.TestCalculatorUnittest
