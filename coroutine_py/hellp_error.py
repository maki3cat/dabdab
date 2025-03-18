

# Example 1: Future attached to a different loop
import asyncio

async def problematic_function():
    # Create a loop
    loop1 = asyncio.new_event_loop()
    
    # Create a future in loop1
    future = asyncio.Future(loop=loop1)
    
    # Try to await this future in the main loop (different from loop1)
    await future  # This will trigger the "attached to a different loop" error

async def main():
    await problematic_function()

asyncio.run(main())

# Example 2: Task awaiting itself

async def self_awaiting_task():
    # Get the current task
    current_task = asyncio.current_task()
    
    # Try to await the current task itself
    await current_task  # This will trigger the "Task cannot await on itself" error

asyncio.run(self_awaiting_task())