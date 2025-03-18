import asyncio
from typing import List, Optional
import time

async def workflow():
    print("workflow started")
    # suspend the coroutine of a workflow,
    # and wait for the waitable to be finished
    # there is no task in this just "Future" & "Eventloop"
    await asyncio.sleep(1)
    print("workflow ended")

class WorkflowExecution:
    def __init__(self, history):
        self.history = history
    
    def execute(self):
        pass
    
    @staticmethod
    async def timer(sec:int):
        await asyncio.sleep(sec)


from enum import Enum

class CoroutineState(Enum):
    INIT = "INIT"
    RUNNING = "RUNNING"
    FINISHED = "SUSPENDED"


class _Runtime:
    def __init__(self, history: List[str]):
        self.history = history

# TODO: so we have each workflow_runtime per event loop
# how many event loops can we have in a process?
class _RuntimeRegister:
    @staticmethod
    def get_current():
        running_eventloop = asyncio.get_running_loop()
        if running_eventloop is None:
            raise RuntimeError("No running event loop")
        return getattr(running_eventloop, "_workflow_runtime", None)

    @staticmethod
    def set_current(runtime: Optional[_Runtime]):
        running_eventloop = asyncio.get_running_loop()
        setattr(running_eventloop, "_workflow_runtime", runtime)
        

# if we only support blocking activities
class Coroutine:
    def __init__(self, func):
        self.func = func
        self.state = CoroutineState.INIT

    def __await__(self):
        if self._task is None:
            self._task = asyncio.create_task(self.target())
        return self._task.__await__()



if __name__ == "__main__":
    asyncio.run(workflow())