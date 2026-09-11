from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from .transform import SvgTransformations

if TYPE_CHECKING:
    from . import SvgChildren


@dataclass(frozen=True, slots=True)
class Use:
    href: str
    x: float
    y: float
    children: tuple[SvgChildren, ...]
    id: str | None = None
    transformations: tuple[SvgTransformations, ...] = ()
    preserved_attributes: dict[str, str] = field(
        default_factory=lambda: dict[str, str]()
    )
