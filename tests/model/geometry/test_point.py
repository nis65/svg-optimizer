import pytest
from dataclasses import FrozenInstanceError
from svgtools.model.geometry.point import Point

def test_point_construction():
    p = Point(1.5, -2.0)

    assert p.x == 1.5
    assert p.y == -2.0

def test_points_are_equal():
    assert Point(1, 2) == Point(1, 2)

def test_points_are_immutable():
    p = Point(1, 2)

    with pytest.raises(FrozenInstanceError):
        p.x = 3
