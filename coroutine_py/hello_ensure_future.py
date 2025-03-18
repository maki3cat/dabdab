import asyncio
import random

# the dumm
async def dummy_api(input):
    print("duammy_api start with input: ", input)
    await asyncio.sleep(random.randint(1, 2))
    return input

# this outside one shouldn't wait on anything
async def dummy_entry():
    pending_requests = ["Alice", "Bob", "Charlie"]
    futures = []
    while True:
        while len(pending_requests) > 0 and len(futures) < 10:
            req = pending_requests.pop()
            print("request coming, and call dummy_api")
            future = asyncio.create_task(dummy_api(req))
            futures.append(future)

        print("yield")
    # TODO: if yield 0, the dummy_api will never be executed to first line
    # TODO: how does this timer callback -> 0.1 but others don't yield: runnable, suspended
        await asyncio.sleep(0.1)
        print("yield done")

    # it seems this entry takes all time
    # TODO: exception is never found
        undone_futures = []
        done_futures = []
        while len(futures) > 0:
            future = futures.pop()
            if not future.done():
                undone_futures.append(future)
            else:
                done_futures.append(future)
        futures = undone_futures
        print(f"done futures: {len(done_futures)}")
        for future in done_futures:
            print(future.result())

loop = asyncio.get_event_loop()
entry = dummy_entry()
future = asyncio.ensure_future(entry)
# this should be start point
loop.run_forever()  # Start the loop without waiting for completion