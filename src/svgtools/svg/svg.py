from dataclasses import dataclass, field

from .defs import Defs
from .group import Group
from .shape import Shape
from .transform import Affine, Rotate, Scale, SkewX, SkewY, Translate
from .use import Use


@dataclass(frozen=True, slots=True)
class Svg:
    children: tuple[Defs | Group | Shape | Use, ...]
    id: str | None = None
    xmlnamespace: str | None = None
    width: str | None = None
    height: str | None = None
    viewBox: tuple[float, ...] = ()
    transformations: tuple[
        Affine | Rotate | Scale | SkewX | SkewY | Translate, ...
    ] = ()
    unknown_attributes: dict[str, str] = field(default_factory=lambda: dict[str, str]())
