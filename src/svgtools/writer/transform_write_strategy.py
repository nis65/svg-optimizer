from enum import Enum, auto

class TransformWriteStrategy(Enum):
    KEEP = auto()
    AGGREGATE = auto()
    DECOMPOSE_MATRIX = auto()
    DECOMPOSE_MATRIX_AND_AGGREGATE = auto()
    CANONICAL_CONSERVATIVE = auto()
    CANONICAL_AGGRESSIVE = auto()
