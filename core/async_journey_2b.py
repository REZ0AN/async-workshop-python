import asyncio

loop = asyncio.get_event_loop()


# runs until the coroutine finishes, then returns
loop.run_until_complete(asyncio.sleep(3))
print("Loop finished — control returned to us")