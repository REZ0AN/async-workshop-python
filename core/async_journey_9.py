import aiohttp
import asyncio
import time
async def fetch_url(session, url):
    async with session.get(url) as response:
        return await response.json()

async def main():
    async with aiohttp.ClientSession() as session:
        results = await asyncio.gather(
            fetch_url(session, "https://jsonplaceholder.typicode.com/todos/1"),
            fetch_url(session, "https://jsonplaceholder.typicode.com/todos/2"),
            fetch_url(session, "https://jsonplaceholder.typicode.com/todos/3"),
            fetch_url(session, "https://jsonplaceholder.typicode.com/todos/4"),
            fetch_url(session, "https://jsonplaceholder.typicode.com/todos/5"),
            fetch_url(session, "https://jsonplaceholder.typicode.com/todos/6"),
            fetch_url(session, "https://jsonplaceholder.typicode.com/todos/7"),
        )
        for i, result in enumerate(results, 1):
            print(f"Result {i}: {result}")

if __name__ == "__main__":
    t0 = time.time()
    asyncio.run(main())
    t1 = time.time()
    print(f"Total time: ~{t1 - t0:.2f}s")