import asyncio

# run-1: get the current event loop
# Python creates one automatically on the main thread
loop = asyncio.get_event_loop()

print(f"Event loop type: {type(loop)}")
print(f"Is running: {loop.is_running()}")