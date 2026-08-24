from dataclasses import dataclass
from typing import ClassVar

from ..point import Point
from .path_element_abc import PathElement


@dataclass(frozen=True, slots=True)
class QuadraticBezier(PathElement):
    parameter_counts: ClassVar[dict[str, int]] = {
        "Q": 4,
        "q": 4,
        "T": 2,
        "t": 2,
    }

    control1: Point
    end: Point
    representation: str

    def __post_init__(self) -> None:
        if not self.representation in {"q", "Q", "t", "T"}:
            raise ValueError(
                f"QuadraticBezier can only be represented by one of 'qQtT', not {self.representation}"
            )

    @property
    def endpoint(self) -> Point:
        return self.end

    @staticmethod
    def _qb(p0: float, p1: float, p2: float, t: float) -> float:
        return (1 - t) * (1 - t) * p0 + 2 * (1 - t) * t * p1 + t * t * p2

    def _point_at(self, start: Point, t: float) -> Point:
        new_x = self._qb(start.x, self.control1.x, self.end.x, t)
        new_y = self._qb(start.y, self.control1.y, self.end.y, t)
        return Point(x=new_x, y=new_y)

    def points_for_bounding_box(self, start: Point, count: int) -> set[Point]:
        points = []
        for i in range(count + 1):
            t = i / count
            points.append(self._point_at(start, t))
        return set(points)
