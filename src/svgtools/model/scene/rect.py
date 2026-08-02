from dataclasses import dataclass
from svgtools.model.geometry.rect import Rect as GeometryRect
from .transform import Translate, Scale

@dataclass(frozen=True, slots=True)
class Rect:
    geometry: GeometryRect
    id: str | None = None
    transformations: tuple[Translate | Scale, ...] = ()
