import enum

# SwitchMode
#   Define switch operating mode.
#
class SwitchMode(enum.IntEnum):
    DEFAULT = 0
    ENABLE = 1
    CONTER = 2
    EN_CONF = 3 

# UserPriority
#   Define user's priority while executing command.
#
class UserPriority(enum.IntEnum):
    ADMIN = 0
    SCHEDULE = 1
    USER = 2

# Log Level
class LogLevel(enum.Enum):
    INFO = '\x1b[0m'
    WARNING = '\x1b[0;33;49m'
    ERROR = '\x1b[0;31;49m'
    SUCCESS = '\x1b[1;32;49m'
