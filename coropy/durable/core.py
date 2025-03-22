

# how to make simplify everything and durable behavior localization to applications
# do we need scalable
# A Durable Function Framework that is just a Lib like Operating System
# hybrid: local & check with remote
# what if the orchestration is local -> this gives monolithic app ?
# the framework is like a system layer
def normal():
    message = "hello"
    id = func_idempotent_1(message)
    msg = func_idempotent_2(message)
    print(f"result {msg} with id {id}")


def durable(ctx: dict):
    message = "hello"
    id = call_activity(func_idempotent_1, message, ctx=ctx)
    msg = call_activity(func_idempotent_2, message, ctx=ctx)
    print(f"result {msg} with id {id}")


def func_idempotent_1(message: str) -> int:
    print(f"store this {message} in the database")
    return 1


def func_idempotent_2(message: str) -> str:
    func_idempotent_1(message)
    print(f"store this result {message} in the database")
    return message

# api to user


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


# internal lib
def send_start_activity(func, *args, **kwargs) -> int:
    print(
        f"record activity {func.__name__} with {args} and {kwargs} in the DB")


def compete_actvitiy(activityID: int):
    print(f"compete activity {activityID} in the DB")


if __name__ == "__main__":
    normal()
    durable({})
