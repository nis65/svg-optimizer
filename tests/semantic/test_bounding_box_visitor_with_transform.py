import math

from svgtools.geometry.point import Point
from svgtools.geometry.rect import Rect
from svgtools.geometry.circle import Circle
from svgtools.geometry.bounding_box import BoundingBox

from svgtools.svg.defs import Defs
from svgtools.svg.document import Document
from svgtools.svg.group import Group
from svgtools.svg.shape import Shape
from svgtools.svg.svg import Svg
from svgtools.svg.use import Use

from svgtools.svg.transform import Translate, Scale, Rotate

from svgtools.semantic.bounding_box_visitor import BoundingBoxVisitor

def test_rect_svg_translate():
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
                    transformations=(),
                ),
            ),
            transformations=(Translate(dx=1, dy=1),),
        ),
    )
    visitor = BoundingBoxVisitor()
    visitor.visit(document)

    assert visitor.bounding_box == BoundingBox(
                                       min=Point(1,1),
                                       max=Point(11,6)
                                   )

def test_rect_rect_translate():
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
                    transformations=(Translate(dx=1, dy=1),),
                ),
            ),
        ),
    )
    visitor = BoundingBoxVisitor()
    visitor.visit(document)

    assert visitor.bounding_box == BoundingBox(
                                       min=Point(1,1),
                                       max=Point(11,6)
                                   )

def test_rect_group_translate():
    document = Document(
        svg=Svg(
            children=(
                Group(
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
                    transformations=(Translate(dx=1, dy=1),),
                ),
            ),
        ),
    )
    visitor = BoundingBoxVisitor()
    visitor.visit(document)

    assert visitor.bounding_box == BoundingBox(
                                       min=Point(1,1),
                                       max=Point(11,6)
                                   )
def test_rect_use_translate():
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
                Use(
                    href="#square",
                    transformations=(Translate(dx=1, dy=1),),
                ),
            ),
        ),
    )
    visitor = BoundingBoxVisitor()
    visitor.visit(document)

    assert visitor.bounding_box == BoundingBox(
                                       min=Point(1,1),
                                       max=Point(11,6)
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
                                Shape(
                                    id="square",
                                    transformations=(Translate(dx=3, dy=-2),),
                                    geometry=Rect(
                                        top_left=Point(0, 0),
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

    assert visitor.bounding_box == BoundingBox(
                                       min=Point(10,-1),
                                       max=Point(11,1)
                                   )



def test_circle_svg_scale():
    document = Document(
        svg=Svg(
            children=(
                Shape(
                    id="circle",
                    geometry=Circle(
                        center=Point(1, 1),
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
        BoundingBox(
            min=Point(0,0),
            max=Point(4,4)
        ),
        1e-9
    )

def test_circle_circle_scale():
    document = Document(
        svg=Svg(
            children=(
                Shape(
                    id="circle",
                    geometry=Circle(
                        center=Point(1, 1),
                        radius=1,
                    ),
                    transformations=(Scale(sx=2, sy=2),),
                ),
            ),
        ),
    )
    visitor = BoundingBoxVisitor()
    visitor.visit(document)

    assert visitor.bounding_box == BoundingBox(
                                       min=Point(0,0),
                                       max=Point(4,4)
                                   )

def test_circle_circle_rotate():
    document = Document(
        svg=Svg(
            children=(
                Shape(
                    id="circle",
                    geometry=Circle(
                        center=Point(1, 1),
                        radius=1,
                    ),
                    transformations=(Rotate(theta=60, cx=1, cy=1),),
                ),
            ),
        ),
    )
    visitor = BoundingBoxVisitor()
    visitor.visit(document)

    assert visitor.bounding_box.isclose(BoundingBox(
                                       min=Point(0,0),
                                       max=Point(2,2)
                                   ), 1e-3)

def test_rect_rect_rotate_1():
    document = Document(
        svg=Svg(
            children=(
                Shape(
                    id="rect",
                    geometry=Rect(
                        top_left=Point(0, 0),
                        width=2,
                        height=2,
                    ),
                    transformations=(Rotate(theta=45, cx=1, cy=1),),
                ),
            ),
        ),
    )
    visitor = BoundingBoxVisitor()
    visitor.visit(document)
    sqrt2=math.sqrt(2)
    assert visitor.bounding_box.isclose(BoundingBox(
                                       min=Point(1-sqrt2,1-sqrt2),
                                       max=Point(1+sqrt2,1+sqrt2),
                                   ), 1e-3)

def test_rect_rect_rotate_2():
    document = Document(
        svg=Svg(
            children=(
                Shape(
                    id="rect",
                    geometry=Rect(
                        top_left=Point(0, 0),
                        width=2,
                        height=2,
                    ),
                    transformations=(Rotate(theta=135, cx=1, cy=1),),
                ),
            ),
        ),
    )
    visitor = BoundingBoxVisitor()
    visitor.visit(document)
    sqrt2=math.sqrt(2)
    assert visitor.bounding_box.isclose(BoundingBox(
                                       min=Point(1-sqrt2,1-sqrt2),
                                       max=Point(1+sqrt2,1+sqrt2),
                                   ), 1e-3)
