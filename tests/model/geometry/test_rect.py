import pytest
from dataclasses import FrozenInstanceError
from svgtools.model.geometry.point import Point
from svgtools.model.geometry.rect import Rect
from svgtools.model.geometry.bounding_box import BoundingBox

def test_rect_construction():
    r = Rect(top_left=Point(1.5, -2.0), width=2, height=3)

    assert r.top_left.x == 1.5
    assert r.top_left.y == -2.0
    assert r.width == 2
    assert r.height == 3

def test_rects_are_equal():
    assert ( Rect(top_left=Point(1, 2), width=3, height=4) ==
             Rect(top_left=Point(1, 2), width=3, height=4)
    )

def test_rect_is_immutable():
    r = Rect(top_left=Point(1, 2), width=3, height=4)

    with pytest.raises(FrozenInstanceError):
        r.width = 5

def test_rect_width_and_height_not_negative ():
    with pytest.raises(ValueError):
        Rect(top_left=Point(1.5, -2.0), width=-0.1, height=2)
    with pytest.raises(ValueError):
        Rect(top_left=Point(1.5, -2.0), width=2, height=-0.1)

def test_rect_bounding_box():
    r = Rect(top_left=Point(1, 1), width=2, height=3)
    assert r.bounding_box() == BoundingBox (
        min=Point(1, 1),
        max=Point(3, 4)
    )

def test_rect_transformed_bounding_box():
    r = Rect(top_left=Point(1, 1), width=2, height=3)
    assert r.points_for_bounding_box(100) == {
        Point(1,1),
        Point(1,4),
        Point(3,4),
        Point(3,1),
        }
