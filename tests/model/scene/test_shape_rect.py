
import pytest
from dataclasses import FrozenInstanceError
from svgtools.model.geometry.point import Point as GeometryPoint
from svgtools.model.geometry.rect import Rect as GeometryRect
from svgtools.model.scene.transform import Translate, Scale, Rotate
from svgtools.model.scene.shape import Shape

def test_rect_construction():
    r = Shape(id="rect",
            geometry=GeometryRect(top_left=GeometryPoint(1.5, -2.0),
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
    r = Shape(geometry=GeometryRect(top_left=GeometryPoint(1.5, -2.0), width=2, height=3))
    assert r.geometry.top_left.x == 1.5
    assert r.geometry.top_left.y == -2.0
    assert r.geometry.width == 2
    assert r.geometry.height == 3
    assert r.id is None
    assert r.transformations == ()

def test_rects_are_equal():
    assert ( Shape(id="rect",
                  geometry=GeometryRect(top_left=GeometryPoint(1.5, -2.0), width=2, height=3),
                  transformations=Translate ( 2, 3)
                  ) ==
             Shape(id="rect",
                  geometry=GeometryRect(top_left=GeometryPoint(1.5, -2.0), width=2, height=3),
                  transformations=Translate ( 2, 3)
                  )
           )

def test_rect_is_immutable():
    r = Shape(id="rect", geometry=GeometryRect(top_left=GeometryPoint(1.5, -2.0), width=2, height=3))
    with pytest.raises(FrozenInstanceError):
        r.geometry.top_left.x = 2
