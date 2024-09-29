import time
from functools import wraps
import asyncio
from loguru import logger


def time_logger(
        number: int = 1,
        concurrent: bool = False,
        need_result: bool = False
):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            if not isinstance(number, int):
                raise ValueError(f'func time_logger, number: {number}')
            total = avg = 0
            result = list()
            if not number == 0:
                if concurrent:
                    tasks = [func(*args, **kwargs) for _ in range(number)]
                    start_time = time.perf_counter()
                    result = await asyncio.gather(*tasks)
                    end_time = time.perf_counter()
                    total += (end_time - start_time)
                else:
                    for _ in range(number):
                        start_time = time.perf_counter()
                        sub_result = await func(*args, **kwargs)
                        end_time = time.perf_counter()
                        total += (end_time - start_time)
                        if need_result:
                            result.append(sub_result)
                    if need_result and number == 1:
                        result = result[0]
                avg = total / number
            logger.info(
                f'func: {func.__name__} -- total time: {total:.6f} -- avg time: {avg:.6f} -- number: {number}'
            )
            if need_result and result:
                return result

        return wrapper

    return decorator
