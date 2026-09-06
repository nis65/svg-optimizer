from dataclasses import dataclass, field

from .transform import SvgTransformations


@dataclass(frozen=True, slots=True)
class Use:
    href: str
    x: float
    y: float
    id: str | None = None
    transformations: tuple[SvgTransformations, ...] = ()
    unknown_attributes: dict[str, str] = field(default_factory=lambda: dict[str, str]())
