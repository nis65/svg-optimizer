import pytest

from svgtools.geometry.bounding_box import BoundingBox
from svgtools.geometry.circle import Circle
from svgtools.geometry.matrix3 import Matrix3
from svgtools.geometry.path import Path
from svgtools.geometry.path_elements.closepath import ClosePath
from svgtools.geometry.path_elements.lineto import LineTo
from svgtools.geometry.path_elements.moveto import MoveTo
from svgtools.geometry.point import Point
from svgtools.geometry.rect import Rect
from svgtools.semantic.bounding_box_visitor import BoundingBoxVisitor
from svgtools.svg.defs import Defs
from svgtools.svg.document import Document
from svgtools.svg.group import Group
from svgtools.svg.shape import Shape
from svgtools.svg.svg import Svg
from svgtools.svg.use import Use


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

    assert visitor.visited["Rect"] == 2


def test_use_references_unknown_tag():

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
                Use(href="#circle"),
            ),
        ),
    )

    visitor = BoundingBoxVisitor()
    with pytest.raises(ValueError, match="Use references unknown label"):
        visitor.visit(document)


def test_empty_set_for_bounding_box():
    with pytest.raises(
        ValueError, match="need at least one point to create a BoundingBox"
    ):
        BoundingBoxVisitor._transformed_points_bounding_box(
            {}, Matrix3.translation(1, 1)
        )


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

    assert visitor.visited["Rect"] == 2
    assert visitor.visited["Circle"] == 1


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

    assert visitor.bounding_box == BoundingBox(min=Point(0, 0), max=Point(10, 5))


def test_bounding_box_circle():
    document = Document(
        svg=Svg(
            children=(
                Shape(
                    id="circle",
                    geometry=Circle(center=Point(4, 5), radius=2),
                ),
            ),
        ),
    )
    visitor = BoundingBoxVisitor()
    visitor.visit(document)

    assert visitor.bounding_box == BoundingBox(min=Point(2, 3), max=Point(6, 7))


def test_bounding_box_path_ml():
    document = Document(
        svg=Svg(
            children=(
                Shape(
                    id="path",
                    geometry=Path(
                        children=(
                            MoveTo(
                                target=Point(
                                    x=3,
                                    y=4,
                                ),
                                representation="m",
                            ),
                            LineTo(
                                target=Point(
                                    x=4,
                                    y=5,
                                ),
                                representation="L",
                            ),
                        ),
                    ),
                ),
            ),
        ),
    )
    visitor = BoundingBoxVisitor()
    visitor.visit(document)

    assert visitor.bounding_box == BoundingBox(min=Point(3, 4), max=Point(4, 5))


def test_bounding_box_path_mz():
    document = Document(
        svg=Svg(
            children=(
                Shape(
                    id="path",
                    geometry=Path(
                        children=(
                            MoveTo(
                                target=Point(
                                    x=3,
                                    y=4,
                                ),
                                representation="m",
                            ),
                            ClosePath(
                                representation="z",
                            ),
                        ),
                    ),
                ),
            ),
        ),
    )
    visitor = BoundingBoxVisitor()
    visitor.visit(document)

    assert visitor.bounding_box == BoundingBox(min=Point(3, 4), max=Point(3, 4))
    assert visitor.visited["path_MoveTo"] == 1
    assert visitor.visited["path_ClosePath"] == 1


def test_bounding_box_with_use():
    document = Document(
        svg=Svg(
            children=(
                Defs(
                    children=(
                        Shape(
                            id="square",
                            geometry=Rect(
                                top_left=Point(5, 5),
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
                                        center=Point(5, 5),
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

    assert visitor.bounding_box == BoundingBox(min=Point(3, 3), max=Point(9, 8))
