from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Group:
    children: tuple
    id: str | None = None
