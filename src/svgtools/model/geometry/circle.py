import math

from dataclasses import dataclass
from .point import Point
from .bounding_box import BoundingBox

@dataclass(frozen=True, slots=True)
class Circle:
    center: Point
    radius: float

    def __post_init__(self) -> None:
        if self.radius < 0:
            raise ValueError(
                f"radius ({self.radius}) must not be negative"
            )

    def points_for_bounding_box(self, count: int) -> set[Point]:
        points = []
        for i in range(count):
            theta = (2 * math.pi * i ) / count
            x = self.center.x + self.radius * math.cos(theta)
            y = self.center.y + self.radius * math.sin(theta)
            points.append(Point(x,y))
        return set(points)
