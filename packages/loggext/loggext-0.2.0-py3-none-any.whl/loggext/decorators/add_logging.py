# -*- coding=utf-8 -*-
r"""

"""
import logging
import functools
import typing as t
from asyncio import iscoroutinefunction
from ._util import timer


__all__ = ['add_logging']


def add_logging(
        fn: t.Callable = None,
        *, logger: logging.Logger = logging,
        call: bool = True,
        call_args: bool = True,
        timeit: bool = True,
        timeit_precision: int = 2,
        result: bool = True,
        ):
    r"""
    adds some logging messages to a function

    >>> @add_logging()
    ... def foo():
    ...     pass

    note: supports async functions

    :param fn: function to be decorated
    :param logger: specific logger to use (otherwise root-logger)
    :param call: whether to log when the function is called
    :param call_args: whether to log the functions call arguments (only with `call=True`)
    :param timeit: whether to log the functions execution time
    :param timeit_precision: precision of the logged execution time (only with `timeit=True`)
    :param result: whether to log the returned value of the function
    """
    def decorator(func: t.Callable) -> t.Callable:
        if iscoroutinefunction(func):
            @functools.wraps(func)
            async def wrapper(*args, **kwargs):
                timing = timer(precision=timeit_precision)
                try:
                    if call:
                        message = f"{func} was called"
                        if call_args:
                            message += f" with ({_format_args(*args, **kwargs)})"
                        logging.debug(message)
                    res = await func(*args, **kwargs)
                    if result or timeit:
                        resfmt = f" {res!r}" if result else ""
                        timefmt = f" after {next(timing)}" if timeit else ""
                        logger.debug(f"{func} returned{resfmt}{timefmt}")
                    return res
                except BaseException as exc:
                    message = f"{func} raised {type(exc).__qualname__}"
                    if timeit:
                        message += f" after {next(timing)}"
                    logger.exception(message, exc_info=exc)
                    raise exc
        else:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                timing = timer(precision=timeit_precision)
                try:
                    if call:
                        message = f"{func} was called"
                        if call_args:
                            message += f" with ({_format_args(*args, **kwargs)})"
                        logging.debug(message)
                    res = func(*args, **kwargs)
                    if result or timeit:
                        resfmt = f" {res!r}" if result else ""
                        timefmt = f" after {next(timing)}" if timeit else ""
                        logger.debug(f"{func} returned{resfmt}{timefmt}")
                    return res
                except BaseException as exc:
                    message = f"{func} raised {type(exc).__qualname__}"
                    if timeit:
                        message += f" after {next(timing)}"
                    logger.exception(message, exc_info=exc)
                    raise exc

        return wrapper

    return decorator if fn is None else decorator(func=fn)


def _format_args(*args, **kwargs):
    return ', '.join([*map(repr, args), *(f"{key}={repr(val)}" for key, val in kwargs.items())])
