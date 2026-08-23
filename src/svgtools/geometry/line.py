from dataclasses import dataclass

from .geometry_abc import Geometry
from .point import Point


@dataclass(frozen=True, slots=True)
class Line(Geometry):
    start: Point
    end: Point

    def points_for_bounding_box(self, count: int) -> set[Point]:
        # count is ignored, as the two points fully define the bounding box
        return {
            self.start,
            self.end
        }
