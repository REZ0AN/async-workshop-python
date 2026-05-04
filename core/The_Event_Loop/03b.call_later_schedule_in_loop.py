import asyncio
import datetime

loop = asyncio.get_event_loop()

def task(name):
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] '{name}' task executed")

# Schedule at different delays
loop.call_later(3, task, "3 seconds later")
loop.call_later(1, task, "1 second later")   # registered second, runs first!
loop.call_later(2, task, "2 seconds later")

loop.run_until_complete(asyncio.sleep(4))