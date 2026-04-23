import asyncio
from datetime import datetime

async def task():
    print(f"{datetime.now()} — Task started")
    await asyncio.sleep(.5)
    print(f"{datetime.now()} — Task done")

async def other_task():
    print(f"{datetime.now()} — Other task started")
    await asyncio.sleep(1)
    print(f"{datetime.now()} — Other task done")


async def main():
    await asyncio.sleep(2)
    await task()
    await other_task()

asyncio.run(main())