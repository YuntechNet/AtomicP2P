import sys
from LibreCisco.utils.logging.formatters import StdoutFormatter
from logging import (
    basicConfig, DEBUG, StreamHandler, Formatter,
    getLogger as org_get_logger
)


def getLogger(name=None, level=DEBUG):
    if name is None:
        logger = org_get_logger()
    else:
        logger = org_get_logger(name)
    logger.setLevel(level)
    if logger.root.handlers == []:
        stdout_handler = StreamHandler(sys.stdout)
        stdout_handler.setLevel(DEBUG)
        stdout_handler.setFormatter(StdoutFormatter())

        logger.root.addHandler(stdout_handler)
    return logger
