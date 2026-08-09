from dataclasses import dataclass
from .point import Point
from .bounding_box import BoundingBox

@dataclass(frozen=True, slots=True)
class Rect:
    top_left: Point
    width: float
    height: float

    def __post_init__(self) -> None:
        if self.width < 0:
            raise ValueError(
                f"width ({self.width}) must not be negative"
            )
        if self.height < 0:
            raise ValueError(
                f"height ({self.height}) must not be negative"
            )

    def bounding_box(self):
        return BoundingBox(
            min = self.top_left,
            max = Point(self.top_left.x + self.width,
                        self.top_left.y + self.height)
        )

    def points_for_bounding_box(self, count: int) -> set[Point]:
        # count is ignored, as 4 points fully define the bounding box
        return {
            self.top_left,
            Point(
                self.top_left.x,
                self.top_left.y + self.height
            ),
            Point(
                self.top_left.x + self.width,
                self.top_left.y + self.height
            ),
            Point(
                self.top_left.x + self.width,
                self.top_left.y
            ),
        }
