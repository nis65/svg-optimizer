import pytest

from svgtools.geometry.point import Point
from svgtools.geometry.path import Path
from svgtools.geometry.path_elements.moveto import MoveTo
from svgtools.geometry.path_elements.lineto import LineTo
from svgtools.geometry.path_elements.closepath import ClosePath
from svgtools.geometry.path_elements.quadraticbezier import QuadraticBezier

def test_path_construction():
    p = Path(children=())
    assert len(p.children) == 0

def test_path_with_moveto():
    p = Path(
            children = (
                MoveTo(
                    target = Point(
                        x = 1,
                        y = 2,
                    ),
                    representation='m',
                ),
            )
        )
    assert p.children[0].target.x == 1
    assert p.children[0].target.y == 2
    assert p.children[0].representation == 'm'

def test_path_with_moveto_invalid():
    with pytest.raises(ValueError, match="MoveTo can only be represented"):
        p = Path(
                children = (
                    MoveTo(
                        target = Point(
                            x = 1,
                            y = 2,
                        ),
                        representation='f',
                    ),
                )
            )

def test_path_with_lineto():
    p = Path(
            children = (
                LineTo(
                    target = Point(
                        x = 1,
                        y = 2,
                    ),
                    representation='L',
                ),
            )
        )
    assert type(p.children[0]) == LineTo
    assert p.children[0].target.x == 1
    assert p.children[0].target.y == 2
    assert p.children[0].representation == 'L'

def test_path_with_simple_bounding_box():
    p = Path(
            children = (
                MoveTo(
                    target = Point(
                        x = 4,
                        y = 4,
                    ),
                    representation='m',
                ),
                LineTo(
                    target = Point(
                        x = 1,
                        y = 2,
                    ),
                    representation='L',
                ),
                ClosePath(
                    representation='Z',
                )
            )
        )
    assert p.points_for_bounding_box(100) == {
        Point(x=4, y=4,),
        Point(x=1, y=2,),
    }

def test_path_with_quadratic_bezier():
    p = Path(
            children = (
                QuadraticBezier(
                    control1 = Point(
                        x = 2,
                        y = 2,
                    ),
                    end = Point(
                        x = 3,
                        y = 3,
                    ),
                    representation='Q',
                ),
            )
        )
    assert type(p.children[0]) == QuadraticBezier
    assert p.children[0].control1.x == 2
    assert p.children[0].control1.y == 2
    assert p.children[0].end.x == 3
    assert p.children[0].end.y == 3
    assert p.children[0].representation == 'Q'

def test_path_with_bounding_box_for_quadratic_bezier_line():
    p = Path(
            children = (
                MoveTo(
                    target = Point(
                        x = 1,
                        y = 1,
                    ),
                    representation='M',
                ),
                QuadraticBezier(
                    control1 = Point(
                        x = 2,
                        y = 2,
                    ),
                    end = Point(
                        x = 3,
                        y = 3,
                    ),
                    representation='Q',
                ),
            )
        )
    assert p.points_for_bounding_box(2) == {
        Point(x=1, y=1,),
        Point(x=2, y=2,),
        Point(x=3, y=3,),
    }

def test_path_with_bounding_box_for_quadratic_bezier_curve():
    p = Path(
            children = (
                MoveTo(
                    target = Point(
                        x = 1,
                        y = 1,
                    ),
                    representation='M',
                ),
                QuadraticBezier(
                    control1 = Point(
                        x = 2,
                        y = 2,
                    ),
                    end = Point(
                        x = 3,
                        y = 1,
                    ),
                    representation='Q',
                ),
            )
        )
    assert p.points_for_bounding_box(2) == {
        Point(x=1, y=1,),
        Point(x=2, y=1.5,),
        Point(x=3, y=1,),
    }
