from dataclasses import dataclass, field

from svgtools.geometry.geometry_abc import Geometry

from .transform import SvgTransformations


@dataclass(frozen=True, slots=True)
class Shape:
    geometry: Geometry
    id: str | None = None
    transformations: tuple[SvgTransformations, ...] = ()
    preserved_attributes: dict[str, str] = field(
        default_factory=lambda: dict[str, str]()
    )
