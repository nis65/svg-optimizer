from enum import Enum, auto

class PathCoordinates(Enum):
    KEEP = auto()
    ABSOLUTE = auto()
    RELATIVE = auto()

class PathCompactness(Enum):
    COMPACT = auto()
    CANONICAL = auto()
