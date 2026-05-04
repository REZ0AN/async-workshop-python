from datetime import datetime
import asyncio
def print_now():
    print(datetime.now())

async def keep_printing(name: str) -> None:
    while True :
        print(name, end=" ")
        print_now()
        await asyncio.sleep(.5)

## without ctrl+c it won't stop
asyncio.run(keep_printing("Hii there.."))