from abc import ABC, abstractmethod
from ..point import Point

class PathElement(ABC):
    representation: str

    @property
    @abstractmethod
    def endpoint(self) -> Point:
        ...

    @abstractmethod
    def points_for_bounding_box(self, start: Point, number_of_points: int) -> set[Point]:
        ...
