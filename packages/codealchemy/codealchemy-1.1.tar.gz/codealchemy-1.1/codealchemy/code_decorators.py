import time
from functools import wraps


def code_execution_time(func):
    """
    Decorator to log the execution time of a function.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time

        # Calculate the length of the separator line
        separator_length = 80
        message_length = len(
            f"* Execution time of {func.__name__}: {execution_time:.4f} seconds *"
        )
        padding_length = (separator_length - message_length) // 2

        # Print the separator line and centered message
        print("*" * separator_length)
        print(
            "*" * padding_length
            + f"  Execution time of {func.__name__}: {execution_time:.4f} seconds  "
            + "*" * padding_length
        )
        print("*" * separator_length)

        return result

    return wrapper
