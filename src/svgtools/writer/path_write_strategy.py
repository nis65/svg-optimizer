from enum import Enum, auto

class PathWriteStrategy(Enum):
    KEEP = auto()
    ABSOLUTE = auto()
    RELATIVE = auto()
