from enum import Enum


class PeerRole(Enum):
    """Basic define of peer roles.
    Enumerations can not be extend.
    Every classes parameter which need to pass PeerRole's type hint is enum.Enum.
    Before use, define your own PeerRole like:
    >>> from enum import Enum
    >>> 
    >>> class PeerRole(Enum):
    >>>     CORE = "CORE"
    >>>     EDGE = "EDGE"
    """
    CORE = "CORE"
    EDGE = "EDGE"
