from dataclasses import dataclass
from .point import Point

@dataclass(frozen=True, slots=True)
class BoundingBox:
    min: Point
    max: Point

    def __post_init__(self) -> None:
        if self.min.x > self.max.x:
            raise ValueError(
                f"min.x ({self.min.x}) must not be greater than max.x ({self.max.x})"
            )

        if self.min.y > self.max.y:
            raise ValueError(
                f"min.y ({self.min.y}) must not be greater than max.y ({self.max.y})"
            )

    def include(self, point: Point) -> "BoundingBox":
        return BoundingBox(
            min=Point(min(self.min.x, point.x), min(self.min.y, point.y)),
            max=Point(max(self.max.x, point.x), max(self.max.y, point.y))
        )

    def union(self, other) -> "BoundingBox":
        return BoundingBox(
            min=Point(min(self.min.x, other.min.x), min(self.min.y, other.min.y)),
            max=Point(max(self.max.x, other.max.x), max(self.max.y, other.max.y))
        )

    def __add__(self, other) -> "BoundingBox":
        return self.union(other)
