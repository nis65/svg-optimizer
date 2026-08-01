
import pytest
from dataclasses import FrozenInstanceError
from svgtools.model.geometry.point import Point as GeometryPoint
from svgtools.model.geometry.rect import Rect as GeometryRect
from svgtools.model.scene.rect import Rect

def test_rect_construction():
    r = Rect(id="rect", geometry=GeometryRect(top_left=GeometryPoint(1.5, -2.0), width=2, height=3))
    assert r.id == "rect"
    assert r.geometry.top_left.x == 1.5
    assert r.geometry.top_left.y == -2.0
    assert r.geometry.width == 2
    assert r.geometry.height == 3

def test_minimal_rect_construction():
    r = Rect(geometry=GeometryRect(top_left=GeometryPoint(1.5, -2.0), width=2, height=3))
    assert r.geometry.top_left.x == 1.5
    assert r.geometry.top_left.y == -2.0
    assert r.geometry.width == 2
    assert r.geometry.height == 3

def test_rects_are_equal():
    assert ( Rect(id="rect", geometry=GeometryRect(top_left=GeometryPoint(1.5, -2.0), width=2, height=3)) ==
             Rect(id="rect", geometry=GeometryRect(top_left=GeometryPoint(1.5, -2.0), width=2, height=3))
    )

def test_rect_is_immutable():
    r = Rect(id="rect", geometry=GeometryRect(top_left=GeometryPoint(1.5, -2.0), width=2, height=3))
    with pytest.raises(FrozenInstanceError):
        r.geometry.top_left.x = 2
