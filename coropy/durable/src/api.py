""" The API of this SDK """
from .internal import send_start_activity


class Activity:
    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs


def call_activity(input: Activity, *, ctx=None) -> int:
    # skip the execution
    if input.func.__name__ in ctx:
        return ctx[input.func.__name]

    # call the remote orchestrator to record it, and asign it, and wait for the callback
    activityID = send_start_activity(input)

    # TODO: should yield it
    return activityID
