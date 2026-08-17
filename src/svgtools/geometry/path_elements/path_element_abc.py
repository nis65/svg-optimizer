from abc import ABC, abstractmethod

from ..geometry_abc import Geometry

class PathElement(Geometry, ABC):
    representation: str
