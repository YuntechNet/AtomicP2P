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
