import asyncio


# maki: if the await checks in the history of the task, and if the task is already done, it will return the result
# maki: this will be the same model as temporal-sdk
# maki: basic primitive inside workflow, activity, timer
# maki: see how coroutine connects them, then try to build temporal which is using coroutine pattern with the workflow model patterns


async def workflow():
    print("workflow started")

    # suspend the coroutine of a workflow,
    # and wait for the waitable to be finished
    await asyncio.sleep(1)


    # asyncrhonously call activity_cook, and activity_clean
    task_cook = asyncio.create_task(activity_cook())
    task_clean = asyncio.create_task(activity_clean())

    await task_cook
    await task_clean

    # get the results of the activities
    result_cook = task_cook.result()
    result_clean = task_clean.result()  
    print(f"results: {result_cook}, {result_clean}")

    result_water = await activity_water()
    print(f"result: {result_water}")
    print("workflow completed")


async def activity_cook():
    print("activity cook started")
    await asyncio.sleep(1)
    print("activity cook completed")
    return "cooked"

async def activity_clean():
    print("activity clean started")
    await asyncio.sleep(1)
    print("activity clean completed")
    return "cleaned"
    
async def activity_water():
    print("finally: activity water started")
    await asyncio.sleep(1)
    print("finally: activity water completed")   
    return "watered"

if __name__ == "__main__":
    asyncio.run(workflow())