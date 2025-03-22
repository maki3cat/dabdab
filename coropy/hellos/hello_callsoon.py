import asyncio


def say_hello():
    print("Hello, world!")


# Get the event loop
loop = asyncio.get_event_loop()

# Schedule the say_hello function to run soon
loop.call_soon(say_hello)

# Run the event loop
loop.run_until_complete(asyncio.sleep(1))
