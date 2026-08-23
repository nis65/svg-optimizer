from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class Defs:
    children: tuple
    id: str | None = None
    unknown_attributes: dict[str, str] = field(default_factory=dict)
