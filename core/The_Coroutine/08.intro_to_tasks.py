import httpx
import asyncio
import time
from collections.abc import Callable, Coroutine


async def crawl_base(prefix : str, url: str = "") -> None :
        url = url or prefix

        print(f"[crawling] {url}")

        client = httpx.AsyncClient()

        try :
            res = await client.get(url)
        finally:
              await client.aclose()
        
        for line in res.text.splitlines():
              if line.startswith(prefix):
                   await crawl_base(prefix,line)


async def track_progress(
            url: str,
            handler: Callable[..., Coroutine]) -> None :
      
      asyncio.create_task(
            handler(url),
            name=url
      )
      todo.add(url)
      start = time.time()
      while len(todo):
            _todo = [x.split('3000/')[-1] for x in todo]
            print(f'{len(todo)}: {", ".join(sorted(_todo))}')
            await asyncio.sleep(.5)
      end_ = time.time()
      print(f'All Tasks Took {int(end_-start)}s')

todo = set()
 
async def crawl_intermediate(
                prefix: str,
                url: str = "" ) -> None:
        url = url or prefix
        client = httpx.AsyncClient()
        try :
            res = await client.get(url)
        finally :
              await client.aclose()
        for line in res.text.splitlines():
            todo.add(line)
            await crawl_intermediate(prefix, line)
        todo.discard(url)
        
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
        todo.add(line)
        asyncio.create_task(
             coro=crawl_beast(prefix,line),
             name=line)
    todo.discard(url)


# asyncio.run(crawl_base(
#       prefix='http://localhost:3000/crawl/'
# ))
    

# asyncio.run(track_progress(
#       url='http://localhost:3000/crawl/',
#       handler=crawl_intermediate
# ))

asyncio.run(track_progress(
      url='http://localhost:3000/crawl/',
      handler=crawl_beast
))
