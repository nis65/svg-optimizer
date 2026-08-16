import pytest
from dataclasses import FrozenInstanceError
from svgtools.geometry.point import Point

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

def test_points_are_close():
    # test abs_tol near 0
    p = Point(0,0)
    q = Point(0.000000001,
             -0.000000001)
    assert not p.isclose(q,1e-10)
    assert p.isclose(q,1e-9)
    # test rel_tol off 0
    p = Point(1000, 1)
    q = Point(1000.00001, 1)
    r = Point(1000.000001, 1)
    assert not p.isclose(q,1e-20)
    assert p.isclose(r,1e-20)
