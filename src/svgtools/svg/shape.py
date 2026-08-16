from dataclasses import dataclass, field
from .transform import Translate, Scale, Rotate

from svgtools.model.geometry.geometry_abc import Geometry

@dataclass(frozen=True, slots=True)
class Shape: 
    geometry: Geometry
    id: str | None = None
    transformations: tuple[Translate | Scale | Rotate, ...] = ()
    unknown_attributes: dict[str, str] = field(default_factory=dict)
