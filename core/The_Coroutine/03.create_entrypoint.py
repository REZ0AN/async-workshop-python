## better way to handle known exceptions

from datetime import datetime
import asyncio
def print_now():
    print(datetime.now())

async def keep_printing(name: str) -> None:
    while True :
        print(name, end=" ")
        print_now()
        await asyncio.sleep(.5)


async def async_main():
    ## we catch the timeout exception
    try :
        await asyncio.wait_for(keep_printing("Helo.."),3)
    except asyncio.TimeoutError :
        print("Oops... Times Up!! Stopped What the Event Loop was doing!!")


asyncio.run(async_main())