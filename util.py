import time
import contextlib


@contextlib.contextmanager
def print_time(label):
    start = time.time()
    yield
    end = time.time()
    elapsed = end - start
    print('{elapsed: 2.4f}s: {label:}'.format(**locals()))

def print_time_f(func):
    def func_(*args, **kwargs):
        with print_time(func.__name__):
            return func(*args, **kwargs)
    return func_
