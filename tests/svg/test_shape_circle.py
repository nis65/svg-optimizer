from dataclasses import FrozenInstanceError

import pytest

from svgtools.geometry.circle import Circle
from svgtools.geometry.point import Point
from svgtools.svg.shape import Shape
from svgtools.svg.transform import Rotate, Scale, Translate


def test_circle_construction():
    c = Shape(
        id="circle",
        geometry=Circle(center=Point(1.5, -2.0), radius=2),
        transformations=Translate(2, 3),
    )
    assert c.geometry.center.x == 1.5
    assert c.geometry.center.y == -2.0
    assert c.geometry.radius == 2
    assert c.id == "circle"
    assert c.transformations == Translate(2, 3)


def test_minimal_circle_construction():
    c = Shape(geometry=Circle(center=Point(1.5, -2.0), radius=2))
    assert c.geometry.center.x == 1.5
    assert c.geometry.center.y == -2.0
    assert c.geometry.radius == 2
    assert c.id is None
    assert c.transformations == ()


def test_circles_are_equal():
    assert Shape(
        id="circle",
        geometry=Circle(center=Point(1.5, -2.0), radius=2),
        transformations=(Scale(3, 3), Rotate(20, 1, 1)),
    ) == Shape(
        id="circle",
        geometry=Circle(center=Point(1.5, -2.0), radius=2),
        transformations=(Scale(3, 3), Rotate(20, 1, 1)),
    )


def test_circle_is_immutable():
    c = Shape(id="circle", geometry=Circle(center=Point(1.5, -2.0), radius=2))
    with pytest.raises(FrozenInstanceError):
        c.geometry.radius = 3
