from dataclasses import dataclass, field

from svgtools.geometry.geometry_abc import Geometry

from .transform import Rotate, Scale, Translate


@dataclass(frozen=True, slots=True)
class Shape:
    geometry: Geometry
    id: str | None = None
    transformations: tuple[Translate | Scale | Rotate, ...] = ()
    unknown_attributes: dict[str, str] = field(default_factory=dict)
