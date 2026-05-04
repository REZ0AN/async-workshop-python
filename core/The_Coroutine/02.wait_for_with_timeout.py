## better way to do using timeouts

from datetime import datetime
import asyncio
def print_now():
    print(datetime.now())

async def keep_printing(name: str) -> None:
    while True :
        print(name, end=" ")
        print_now()
        await asyncio.sleep(.5)

## will throw a timeout exception
asyncio.run(asyncio.wait_for(keep_printing("Hii there.."),5))