from enum import Enum, auto
from dataclasses import dataclass

from svgtools.geometry.point import Point

class PathCoordinates(Enum):
    ABSOLUTE = auto()
    RELATIVE = auto()
    KEEP = auto()

class PathCompactness(Enum):
    CANONICAL = auto()
    COMPACT = auto()

class PathCommandSet(Enum):
    BASE = auto()
    FULL = auto()

@dataclass(frozen=True, slots=True)
class PathCommand:
    command: str
    parameters: str

@dataclass
class PathWriteState:
    current_point: Point = Point(0, 0)
    current_subpath_start: Point = Point(0, 0)
