from dataclasses import dataclass

@dataclass(frozen=True, slots=True)
class Document:
    elements: tuple[int|str, ...]

