import asyncio

async def some_slow_api():
    await asyncio.sleep(10)  # Simulate a slow API call

async def risky_call():
    try:
        async with asyncio.timeout(5): # python 3.11+ only
            await some_slow_api()
    except asyncio.TimeoutError:
        print("Too slow, moving on")
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    asyncio.run(risky_call())