from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Svg:
    children: tuple
    id: str | None = None
