from dataclasses import dataclass

from .geometry_abc import Geometry
from .point import Point


@dataclass(frozen=True, slots=True)
class Rect(Geometry):
    top_left: Point
    width: float
    height: float

    def __post_init__(self) -> None:
        if self.width < 0:
            raise ValueError(f"width ({self.width}) must not be negative")
        if self.height < 0:
            raise ValueError(f"height ({self.height}) must not be negative")

    def points_for_bounding_box(self, number_of_points: int) -> set[Point]:
        # number_of_points is ignored, as 4 points fully define the bounding box
        return {
            self.top_left,
            Point(self.top_left.x, self.top_left.y + self.height),
            Point(self.top_left.x + self.width, self.top_left.y + self.height),
            Point(self.top_left.x + self.width, self.top_left.y),
        }
