from svgtools.model.geometry.point import Point as GeometryPoint
from svgtools.model.geometry.rect import Rect as GeometryRect
from svgtools.model.geometry.circle import Circle as GeometryCircle
from svgtools.model.geometry.bounding_box import BoundingBox as GeometryBoundingBox

from svgtools.model.scene.defs import Defs
from svgtools.model.scene.document import Document
from svgtools.model.scene.group import Group
from svgtools.model.scene.rect import Rect
from svgtools.model.scene.circle import Circle
from svgtools.model.scene.svg import Svg
from svgtools.model.scene.use import Use

from svgtools.model.scene.transform import Translate, Scale

from svgtools.semantic.bounding_box_visitor import BoundingBoxVisitor

def test_rect_svg_translate():
    document = Document(
        svg=Svg(
            children=(
                Rect(
                    id="square",
                    geometry=GeometryRect(
                        top_left=GeometryPoint(0, 0),
                        width=10,
                        height=5,
                    ),
                    transformations=(),
                ),
            ),
            transformations=(Translate(dx=1, dy=1),),
        ),
    )
    visitor = BoundingBoxVisitor()
    visitor.visit(document)

    assert visitor.bounding_box == GeometryBoundingBox(
                                       min=GeometryPoint(1,1),
                                       max=GeometryPoint(11,6)
                                   )

def test_rect_rect_translate():
    document = Document(
        svg=Svg(
            children=(
                Rect(
                    id="square",
                    geometry=GeometryRect(
                        top_left=GeometryPoint(0, 0),
                        width=10,
                        height=5,
                    ),
                    transformations=(Translate(dx=1, dy=1),),
                ),
            ),
        ),
    )
    visitor = BoundingBoxVisitor()
    visitor.visit(document)

    assert visitor.bounding_box == GeometryBoundingBox(
                                       min=GeometryPoint(1,1),
                                       max=GeometryPoint(11,6)
                                   )

def test_rect_group_translate():
    document = Document(
        svg=Svg(
            children=(
                Group(
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
                    transformations=(Translate(dx=1, dy=1),),
                ),
            ),
        ),
    )
    visitor = BoundingBoxVisitor()
    visitor.visit(document)

    assert visitor.bounding_box == GeometryBoundingBox(
                                       min=GeometryPoint(1,1),
                                       max=GeometryPoint(11,6)
                                   )
def test_rect_use_translate():
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
                Use(
                    href="#square",
                    transformations=(Translate(dx=1, dy=1),),
                ),
            ),
        ),
    )
    visitor = BoundingBoxVisitor()
    visitor.visit(document)

    assert visitor.bounding_box == GeometryBoundingBox(
                                       min=GeometryPoint(1,1),
                                       max=GeometryPoint(11,6)
                                   )

def test_rect_all_translate():
    document = Document(
        svg=Svg(
            transformations=(Translate(dx=1, dy=1),),
            children=(
                Defs(
                    children=(
                        Group(
                            id="group",
                            transformations=(Translate(dx=2, dy=-1),),
                            children=(
                                Rect(
                                    id="square",
                                    transformations=(Translate(dx=3, dy=-2),),
                                    geometry=GeometryRect(
                                        top_left=GeometryPoint(0, 0),
                                        width=1,
                                        height=2,
                                    ),
                                ),
                            ),
                        ),
                    ),
                ),
                Use(
                    transformations=(Translate(dx=4, dy=1),),
                    href="#group",
                ),
            ),
        ),
    )
    visitor = BoundingBoxVisitor()
    visitor.visit(document)

    assert visitor.bounding_box == GeometryBoundingBox(
                                       min=GeometryPoint(10,-1),
                                       max=GeometryPoint(11,1)
                                   )



def test_circle_svg_scale():
    document = Document(
        svg=Svg(
            children=(
                Circle(
                    id="circle",
                    geometry=GeometryCircle(
                        center=GeometryPoint(1, 1),
                        radius=1,
                    ),
                    transformations=(),
                ),
            ),
            transformations=(Scale(sx=2, sy=2),),
        ),
    )
    visitor = BoundingBoxVisitor()
    visitor.visit(document)

    assert visitor.bounding_box.isclose(
        GeometryBoundingBox(
            min=GeometryPoint(0,0),
            max=GeometryPoint(4,4)
        ),
        1e-9
    )

def test_circle_circle_scale():
    document = Document(
        svg=Svg(
            children=(
                Circle(
                    id="circle",
                    geometry=GeometryCircle(
                        center=GeometryPoint(1, 1),
                        radius=1,
                    ),
                    transformations=(Scale(sx=2, sy=2),),
                ),
            ),
        ),
    )
    visitor = BoundingBoxVisitor()
    visitor.visit(document)

    assert visitor.bounding_box == GeometryBoundingBox(
                                       min=GeometryPoint(0,0),
                                       max=GeometryPoint(4,4)
                                   )
