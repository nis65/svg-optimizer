from dataclasses import dataclass
from typing import ClassVar

from ..point import Point
from .path_element_abc import PathElement


@dataclass(frozen=True, slots=True)
class ClosePath(PathElement):
    parameter_counts: ClassVar[dict[str, int]] = {
        "Z": 0,
        "z": 0,
    }

    representation: str

    def __post_init__(self) -> None:
        if not self.representation in {"z", "Z"}:
            raise ValueError(
                f"ClosePath can only be represented by one of 'zZ', not {self.representation}"
            )

    @property
    def endpoint(self) -> Point:
        raise ValueError("ClosePath has no internal endpoint")

    def points_for_bounding_box(    # noqa: PLR6301
        self, start: Point, number_of_points: int
    ) -> set[Point]:
        raise ValueError("ClosePath has no points for bounding box")
