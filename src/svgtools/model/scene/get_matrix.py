from svgtools.model.geometry.matrix3 import Matrix3
from svgtools.model.scene.transform import Translate, Scale, Rotate, SkewX, SkewY, Affine

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
            return Matrix3.affine(transform.a, transform.b, transform.c,
                                  transform.d, transform.e, transform.f)
