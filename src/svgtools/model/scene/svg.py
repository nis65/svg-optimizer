from dataclasses import dataclass, field
from .transform import Translate, Scale

@dataclass(frozen=True, slots=True)
class Svg:
    children: tuple
    id: str | None = None
    xmlnamespace: str | None = None
    width: str | None = None
    height: str | None = None
    viewBox: tuple[float, ...] = ()
    transformations: tuple[Translate | Scale, ...] = ()
    unknown_attributes: dict[str, str] = field(default_factory=dict)
