import math

from dataclasses import dataclass
from .path_element_abc import PathElement
from ..point import Point

@dataclass(frozen=True, slots=True)
class MoveTo(PathElement):

    x: float
    y: float
    representation: str

    def __post_init__(self) -> None:
        if not (self.representation == 'm' or self.representation == 'M'):
            raise ValueError(
                f"moveto can only be represented by 'm' or 'M', not {self.representation})"
            )

    def points_for_bounding_box(self, count: int) -> set[Point]:
        return {}
