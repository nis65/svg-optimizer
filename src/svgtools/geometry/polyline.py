from dataclasses import dataclass
from .geometry_abc import Geometry
from .point import Point
from .bounding_box import BoundingBox

@dataclass(frozen=True, slots=True)
class Polyline(Geometry):
    children: tuple = ()

    def points_for_bounding_box(self, count: int) -> set[Point]:
        # count is ignored, as the n points fully define the bounding box
        points = []
        for point in self.children:
            points.append(point)
        return set(points)
