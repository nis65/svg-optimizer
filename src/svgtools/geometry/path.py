from dataclasses import dataclass
from .geometry_abc import Geometry
from .point import Point
from .path_elements.moveto import MoveTo
from .path_elements.lineto import LineTo
from .path_elements.closepath import ClosePath

@dataclass(frozen=True, slots=True)
class Path(Geometry):
    children: tuple = ()

    def points_for_bounding_box(self, count: int) -> set[Point]:
        # as every path MUST start with a moveto, we don't need to
        # initialise current_point and current_subpath_start here
        points = []

        for child in self.children:
            if type(child) == MoveTo:
                current_point = child.target
                current_subpath_start = current_point
            elif type(child) == ClosePath:
                current_point = current_subpath_start
            else:
                for point in child.points_for_bounding_box(current_point, count):
                    points.append(point)
                current_point = child.endpoint
        return set(points)
