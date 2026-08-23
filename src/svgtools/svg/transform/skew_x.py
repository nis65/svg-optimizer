from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SkewX:
    theta: float
