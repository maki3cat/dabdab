"""
The hello world program of this SDK
"""

# how to make simplify everything and durable behavior localization to applications
# do we need scalable
# A Durable Function Framework that is just a Lib like Operating System
# hybrid: local & check with remote
# what if the orchestration is local -> this gives monolithic app ?
# the framework is like a system layer

from .src.api import call_activity


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


if __name__ == "__main__":
    normal()
    durable({})
