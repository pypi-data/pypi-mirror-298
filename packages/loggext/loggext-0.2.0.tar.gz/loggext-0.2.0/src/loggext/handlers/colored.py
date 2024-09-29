# -*- coding=utf-8 -*-
r"""

"""
import sys
import logging
import typing as t


__all__ = ['ColoredConsoleHandler', 'LevelColorConsoleHandler']


ENDCOLOR = "\033[0m"
COLOR_MAP: t.Dict[int, str] = {
    logging.DEBUG: "\033[37m",  # light gray
    logging.INFO: "\033[94m",  # light blue
    logging.WARN: "\033[93m",  # light yellow
    logging.ERROR: "\033[91m",  # light red
    logging.CRITICAL: "\033[95m",  # light magenta
}


class ColoredConsoleHandler(logging.StreamHandler):
    r"""
    same as :class:`logging.StreamHandler` but with colored output based on the logging-level of each message
    """
    STDOUT = sys.stdout
    STDERR = sys.stderr

    def format(self, record):
        colorcode = COLOR_MAP.get(record.levelno)
        msg = super().format(record)
        if colorcode is None:
            return msg
        return f"{colorcode}{msg}{ENDCOLOR}"


class LevelColorConsoleHandler(logging.StreamHandler):
    r"""
    similar to :class:`ColoredConsoleHandler` but colors only the levelname
    """
    STDOUT = sys.stdout
    STDERR = sys.stderr

    def emit(self, record):
        colorcode = COLOR_MAP.get(record.levelno)
        if colorcode is not None:
            record = logging.makeLogRecord(record.__dict__)  # copy to not modify for other logging-handlers
            record.levelname = f"{colorcode}{record.levelname}{ENDCOLOR}"
        super().emit(record)
