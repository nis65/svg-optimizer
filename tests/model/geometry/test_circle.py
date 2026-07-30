import pytest
from dataclasses import FrozenInstanceError
from svgtools.model.geometry.point import Point
from svgtools.model.geometry.circle import Circle

def test_circle_construction():
    c = Circle(Point(1.5, -2.0), 23)

    assert c.center.x == 1.5
    assert c.center.y == -2.0
    assert c.radius == 23

def test_circles_are_equal():
    assert Circle(Point(1, 2), 3) == Circle(Point(1, 2), 3)

def test_circle_is_immutable():
    c = Circle(Point(1.5, -2.0), 23)

    with pytest.raises(FrozenInstanceError):
        c.radius = 3

def test_circle_radius_not_negative ():
    with pytest.raises(ValueError):
        Circle(Point(1.5, -2.0), -0.1)
