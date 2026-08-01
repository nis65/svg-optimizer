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

    def bounding_box(self):
        return BoundingBox(
            min = Point(self.center.x - self.radius,
                        self.center.y - self.radius),
            max = Point(self.center.x + self.radius,
                        self.center.y + self.radius)
        )
