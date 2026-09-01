from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .group import Group
    from .shape import Shape
    from .use import Use


@dataclass(frozen=True, slots=True)
class Defs:
    children: tuple[Defs | Group | Shape | Use, ...]
    id: str | None = None
    unknown_attributes: dict[str, str] = field(default_factory=lambda: dict[str, str]())
