## saw some keywords like Task, Future, Awaitable

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
    
    ## awaitable object
    aw_kp = keep_printing("Hey..")
    aw_wf = asyncio.wait_for(aw_kp,3) # doesn't start counting secs
    ## we catch the timeout exception
    try :
        # ## we need to await it for counting the secs
        await aw_wf
        ## if we don't start await on them nothing will happen
        ## the warning you don't see it you need to enable it by setting
        ## PYTHONASYNCIODEBUG=1
        ## PYTHONTRACEMALLOC=1 ## this will tell you where you actually created an awaitable object
        ## export them in you env
        
        aw_wf
    except asyncio.TimeoutError :
        print("Oops... Times Up!! Stopped What the Event Loop was doing!!")


asyncio.run(async_main())