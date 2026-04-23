import asyncio
import datetime

loop = asyncio.get_event_loop()
loop.set_debug(True)  # Enable debug mode to see who is hogging the loop
def trampoline(name: str) -> None:
    now = datetime.datetime.now().strftime('%H:%M:%S.%f')
    print(f"[{now}] '{name}'")
    loop.call_later(0.5, trampoline, name)

def hog(name: str) -> None:
    print(f"\n*** {name} HOG STARTS — loop will freeze! ***")
    total = sum(i * j for i in range(10000) for j in range(10000))
    print(f"*** {name} HOG DONE — loop resumes ***\n")

# Normal trampolines
loop.call_soon(trampoline, "ALPHA")
loop.call_soon(trampoline, "BETA")

# Hog kicks in at 2 seconds — freezes everything
loop.call_later(2, hog, "CPU")

loop.call_later(6, loop.stop)
loop.run_forever()