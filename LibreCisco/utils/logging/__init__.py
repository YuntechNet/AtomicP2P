import sys
from logging import (
    basicConfig, DEBUG, StreamHandler,
    getLogger as org_get_logger
)


def logger_init(level=DEBUG):
    basicConfig(level=DEBUG)


def getLogger(name, level=DEBUG):
    logger = org_get_logger(name)
    logger.setLevel(level)
    if logger.handlers is None:
        stdout_handler = StreamHandler(sys.stdout)
        stdout_handler.setLevel(DEBUG)

        logger.addHandler(stdout_handler)

    return logger
