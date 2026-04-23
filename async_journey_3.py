import asyncio
import datetime

loop = asyncio.get_event_loop()

def task(name):
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S.%f')}]  '{name}' task executed")

# Schedule three tasks — they run in order, as soon as the loop starts
loop.call_soon(task, "first")
loop.call_soon(task, "second")
loop.call_soon(task, "third")

# Give the loop run for .5 to run the callbacks
loop.run_until_complete(asyncio.sleep(.5))

print("Done")