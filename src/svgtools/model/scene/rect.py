from dataclasses import dataclass, field
from svgtools.model.geometry.rect import Rect as GeometryRect
from .transform import Translate, Scale

@dataclass(frozen=True, slots=True)
class Rect:
    geometry: GeometryRect
    id: str | None = None
    transformations: tuple[Translate | Scale, ...] = ()
    unknown_attributes: dict[str, str] = field(default_factory=dict)
