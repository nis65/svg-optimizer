
import pytest
from dataclasses import FrozenInstanceError
from svgtools.geometry.point import Point
from svgtools.geometry.rect import Rect
from svgtools.svg.transform import Translate, Scale, Rotate
from svgtools.svg.shape import Shape

def test_rect_construction():
    r = Shape(id="rect",
            geometry=Rect(top_left=Point(1.5, -2.0),
                width=2, height=3
                ),
                transformations=( Translate ( 2, 3), Rotate (30,1,2))
             )
    assert r.id == "rect"
    assert r.geometry.top_left.x == 1.5
    assert r.geometry.top_left.y == -2.0
    assert r.geometry.width == 2
    assert r.geometry.height == 3
    assert r.transformations == (Translate ( 2, 3), Rotate(30,1,2))

def test_minimal_rect_construction():
    r = Shape(geometry=Rect(top_left=Point(1.5, -2.0), width=2, height=3))
    assert r.geometry.top_left.x == 1.5
    assert r.geometry.top_left.y == -2.0
    assert r.geometry.width == 2
    assert r.geometry.height == 3
    assert r.id is None
    assert r.transformations == ()

def test_rects_are_equal():
    assert ( Shape(id="rect",
                  geometry=Rect(top_left=Point(1.5, -2.0), width=2, height=3),
                  transformations=Translate ( 2, 3)
                  ) ==
             Shape(id="rect",
                  geometry=Rect(top_left=Point(1.5, -2.0), width=2, height=3),
                  transformations=Translate ( 2, 3)
                  )
           )

def test_rect_is_immutable():
    r = Shape(id="rect", geometry=Rect(top_left=Point(1.5, -2.0), width=2, height=3))
    with pytest.raises(FrozenInstanceError):
        r.geometry.top_left.x = 2
