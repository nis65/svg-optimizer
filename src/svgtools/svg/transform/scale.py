from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Scale:
    sx: float
    sy: float
