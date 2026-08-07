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

def points_are_close(set1: set[Point], set2: set[Point]) -> bool:
    if len(set1) != len(set2):
        return False
    remaining = list(set2)
    for point1 in set1:
        for i, point2 in enumerate(remaining):
            if point1.isclose(point2, 1e-8):
                remaining.pop(i)
                break
            return False
    return True

def test_points_are_close():
    ps={Point(0,0),Point(1,1)}
    assert points_are_close(ps, ps)
    qs={Point(1,1),Point(0,0)}
    assert points_are_close(ps, qs)
    rs={Point(1.0000001,1),Point(0,0)}
    assert not points_are_close(ps, rs)
    ss={Point(1.00000001,1),Point(0,0)}
    assert points_are_close(ps, ss)

def test_circle_transformed_bounding_box():
    c = Circle(center=Point(0,0), radius=2)
    assert c.points_for_bounding_box(4) == {
        Point(0,2),
        Point(2,0),
        Point(0,-2),
        Point(-2,0),
    }
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
    assert points_are_close(expected, c.points_for_bounding_box(8))
