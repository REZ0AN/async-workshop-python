## saw some keywords like Task, Future, Awaitable

from datetime import datetime
import asyncio
def print_now():
    print(datetime.now())

async def print_3_time(name: str = "") -> None:
    for i in range(3) :
        print(f"{name} {i} !!")
        print_now()
        await asyncio.sleep(.5)


coro_1 = print_3_time('Hi')
coro_2 = print_3_time('Helo')

# type of the async definition
print(type(print_3_time))

# type of the called async function
print(type(coro_1))

# will throw an exception
asyncio.run(print_3_time)

asyncio.run(coro_1)
asyncio.run(coro_2)

# ## coroutines can run only at once
# asyncio.run(coro_1)