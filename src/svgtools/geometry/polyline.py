from dataclasses import dataclass

from . import Geometry, Point


@dataclass(frozen=True, slots=True)
class Polyline(Geometry):
    children: tuple[Point, ...] = ()

    def points_for_bounding_box(self, number_of_points: int) -> set[Point]:
        points = list(self.children)
        return set(points)
