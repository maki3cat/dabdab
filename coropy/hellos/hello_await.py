import time
import asyncio

class DelayedMessage:
    def __init__(self, message, delay):
        self.message = message
        self.delay = delay

    def __await__(self):
        print("Delayed Message: before yield")
        # Return a generator that simulates async behavior
        yield from asyncio.sleep(self.delay).__await__()
        return self.message  # Final result

async def my_coroutine():
    print("Starting")
    result = await DelayedMessage("Hello, world!", 3)
    print(f"Got result: {result}")

# Manual driving (without asyncio for clarity)
# coro = my_coroutine()
# coro.send(None)  # Start coroutine, prints "Starting", yields at await
# print("After first send")
# try:
#     coro.send(None)  # Resume after yield, waits 3 seconds, prints "Got result: Hello, world!"
# except StopIteration:
#     print("Coroutine done")
# # A coroutine (like a generator) signals completion by raising StopIteration
# print("After second send")


asyncio.run(my_coroutine())

# Manual Driving with send(): Using coro.send(None) to step through the coroutine manually, 
# which is useful for understanding the internals or when not using an event loop.
# Using asyncio.run(): Running the coroutine with asyncio’s event loop, which is the standard way to execute async code in Python applications.