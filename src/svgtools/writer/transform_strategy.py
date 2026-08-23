import math
from enum import Enum, auto

from svgtools.geometry.matrix3 import Matrix3
from svgtools.geometry.tolerance import GEOMETRY_ABS_TOL, GEOMETRY_REL_TOL
from svgtools.svg.get_matrix import get_matrix, transforms_to_matrix
from svgtools.svg.transform import Affine, Rotate, Scale, SkewX, SkewY, Translate

from .write_utils import numberlist_to_string


class TransformWriteStrategy(Enum):
    KEEP = auto()
    AGGREGATE = auto()
    DECOMPOSE_MATRIX = auto()
    DECOMPOSE_MATRIX_AND_AGGREGATE = auto()
    CANONICAL_CONSERVATIVE = auto()
    CANONICAL_AGGRESSIVE = auto()

class TransformStrategy:
    def __init__(self, strategy: TransformWriteStrategy):
        self.strategy = strategy
        self.total_aggregated_chains = 0
        self.total_aggressive_chains = 0

    def apply(self, transformations):
        match self.strategy:
            case TransformWriteStrategy.KEEP:
                return transformations
            case TransformWriteStrategy.AGGREGATE:
                return self._transform_strategy_aggregate(transformations)
            case TransformWriteStrategy.DECOMPOSE_MATRIX:
                return self._transform_strategy_decompose_matrix(transformations)
            case TransformWriteStrategy.DECOMPOSE_MATRIX_AND_AGGREGATE:
                decomposed=self._transform_strategy_decompose_matrix(transformations)
                return self._transform_strategy_aggregate(decomposed)
            case TransformWriteStrategy.CANONICAL_CONSERVATIVE :
                return self._transform_strategy_conservative(transformations)
            case TransformWriteStrategy.CANONICAL_AGGRESSIVE:
                return self._transform_strategy_aggressive(transformations)
            case _:    # pragma: no cover
                    raise ValueError(f"transform_strategy {self.strategy} not implemented")

    @staticmethod
    def transforms_to_string(transformations) -> str:
        result = ""
        for trans in transformations:
            match trans:
                case Translate():
                    numberlist=(trans.dx, trans.dy, )
                    result += f' translate({numberlist_to_string(numberlist)})'
                case Scale():
                    numberlist=(trans.sx, trans.sy, )
                    result += f' scale({numberlist_to_string(numberlist)})'
                case Rotate():
                    numberlist=(trans.theta, trans.cx, trans.cy, )
                    result += f' rotate({numberlist_to_string(numberlist)})'
                case SkewX():
                    numberlist=(trans.theta, )
                    result += f' skewX({numberlist_to_string(numberlist)})'
                case SkewY():
                    numberlist=(trans.theta, )
                    result += f' skewY({numberlist_to_string(numberlist)})'
                case Affine():
                    numberlist=(trans.a, trans.b, trans.c, trans.d, trans.e, trans.f, )
                    result += f' matrix({numberlist_to_string(numberlist)})'

        return result.strip()

    @staticmethod
    def _is_canonical(transformations) -> bool:
        _CANONICAL_ORDER = (Translate, Rotate, SkewX, Scale)
        reference = iter(_CANONICAL_ORDER)
        for t in transformations:
            if type(t) == Rotate and not (t.cx == 0 and t.cy == 0):
                return False
            for expected in reference:
                if type(t) == expected:
                    break
            else:
                return False
        return True

    @staticmethod
    def _transform_strategy_aggregate(transformations):
        if len(transformations) == 0:
            raise ValueError("should not be called with 0 transformations")
        t_list = []
        agg_t = None
        for t in transformations:
            if agg_t is None:
                agg_t = t
            elif type(t) == type(agg_t):
                match t:
                    case Translate():
                        agg_t = Translate(dx = agg_t.dx + t.dx, dy = agg_t.dy + t.dy)
                    case Scale():
                        agg_t = Scale(sx = agg_t.sx * t.sx, sy = agg_t.sy * t.sy)
                    case Rotate():
                        if agg_t.cx == t.cx and agg_t.cy == t.cy:
                            agg_t = Rotate(theta = agg_t.theta + t.theta, cx = t.cx, cy = t.cy)
                        else:
                            # rotate can only be aggregated exactly with the same rotation center
                            t_list.append(agg_t)
                            agg_t = t
                    case SkewX() | SkewY():
                        # skew cannot be aggregated in an exact way
                        t_list.append(agg_t)
                        agg_t = t
                    case Affine():
                        agg_m = get_matrix(agg_t) * get_matrix(t)
                        agg_t= Affine(a=agg_m.m11, b=agg_m.m21, c=agg_m.m12,
                                      d=agg_m.m22, e=agg_m.m13, f=agg_m.m23)
            else:
                t_list.append(agg_t)
                agg_t = t
        t_list.append(agg_t)
        return tuple(t_list)

    @staticmethod
    def _transform_strategy_decompose_matrix(transformations):
        t_list = []
        for t in transformations:
            match t:
                case Affine():
                    md = Matrix3.TRHxS_decompose(
                            Matrix3.affine(a=t.a, b=t.b, c=t.c,
                                           d=t.d, e=t.e, f=t.f
                        )
                    )
                    if not (md.tx == 0 and md.ty == 0):
                        t_list.append(Translate(dx=md.tx, dy=md.ty))
                    if not math.isclose(md.theta_rotate, 0, rel_tol=GEOMETRY_REL_TOL, abs_tol=GEOMETRY_ABS_TOL):
                        t_list.append(Rotate(theta=md.theta_rotate, cx=0, cy=0))
                    if not math.isclose(md.theta_skew_x, 0, rel_tol=GEOMETRY_REL_TOL, abs_tol=GEOMETRY_ABS_TOL):
                        t_list.append(SkewX(theta=md.theta_skew_x))
                    if not (md.sx == 1 and md.sy == 1):
                        t_list.append(Scale(sx=md.sx, sy=md.sy))
                case _:
                    t_list.append(t)
        return tuple(t_list)

    def _transform_strategy_conservative(self, transformations):
        # attempt aggregate
        aggregated = self._transform_strategy_aggregate(transformations)
        if self._is_canonical(aggregated):
            self.total_aggregated_chains +=1
            return aggregated
        else:
            self.total_aggressive_chains +=1
            return self._transform_strategy_aggressive(transformations)

    def _transform_strategy_aggressive(self, transformations):
        m = transforms_to_matrix(transformations)
        return self._transform_strategy_decompose_matrix((Affine(a=m.m11, b=m.m21, c=m.m12, d=m.m22, e=m.m13, f=m.m23),))
