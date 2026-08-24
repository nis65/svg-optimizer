import math
from dataclasses import dataclass

from .geometry_abc import Geometry
from .point import Point


@dataclass(frozen=True, slots=True)
class Ellipse(Geometry):
    center: Point
    radiusx: float
    radiusy: float

    def __post_init__(self) -> None:
        if self.radiusx < 0 or self.radiusy < 0:
            raise ValueError(
                f"both radius x ({self.radiusx}) and radius y ({self.radiusy}) must not be negative"
            )

    def points_for_bounding_box(self, count: int) -> set[Point]:
        points = []
        for i in range(count):
            theta = (2 * math.pi * i) / count
            x = self.center.x + self.radiusx * math.cos(theta)
            y = self.center.y + self.radiusy * math.sin(theta)
            points.append(Point(x, y))
        return set(points)
