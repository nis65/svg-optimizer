from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Affine:
    a: float
    b: float
    c: float
    d: float
    e: float
    f: float
