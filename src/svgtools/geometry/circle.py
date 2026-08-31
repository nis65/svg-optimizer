import math
from dataclasses import dataclass

from .geometry_abc import Geometry
from .point import Point


@dataclass(frozen=True, slots=True)
class Circle(Geometry):
    center: Point
    radius: float

    def __post_init__(self) -> None:
        if self.radius < 0:
            raise ValueError(f"radius ({self.radius}) must not be negative")

    def points_for_bounding_box(self, number_of_points: int) -> set[Point]:
        points = []
        for i in range(number_of_points):
            theta = (2 * math.pi * i) / number_of_points
            x = self.center.x + self.radius * math.cos(theta)
            y = self.center.y + self.radius * math.sin(theta)
            points.append(Point(x, y))
        return set(points)
