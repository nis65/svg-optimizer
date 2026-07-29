from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Matrix3:
    m11: float
    m12: float
    m13: float

    m21: float
    m22: float
    m23: float

    m31: float
    m32: float
    m33: float
