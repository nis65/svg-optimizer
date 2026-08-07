import math

from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Point:
    x: float
    y: float

    # abs_tol is dependent on the viewBox (i.e. the size of the
    # whole picture in user space coordinates)
    def isclose(self, other, scene_tol):
        REL_TOL=1e-9
        return (math.isclose(self.x, other.x, rel_tol=REL_TOL, abs_tol=scene_tol) and
                math.isclose(self.y, other.y, rel_tol=REL_TOL, abs_tol=scene_tol)
        )
