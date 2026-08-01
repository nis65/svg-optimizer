import pytest
from dataclasses import FrozenInstanceError
from svgtools.model.geometry.point import Point
from svgtools.model.geometry.circle import Circle
from svgtools.model.geometry.bounding_box import BoundingBox

def test_circle_construction():
    c = Circle(center=Point(1.5, -2.0), radius=23)

    assert c.center.x == 1.5
    assert c.center.y == -2.0
    assert c.radius == 23

def test_circles_are_equal():
    assert (Circle(center=Point(1, 2), radius=3) ==
            Circle(center=Point(1, 2), radius=3)
    )

def test_circle_is_immutable():
    c = Circle(center=Point(1.5, -2.0), radius=23)

    with pytest.raises(FrozenInstanceError):
        c.radius = 3

def test_circle_radius_not_negative ():
    with pytest.raises(ValueError):
        Circle(center=Point(1.5, -2.0), radius=-0.1)

def test_circle_bounding_box():
    c = Circle(center=Point(2, 2), radius=1)
    assert c.bounding_box() == BoundingBox (
        min=Point(1, 1),
        max=Point(3, 3)
    )

