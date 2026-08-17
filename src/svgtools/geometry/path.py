from dataclasses import dataclass
from .geometry_abc import Geometry
from .point import Point

@dataclass(frozen=True, slots=True)
class Path(Geometry):
    children: tuple = ()

    def points_for_bounding_box(self, count: int) -> set[Point]:
        # todo: Loop over all children and merge all points into one set
        # for child in children
        pass
