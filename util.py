import time
import contextlib
import gevent


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

def take_at_least(delay):
    def decorator(func):
        def func_(*args, **kwargs):
            start = time.time()
            ret = func(*args, **kwargs)
            elapsed = time.time() - start
            if elapsed < delay:
                gevent.sleep(delay - elapsed)
            return ret
        return func_
    return decorator
