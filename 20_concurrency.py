# Lesson 20: Concurrency (threading, multiprocessing, asyncio)

# Three models:
# 1. Threading — concurrent I/O, shared memory, GIL-limited
# 2. Multiprocessing — true parallelism, separate memory
# 3. Asyncio — single-threaded concurrency for I/O-bound work

import time
import threading
import multiprocessing
import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
import random


# --- Functions at module level (required for multiprocessing on macOS) ---

def cpu_heavy(n):
    """CPU-intensive task."""
    return sum(i * i for i in range(n))


def process_worker(name):
    pid = multiprocessing.current_process().pid
    print(f"  {name} running in PID {pid}")
    return name


def mp_producer(queue, items):
    for item in items:
        queue.put(item)
        print(f"  Produced: {item}")
    queue.put(None)


def mp_consumer(queue):
    while True:
        item = queue.get()
        if item is None:
            break
        print(f"  Consumed: {item}")


# multiprocessing requires if __name__ == "__main__" on macOS (spawn)
if __name__ == "__main__":

    # ============================================================
    # PART 1: Threading
    # ============================================================
    print("=" * 60)
    print("PART 1: Threading")
    print("=" * 60)

    # --- Basic Thread ---
    print("\n=== Basic Thread ===")

    def worker(name, seconds):
        print(f"  {name} starting")
        time.sleep(seconds)
        print(f"  {name} finished after {seconds}s")

    # Sequential (slow)
    start = time.perf_counter()
    worker("Task-1", 0.5)
    worker("Task-2", 0.5)
    seq_time = time.perf_counter() - start
    print(f"  Sequential: {seq_time:.2f}s")

    # Threaded (fast — runs concurrently)
    start = time.perf_counter()
    t1 = threading.Thread(target=worker, args=("Thread-1", 0.5))
    t2 = threading.Thread(target=worker, args=("Thread-2", 0.5))
    t1.start()
    t2.start()
    t1.join()  # wait for thread to finish
    t2.join()
    thread_time = time.perf_counter() - start
    print(f"  Threaded: {thread_time:.2f}s")

    # --- Thread with Return Values ---
    print("\n=== Thread Results ===")

    results = {}

    def fetch_data(url, result_dict, key):
        """Simulate fetching data (threads can't return values directly)."""
        time.sleep(0.3)
        result_dict[key] = f"Data from {url}"

    threads = []
    urls = ["api.example.com/1", "api.example.com/2", "api.example.com/3"]
    for i, url in enumerate(urls):
        t = threading.Thread(target=fetch_data, args=(url, results, i))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
    print(f"  Results: {results}")

    # --- ThreadPoolExecutor (preferred API) ---
    print("\n=== ThreadPoolExecutor ===")

    def fetch(url):
        time.sleep(0.2)
        return f"Data from {url}"

    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=5) as executor:
        # submit — returns Future
        future = executor.submit(fetch, "api.example.com/single")
        print(f"  Future result: {future.result()}")

        # map — parallel map, results in order
        urls = [f"api.example.com/{i}" for i in range(5)]
        results = list(executor.map(fetch, urls))
        print(f"  Map results: {results}")

    elapsed = time.perf_counter() - start
    print(f"  Total time: {elapsed:.2f}s (vs ~1.0s sequential)")

    # --- as_completed — get results as they finish ---
    print("\n=== as_completed ===")

    def variable_task(task_id):
        delay = random.uniform(0.1, 0.5)
        time.sleep(delay)
        return f"Task-{task_id} ({delay:.2f}s)"

    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = {executor.submit(variable_task, i): i for i in range(4)}
        for future in as_completed(futures):
            task_id = futures[future]
            print(f"  Completed: {future.result()}")

    # --- Thread Safety & Locks ---
    print("\n=== Thread Safety ===")

    # Problem: race condition
    counter = 0

    def increment_unsafe(n):
        global counter
        for _ in range(n):
            counter += 1  # NOT atomic! read → modify → write

    counter = 0
    threads = [threading.Thread(target=increment_unsafe, args=(100000,)) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(f"  Unsafe counter (expect 500000): {counter}")  # likely wrong!

    # Solution: use a Lock
    lock = threading.Lock()
    counter = 0

    def increment_safe(n):
        global counter
        for _ in range(n):
            with lock:  # acquire/release automatically
                counter += 1

    counter = 0
    threads = [threading.Thread(target=increment_safe, args=(100000,)) for _ in range(5)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(f"  Safe counter (expect 500000): {counter}")  # always correct

    # --- Other Synchronization Primitives ---
    print("\n=== Synchronization Primitives ===")

    # Event — one thread signals, others wait
    event = threading.Event()

    def waiter(name):
        print(f"  {name} waiting...")
        event.wait()
        print(f"  {name} proceeding!")

    t1 = threading.Thread(target=waiter, args=("W1",))
    t2 = threading.Thread(target=waiter, args=("W2",))
    t1.start()
    t2.start()
    time.sleep(0.2)
    print("  Signaling event!")
    event.set()
    t1.join()
    t2.join()

    # Semaphore — limit concurrent access
    print()
    semaphore = threading.Semaphore(2)

    def limited_worker(name):
        with semaphore:
            print(f"  {name} acquired (max 2 at a time)")
            time.sleep(0.2)
            print(f"  {name} released")

    threads = [threading.Thread(target=limited_worker, args=(f"W{i}",)) for i in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # --- Thread-local Data ---
    print("\n=== Thread-local ===")
    local_data = threading.local()

    def set_and_get(value):
        local_data.value = value
        time.sleep(0.1)
        print(f"  Thread {value}: local_data.value = {local_data.value}")

    threads = [threading.Thread(target=set_and_get, args=(i,)) for i in range(3)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    # --- The GIL ---
    print("\n=== The GIL ===")
    print("""  The GIL prevents multiple threads from executing Python
  bytecode simultaneously.

  - I/O-bound tasks (network, files): threading WORKS well
    (GIL is released during I/O waits)
  - CPU-bound tasks (math, processing): threading DOESN'T help
    (use multiprocessing instead)
""")

    # ============================================================
    # PART 2: Multiprocessing
    # ============================================================
    print("=" * 60)
    print("PART 2: Multiprocessing")
    print("=" * 60)

    # --- CPU-bound: Threading vs Multiprocessing ---
    print("\n=== CPU-bound Comparison ===")

    N = 2_000_000

    # Sequential
    start = time.perf_counter()
    results = [cpu_heavy(N) for _ in range(4)]
    seq_time = time.perf_counter() - start
    print(f"  Sequential:      {seq_time:.2f}s")

    # Threading (GIL limits — not faster for CPU work)
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=4) as ex:
        results = list(ex.map(cpu_heavy, [N] * 4))
    thread_time = time.perf_counter() - start
    print(f"  ThreadPool:      {thread_time:.2f}s")

    # Multiprocessing (true parallelism!)
    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=4) as ex:
        results = list(ex.map(cpu_heavy, [N] * 4))
    proc_time = time.perf_counter() - start
    print(f"  ProcessPool:     {proc_time:.2f}s")

    # --- multiprocessing.Process ---
    print("\n=== multiprocessing.Process ===")

    p1 = multiprocessing.Process(target=process_worker, args=("P1",))
    p2 = multiprocessing.Process(target=process_worker, args=("P2",))
    p1.start()
    p2.start()
    p1.join()
    p2.join()

    # --- Sharing Data Between Processes ---
    print("\n=== Sharing Data ===")

    q = multiprocessing.Queue()
    p = multiprocessing.Process(target=mp_producer, args=(q, [1, 2, 3]))
    c = multiprocessing.Process(target=mp_consumer, args=(q,))
    p.start()
    c.start()
    p.join()
    c.join()

    # ============================================================
    # PART 3: Asyncio
    # ============================================================
    print("\n" + "=" * 60)
    print("PART 3: Asyncio")
    print("=" * 60)

    # --- async/await basics ---
    print("\n=== async/await Basics ===")

    async def say_hello(name, delay):
        await asyncio.sleep(delay)
        print(f"  Hello, {name}! (after {delay}s)")
        return f"result-{name}"

    result = asyncio.run(say_hello("Alice", 0.1))
    print(f"  Returned: {result}")

    # --- Running Tasks Concurrently ---
    print("\n=== Concurrent Tasks ===")

    async def main_gather():
        start = time.perf_counter()
        results = await asyncio.gather(
            say_hello("Alice", 0.3),
            say_hello("Bob", 0.2),
            say_hello("Charlie", 0.1),
        )
        elapsed = time.perf_counter() - start
        print(f"  All done in {elapsed:.2f}s (not 0.6s!)")
        print(f"  Results: {results}")

    asyncio.run(main_gather())

    # --- Tasks (more control than gather) ---
    print("\n=== asyncio.create_task ===")

    async def main_tasks():
        task1 = asyncio.create_task(say_hello("Task1", 0.3))
        task2 = asyncio.create_task(say_hello("Task2", 0.1))
        print("  Tasks are running in background...")
        result1 = await task1
        result2 = await task2
        print(f"  Got: {result1}, {result2}")

    asyncio.run(main_tasks())

    # --- TaskGroup (Python 3.11+) ---
    print("\n=== TaskGroup (3.11+) ===")

    async def main_taskgroup():
        async with asyncio.TaskGroup() as tg:
            for i in range(3):
                tg.create_task(say_hello(f"TG-{i}", 0.1 * (i + 1)))
        print("  All TaskGroup tasks completed!")

    asyncio.run(main_taskgroup())

    # --- Async Iteration ---
    print("\n=== Async Generators & Iteration ===")

    async def async_counter(n, delay=0.05):
        for i in range(n):
            await asyncio.sleep(delay)
            yield i

    async def main_async_iter():
        values = []
        async for num in async_counter(5):
            values.append(num)
        print(f"  Async iteration: {values}")

        squared = [x ** 2 async for x in async_counter(5)]
        print(f"  Async comprehension: {squared}")

    asyncio.run(main_async_iter())

    # --- Async Context Managers ---
    print("\n=== Async Context Manager ===")

    class AsyncTimer:
        def __init__(self, label):
            self.label = label

        async def __aenter__(self):
            self.start = time.perf_counter()
            return self

        async def __aexit__(self, *exc):
            elapsed = time.perf_counter() - self.start
            print(f"  {self.label}: {elapsed:.4f}s")

    async def main_async_ctx():
        async with AsyncTimer("async work"):
            await asyncio.sleep(0.1)
            print("  Inside async context manager")

    asyncio.run(main_async_ctx())

    # --- Semaphore (limit concurrent async tasks) ---
    print("\n=== Async Semaphore ===")

    async def rate_limited_fetch(sem, url):
        async with sem:
            print(f"  Fetching {url}")
            await asyncio.sleep(0.2)
            return f"Data from {url}"

    async def main_semaphore():
        sem = asyncio.Semaphore(3)
        urls = [f"api.example.com/{i}" for i in range(6)]
        tasks = [rate_limited_fetch(sem, url) for url in urls]
        results = await asyncio.gather(*tasks)
        print(f"  Got {len(results)} results")

    asyncio.run(main_semaphore())

    # --- Timeouts ---
    print("\n=== Timeouts ===")

    async def slow_operation():
        await asyncio.sleep(10)
        return "done"

    async def main_timeout():
        try:
            await asyncio.wait_for(slow_operation(), timeout=0.1)
        except asyncio.TimeoutError:
            print("  wait_for: timed out!")

        try:
            async with asyncio.timeout(0.1):
                await slow_operation()
        except TimeoutError:
            print("  asyncio.timeout: timed out!")

    asyncio.run(main_timeout())

    # --- Mixing Sync and Async ---
    print("\n=== Mixing Sync & Async ===")

    def blocking_io():
        time.sleep(0.2)
        return "blocking result"

    async def main_mixed():
        loop = asyncio.get_event_loop()

        # Run blocking function in thread pool
        result = await loop.run_in_executor(None, blocking_io)
        print(f"  Blocking result: {result}")

        with ThreadPoolExecutor(max_workers=3) as pool:
            results = await asyncio.gather(
                loop.run_in_executor(pool, blocking_io),
                loop.run_in_executor(pool, blocking_io),
                loop.run_in_executor(pool, blocking_io),
            )
            print(f"  Parallel blocking: {len(results)} results")

    asyncio.run(main_mixed())

    # ============================================================
    # PART 4: Choosing the Right Model
    # ============================================================
    print("\n" + "=" * 60)
    print("PART 4: Choosing the Right Model")
    print("=" * 60)
    print("""
| Task Type      | Best Tool              | Why                       |
|----------------|------------------------|---------------------------|
| I/O-bound      | asyncio                | Thousands of concurrent   |
| (many tasks)   |                        | tasks, minimal overhead   |
|                |                        |                           |
| I/O-bound      | ThreadPoolExecutor     | Simple, works with sync   |
| (few tasks)    |                        | libraries                 |
|                |                        |                           |
| CPU-bound      | ProcessPoolExecutor    | True parallelism,         |
|                |                        | bypasses GIL              |
|                |                        |                           |
| Mixed          | asyncio +              | Async for I/O, executor   |
|                | run_in_executor        | for CPU/blocking calls    |

Quick decision:
- Network requests, web scraping → asyncio (or threading)
- File I/O, database queries    → threading or asyncio
- Math, image processing, ML    → multiprocessing
- Simple parallelism            → concurrent.futures
""")
