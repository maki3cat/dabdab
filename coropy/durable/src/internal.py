

# internal lib
def send_start_activity(func, *args, **kwargs) -> int:
    print(
        f"record activity {func.__name__} with {args} and {kwargs} in the DB")


def compete_actvitiy(activityID: int):
    print(f"compete activity {activityID} in the DB")
