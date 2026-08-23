from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Rotate:
    theta: float
    cx: float
    cy: float
