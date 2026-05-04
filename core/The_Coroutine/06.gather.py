## coroutine compose
from datetime import datetime
import asyncio

def print_now():
    print(datetime.now())

async def keep_printing(name):
    while True :
        print(name,end=" ")
        print_now()
        await asyncio.sleep(.5)



async def async_main() :
    # await keep_printing("one")
    # # second one won't start executing if first one isn't done
    # await keep_printing("two")
    # await keep_printing("three")

    ## if we want to run all coroutines at the same time (concurrently)
    # and all of these is happing in a single thread
    # co-operative multitasking doing many things in a single thread
    await asyncio.gather(
        keep_printing('one'),
        keep_printing('two'),
        keep_printing('three')
    )

asyncio.run(async_main())