# Lesson 13: File I/O

import os

# --- Writing Files ---
print("=== Writing Files ===")

# Always use 'with' statement — auto-closes file even on error
with open("example.txt", "w") as f:
    f.write("Hello, World!\n")
    f.write("Second line\n")
    f.write("Third line\n")

print("File written!")

# writelines — writes a list of strings (no newlines added!)
lines = ["Line A\n", "Line B\n", "Line C\n"]
with open("example2.txt", "w") as f:
    f.writelines(lines)

# --- Reading Files ---
print("\n=== Reading Files ===")

# read() — entire file as one string
with open("example.txt", "r") as f:
    content = f.read()
print(f"read():\n{content}")

# readline() — one line at a time
with open("example.txt", "r") as f:
    first = f.readline()   # includes \n
    second = f.readline()
print(f"readline(): {first.strip()}, {second.strip()}")

# readlines() — list of all lines
with open("example.txt", "r") as f:
    all_lines = f.readlines()
print(f"readlines(): {all_lines}")

# Iterate line by line (memory efficient — best for large files)
print("\nIterating:")
with open("example.txt", "r") as f:
    for line in f:
        print(f"  {line.strip()}")

# --- File Modes ---
print("\n=== File Modes ===")
print("""
| Mode | Description                          |
|------|--------------------------------------|
| 'r'  | Read (default). Error if not exists  |
| 'w'  | Write. Creates/truncates file        |
| 'a'  | Append. Creates if not exists        |
| 'x'  | Exclusive create. Error if exists    |
| 'r+' | Read + Write (file must exist)       |
| 'w+' | Write + Read (truncates)             |
| 'a+' | Append + Read                        |
| 'rb' | Read binary                          |
| 'wb' | Write binary                         |
""")

# Append mode
with open("example.txt", "a") as f:
    f.write("Appended line\n")

with open("example.txt", "r") as f:
    print(f.read())

# Exclusive create (fails if exists)
try:
    with open("example.txt", "x") as f:
        f.write("new file")
except FileExistsError:
    print("File already exists! (x mode failed)")

# --- Working with Paths ---
print("\n=== Paths (os.path & pathlib) ===")

# os.path (traditional)
print(os.path.exists("example.txt"))      # True
print(os.path.isfile("example.txt"))      # True
print(os.path.isdir("example.txt"))       # False
print(os.path.getsize("example.txt"))     # file size in bytes
print(os.path.abspath("example.txt"))     # absolute path
print(os.path.basename("/usr/local/bin")) # bin
print(os.path.dirname("/usr/local/bin"))  # /usr/local
print(os.path.join("dir", "sub", "file.txt"))  # dir/sub/file.txt

# pathlib (modern, preferred — Python 3.4+)
from pathlib import Path

p = Path("example.txt")
print(f"\nPathlib:")
print(f"  exists: {p.exists()}")
print(f"  name: {p.name}")
print(f"  stem: {p.stem}")          # filename without extension
print(f"  suffix: {p.suffix}")      # .txt
print(f"  parent: {p.parent}")
print(f"  absolute: {p.absolute()}")
print(f"  size: {p.stat().st_size}")

# Path operations
data_dir = Path("data") / "subdir" / "file.csv"
print(f"  joined: {data_dir}")  # data/subdir/file.csv

# Read/write shortcuts (Python 3.5+)
Path("quick.txt").write_text("Quick write!\nLine 2\n")
content = Path("quick.txt").read_text()
print(f"\n  Path.read_text(): {content.strip()}")

# List directory
print(f"\n  .py files: {list(Path('.').glob('*.txt'))}")

# --- Common Patterns ---
print("\n=== Common Patterns ===")

# 1. Read file into list of stripped lines
with open("example.txt") as f:
    lines = [line.strip() for line in f if line.strip()]
print(f"Non-empty lines: {lines}")

# 2. Process CSV-like data
with open("data.csv", "w") as f:
    f.write("name,age,city\n")
    f.write("Alice,30,NYC\n")
    f.write("Bob,25,London\n")
    f.write("Charlie,35,Tokyo\n")

with open("data.csv") as f:
    header = f.readline().strip().split(",")
    records = []
    for line in f:
        values = line.strip().split(",")
        records.append(dict(zip(header, values)))
print(f"Records: {records}")

# 3. Using the csv module (better for real CSV)
import csv

with open("data.csv") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(f"  {row['name']} is {row['age']} from {row['city']}")

# Write CSV
with open("output.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["name", "score"])
    writer.writerows([["Alice", 85], ["Bob", 92]])

# 4. JSON files
import json

data = {
    "name": "Alice",
    "scores": [85, 92, 78],
    "active": True,
}

# Write JSON
with open("data.json", "w") as f:
    json.dump(data, f, indent=2)

# Read JSON
with open("data.json") as f:
    loaded = json.load(f)
print(f"\nJSON loaded: {loaded}")
print(f"  name: {loaded['name']}")
print(f"  scores: {loaded['scores']}")

# JSON to/from string
json_str = json.dumps(data, indent=2)
print(f"\nJSON string:\n{json_str}")
parsed = json.loads(json_str)

# 5. Working with binary files
with open("binary.dat", "wb") as f:
    f.write(b"\x00\x01\x02\x03\x04")

with open("binary.dat", "rb") as f:
    data = f.read()
    print(f"\nBinary: {data}")
    print(f"  bytes: {list(data)}")

# --- Error Handling with Files ---
print("\n=== Error Handling ===")

# Check before opening
if os.path.exists("maybe.txt"):
    with open("maybe.txt") as f:
        print(f.read())
else:
    print("maybe.txt doesn't exist")

# Or use try/except (EAFP style — preferred in Python)
try:
    with open("nonexistent.txt") as f:
        content = f.read()
except FileNotFoundError:
    print("File not found!")
except PermissionError:
    print("No permission to read!")
except IOError as e:
    print(f"IO error: {e}")

# --- Temporary Files ---
print("\n=== Temp Files ===")
import tempfile

# Auto-deleted when closed
with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
    f.write("temporary data")
    temp_path = f.name
print(f"Temp file at: {temp_path}")
os.unlink(temp_path)  # manual cleanup since delete=False

# Temp directory
with tempfile.TemporaryDirectory() as tmpdir:
    print(f"Temp dir: {tmpdir}")
    temp_file = Path(tmpdir) / "file.txt"
    temp_file.write_text("hello from temp")
    print(f"  Content: {temp_file.read_text()}")
# Directory and contents auto-deleted here

# --- Cleanup demo files ---
for f in ["example.txt", "example2.txt", "quick.txt", "data.csv",
          "output.csv", "data.json", "binary.dat"]:
    Path(f).unlink(missing_ok=True)
print("\nCleaned up demo files.")
