# Async Journey, Python asyncio from Zero to Production

One concept per file. Run them in order.

```
pip install -r requirements.txt
python sync_problem.py          # start here
python Async_Journey_1.py       # then work through each
```

---

## The Problem, `sync_problem.py`

Fetches 7 URLs one by one. Each request blocks the thread until the server replies.

```
url/1 → wait → url/2 → wait → ... → 7 × ~200ms = slow
```

> **Note:** Your thread is frozen while waiting. It can't do anything else. This is the problem async solves.

---

## Async_Journey_1, Get the event loop

```python
loop = asyncio.get_event_loop()
print(type(loop))        # SelectorEventLoop on Unix
print(loop.is_running()) # False, exists but not started
```

> **Note:** The loop is just a Python object. It exists but hasn't started yet, like a car engine that hasn't been turned on.

---

## Async_Journey_2a, `run_forever`

```python
loop.run_forever()  # surrenders control, never returns
```

> **Note:** You've handed the thread to the loop permanently. Only `loop.stop()` from inside a callback (or Ctrl+C) gets you out.

---

## Async_Journey_2b, `run_until_complete`

```python
loop.run_until_complete(asyncio.sleep(3))
print("control returned")
```

> **Note:** Gives the loop a finish line. When the coroutine completes, control comes back to you. This is what you'll use most in scripts.

---

## Async_Journey_3a, `call_soon`

```python
loop.call_soon(task, "first")
loop.call_soon(task, "second")
loop.call_soon(task, "third")
```

Output, microseconds apart, strictly in order:
```
[10:42:01.000123] 'first'
[10:42:01.000145] 'second'
[10:42:01.000160] 'third'
```

> **Note:** `call_soon` queues a callback, it doesn't run it immediately. One at a time, never in parallel.

---

## Async_Journey_3b, `call_later`

```python
loop.call_later(3, task, "3 seconds later")
loop.call_later(1, task, "1 second later")   # runs first!
loop.call_later(2, task, "2 seconds later")
```

> **Note:** Sorted by delay, not registration order. Also a promise, not a guarantee, if the loop is busy, it fires late.

---

## Async_Journey_4, Trampolines

One `call_soon`. Four executions.

```python
def trampoline(name):
    print(name)
    loop.call_later(0.5, trampoline, name)  # reschedules itself

loop.call_soon(trampoline, "bouncer")
```

> **Note:** A callback that re-registers itself. This is the foundation of all async programming, `async/await` is just trampolines with nicer syntax.

---

## Async_Journey_5, Multiple trampolines

Three independent trampolines. One loop. One thread.

```
[03:00:00.001] 'ALPHA'
[03:00:00.002] 'BETA'
[03:00:00.003] 'GAMMA'
[03:00:00.501] 'ALPHA'   ← starts again
```

> **Note:** Cooperative multitasking. Each callback hands control back to the loop when done. This is exactly how `asyncio.gather()` works internally.

---

## Async_Journey_6, The hog + debug mode

```python
loop.set_debug(True)
loop.call_later(2, hog, "CPU")     # runs a 36-second computation
loop.call_later(6, loop.stop)      # expected to fire at t=6s
```

The 6-second timer fired at **t=38s**. The loop was frozen the entire time.

```
Executing <hog> took 35.911 seconds   ← debug mode caught it
```

> **Note:** `call_later` timers only fire between callbacks. A blocking callback delays everything. `set_debug(True)` tells you exactly what blocked the loop, where it was defined, and how long it ran. Use it always in development.

---

## Async_Journey_7, `async/await` basics

```python
async def main():
    await task()        # runs task fully, then...
    await other_task()  # runs this, still sequential!
```

> **Note:** `await` yields control back to the loop until the coroutine finishes. Sequential `await` is not concurrent, use `gather()` for that. `asyncio.run()` is the modern way to start everything.

---

## Async_Journey_8, `asyncio.gather`, concurrent tasks

```python
await asyncio.gather(
    fetch("A", 3),
    fetch("B", 1),
    fetch("C", 2),
)
# Total time: ~3.00s  (not 6s)
```

> **Note:** All coroutines start at the same time. Total time = slowest, not sum. While A sleeps, B and C make progress. This is the payoff.

---

## Async_Journey_9, Real HTTP with `aiohttp`

```python
async with aiohttp.ClientSession() as session:
    results = await asyncio.gather(
        fetch_url(session, "...todos/1"),
        ...
        fetch_url(session, "...todos/7"),
    )
```

The async answer to `sync_problem.py`. All 7 requests go out simultaneously.

> **Note:** `aiohttp` yields at the network boundary instead of blocking. Always use `ClientSession` as a context manager, never create a new session per request.

---

## Async_Journey_10, Producer / Consumer with `asyncio.Queue`

```python
# Producer puts items. Workers consume them. Queue is the handoff.
workers = [asyncio.create_task(worker(queue, f"W{i}")) for i in range(3)]
await producer(queue)
await queue.join()           # wait until all items processed
for _ in range(3):
    await queue.put(None)    # sentinel, tells each worker to exit
await asyncio.gather(*workers)
```

> **Note:** Workers run `while True` and never stop on their own. Always shut them down explicitly, with a sentinel value or `task.cancel()`. Forgetting this leaks resources.

---

## Async_Journey_11, Timeouts

```python
async with asyncio.timeout(5):   # Python 3.11+
    await some_slow_api()        # takes 10s, gets cancelled at 5s
```

> **Note:** Never trust external services to respond quickly. Without timeouts, one slow dependency holds a worker hostage indefinitely. On Python < 3.11 use `asyncio.wait_for(coro, timeout=5)`.

---

## Async_Journey_12, Production: uvloop + logging

```python
logging.basicConfig(level=logging.DEBUG)

uvloop.install()        # one line, 2-4x faster event loop
asyncio.run(main())
```

> **Note:** `uvloop` is built on `libuv` (the C library powering Node.js). Drop it in before `asyncio.run()` and you're done. Use `logging` instead of `print()` in production, it gives you levels, timestamps, and routing for free.

---

## Full Journey

```
sync_problem          → the pain
1, 2a, 2b             → the loop exists and can be started
3a, 3b                → scheduling callbacks
4, 5                  → trampolines, the real mechanism
6                     → what breaks it, how to catch it
7, 8                  → async/await, the natural syntax
9                     → real I/O
10, 11                → production patterns
12                    → ship it
```

---

## Quick reference

| Thing | What it means |
|---|---|
| `call_soon` | Queue this for the next loop tick |
| `call_later(n, fn)` | Fire after n seconds, if the loop is free |
| `await` | Pause here, let others run, resume when done |
| `gather()` | Run all concurrently, total time = slowest |
| `queue.join()` | Block until every `task_done()` is called |
| `set_debug(True)` | Smoke detector for blocking code |
| `uvloop.install()` | Swap in a faster engine, same API |

## Some Suggestions

| Mistake | Fix |
|---|---|
| CPU work in `async def` | Use `run_in_executor()` with `ProcessPoolExecutor` |
| `requests` in async code | Replace with `aiohttp` or `httpx` |
| No timeout on external calls | Wrap with `asyncio.timeout(n)` |
| Forgetting `task_done()` | `queue.join()` will hang forever |
| Workers never cancelled | Send sentinel `None` or call `task.cancel()` |