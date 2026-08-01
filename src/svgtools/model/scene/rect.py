from dataclasses import dataclass
from svgtools.model.geometry.rect import Rect as GeometryRect

@dataclass(frozen=True, slots=True)
class Rect:
    geometry: GeometryRect
    id: str | None = None
