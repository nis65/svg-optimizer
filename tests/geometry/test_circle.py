import math
from dataclasses import FrozenInstanceError

import pytest

from svgtools.geometry.circle import Circle
from svgtools.geometry.point import Point


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

def test_points_are_close():
    ps={Point(0,0),Point(1,1)}
    assert Point.points_are_close(ps, ps, 1e-8)
    qs={Point(1,1),Point(0,0)}
    assert Point.points_are_close(ps, qs, 1e-8)
    rs={Point(1.0000001,1),Point(0,0)}
    assert not Point.points_are_close(ps, rs, 1e-8)
    ss={Point(1.00000001,1),Point(0,0)}
    assert Point.points_are_close(ps, ss, 1e-8)

def test_circle_transformed_bounding_box():
    c = Circle(center=Point(0,0), radius=2)
    expected = {
        Point(0,2),
        Point(2,0),
        Point(0,-2),
        Point(-2,0),
    }
    assert Point.points_are_close(expected, c.points_for_bounding_box(4), 1e-8)
    sqrt2 = math.sqrt(2)
    expected = {
        Point(0,2),
        Point(2,0),
        Point(0,-2),
        Point(-2,0),
        Point(sqrt2, sqrt2),
        Point(sqrt2, -sqrt2),
        Point(-sqrt2, sqrt2),
        Point(-sqrt2, -sqrt2),
    }
    assert Point.points_are_close(expected, c.points_for_bounding_box(8), 1e-8)
