
import pytest
from dataclasses import FrozenInstanceError
from svgtools.model.geometry.point import Point as GeometryPoint
from svgtools.model.geometry.circle import Circle as GeometryCircle
from svgtools.model.scene.circle import Circle

def test_circle_construction():
    c = Circle(geometry=GeometryCircle(center=GeometryPoint(1.5, -2.0), radius=2))
    assert c.geometry.center.x == 1.5
    assert c.geometry.center.y == -2.0
    assert c.geometry.radius == 2

def test_circles_are_equal():
    assert (Circle(geometry=GeometryCircle(center=GeometryPoint(1.5, -2.0), radius=2)) ==
            Circle(geometry=GeometryCircle(center=GeometryPoint(1.5, -2.0), radius=2))
    )

def test_circle_is_immutable():
    c = Circle(geometry=GeometryCircle(center=GeometryPoint(1.5, -2.0), radius=2))
    with pytest.raises(FrozenInstanceError):
       c.geometry.radius = 3
