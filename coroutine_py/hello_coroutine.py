import asyncio

async def my_coroutine():
    print("Step 1")
    await asyncio.sleep(0)  # Yields control
    print("Step 2")

coro = my_coroutine()

# Start the coroutine manually
coro.send(None)  # Prints "Step 1", pauses at await
# At this point, it’s waiting for the sleep(0) to resolve

# Resume it (though in practice, the event loop would handle this)
try:
    coro.send(None)  # Prints "Step 2", then raises StopIteration
except StopIteration:
    print("Coroutine done")


# The send(value) method is inherited from the generator protocol and is used to drive the coroutine’s execution.
# For a fresh coroutine, you must call send(None) to start it (just like priming a generator with next()).
# Each call to send() advances the coroutine to the next await point or completion, returning whatever the coroutine yields (typically an awaitable like a Future).L