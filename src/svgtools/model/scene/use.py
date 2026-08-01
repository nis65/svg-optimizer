from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Use:
    href: str
    id: str | None = None
