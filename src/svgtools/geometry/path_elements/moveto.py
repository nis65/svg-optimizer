from dataclasses import dataclass
from typing import ClassVar

from ..point import Point
from .path_element_abc import PathElement


@dataclass(frozen=True, slots=True)
class MoveTo(PathElement):

    parameter_counts: ClassVar[dict[str, int]] = {
            "M": 2,
            "m": 2,
    }

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
