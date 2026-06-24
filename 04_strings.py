# Lesson 4: Strings

# --- Creating Strings ---
single = 'hello'
double = "hello"
multi = """This spans
multiple lines"""

# --- String Indexing (0-based) ---
print("=== Indexing ===")
s = "Python"
print(s[0])    # P (first)
print(s[-1])   # n (last)
print(s[-2])   # o (second from end)

# --- Slicing [start:stop:step] ---
print("\n=== Slicing ===")
s = "Hello, World!"
print(s[0:5])    # Hello (start to stop-1)
print(s[7:])     # World! (7 to end)
print(s[:5])     # Hello (start to 5)
print(s[::2])    # Hlo ol! (every 2nd char)
print(s[::-1])   # !dlroW ,olleH (reversed)

# --- String Methods (strings are immutable — methods return new strings) ---
print("\n=== Methods ===")
text = "  Hello, World!  "

print(text.strip())       # "Hello, World!" (remove whitespace)
print(text.lstrip())      # "Hello, World!  "
print(text.rstrip())      # "  Hello, World!"

msg = "hello world"
print(msg.upper())        # HELLO WORLD
print(msg.lower())        # hello world
print(msg.title())        # Hello World
print(msg.capitalize())   # Hello world

print(msg.replace("world", "Python"))  # hello Python
print(msg.count("l"))     # 3
print(msg.find("world"))  # 6 (index where found, -1 if not)
print(msg.startswith("hello"))  # True
print(msg.endswith("world"))    # True

# Split and Join
print("\n=== Split & Join ===")
csv = "apple,banana,cherry"
fruits = csv.split(",")
print(fruits)  # ['apple', 'banana', 'cherry']

words = ["Python", "is", "awesome"]
sentence = " ".join(words)
print(sentence)  # Python is awesome

path = "/".join(["usr", "local", "bin"])
print(path)  # usr/local/bin

# --- String Formatting (3 ways) ---
print("\n=== Formatting ===")
name = "Alice"
age = 30

# 1. f-strings (recommended — Python 3.6+)
print(f"My name is {name} and I'm {age} years old")
print(f"Next year I'll be {age + 1}")  # expressions inside {}
print(f"{'hello':>10}")   # "     hello" (right-align, width 10)
print(f"{'hello':<10}!")  # "hello     !" (left-align)
print(f"{'hello':^10}")   # "  hello   " (center)
print(f"{3.14159:.2f}")   # "3.14" (2 decimal places)
print(f"{1000000:,}")     # "1,000,000" (thousands separator)

# 2. .format() method
print("Hello, {}! You are {}".format(name, age))
print("{1} is {0} years old".format(age, name))

# 3. % operator (old style — you'll see in legacy code)
print("Hello, %s! You are %d" % (name, age))

# --- Escape Characters ---
print("\n=== Escape Characters ===")
print("Line 1\nLine 2")       # newline
print("Tab\there")             # tab
print("She said \"hi\"")      # escaped quotes
print('She said "hi"')        # or use other quote type
print("Backslash: \\")        # literal backslash

# Raw strings (no escaping)
print(r"C:\new\folder")  # C:\new\folder (no \n interpretation)

# --- Useful String Checks ---
print("\n=== Checking Strings ===")
print("hello123".isalnum())    # True (letters + digits)
print("hello".isalpha())       # True (only letters)
print("12345".isdigit())       # True (only digits)
print("hello".islower())       # True
print("HELLO".isupper())       # True
print("   ".isspace())         # True

# --- String Immutability ---
print("\n=== Immutability ===")
s = "hello"
# s[0] = "H"  # ERROR! Strings cannot be modified in place
s = "H" + s[1:]  # Create a new string instead
print(s)  # Hello

# --- String Multiplication & Membership ---
print("\n=== Other Tricks ===")
print("-" * 30)          # ------------------------------ (repeat)
print("py" in "python")  # True (substring check)
print(len("hello"))      # 5 (length)
