import asyncio

async def my_coroutine():
    print("Coroutine started")
    await asyncio.sleep(1)  # This yields control back to the event loop
# TODO: Q-1: why Coroutine resumed not printed -> either add 2 sends OR use await my_coroutine() instead of coro.send(None)
    print("Coroutine resumed")

async def main():
    coro = my_coroutine()
    try:
    # because this means the coro is managed manually
    #  instead of asking ayyncio to manage it
    # TODO: Q-2: how does the manager know how many send it shall send, 
    # how does the task._step manage
        coro.send(None)
    except StopIteration:
        print("Coroutine ended")
    print("Main sends")

    await asyncio.sleep(1.5)
    # TODO: q3, why the await asyncio.sleep(1.5) should be before the coro.send
    # the problem is not at the sleep but at the 2 sends, because the my_coroutine is suspended on await
    # When you call coro.send(None), you're manually advancing the coroutine. 
    # If the coroutine then tries to await something while still in the context of another send, 
    # it can lead to confusion within the event loop about which coroutine's state is being managed.
    try:
        coro.send(None)
    except StopIteration:
        print("Coroutine ended")

    # use await to yield control back to the event loop, allowing other tasks to run.
    # When a coroutine hits an await statement, it pauses its execution and yields control back to the event loop until the awaited future is ready.Vgc
    # So: 1) await on a future; 2) there is some callback to resume the coroutine ---> what happens in the await
    # 3) When you manually control a coroutine using coro.send(None), you're stepping through its execution manually.
    #  -> there is no callbeck from eventloop
    print("Main ends")

asyncio.run(main())