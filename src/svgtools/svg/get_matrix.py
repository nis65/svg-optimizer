from svgtools.geometry.matrix3 import Matrix3
from svgtools.svg.transform import Affine, Rotate, Scale, SkewX, SkewY, Translate


def transforms_to_matrix(transforms) -> Matrix3:
    matrix = Matrix3.identity()
    for transform in transforms:
        matrix *= get_matrix(transform)
    return matrix


def get_matrix(transform) -> Matrix3:
    match transform:
        case Translate():
            return Matrix3.translation(transform.dx, transform.dy)
        case Scale():
            return Matrix3.scaling(transform.sx, transform.sy)
        case Rotate():
            return Matrix3.rotation(transform.theta, transform.cx, transform.cy)
        case SkewX():
            return Matrix3.skew_x(transform.theta)
        case SkewY():
            return Matrix3.skew_y(transform.theta)
        case Affine():
            return Matrix3.affine(
                transform.a,
                transform.b,
                transform.c,
                transform.d,
                transform.e,
                transform.f,
            )
