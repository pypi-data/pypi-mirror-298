import inspect
from functools import wraps
from typing import Callable, Any


def frame_info(back_count: int = 2):
    frame = inspect.currentframe()
    for _ in range(back_count):
        frame = frame.f_back
        if not frame:
            _frame = lambda: frame_info(back_count=2)
            raise ValueError(f'{_frame()}')
    module = inspect.getmodule(frame)
    module_name = module.__name__ if module else None
    return module_name, frame.f_code.co_name, frame.f_lineno


def judge_factor(
        factor: str = 'factor',
        *,
        call: Callable[..., Any]
):
    def decorator(func):
        sig = inspect.signature(func)
        params = list(sig.parameters.values())
        params.append(
            inspect.Parameter(
                name=factor,
                kind=inspect.Parameter.KEYWORD_ONLY,
                default=False
            )
        )
        sig = sig.replace(parameters=params)

        @wraps(func)
        def wrapper(*args, **kwargs):
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            _factor = bound_args.arguments.pop(factor)
            if _factor is True:
                call()
            return func(*bound_args.args, **bound_args.kwargs)

        return wrapper
    return decorator
