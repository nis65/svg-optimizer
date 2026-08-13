from enum import Enum, auto

class TransformWriteStrategy(Enum):
    KEEP = auto()
    AGGREGATE = auto()
    DECOMPOSE_MATRIX = auto()
    AGGREGATE_AND_DECOMPOSE_MATRIX = auto()
    CANONICAL_CONSERVATIVE = auto()
    CANONICAL_AGGRESSIVE = auto()
