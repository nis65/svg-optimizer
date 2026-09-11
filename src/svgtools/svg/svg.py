from dataclasses import dataclass, field

from . import SvgChildren
from .transform import SvgTransformations


@dataclass(frozen=True, slots=True)
class Svg:
    children: tuple[SvgChildren, ...]
    id: str | None = None
    xmlnamespace: str | None = None
    width: str | None = None
    height: str | None = None
    viewBox: tuple[float, ...] = ()
    transformations: tuple[SvgTransformations, ...] = ()
    preserved_attributes: dict[str, str] = field(
        default_factory=lambda: dict[str, str]()
    )
