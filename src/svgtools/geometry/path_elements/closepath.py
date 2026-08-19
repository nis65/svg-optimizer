import math

from dataclasses import dataclass
from .path_element_abc import PathElement
from ..point import Point

@dataclass(frozen=True, slots=True)
class ClosePath(PathElement):

    representation: str

    def __post_init__(self) -> None:
        if not (self.representation == 'z' or self.representation == 'Z'):
            raise ValueError(
                f"ClosePath can only be represented by one of 'zZ', not {self.representation}"
            )

    @property
    def endpoint(self) -> Point:
        raise ValueError("ClosePath has no internal endpoint")

    def points_for_bounding_box(self, start: Point, number_of_points: int) -> set[Point]:
        raise ValueError("ClosePath has no points for bounding box")
