## deeper concept of timeouts
from datetime import datetime
import asyncio

def print_now():
    print(datetime.now())

async def keep_printing(name):
    while True :
        print(name,end=" ")
        print_now()
        # one fix is to use the try  here
        try :
            await asyncio.sleep(.5)
        except asyncio.CancelledError :
            print(f'{name} cancelled')
            break



async def async_main() :
 
    try :
    # 2 now here we have only one coroutine which is wait_for
    # which wraps a gather coroutine
    # gather wraps another three coroutine
    # when a timout occurs it cancels the task (what we are waiting for is gather) and raise TimeoutError
    # when a gather() coroutine is canclled, all submitted awaitables to this (that is not completed yet) also cancelled
    # propagating the event to the submitted awaitables 3
        await asyncio.wait_for(
             asyncio.gather(
                keep_printing('one'),
                keep_printing('two'),
                keep_printing('three')
            ),
            3
        )
    except asyncio.TimeoutError:
        print('oopss!! time\'s up')
# 1 our keep printing coroutines give some exceptions that we didn't retrieved
# this introduce us to cancel 2
asyncio.run(async_main())