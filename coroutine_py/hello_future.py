import asyncio

async def slow_operation(future):
    # pretend it is some calculation and slow work
    await asyncio.sleep(1)
    future.set_result('set the fake response!')

loop = asyncio.get_event_loop()

# we can use future to connect coroutine and event loop
future = asyncio.Future()

# Schedule the execution of a coroutine object: wrap it in a future.
asyncio.ensure_future(slow_operation(future))

loop.run_until_complete(future)

print(future.result())
loop.close()