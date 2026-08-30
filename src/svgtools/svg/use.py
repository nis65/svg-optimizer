from dataclasses import dataclass, field

from .transform import Rotate, Scale, Translate


@dataclass(frozen=True, slots=True)
class Use:
    href: str
    x: str
    y: str
    id: str | None = None
    transformations: tuple[Translate | Scale | Rotate, ...] = ()
    unknown_attributes: dict[str, str] = field(default_factory=dict)
