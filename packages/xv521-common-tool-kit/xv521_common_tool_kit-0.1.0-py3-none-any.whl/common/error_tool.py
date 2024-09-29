from typing import Callable, Any
from functools import wraps
import time


def cat_error(
        error_type: type = Exception,
        call: Callable[..., Any] = lambda ctx: None,
        need_raise: bool = False,
):
    """
    :param error_type: exception type to catch
    :param call: callable after catching an exception.
    :param need_raise: decide whether raise be need.
    :return: Any.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except error_type as e:
                ctx = {
                    'f_name': func.__name__,
                    'args': args,
                    'kwargs': kwargs,
                    'e': e,
                }
                call(ctx=ctx)
                if need_raise:
                    raise e

        return wrapper

    return decorator


def cat_error_bool(
        error_type: type = Exception,
):
    """
    :param error_type: exception type to catch
    :return: return True if not exception, else False.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
                return True
            except error_type:
                return False

        return wrapper

    return decorator


def cat_error_retry(
        error_type: type = Exception,
        max_count: int = 5,
        retry_delay: float = 0.1
):
    """
    :param error_type: the exception type to catch
    :param max_count: max count of retry
    :param retry_delay: delay of retry.
    :return:
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            count = -1
            while count < max_count:
                try:
                    return func(*args, **kwargs)
                except error_type as e:
                    count += 1
                    if count == max_count:
                        raise e
                    time.sleep(retry_delay)
        return wrapper
    return decorator

