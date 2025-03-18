import time

# First topic is still about coroutine
# TODO: compare this to the python official version to get the basic concepts and working mechanisms of coroutine model
# TODO: advanced a bit is to support the coroutine with multi-threading implementation using python way?

# Second topic is using the coroutine model with system domains like durable funcitons like Temporal

_PENDING = "pending"
_DONE = "done"
# TODO: feature-2
_CANCELLED = "cancelled"
# TODO: feature-add timer, suspended not just ready?

# can be threadlocal, depending on the design pattern
_current_loop = None

# Future shall be a simple 
# result, state, and callbacks with itself as the parameter
# set result with trigger callbacks that's why Future connects things
class _Future:
    def __init__(self, loop=None, callback: callable=None):
        self.callback = callback # only support one callback for now
        self.result = None
        self.state = "pending"
        self.loop = loop
        if loop == None:
            self.loop = _Eventloop.get_current_eventloop()

    def set_callback(self, callback: callable):
        self.callback = callback

    def set_result(self, res=None):
        self.result = res
        self.state = "done"
        self.loop.call_now(None, self.callback, self)

class _Eventloop:
    def __init__(self):
        self.ready = []

    @staticmethod
    def get_current_eventloop():
        global _current_loop
        if _current_loop == None:
            _current_loop = _Eventloop()
        return _current_loop

    def call_now(self, future: _Future, func: callable, *args, **kwargs): # type: ignore
        self.ready.append((future, func, args, kwargs))

    def run_to_end(self, func: callable=None, *args, **kwargs):
        self.ready.append((None, func, args, kwargs))

    def run(self):
        while self.ready:
            coro = self.ready.pop()
            future, func, args, kwargs = coro
            # right now this func can be blocking the whole thread
            # in temporal, this should be sending to remote synchronously
            # and the whole workflow probably should be waiting for the remote to give a callback for some future
            # TODO: feature1 we need to get a remote server reply to continue the runtime
            # now we focus on coroutine first
            res = func(*args, **kwargs)
            if future != None:
                # callback is a part of it
                future.set_result(res)

# CoroutineContext is a simple state machine
class _CoroutineContext:
    def __init__(
            self, params:dict={}, *, 
            state:int=0, history: dict={}, current_coro=""):
        self.state = state
        self.history = history
        self.current_coro = None
        self.params = params
        self.coroutine = None

    def set_coroutine(self, func: callable):
        self.coroutine = func

    def resume(self, future: _Future):
        print(f"resume to state {self.state}")
        self.history[self.current_coro] = future.result
        if self.coroutine != None:
            self.coroutine(self)

def coroutine_simple_1(message:str):
    def _coroutine_simple_1(con:_CoroutineContext=_CoroutineContext()):
        print(f"simple 1 executed with message {con.params.get('message')}")
        return "result_activity_1"
    con = _CoroutineContext()
    con.params["message"] = message
    return _coroutine_simple_1(con)

def coroutine_simple_2(message:str):
    def _coroutine_simple_2(con:_CoroutineContext=_CoroutineContext()):
        print(f"simple 2 executed with message {con.params.get('message')}")
        return "result_activity_2"
    con = _CoroutineContext()
    con.params["message"] = message
    return _coroutine_simple_2(con)

def common_workflow(name: str):
    def _common_workflow(con:_CoroutineContext=_CoroutineContext()):
        # print(f"common workflow {con.params} called with state= {con.state}")
        loop = _Eventloop.get_current_eventloop()
        name = con.params.get("name")
        # state before the chained coroutine call
        if con.state == 0:
            print(f"Step {con.state}: local calculation of {name}")
            # for real coroutine, this should be the stack
            calculation_result = 1000
            con.history["calculation_result"] = calculation_result
            con.state = 1

        if con.state == 1:
            print(f"Step {con.state}: calls simple activity 1 of {name}")
            # save the state of caller coroutine
            con.state = 2
            con.current_coro = "coroutine_simple_1"
            future = _Future()
            
            # maki: very important to add resume to future when await on some future
            future.set_callback(con.resume)
            # maki: key to register the coroutine and future together
            loop.call_now(future, coroutine_simple_1, "first message")
            print(f"yield from state {con.state}")
            return

        # state after the coroutine call
        if con.state == 2:
            print(f"Step {con.state} calls simple activity 2 of {name}")
            con.state = 3
            con.current_coro = "coroutine_simple_2"
            message = con.history.get("coroutine_simple_1")
            future = _Future(callback=con.resume)
            loop.call_now(future, coroutine_simple_2, message)
            print(f"yield from state {con.state}")
            return

        calculation_result = con.history.get("calculation_result")
        final_result = calculation_result + 100
        print(f"Step {con.state}: final result is {final_result}")
        return final_result

    con = _CoroutineContext(params={"name": name})
    con.set_coroutine(_common_workflow)
    return _common_workflow(con)

if __name__ == "__main__":
    c_runtime = _Eventloop.get_current_eventloop()
    c_runtime.run_to_end(common_workflow, "GLOVER")
    c_runtime.run_to_end(common_workflow, "REBETA")
    c_runtime.run()