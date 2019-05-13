import sys
from logging import (
    basicConfig, DEBUG, Formatter,
    getLogger as org_get_logger
)

from atomic_p2p.utils.logging.handlers import StreamHandler, SocketHandler
from atomic_p2p.utils.logging.formatters import StdoutFormatter


def getLogger(name=None, level=DEBUG, add_monitor_pass=None):
    if name is None:
        logger = org_get_logger()
    else:
        logger = org_get_logger(name)
    logger.setLevel(level)
    toggle = {
        'stdout': True,
        'monitor': True
    }

    formatter = StdoutFormatter()

    for each in logger.root.handlers:
        if hasattr(each, 'name') is True:
            toggle[each.name] = False

    for (key, value) in toggle.items():
        if value is True:
            handler = None
            if key == 'stdout':
                handler = StreamHandler(name='stdout', stream=sys.stdout)
            elif key == 'monitor' and add_monitor_pass is not None:
                handler = SocketHandler(name='monitor',
                                        password=add_monitor_pass)

            if handler is not None:
                handler.setLevel(DEBUG)
                handler.setFormatter(formatter)
                logger.root.addHandler(handler)

    return logger
