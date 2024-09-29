# -*- coding=utf-8 -*-
r"""

"""
from time import perf_counter_ns


__all__ = ['timer', 'format_delta_ns']


def timer(*, precision: int):
    r"""
    >>> timing = timer(precision=2)
    >>> next(timing)
    >>> next(timing)

    :param precision: formatted time precision
    """
    start_time = perf_counter_ns()

    def gen():
        while True:
            end_time = perf_counter_ns()
            yield format_delta_ns(end_time - start_time, precision)

    return gen()


TIME_UNITS_NS = {
    1: "ns",  # nanoseconds
    1000: "μs",  # microseconds
    1000000: "ms",  # milliseconds
    1000000000: "s",  # seconds
    60000000000: "m",  # minutes
    3600000000000: "h",  # hours
    86400000000000: "d",  # days
    # 604800000000000: "wk",  # weeks
    2628000000000000: "mo",  # months
}
TIME_UNITS_NS_FACTORS = sorted(TIME_UNITS_NS, reverse=True)  # biggest first
TIME_UNITS_NS_COUNT = len(TIME_UNITS_NS)


def format_delta_ns(delta: int, precision: int = 3) -> str:
    r"""
    format time-delta measured with time.perf_counter_ns()
    """
    start = next((index for index, factor in enumerate(TIME_UNITS_NS_FACTORS) if delta >= factor), None)
    if start is None:
        return f"{delta}s"  # in case of delta <= 0
    parts = []
    rest = delta
    for index in range(start, min(start + precision, TIME_UNITS_NS_COUNT)):
        factor = TIME_UNITS_NS_FACTORS[index]
        count, rest = divmod(rest, factor)
        if count:
            parts.append(f"{count}{TIME_UNITS_NS[factor]}")
        if not rest:
            break
    return '+'.join(parts)
