import httpx
import asyncio
import time
from collections.abc import Callable, Coroutine

# this is a cleaner implementation by which
"""
we know in a specific time which tasks is running in the eventloop
"""

async def track_progress(
            url: str,
            handler: Callable[..., Coroutine]) -> None :
      
      task = asyncio.create_task(
            handler(url),
            name=url
      )
      todos.add(task)
      start = time.time()
      while len(todos):
            done, _pending = await asyncio.wait(todos, timeout=13)
            todos.difference_update(done)
            _todos = [x.get_name().split('3000/')[-1] for x in todos]
            print(f'{len(todos)}: {", ".join(sorted(_todos))}')
      end_ = time.time()
      print(f'All Tasks Took {int(end_-start)}s')

todos = set()

async def crawl_beast (
            prefix: str,
            url : str = ""
) -> None:
    url = url or prefix
    client = httpx.AsyncClient()
    try :
        res = await client.get(url)
    finally :
         await client.aclose()
    
    for line in res.text.splitlines():
        task = asyncio.create_task(
             coro=crawl_beast(prefix,line),
             name=line)
        todos.add(task)


## let's handle interrupt cases

async def async_main() -> None:
    try:
        await track_progress(
            url='http://localhost:3000/crawl/',
            handler=crawl_beast)
    except asyncio.CancelledError :
        for task in todos:
              task.cancel()
        done, _pending = await asyncio.wait(todos, timeout=1)
        todos.difference_update(done)
        todos.difference_update(_pending)
        if todos:
             print('[warning] during cancellation new tasks were added to the loop!!!')

# # we can't control the termination
# asyncio.run(async_main())

loop = asyncio.get_event_loop()
main_task = loop.create_task(async_main())
loop.call_later(2.5,main_task.cancel)
loop.run_until_complete(main_task)