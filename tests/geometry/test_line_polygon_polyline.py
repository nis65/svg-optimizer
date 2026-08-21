import pytest
from dataclasses import FrozenInstanceError
from svgtools.geometry.point import Point
from svgtools.geometry.line import Line
from svgtools.geometry.polyline import Polyline
from svgtools.geometry.polygon import Polygon
from svgtools.geometry.bounding_box import BoundingBox

def test_line_construction():
    l = Line(start=Point(1, 2), end=Point(5, 6))

    assert l.start.x == 1
    assert l.start.y == 2
    assert l.end.x == 5
    assert l.end.y == 6

def test_line_is_immutable():
    l = Line(start=Point(1, 2), end=Point(5, 6))
    with pytest.raises(FrozenInstanceError):
        l.start.x = 100

def test_line_points_for_bounding_box():
    l = Line(start=Point(1, 2), end=Point(5, 6))
    assert l.points_for_bounding_box(100) == {
        Point(1,2),
        Point(5,6),
    }

def test_polyline_construction():
    p = Polyline(
            children = (
                Point(1, 2),
                Point(5, 6),
                Point(1,-1),
            )
        )
    assert p.children[0].x == 1
    assert p.children[0].y == 2
    assert p.children[1].x == 5
    assert p.children[1].y == 6
    assert p.children[2].x == 1
    assert p.children[2].y == -1

def test_polyline_immutable():
    p = Polyline(
            children = (
                Point(1, 2),
                Point(5, 6),
            )
        )
    with pytest.raises(FrozenInstanceError):
        p.children[1].x = 42

def test_polyline_points_for_bounding_box():
    p = Polyline(
            children = (
                Point(1, 2),
                Point(5, 6),
                Point(1,-1),
            )
        )
    assert p.points_for_bounding_box(100) == {
        Point(1, 2),
        Point(5, 6),
        Point(1,-1),
    }

def test_polygon_construction():
    p = Polygon(
            children = (
                Point(1, 2),
                Point(5, 6),
                Point(1,-1),
            )
        )
    assert p.children[0].x == 1
    assert p.children[0].y == 2
    assert p.children[1].x == 5
    assert p.children[1].y == 6
    assert p.children[2].x == 1
    assert p.children[2].y == -1

def test_polygon_immutable():
    p = Polygon(
            children = (
                Point(1, 2),
                Point(5, 6),
            )
        )
    with pytest.raises(FrozenInstanceError):
        p.children[1].x = 42

def test_polygon_points_for_bounding_box():
    p = Polygon(
            children = (
                Point(1, 2),
                Point(5, 6),
                Point(1,-1),
            )
        )
    assert p.points_for_bounding_box(100) == {
        Point(1, 2),
        Point(5, 6),
        Point(1,-1),
    }
