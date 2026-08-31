from collections import Counter
from dataclasses import dataclass

from .geometry_abc import Geometry
from .path_elements.closepath import ClosePath
from .path_elements.moveto import MoveTo
from .point import Point


@dataclass(frozen=True, slots=True)
class Path(Geometry):
    children: tuple = ()

    def points_for_bounding_box(self, number_of_points: int) -> set[Point]:
        _dummy, points = self.points_for_bounding_box_with_stats(number_of_points)
        return points

    def points_for_bounding_box_with_stats(
        self, number_of_points: int
    ) -> tuple[Counter[str], set[Point]]:
        path_elements_visited = Counter()
        points = []
        # a path does not need to start with an explicit MoveTo
        current_point = Point(0, 0)
        current_subpath_start = current_point

        for child in self.children:
            if type(child) == MoveTo:
                current_point = child.target
                current_subpath_start = current_point
            elif type(child) == ClosePath:
                points.append(current_point)
                points.append(current_subpath_start)
                current_point = current_subpath_start
            else:
                points.extend(
                    child.points_for_bounding_box(current_point, number_of_points)
                )
                current_point = child.endpoint
            path_elements_visited[type(child).__name__] += 1
        return path_elements_visited, set(points)
