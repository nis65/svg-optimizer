from svgtools.geometry.point import Point
from svgtools.geometry.rect import Rect
from svgtools.geometry.circle import Circle
from svgtools.geometry.path import Path
from svgtools.geometry.path_elements.moveto import MoveTo
from svgtools.geometry.path_elements.lineto import LineTo
from svgtools.geometry.path_elements.closepath import ClosePath
from svgtools.geometry.path_elements.quadraticbezier import QuadraticBezier
from svgtools.geometry.path_elements.cubicbezier import CubicBezier
from svgtools.geometry.path_elements.arc import Arc

from svgtools.geometry.bounding_box import BoundingBox

from svgtools.svg.defs import Defs
from svgtools.svg.document import Document
from svgtools.svg.group import Group
from svgtools.svg.shape import Shape
from svgtools.svg.svg import Svg
from svgtools.svg.use import Use

from svgtools.semantic.bounding_box_visitor import BoundingBoxVisitor

def test_use_is_followed_twice():

    document = Document(
        svg=Svg(
            children=(
                Defs(
                    children=(
                        Shape(
                            id="square",
                            geometry=Rect(
                                top_left=Point(0, 0),
                                width=10,
                                height=5,
                            ),
                        ),
                    ),
                ),
                Use(href="#square"),
                Use(href="#square"),
            ),
        ),
    )

    visitor = BoundingBoxVisitor()
    visitor.visit(document)

    assert visitor.rectangles_visited == 2

def test_use_with_all_known_types():

    document = Document(
        svg=Svg(
            children=(
                Defs(
                    children=(
                        Shape(
                            id="square",
                            geometry=Rect(
                                top_left=Point(0, 0),
                                width=10,
                                height=5,
                            ),
                        ),
                        Group(
                            id="groupid",
                            children=(
                                Shape(
                                    id="circle",
                                    geometry=Circle(
                                        center=Point(0, 0),
                                        radius=10,
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
                Use(href="#square"),
                Use(href="#square"),
                Use(href="#groupid"),
            ),
        ),
    )

    visitor = BoundingBoxVisitor()
    visitor.visit(document)

    assert visitor.rectangles_visited == 2
    assert visitor.circles_visited == 1

def test_bounding_box_rect():
    document = Document(
        svg=Svg(
            children=(
                Shape(
                    id="square",
                    geometry=Rect(
                        top_left=Point(0, 0),
                        width=10,
                        height=5,
                    ),
                ),
            ),
        ),
    )
    visitor = BoundingBoxVisitor()
    visitor.visit(document)

    assert visitor.bounding_box == BoundingBox(
                                       min=Point(0,0),
                                       max=Point(10,5)
                                   )

def test_bounding_box_circle():
    document = Document(
        svg=Svg(
            children=(
                Shape(
                    id="circle",
                    geometry=Circle(
                        center=Point(4, 5),
                        radius=2
                    ),
                ),
            ),
        ),
    )
    visitor = BoundingBoxVisitor()
    visitor.visit(document)

    assert visitor.bounding_box == BoundingBox(
                                       min=Point(2,3),
                                       max=Point(6,7)
                                   )

def test_bounding_box_path_ml():
    document = Document(
        svg=Svg(
            children=(
                Shape (
                    id="path",
                    geometry = Path (
                        children = (
                            MoveTo(
                                target = Point(
                                    x = 3,
                                    y = 4,
                                ),
                                representation = 'm',
                            ),
                            LineTo(
                                target = Point(
                                    x = 4,
                                    y = 5,
                                ),
                                representation = 'L',
                            ),
                        ),
                    ),
                ),
            ),
        ),
    )
    visitor = BoundingBoxVisitor()
    visitor.visit(document)

    assert visitor.bounding_box == BoundingBox(
                                       min=Point(3,4),
                                       max=Point(4,5)
                                   )


def test_bounding_box_with_use():
    document = Document(
        svg=Svg(
            children=(
                Defs(
                    children=(
                        Shape(
                            id="square",
                            geometry=Rect(
                                top_left=Point(5,5),
                                width=4,
                                height=3,
                            ),
                        ),
                        Group(
                            id="groupid",
                            children=(
                                Shape(
                                    id="circle",
                                    geometry=Circle(
                                        center=Point(5,5),
                                        radius=2,
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
                Use(href="#square"),
                Use(href="#groupid"),
            ),
        ),
    )

    visitor = BoundingBoxVisitor()
    visitor.visit(document)

    assert visitor.bounding_box == BoundingBox(
                                       min=Point(3,3),
                                       max=Point(9,8)
                                   )
