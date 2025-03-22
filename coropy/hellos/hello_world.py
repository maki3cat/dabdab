import asyncio

# How to define a coroutine function
# which returns a coroutine object
async def hello_world():
    print("Hello World!")
loop = asyncio.get_event_loop()
coroutine_obj = hello_world()
loop.run_until_complete(coroutine_obj)

# does the close impact the next say_name?
loop.close()

async def say_name():
    await asyncio.sleep(1)
    return "Maki"
loop = asyncio.get_event_loop()
coro = say_name()  # Creates a coroutine object
task = loop.create_task(coro)  # Schedules it and returns a Task
result = loop.run_until_complete(task)  # Runs the loop until task is done
print(result)  # Outputs: "Hello"

import asyncio
async def say_hello():
    await asyncio.sleep(1)
    print("Hello World!")

async def main():
    task = asyncio.create_task(say_hello())  # Starts the coroutine
    print("Task scheduled, doing other stuff...")
    await asyncio.sleep(2)  # Simulate other work
asyncio.run(main())  # Runs the event loop