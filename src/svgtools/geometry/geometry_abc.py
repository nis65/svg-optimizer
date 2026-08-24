from abc import ABC, abstractmethod

from .point import Point


class Geometry(ABC):
    @abstractmethod
    def points_for_bounding_box(
        self, number_of_points: int
    ) -> set[Point]: ...  # pragma: no cover
