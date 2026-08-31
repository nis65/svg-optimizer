from dataclasses import dataclass
from typing import ClassVar

from ..point import Point
from .path_element_abc import PathElement


@dataclass(frozen=True, slots=True)
class CubicBezier(PathElement):
    parameter_counts: ClassVar[dict[str, int]] = {
        "C": 6,
        "c": 6,
        "S": 4,
        "s": 4,
    }

    control1: Point
    control2: Point
    end: Point
    representation: str

    def __post_init__(self) -> None:
        if not self.representation in {"c", "C", "s", "S"}:
            raise ValueError(
                f"CubicBezier can only be represented by one of 'cCsS', not {self.representation}"
            )

    @property
    def endpoint(self) -> Point:
        return self.end

    @staticmethod
    def _qb(p0: float, p1: float, p2: float, p3: float, t: float) -> float:
        return (
            (1 - t) * (1 - t) * (1 - t) * p0
            + 3 * (1 - t) * (1 - t) * t * p1
            + 3 * (1 - t) * t * t * p2
            + t * t * t * p3
        )

    def _point_at(self, start: Point, t: float) -> Point:
        new_x = self._qb(start.x, self.control1.x, self.control2.x, self.end.x, t)
        new_y = self._qb(start.y, self.control1.y, self.control2.y, self.end.y, t)
        return Point(x=new_x, y=new_y)

    def points_for_bounding_box(
        self, start: Point, number_of_points: int
    ) -> set[Point]:
        points: list[Point] = []
        for i in range(number_of_points + 1):
            t = i / number_of_points
            points.append(self._point_at(start, t))
        return set(points)
