from typing import Callable, Any
from functools import wraps
import asyncio


def cat_error(
        error_type: type = Exception,
        call: Callable[..., Any] = lambda ctx: None,
        need_raise: bool = False,
):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except error_type as e:
                ctx = {
                    'f_name': func.__name__,
                    'args': args,
                    'kwargs': kwargs,
                    'e': e,
                }
                if asyncio.iscoroutinefunction(call):
                    await call(ctx=ctx)
                else:
                    await asyncio.to_thread(call, ctx=ctx)
                if need_raise:
                    raise e

        return wrapper

    return decorator


def cat_error_bool(
        error_type: type = Exception,
):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                await func(*args, **kwargs)
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
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            count = -1
            while count < max_count:
                try:
                    return await func(*args, **kwargs)
                except error_type as e:
                    count += 1
                    if count == max_count:
                        raise e
                    await asyncio.sleep(retry_delay)
        return wrapper
    return decorator
