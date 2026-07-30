from dataclasses import dataclass
from svgtools.model.geometry.circle import Circle as GeometryCircle

@dataclass(frozen=True, slots=True)
class Circle:
    geometry: GeometryCircle
