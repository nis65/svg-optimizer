from svgtools.model.geometry.point import Point as GeometryPoint
from svgtools.model.geometry.rect import Rect as GeometryRect
from svgtools.model.geometry.circle import Circle as GeometryCircle
from svgtools.model.geometry.bounding_box import BoundingBox as GeometryBoundingBox

from svgtools.model.scene.defs import Defs
from svgtools.model.scene.document import Document
from svgtools.model.scene.group import Group
from svgtools.model.scene.shape import Shape
from svgtools.model.scene.svg import Svg
from svgtools.model.scene.use import Use

from svgtools.semantic.bounding_box_visitor import BoundingBoxVisitor

def test_use_is_followed_twice():

    document = Document(
        svg=Svg(
            children=(
                Defs(
                    children=(
                        Shape(
                            id="square",
                            geometry=GeometryRect(
                                top_left=GeometryPoint(0, 0),
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
                            geometry=GeometryRect(
                                top_left=GeometryPoint(0, 0),
                                width=10,
                                height=5,
                            ),
                        ),
                        Group(
                            id="groupid",
                            children=(
                                Shape(
                                    id="circle",
                                    geometry=GeometryCircle(
                                        center=GeometryPoint(0, 0),
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

def test_scene_bounding_box_rect():
    document = Document(
        svg=Svg(
            children=(
                Shape(
                    id="square",
                    geometry=GeometryRect(
                        top_left=GeometryPoint(0, 0),
                        width=10,
                        height=5,
                    ),
                ),
            ),
        ),
    )
    visitor = BoundingBoxVisitor()
    visitor.visit(document)

    assert visitor.bounding_box == GeometryBoundingBox(
                                       min=GeometryPoint(0,0),
                                       max=GeometryPoint(10,5)
                                   )

def test_scene_bounding_box_circle():
    document = Document(
        svg=Svg(
            children=(
                Shape(
                    id="circle",
                    geometry=GeometryCircle(
                        center=GeometryPoint(4, 5),
                        radius=2
                    ),
                ),
            ),
        ),
    )
    visitor = BoundingBoxVisitor()
    visitor.visit(document)

    assert visitor.bounding_box == GeometryBoundingBox(
                                       min=GeometryPoint(2,3),
                                       max=GeometryPoint(6,7)
                                   )

def test_scene_bounding_box_with_use():
    document = Document(
        svg=Svg(
            children=(
                Defs(
                    children=(
                        Shape(
                            id="square",
                            geometry=GeometryRect(
                                top_left=GeometryPoint(5,5),
                                width=4,
                                height=3,
                            ),
                        ),
                        Group(
                            id="groupid",
                            children=(
                                Shape(
                                    id="circle",
                                    geometry=GeometryCircle(
                                        center=GeometryPoint(5,5),
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

    assert visitor.bounding_box == GeometryBoundingBox(
                                       min=GeometryPoint(3,3),
                                       max=GeometryPoint(9,8)
                                   )
