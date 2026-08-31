from dataclasses import dataclass, field

from .transform import Affine, Rotate, Scale, SkewX, SkewY, Translate


@dataclass(frozen=True, slots=True)
class Group:
    children: tuple
    id: str | None = None
    href: str | None = None
    transformations: tuple[
        Affine | Rotate | Scale | SkewX | SkewY | Translate, ...
    ] = ()
    unknown_attributes: dict[str, str] = field(default_factory=dict)
