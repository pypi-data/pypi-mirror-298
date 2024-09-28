"""
Hello!
"""

from contextlib import contextmanager
import logging
import sys
from typing import (
    Dict,
    Iterator,
    List,
    Literal,
    Sequence,
)

import colorama
import termcolor


def multi_exception_shim(
    exceptions: Sequence[Exception], logger: logging.Logger, emsg: str
) -> None:
    if not exceptions:
        return

    if len(exceptions) == 1:
        raise exceptions[0]

    if sys.version_info >= (3, 11):
        raise ExceptionGroup(emsg, exceptions)

    # For older versions of Python, just raise the first Exception.

    for exc in exceptions[1:]:
        logger.error(f"Exception: {exc_summary(exc)}")
        logger.debug("Detail: ", exc_info=exc)

    raise exceptions[0]


def exc_name(exc: BaseException) -> str:
    name = type(exc).__qualname__
    smod = type(exc).__module__
    if smod not in ("__main__", "builtins"):
        name = smod + "." + name
    return name


def exc_summary(exc: BaseException) -> str:
    ret = str(exc)
    if ret:
        return f"{exc_name(exc)}: {ret}"
    return exc_name(exc)


Color = Literal[
    "black",
    "grey",
    "red",
    "green",
    "yellow",
    "blue",
    "magenta",
    "cyan",
    "light_grey",
    "dark_grey",
    "light_red",
    "light_green",
    "light_yellow",
    "light_blue",
    "light_magenta",
    "light_cyan",
    "white",
]


class ColorFormatter(logging.Formatter):
    colmap: Dict[int, Color] = {
        logging.INFO: "light_grey",
        logging.DEBUG: "dark_grey",
        logging.WARNING: "yellow",
        logging.ERROR: "red",
    }

    def format(self, record: logging.LogRecord) -> str:
        msg = super().format(record)
        if record.levelno in self.colmap:
            msg = termcolor.colored(msg, self.colmap[record.levelno])
        return msg


class WarningHandler(logging.Handler):
    def __init__(self, logger: logging.Logger) -> None:
        self.messages: List[str] = []
        self.logger = logger
        self.propagate = logger.propagate
        self.force = logger.getEffectiveLevel() <= logging.DEBUG

        # Force this handler to always "handle" events ...
        super().__init__(logging.NOTSET)

    def handle(self, record: logging.LogRecord) -> bool:
        propagate = self.propagate and (self.force or (record.levelno != logging.WARNING))
        if propagate:
            if parent := self.logger.parent:
                parent.callHandlers(record)

        if record.levelno == logging.WARNING:
            # only *actually* handle warnings.
            return super().handle(record)
        return False

    def emit(self, record: logging.LogRecord) -> None:
        msg = self.format(record)
        self.messages.append(msg)


@contextmanager
def capture_warnings(node: str) -> Iterator[List[str]]:
    """
    Simple context manager that captures logging at a given level.

    Messages will cease to propagate while in the context block; they
    will resume propagating (if they were before) upon exit from the
    block. Any messages captured during the block will be in the List
    yielded during the block.

    Example::
        with capture_logging('cici') as messages:
            avb = Binary('file.avb')

        for message in messages:
            print(message)
    """
    logger = logging.getLogger(node)
    propagate = logger.propagate

    # This weird little guy stores warnings for later, and also will
    # *conditionally* propagate only non-warning LogRecords, which
    # lets us fully capture warnings.
    handler = WarningHandler(logger)

    try:
        logger.propagate = False
        logger.addHandler(handler)
        yield handler.messages
    finally:
        logger.propagate = propagate
        logger.removeHandler(handler)


def setup_logging(debug: bool = False) -> None:
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.WARNING,
    )

    fmt = "%(levelname)s: %(message)s" if debug else "%(message)s"

    rootlogger = logging.getLogger()
    for handler in rootlogger.handlers:
        if isinstance(handler, logging.StreamHandler):
            handler.setFormatter(ColorFormatter(fmt))
            break

    colorama.init()
