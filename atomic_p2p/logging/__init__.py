from sys import stdout
from logging import basicConfig, DEBUG, getLogger as get_logger

from .handlers import StreamHandler, SocketHandler
from .formatters import StdoutFormatter


def getLogger(
    name=None, level=DEBUG, local_monitor_password=None, local_monitor_bind_port=None
):
    if name is None:
        logger = get_logger()
    else:
        logger = get_logger(name)
    logger.setLevel(level)
    toggle = {"stdout": True, "monitor": True}

    formatter = StdoutFormatter()

    for each in logger.root.handlers:
        if hasattr(each, "name") is True:
            toggle[each.name] = False

    for (key, value) in toggle.items():
        if value is True:
            if key == "monitor" and local_monitor_password is not None:
                handler = SocketHandler(
                    name="monitor",
                    local_monitor_password=local_monitor_password,
                    local_monitor_bind_port=local_monitor_bind_port,
                )
            elif key == "stdout":
                handler = StreamHandler(name="stdout", stream=stdout)
            else:
                continue

            handler.setLevel(DEBUG)
            handler.setFormatter(formatter)
            logger.root.addHandler(handler)

    return logger
