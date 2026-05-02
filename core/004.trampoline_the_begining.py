import asyncio
import datetime

loop = asyncio.get_event_loop()

def trampoline(name: str) -> None:
    now = datetime.datetime.now().strftime('%H:%M:%S')
    print(f"[{now}] '{name}' bouncing...")

    # The trick: schedule yourself again after a short delay
    loop.call_later(0.5, trampoline, name)

# Schedule ONE call — it will keep rescheduling itself forever
loop.call_soon(trampoline, "bouncer")

# Stop after 2 seconds so we don't run forever
loop.call_later(2, loop.stop)

loop.run_forever()
print("Loop stopped")