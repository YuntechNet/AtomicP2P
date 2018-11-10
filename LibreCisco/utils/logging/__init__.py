import sys
from logging import (
    basicConfig, DEBUG, StreamHandler, Formatter,
    getLogger as org_get_logger
)

from LibreCisco.utils.logging.handlers import SocketHandler
from LibreCisco.utils.logging.formatters import StdoutFormatter


def getLogger(name=None, level=DEBUG, add_monitor=False):
    if name is None:
        logger = org_get_logger()
    else:
        logger = org_get_logger(name)
    logger.setLevel(level)
    if logger.root.handlers == []:
        formatter = StdoutFormatter()

        stdout_handler = StreamHandler(sys.stdout)
        stdout_handler.setLevel(DEBUG)
        stdout_handler.setFormatter(formatter)

        if add_monitor is True:
            monitor_handler = SocketHandler()
            monitor_handler.setFormatter(formatter)
            logger.root.addHandler(monitor_handler)

        logger.root.addHandler(stdout_handler)
    return logger
