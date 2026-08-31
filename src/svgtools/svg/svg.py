from dataclasses import dataclass, field

from .transform import Affine, Rotate, Scale, SkewX, SkewY, Translate


@dataclass(frozen=True, slots=True)
class Svg:
    children: tuple
    id: str | None = None
    xmlnamespace: str | None = None
    width: str | None = None
    height: str | None = None
    viewBox: tuple[float, ...] = ()
    transformations: tuple[
        Affine | Rotate | Scale | SkewX | SkewY | Translate, ...
    ] = ()
    unknown_attributes: dict[str, str] = field(default_factory=dict)
