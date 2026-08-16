import math
from dataclasses import dataclass
from .point import Point
from .isclose import geometry_isclose

@dataclass(frozen=True, slots=True)
class TRHxSDecomposition:
    tx: float
    ty: float
    theta_rotate: float
    h_skew_x: float
    sx: float
    sy: float

    @property
    def theta_skew_x(self) -> float:
        return math.degrees(math.atan(self.h_skew_x))

    def isclose(self, other):
        if not isinstance(other, TRHxSDecomposition):
            return False
        return (geometry_isclose(self.tx, other.tx) and
                geometry_isclose(self.ty, other.ty) and
                geometry_isclose(self.theta_rotate, other.theta_rotate) and
                geometry_isclose(self.theta_skew_x, other.theta_skew_x) and
                geometry_isclose(self.sx, other.sx)
        )

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
        theta = math.radians(theta_degree)
        c=math.cos(theta)
        s=math.sin(theta)
        rotate=Matrix3(
            c, -s, 0,
            s,  c, 0,
            0,  0, 1
        )
        return t_from_origin * rotate * t_to_origin

    @classmethod
    def skew_x(cls, theta_degree: float) -> "Matrix3":
        if theta_degree % 180 == 90:
            raise ValueError(f"cannot skew by {theta_degree}, undefined")
        s = math.tan(math.radians(theta_degree))
        return Matrix3(
            1, s, 0,
            0, 1, 0,
            0, 0, 1
        )

    @classmethod
    def skew_y(cls, theta_degree: float) -> "Matrix3":
        if theta_degree % 180 == 90:
            raise ValueError(f"cannot skew by {theta_degree}, undefined")
        s = math.tan(math.radians(theta_degree))
        return Matrix3(
            1, 0, 0,
            s, 1, 0,
            0, 0, 1
        )

    @classmethod
    def affine(cls, a: float, b: float, c: float,
                    d: float, e: float, f: float) -> "Matrix3":
        return Matrix3(
            a, c, e,
            b, d, f,
            0, 0, 1
        )

    @staticmethod
    def TRHxS_decompose(a: "Matrix3") -> TRHxSDecomposition:

        # first, extract translation
        tx, ty = a.m13, a.m23

        # rotation and scale_x from first colum
        scale_x = math.sqrt(a.m11*a.m11 + a.m21*a.m21)
        if math.isclose(scale_x, 0, rel_tol=1e-9, abs_tol=1e-9):
            raise ValueError(f"scale_x is close to 0 ({scale_x}), cannot decompose")
        theta_rotate = math.degrees(math.atan2(a.m21, a.m11))

        # scale_y from det and scale_x
        det = a.m11*a.m22 - a.m12*a.m21
        if math.isclose(det, 0, rel_tol=1e-9, abs_tol=1e-9):
            raise ValueError(f"determinant is close to 0 ({det}), cannot decompose")
        scale_y = det / scale_x

        # finally, skewX
        skew_x = ( a.m11*a.m12 + a.m21*a.m22 ) / det

        return TRHxSDecomposition(
            tx= tx,
            ty= ty,
            theta_rotate= theta_rotate,
            h_skew_x= skew_x,
            sx= scale_x,
            sy= scale_y,
            )

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

    def isclose(self, other):
        if not isinstance(other, Matrix3):
            return False
        return (geometry_isclose(self.m11, other.m11) and
                geometry_isclose(self.m12, other.m12) and
                geometry_isclose(self.m13, other.m13) and
                geometry_isclose(self.m21, other.m21) and
                geometry_isclose(self.m22, other.m22) and
                geometry_isclose(self.m23, other.m23) and
                geometry_isclose(self.m31, other.m31) and
                geometry_isclose(self.m32, other.m32) and
                geometry_isclose(self.m33, other.m33)
        )
