"""
    Author  : Tal Avraham
    Created : 5/17/2020
    Purpose : Bot decorators.
"""

import logging
import functools
from retrying import retry, RetryError
import threading


def retry_no_raise(*args, **kwargs):
    """Retry a function without raising exception if max retries exceeded."""
    def decorator(func):
        retried_func = retry(*args, **kwargs, wrap_exception=True)(func)

        @functools.wraps(retried_func)
        def wrapper(*modified_args, **modified_kwargs):
            try:
                return retried_func(*modified_args, **modified_kwargs)
            except RetryError:
                logging.warning("Max retries exceeded.")

        return wrapper

    if len(args) == 1 and callable(args[0]):
        return decorator(args[0])
    return decorator


def threaded(func):
    """Run a function in a new thread."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=func, args=args, kwargs=kwargs)
        thread.setDaemon(True)
        thread.start()
        return thread

    return wrapper


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args,
                                                                 **kwargs)
        return cls._instances[cls]
