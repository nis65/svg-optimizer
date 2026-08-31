from dataclasses import dataclass, field

from .transform import Affine, Rotate, Scale, SkewX, SkewY, Translate


@dataclass(frozen=True, slots=True)
class Use:
    href: str
    x: float
    y: float
    id: str | None = None
    transformations: tuple[
        Affine | Rotate | Scale | SkewX | SkewY | Translate, ...
    ] = ()
    unknown_attributes: dict[str, str] = field(default_factory=lambda: dict[str, str]())
