from dataclasses import dataclass
from .transform import Translate, Scale

@dataclass(frozen=True, slots=True)
class Use:
    href: str
    id: str | None = None
    transformations: tuple[Translate | Scale, ...] = ()
