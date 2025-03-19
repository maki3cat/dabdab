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


class _CompletionExc(Exception):

    def __init__(self, value: any):
        self.value = value

    def get_value(self):
        return self.value


class _Future:
    """
 Future shall be a simple
 result, state, and callbacks with itself as the parameter
 set result with trigger callbacks that's why Future connects things
    """

    def __init__(self, loop=None, callback: callable = None):
        self.result = None
        self.state = "pending"
        self.loop = loop
        if loop is None:
            self.loop = _Eventloop.get_current_eventloop()

        self.callback = callback  # only support one callback for now
        self.chained_future = None

    def set_callback(self, callback: callable):
        self.callback = callback

    def set_result(self, res=None):
        self.result = res
        self.state = "done"
        if self.callback is not None:
            self.loop.call_now(self.chained_future, self.callback, self)


class _Eventloop:

    def __init__(self):
        self.ready = []

    @staticmethod
    def get_current_eventloop():
        global _current_loop
        if _current_loop is None:
            _current_loop = _Eventloop()
        return _current_loop

    def call_now(self, future: _Future, func: callable, *args, **kwargs):
        if future is None:
            future = _Future()
        self.ready.append((future, func, args, kwargs))

    def run(self):
        while self.ready:
            future, func, args, kwargs = self.ready.pop()
            try:
                next_future = func(*args, **kwargs)
                # maki: keyline, the future shall be chained,
                #  an alternative is we can ue a stack to manage the coroutine
                #  this alternative requires the loop has a stack
                next_future.chained_future = future
            except _CompletionExc as es:
                future.set_result(es.get_value())
