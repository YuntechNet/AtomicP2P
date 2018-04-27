import logging


_nameToColor = {
    'CRITICAL': '\x1b[0;31;49m',
    'ERROR': '\x1b[0;31;49m',
    'WARNING': '\x1b[0;33;49m',
    'INFO': '\x1b[0m',
    'DEBUG': '\x1b[0m',
    'NOTSET': '\x1b[0m',
}    

_levelToColor = {
    logging.CRITICAL: '\x1b[0;31;49m',
    logging.ERROR: '\x1b[0;31;49m',
    logging.WARNING: '\x1b[0;33;49m',
    logging.INFO: '\x1b[0m',
    logging.DEBUG: '\x1b[0m',
    logging.NOTSET: '\x1b[0m',
}

class LibCiscoLogger(logging.Logger):

    def __init__(self, name, level=logging.NOTSET):
        return super(LibCiscoLogger, self).__init__(name, level)

    def log(self, level, msg, *args, **kwargs): # Override
        msg = '%s%s\x1b[0m' % (_levelToColor[level], msg)
        super(LibCiscoLogger, self).log(level, msg, *args, **kwargs)

