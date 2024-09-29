import time
from datetime import datetime
from functools import wraps
from loguru import logger
from typing import Literal
import re


def time_logger(
        number: int = 1,
        need_result: bool = False
):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not isinstance(number, int):
                raise ValueError(f'func time_logger, number: {number}')
            total = avg = 0
            result = list()
            if not number == 0:
                for _ in range(number):
                    start_time = time.perf_counter()
                    sub_result = func(*args, **kwargs)
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


def time_block(
        accu: Literal['W', 'D', 'H', 'M', 'S'] = 'M',
        logo: str = '',
        need_divisor: bool = False
) -> str | tuple[str, int]:
    t = int(time.time())
    match accu:
        case 'W':
            divisor = 604800
        case 'D':
            divisor = 86400
        case 'H':
            divisor = 3600
        case 'M':
            divisor = 60
        case 'S':
            divisor = 1
        case _:
            raise ValueError(f"func: time_block, accu: {accu}")
    w_t = t // divisor
    if not need_divisor:
        return f"{logo}{w_t}"
    else:
        return f"{logo}{w_t}", divisor


def time_format_doc() -> None:
    doc_sign = f'''
        0   us (number): %f
        1   S (number): %S
        2   M (number): %M
        3   H (12 h): %I
        4   H (24 h): %H
        5   AM | PM: %p
        6   Day (number): %d
        7   Week (number): %w
        8   Week (name): %A
        9   Week (simple name): %a
        10  Month (number): %m
        11  Month (name): %B
        12  Month (simple name): %b
        13  Year (four digit): %Y
        14  Year (four digit): %y
        15  Year (count day): %j
        16  Year (count weak.s): %U
        17  Year (count weak.m): %W
    '''
    doc_fmt = '''
        0   T (12 h): %I:%M %p
        1   T (24 h): %H:%M:%S
        2   D (base): %Y-%m-%d
        3   D (ISO 8601): %Y-%m-%dT%H:%M:%S
        4   D (complete): %A, %B %d, %Y
        5   D (short): %b %d, %Y
        6   D (simple): %m/%d/%Y
        7   D (with week): %A %d %B %Y
        8   D (with count day): %Y-%m-%d %j
        9   D (USA): %m/%d/%Y %I:%M %p
    '''

    def format_doc(doc):
        pattern = re.compile(r'([0-9]{1,2}.*: )(%.+)$', re.M)
        fmt_finditer = pattern.finditer(doc)
        new_doc = []
        for i in fmt_finditer:
            text = i.group(1)
            fmt = i.group(2)
            date_time = datetime.now().strftime(fmt)
            space_t_f = ' ' * (30 - len(text))
            space_f_d = ' ' * (50 - (30 + len(fmt)))

            new_doc.append(text + space_t_f + fmt + space_f_d + f'{date_time}')

        return '\n'.join(new_doc)

    doc_sign = format_doc(doc=doc_sign)
    doc_fmt = format_doc(doc=doc_fmt)

    doc = f'doc sign:\n{doc_sign}\n\ndoc fmt:\n{doc_fmt}\n'
    print(doc)
