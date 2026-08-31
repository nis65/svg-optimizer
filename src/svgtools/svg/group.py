from __future__ import annotations

from dataclasses import dataclass, field

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .defs import Defs 
    from .shape import Shape 
    from .use import Use
from .transform import Affine, Rotate, Scale, SkewX, SkewY, Translate



@dataclass(frozen=True, slots=True)
class Group:
    children: tuple[Defs | Group | Shape | Use]
    id: str | None = None
    href: str | None = None
    transformations: tuple[
        Affine | Rotate | Scale | SkewX | SkewY | Translate, ...
    ] = ()
    unknown_attributes: dict[str, str] = field(default_factory=lambda: dict[str, str]())
