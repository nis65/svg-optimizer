from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from svgtools.geometry.geometry_abc import Geometry

from .transform import SvgTransformations

if TYPE_CHECKING:
    from . import SvgChildren


@dataclass(frozen=True, slots=True)
class Shape:
    children: tuple[SvgChildren, ...]
    geometry: Geometry
    id: str | None = None
    transformations: tuple[SvgTransformations, ...] = ()
    preserved_attributes: dict[str, str] = field(
        default_factory=lambda: dict[str, str]()
    )
