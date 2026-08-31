from dataclasses import dataclass

from .geometry_abc import Geometry
from .point import Point


@dataclass(frozen=True, slots=True)
class Polygon(Geometry):
    children: tuple = ()

    def points_for_bounding_box(self, number_of_points: int) -> set[Point]:
        # number_of_points is ignored, as the n points fully define the bounding box
        points = list(self.children)
        return set(points)
