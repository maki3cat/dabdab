from asyncio import get_event_loop
import asyncio

loop = get_event_loop()
future = loop.create_future()

async def hello():
    await asyncio.sleep(1)
    print('Hello World')

task = loop.create_task(hello())