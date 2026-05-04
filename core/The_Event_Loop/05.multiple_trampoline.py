import asyncio
import datetime

loop = asyncio.get_event_loop()

def trampoline(name: str) -> None:
    now = datetime.datetime.now().strftime('%H:%M:%S.%f')
    print(f"[{now}] '{name}'")
    loop.call_later(0.5, trampoline, name)

# Three independent trampolines running on ONE loop
loop.call_soon(trampoline, "ALPHA")
loop.call_soon(trampoline, "BETA")
loop.call_soon(trampoline, "GAMMA")

loop.call_later(2, loop.stop)
loop.run_forever()