import time
import functools


def log_decorator(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()

        with open("logs/log.txt", "a") as log_file:
            log_file.write(f"Function {func.__name__} started at {time.ctime(start_time)}\n")

        res = func(*args, **kwargs)
        end_time = time.time()
        duration = end_time - start_time

        with open("logs/log.txt", "a") as log_file:
            log_file.write(f"Function {func.__name__} finished at {time.ctime(end_time)}\n")
            log_file.write(f"Function {func.__name__} took {duration:.2f} seconds to execute.\n")
        return res
    return wrapper
