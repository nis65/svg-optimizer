import math

import pytest

from svgtools.geometry.path import Path
from svgtools.geometry.path_elements.arc import Arc
from svgtools.geometry.path_elements.closepath import ClosePath
from svgtools.geometry.path_elements.cubicbezier import CubicBezier
from svgtools.geometry.path_elements.lineto import LineTo
from svgtools.geometry.path_elements.moveto import MoveTo
from svgtools.geometry.path_elements.quadraticbezier import QuadraticBezier
from svgtools.geometry.point import Point
from svgtools.geometry.tolerance import GEOMETRY_REL_TOL, GEOMETRY_ABS_TOL


def test_invalid_arc_repr():
    with pytest.raises(ValueError, match="Arc can only be represented"):
        a = Arc(                       # noqa: F841
                rx = 1,
                ry = 2,
                phi = 45,
                large_arc_flag = 0,
                sweep_flag = 1,
                end = Point(
                    x = 3,
                    y = 4,
                ),
                representation='x',
            )

def test_invalid_closepath_repr():
    with pytest.raises(ValueError, match="ClosePath can only be represented"):
        c = ClosePath(                # noqa: F841
                representation='x',
            )

def test_closepath_has_no_endpoint_no_boundingbox():
    c = ClosePath(
            representation='z',
        )
    with pytest.raises(ValueError, match="ClosePath has no internal endpoint"):
        p = c.endpoint()              # noqa: F841
    with pytest.raises(ValueError, match="ClosePath has no points for bounding box"):
        points = c.points_for_bounding_box(Point(0,0), 100)       # noqa: F841

def test_invalid_qbezier_repr():
    with pytest.raises(ValueError, match="QuadraticBezier can only be represented by"):
        q = QuadraticBezier(          # noqa: F841
                control1 = Point(
                    x = 2,
                    y = 2,
                ),
                end = Point(
                    x = 3,
                    y = 3,
                ),
                representation='x',
            )

def test_invalid_cbezier_repr():
    with pytest.raises(ValueError, match="CubicBezier can only be represented by"):
        q = CubicBezier(              # noqa: F841
                control1 = Point(
                    x = 2,
                    y = 2,
                ),
                control2 = Point(
                    x = 1.5,
                    y = 1.5,
                ),
                end = Point(
                    x = 3,
                    y = 3,
                ),
                representation='x',
            )

def test_invalid_lineto():
    with pytest.raises(ValueError, match="LineTo can only be represented by"):
        l = LineTo(                  # noqa: F841
            target = Point(
                x = 1,
                y = 2,
            ),
            representation='x',
        ),

def test_invalid_moveto():
    with pytest.raises(ValueError, match="MoveTo can only be represented by"):
        m = MoveTo(                  # noqa: F841
            target = Point(
                x = 1,
                y = 2,
            ),
            representation='x',
        ),

def test_endpoint_but_no_bb_moveto():
    target_point = Point(1,2)
    m = MoveTo(
        target = target_point,
        representation='m',
    )
    assert m.endpoint == target_point
    with pytest.raises(ValueError, match="MoveTo has no points for bounding box"):
        m.points_for_bounding_box(200)

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
        p = Path(                                   # noqa: F841
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

def test_path_with_cubic_bezier():
    p = Path(
            children = (
                CubicBezier(
                    control1 = Point(
                        x = 2,
                        y = 2,
                    ),
                    control2 = Point(
                        x = 3,
                        y = 3,
                    ),
                    end = Point(
                        x = 4,
                        y = 4,
                    ),
                    representation='C',
                ),
            )
        )
    assert type(p.children[0]) == CubicBezier
    assert p.children[0].control1.x == 2
    assert p.children[0].control1.y == 2
    assert p.children[0].control2.x == 3
    assert p.children[0].control2.y == 3
    assert p.children[0].end.x == 4
    assert p.children[0].end.y == 4
    assert p.children[0].representation == 'C'

def test_path_with_bounding_box_for_cubic_bezier_line():
    p = Path(
            children = (
                MoveTo(
                    target = Point(
                        x = 1,
                        y = 1,
                    ),
                    representation='M',
                ),
                CubicBezier(
                    control1 = Point(
                        x = 2,
                        y = 2,
                    ),
                    control2 = Point(
                        x = 3,
                        y = 3,
                    ),
                    end = Point(
                        x = 4,
                        y = 4,
                    ),
                    representation='C',
                ),
            )
        )
    assert p.points_for_bounding_box(3) == {
        Point(x=1, y=1,),
        Point(x=2, y=2,),
        Point(x=3, y=3,),
        Point(x=4, y=4,),
    }

def test_path_with_bounding_box_for_cubic_bezier_curve():
    p = Path(
            children = (
                MoveTo(
                    target = Point(
                        x = 1,
                        y = 1,
                    ),
                    representation='M',
                ),
                CubicBezier(
                    control1 = Point(
                        x = 3,
                        y = 2,
                    ),
                    control2 = Point(
                        x = 0,
                        y = 2,
                    ),
                    end = Point(
                        x = 2,
                        y = 1,
                    ),
                    representation='C',
                ),
            )
        )
    assert Point.points_are_close(p.points_for_bounding_box(3), {
        Point(x=1, y=1,),
        Point(x=46/27, y=5/3,),
        Point(x=35/27, y=5/3,),
        Point(x=2, y=1,),
    }, abs_tol=GEOMETRY_ABS_TOL)

def test_path_with_arc():
    p = Path(
            children = (
                Arc(
                    rx = 1,
                    ry = 2,
                    phi = 45,
                    large_arc_flag = 0,
                    sweep_flag = 1,
                    end = Point(
                        x = 3,
                        y = 4,
                    ),
                    representation='A',
                ),
            )
        )
    assert type(p.children[0]) == Arc
    assert p.children[0].rx == 1
    assert p.children[0].ry == 2
    assert p.children[0].phi == 45
    assert p.children[0].large_arc_flag == 0
    assert p.children[0].sweep_flag == 1
    assert p.children[0].end.x == 3
    assert p.children[0].end.y == 4
    assert p.children[0].representation == 'A'

def test_path_with_bounding_box_for_small_arc_circle():
    p = Path(
            children = (
                MoveTo(
                    target = Point(
                        x = 200,
                        y = 200,
                    ),
                    representation='M',
                ),
                Arc(
                    rx = 100,
                    ry = 100,
                    phi = -10,
                    large_arc_flag = 0,
                    sweep_flag = 1,
                    end = Point(
                        x = 300,
                        y = 100,
                    ),
                    representation='A',
                ),
            )
        )
    assert Point.points_are_close(p.points_for_bounding_box(2), {
        Point(x=200, y=200,),
        Point(x=300 - 100 * math.sqrt(2) / 2,
              y=200 - 100 * math.sqrt(2) / 2
             ),
        Point(x=300, y=100,),
    }, abs_tol=GEOMETRY_ABS_TOL)

def test_path_with_bounding_box_for_big_arc_circle():
    p = Path(
            children = (
                MoveTo(
                    target = Point(
                        x = 200,
                        y = 500,
                    ),
                    representation='M',
                ),
                Arc(
                    rx = 100,
                    ry = 100,
                    phi = 15,
                    large_arc_flag = 1,
                    sweep_flag = 1,
                    end = Point(
                        x = 300,
                        y = 400,
                    ),
                    representation='A',
                ),
            )
        )
    assert Point.points_are_close(p.points_for_bounding_box(3), {
        Point(x=200, y=500,),
        Point(x=100, y=400,),
        Point(x=200, y=300,),
        Point(x=300, y=400,),
    }, abs_tol=GEOMETRY_ABS_TOL)

def test_path_with_bounding_box_for_two_similar_random_arcs():
    p1 = Path(
            children = (
                MoveTo(
                    target = Point(
                        x = 3,
                        y = 7,
                    ),
                    representation='M',
                ),
                Arc(
                    rx = 3,
                    ry = 7,
                    phi = 27,
                    large_arc_flag = 1,
                    sweep_flag = 1,
                    end = Point(
                        x = 10,
                        y = 11,
                    ),
                    representation='A',
                ),
            )
        )
    p2 = Path(
            children = (
                MoveTo(
                    target = Point(
                        x = 10,
                        y = 11,
                    ),
                    representation='M',
                ),
                Arc(
                    rx = 3,
                    ry = 7,
                    phi = 27,
                    large_arc_flag = 1,
                    sweep_flag = 0,
                    end = Point(
                        x = 3,
                        y = 7,
                    ),
                    representation='A',
                ),
            )
        )
    assert Point.points_are_close(
             p1.points_for_bounding_box(36),
             p2.points_for_bounding_box(36),
             abs_tol=GEOMETRY_ABS_TOL)
