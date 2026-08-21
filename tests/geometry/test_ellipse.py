import pytest
import math
from dataclasses import FrozenInstanceError
from svgtools.geometry.point import Point
from svgtools.geometry.ellipse import Ellipse
from svgtools.geometry.bounding_box import BoundingBox

def test_ellipse_construction():
    e = Ellipse(center=Point(1.5, -2.0), radiusx=23, radiusy=10)

    assert e.center.x == 1.5
    assert e.center.y == -2.0
    assert e.radiusx == 23
    assert e.radiusy == 10

def test_ellipses():
    assert (Ellipse(center=Point(1, 2), radiusx=3, radiusy=2) ==
            Ellipse(center=Point(1, 2), radiusx=3, radiusy=2)
    )

def test_ellipse_is_immutable():
    e = Ellipse(center=Point(1.5, -2.0), radiusx=23, radiusy=22)
    with pytest.raises(FrozenInstanceError):
        e.radiusx = 3

def test_ellipse_radiuses_not_negative ():
    with pytest.raises(ValueError):
        Ellipse(center=Point(1.5, -2.0), radiusx=-0.1, radiusy=1)
    with pytest.raises(ValueError):
        Ellipse(center=Point(1.5, -2.0), radiusx=1, radiusy=-0.1)

def test_ellipse_transformed_bounding_box():
    e = Ellipse(center=Point(0,0), radiusx=2, radiusy=1)
    expected = {
        Point(2,0),
        Point(0,-1),
        Point(-2,0),
        Point(0,1),
    }
    assert Point.points_are_close(expected, e.points_for_bounding_box(4), 1e-8)

    sqrt2 = math.sqrt(2)
    expected = {
        Point(2,0),
        Point(0,-1),
        Point(-2,0),
        Point(0,1),
        Point(sqrt2, sqrt2/2),
        Point(sqrt2, -sqrt2/2),
        Point(-sqrt2, sqrt2/2),
        Point(-sqrt2, -sqrt2/2),
    }
    assert Point.points_are_close(expected, e.points_for_bounding_box(8), 1e-8)
