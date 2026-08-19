import math

from dataclasses import dataclass
from .path_element_abc import PathElement
from ..point import Point

@dataclass(frozen=True, slots=True)
class LineTo(PathElement):

    parameter_counts = {
            "L": 2,
            "l": 2,
            "H": 1,
            "h": 1,
            "V": 1,
            "v": 1,
    }

    target: Point
    representation: str

    def __post_init__(self) -> None:
        if not (self.representation == 'l' or self.representation == 'L'
             or self.representation == 'h' or self.representation == 'H'
             or self.representation == 'v' or self.representation == 'V'
            ):
            raise ValueError(
                f"LineTo can only be represented by one of 'lLhHvV', not {self.representation}"
            )

    @property
    def endpoint(self) -> Point:
        return self.target

    def points_for_bounding_box(self, start: Point, count: int) -> set[Point]:
        return { start, self.endpoint, }
