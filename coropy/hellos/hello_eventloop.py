import collections
import types

# Simplified Future class to represent awaitable results
class Future:
    def __init__(self, loop):
        self.loop = loop
        self._done = False
        self._result = None
        self._callbacks = []

    def set_result(self, result):
        self._result = result
        self._done = True
        for callback in self._callbacks:
            self.loop.call_soon(callback)

    def add_done_callback(self, callback):
        self._callbacks.append(callback)

    def __await__(self):
        if not self._done:
            yield self  # Yield control to the event loop
        return self._result

# Simple Event Loop
class SimpleEventLoop:
    def __init__(self):
        self._ready = collections.deque()
        self._stopping = False

    def call_soon(self, callback, *args):
        self._ready.append((callback, args))

    def create_task(self, coro):
        task = Task(coro, self)
        self.call_soon(task.step)
        return task

    def run_forever(self):
        while self._ready and not self._stopping:
            callback, args = self._ready.popleft()
            try:
                callback(*args)
            except StopIteration:
                pass
            except Exception as e:
                print(f"Error in task: {e}")

# Task class to manage coroutines
class Task:
    def __init__(self, coro, loop):
        self.coro = coro
        self.loop = loop
        self.done = False

    def step(self):
        if not self.done:
            try:
                # Advance the coroutine
                result = self.coro.send(None)
                # If result is a Future, suspend and wait for it
                if isinstance(result, Future):
                    result.add_done_callback(self.step)
                else:
                    self.loop.call_soon(self.step)  # Reschedule if not done
            except StopIteration:
                self.done = True

# Example coroutines
async def child_coroutine(name):
    print(f"{name} starting")
    future = Future(loop)  # Simulate an async operation
    loop.call_soon(lambda: future.set_result(f"{name} done"))  # Simulate completion
    result = await future
    print(result)

async def parent_coroutine():
    print("Parent starting")
    await child_coroutine("Child")  # Await another coroutine
    print("Parent resuming")

# Usage
if __name__ == "__main__":
    loop = SimpleEventLoop()
    loop.create_task(parent_coroutine())
    loop.run_forever()