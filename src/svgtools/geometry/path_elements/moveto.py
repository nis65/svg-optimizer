import math

from dataclasses import dataclass
from .path_element_abc import PathElement
from ..point import Point

@dataclass(frozen=True, slots=True)
class MoveTo(PathElement):

    target: Point
    representation: str

    def __post_init__(self) -> None:
        if not (self.representation == 'm' or self.representation == 'M'):
            raise ValueError(
                f"MoveTo can only be represented by one of 'mM', not {self.representation}"
            )

    @property
    def endpoint(self) -> Point:
        return self.target

    def points_for_bounding_box(start: Point, number_of_points: int) -> set[Point]:
        raise ValueError("MoveTo has no points for bounding box")
