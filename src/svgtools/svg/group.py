from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import SvgNestables

from .transform import SvgTransformations


@dataclass(frozen=True, slots=True)
class Group:
    children: tuple[SvgNestables, ...]
    id: str | None = None
    href: str | None = None
    transformations: tuple[SvgTransformations, ...] = ()
    preserved_attributes: dict[str, str] = field(
        default_factory=lambda: dict[str, str]()
    )
