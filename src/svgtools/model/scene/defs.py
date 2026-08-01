from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Defs:
    children: tuple
    id: str | None = None
