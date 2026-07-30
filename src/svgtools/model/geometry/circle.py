from dataclasses import dataclass
from .point import Point

@dataclass(frozen=True, slots=True)
class Circle:
    center: Point
    radius: float

    def __post_init__(self) -> None:
        if self.radius < 0:
            raise ValueError(
                f"radius ({self.radius}) must not be negative"
            )
