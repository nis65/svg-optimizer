from dataclasses import dataclass, field
from svgtools.model.geometry.circle import Circle as GeometryCircle
from .transform import Translate, Scale, Rotate

@dataclass(frozen=True, slots=True)
class Circle:
    geometry: GeometryCircle
    id: str | None = None
    transformations: tuple[Translate | Scale | Rotate, ...] = ()
    unknown_attributes: dict[str, str] = field(default_factory=dict)
