from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from . import SvgNestables


@dataclass(frozen=True, slots=True)
class Defs:
    children: tuple[SvgNestables, ...]
    id: str | None = None
    preserved_attributes: dict[str, str] = field(
        default_factory=lambda: dict[str, str]()
    )
