import functools
import asyncio
from typing import Callable, Any


def catchable(exception_cls: type(BaseException)):
    def impl(cls):
        for name, value in vars(cls).items():
            if callable(value):
                setattr(cls, name, catchable_method(value, exception_cls))
        return cls

    return impl


def catchable_method(method: Callable[[Any], Any], exception_cls: type(BaseException)):
    if asyncio.iscoroutinefunction(method):
        @functools.wraps(method)
        async def wrapper(*args, **kwargs):
            try:
                return await method(*args, **kwargs)
            except exception_cls as e:
                raise exception_cls(e)
    else:
        @functools.wraps(method)
        def wrapper(*args, **kwargs):
            try:
                return method(*args, **kwargs)
            except exception_cls as e:
                raise exception_cls(e)

    return wrapper
