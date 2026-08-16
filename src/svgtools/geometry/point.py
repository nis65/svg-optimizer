import math

from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Point:
    x: float
    y: float

    # abs_tol is dependent on the viewBox (i.e. the size of the
    # whole picture in user space coordinates)
    def isclose(self, other, svg_abs_tol):
        REL_TOL=1e-9
        return (math.isclose(self.x, other.x, rel_tol=REL_TOL, abs_tol=svg_abs_tol) and
                math.isclose(self.y, other.y, rel_tol=REL_TOL, abs_tol=svg_abs_tol)
        )

    @staticmethod
    def points_are_close(set1: set["Point"], set2: set["Point"], svg_abs_tol: float) -> bool:
        if len(set1) != len(set2):
            return False
        remaining = list(set2)
        for point1 in set1:
            for i, point2 in enumerate(remaining):
                if point1.isclose(point2, svg_abs_tol):
                    remaining.pop(i)
                    break
            else:
                return False
        return True
