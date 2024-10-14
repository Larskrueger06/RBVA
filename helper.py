import time
from functools import wraps

def time_func(func):
    @wraps(func)
    def time_func_wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        stop = time.time()
        print("time took to execute: ", stop - start)
        return result
    return time_func_wrapper

def psleep(seconds):
    for s in reversed(range(1, seconds+1)):
        print("sleeping for: ", s)
        time.sleep(1)