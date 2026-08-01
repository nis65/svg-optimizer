from svgtools.model.geometry.point import Point as GeometryPoint
from svgtools.model.geometry.rect import Rect as GeometryRect

from svgtools.model.scene.defs import Defs
from svgtools.model.scene.document import Document
from svgtools.model.scene.group import Group
from svgtools.model.scene.rect import Rect
from svgtools.model.scene.svg import Svg
from svgtools.model.scene.use import Use

from svgtools.semantic.bounding_box_visitor import BoundingBoxVisitor

def test_use_is_followed_twice():

    document = Document(
        svg=Svg(
            children=(
                Defs(
                    children=(
                        Rect(
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
