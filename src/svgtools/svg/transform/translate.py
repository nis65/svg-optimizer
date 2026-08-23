from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Translate:
    dx: float
    dy: float
