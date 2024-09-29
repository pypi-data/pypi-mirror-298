# -*- coding=utf-8 -*-
r"""

"""
import logging


__all__ = ['logging_is_configured']


def logging_is_configured() -> bool:
    return len(logging.root.handlers) > 0
