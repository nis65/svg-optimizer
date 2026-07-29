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
