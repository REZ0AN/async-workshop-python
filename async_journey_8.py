import asyncio
import time
async def fetch(name, delay):
    print(f"{name} starting...")
    await asyncio.sleep(delay)
    print(f"{name} done!")

async def main():
    # These run CONCURRENTLY, not sequentially
    await asyncio.gather(
        fetch("A", 3),
        fetch("B", 1),
        fetch("C", 2),
    )

if __name__ == "__main__":
    start_time = time.time()
    asyncio.run(main())
    end_time = time.time()
    print(f"Total time: ~{end_time - start_time:.2f}s")