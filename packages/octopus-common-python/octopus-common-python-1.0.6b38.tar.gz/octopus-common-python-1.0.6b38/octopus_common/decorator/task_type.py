from octopus_common.constant.constants import TASK_TYPE_FIELD_NAME


def task_type(*task_types: int):
    def decorator(func):
        setattr(func, TASK_TYPE_FIELD_NAME, task_types)
        return func

    return decorator
