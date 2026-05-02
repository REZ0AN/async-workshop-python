import asyncio

async def producer(queue):
    for item in range(10):
        await queue.put(item)
        await asyncio.sleep(0.1)

async def worker(queue, name):
    while True:
        item = await queue.get()
        
        if item is None:              # Sentinel received — time to exit
            queue.task_done()         # Still need to signal this, or join() hangs
            break
        
        print(f"{name} processing {item}")
        queue.task_done()

async def main():
    queue = asyncio.Queue()
    num_workers = 3

    workers = [asyncio.create_task(worker(queue, f"W{i}"))
               for i in range(num_workers)]

    await producer(queue)
    await queue.join()

    # Send one None per worker so each one hits the sentinel and exits
    for _ in range(num_workers):
        await queue.put(None)

    await asyncio.gather(*workers)    # Wait for all workers to fully finish

if __name__ == "__main__":
    asyncio.run(main())