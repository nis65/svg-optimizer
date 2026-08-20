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
        points = []
        # a path does not need to start with an explicit MoveTo
        current_point = Point(0,0)
        current_subpath_start = current_point

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
