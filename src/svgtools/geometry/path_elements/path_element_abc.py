from abc import ABC, abstractmethod
from typing import ClassVar

from ..point import Point


class PathElement(ABC):
    # this is not enforced by python itself, would need "mypy" or "pyright" to enforce
    parameter_counts: ClassVar[dict[str, int]]
    representation: str

    @property
    @abstractmethod
    def endpoint(self) -> Point: ...  # pragma: no cover

    @abstractmethod
    def points_for_bounding_box(
        self, start: Point, number_of_points: int
    ) -> set[Point]: ...  # pragma: no cover
