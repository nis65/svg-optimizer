import math
from dataclasses import dataclass
from .point import Point

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

    @classmethod
    def identity(cls) -> "Matrix3":
        return cls(
            1, 0, 0,
            0, 1, 0,
            0, 0, 1,
        )

    @classmethod
    def translation(cls, dx: float, dy: float) -> "Matrix3":
        return cls(
            1, 0, dx,
            0, 1, dy,
            0, 0, 1,
        )

    @classmethod
    def scaling(cls, sx: float, sy: float) -> "Matrix3":
        return cls(
            sx, 0, 0,
            0, sy, 0,
            0, 0, 1,
        )

    @classmethod
    def rotation(cls, theta_degree: float, cx: float, cy: float) -> "Matrix3":
        t_to_origin=cls.translation(-cx, -cy)
        t_from_origin=cls.translation(cx, cy)
        theta = 2 * math.pi * theta_degree / 360
        c=math.cos(theta)
        s=math.sin(theta)
        rotate=Matrix3(
            c, -s, 0,
            s,  c, 0,
            0,  0, 1
        )
        return t_from_origin * rotate * t_to_origin

    def _mul_column(self, x: float, y: float, w: float) -> tuple[float, float, float]:
        return (
            self.m11 * x + self.m12 * y + self.m13 * w,
            self.m21 * x + self.m22 * y + self.m23 * w,
            self.m31 * x + self.m32 * y + self.m33 * w
        )

    def __mul__(self, other):
        if isinstance(other, Matrix3):
            c1 = self._mul_column(other.m11, other.m21, other.m31)
            c2 = self._mul_column(other.m12, other.m22, other.m32)
            c3 = self._mul_column(other.m13, other.m23, other.m33)

            return Matrix3(
                c1[0], c2[0], c3[0],
                c1[1], c2[1], c3[1],
                c1[2], c2[2], c3[2]
            )
        if isinstance(other, Point):
            x, y, w = self._mul_column(other.x, other.y, 1)
            return Point(
                x / w,
                y / w
            )
        return NotImplemented

    @staticmethod
    def _isclose(a: float, b: float):
        return math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-9)

    def isclose(self, other):
        if not isinstance(other, Matrix3):
            return False
        return (self._isclose(self.m11, other.m11) and
                self._isclose(self.m12, other.m12) and
                self._isclose(self.m13, other.m13) and
                self._isclose(self.m21, other.m21) and
                self._isclose(self.m22, other.m22) and
                self._isclose(self.m23, other.m23) and
                self._isclose(self.m31, other.m31) and
                self._isclose(self.m32, other.m32) and
                self._isclose(self.m33, other.m33)
        )
