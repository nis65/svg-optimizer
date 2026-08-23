from dataclasses import dataclass

from .svg import Svg


@dataclass(frozen=True, slots=True)
class Document:
    svg: Svg

