
from textwrap import dedent

from svgtools.writer.svg_writer import SvgWriter

from svgtools.svg.document import Document
from svgtools.svg.svg import Svg
from svgtools.svg.defs import Defs
from svgtools.svg.group import Group
from svgtools.svg.use import Use
from svgtools.svg.shape import Shape
from svgtools.svg.transform import Translate, Scale, Rotate, SkewX, SkewY, Affine
from svgtools.geometry.rect import Rect
from svgtools.geometry.circle import Circle
from svgtools.geometry.path import Path
from svgtools.geometry.path_elements.moveto import MoveTo
from svgtools.geometry.path_elements.lineto import LineTo
from svgtools.geometry.path_elements.closepath import ClosePath
from svgtools.geometry.path_elements.quadraticbezier import QuadraticBezier
from svgtools.geometry.path_elements.cubicbezier import CubicBezier
from svgtools.geometry.path_elements.arc import Arc

from svgtools.geometry.point import Point

def test_write_empty_svg():
    d = Document(
            svg=Svg(
                children=()
                )
            )
    writer = SvgWriter()
    assert writer.write_svg_string(d) == dedent("""\
    <?xml version='1.0' encoding='UTF-8'?>
    <svg />
    """)

def test_write_empty_svg_with_attributes():
    d = Document(
            svg=Svg(
                children=(),
                id="svgid",
                transformations=(
                    Translate(dx=4, dy=5),
                    ),
                xmlnamespace="http://www.w3.org/2000/svg",
                width="1024",
                height="1024",
                viewBox=(0, 0, 1024, 1024,),
                unknown_attributes={
                    "unknown": "unknown_value"
                }
            )
        )
    writer = SvgWriter()
    assert writer.write_svg_string(d) == dedent("""\
    <?xml version='1.0' encoding='UTF-8'?>
    <svg xmlns="http://www.w3.org/2000/svg" id="svgid" width="1024" height="1024" viewBox="0 0 1024 1024" transform="translate(4 5)" unknown="unknown_value" />
    """)

def test_write_empty_defs_with_id():
    d = Document(
            svg=Svg(
                children=(
                    Defs(
                        children=(),
                        id="defid",
                        unknown_attributes={
                            "unknown": "unknown_value",
                        }
                    ),
                )
            )
        )
    writer = SvgWriter()
    assert writer.write_svg_string(d) == dedent("""\
    <?xml version='1.0' encoding='UTF-8'?>
    <svg>
    <defs id="defid" unknown="unknown_value" />
    </svg>
    """)

def test_write_defs_with_children():
    d = Document(
            svg=Svg(
                children=(
                    Defs(
                        children=(
                            Shape(
                                id="rectid",
                                geometry=Rect(
                                    top_left=Point(
                                        x=0,
                                        y=0,
                                    ),
                                    width=2,
                                    height=1,
                                ),
                            ),
                        ),
                    ),
                )
            )
        )
    writer = SvgWriter()
    assert writer.write_svg_string(d) == dedent("""\
    <?xml version='1.0' encoding='UTF-8'?>
    <svg>
    <defs>
      <rect id="rectid" x="0" y="0" width="2" height="1" />
    </defs>
    </svg>
    """)

def test_write_empty_group_with_attributes():
    d = Document(
            svg=Svg(
                children=(
                    Group(
                        children=(),
                        id="grpid",
                        transformations=(
                             Scale(sx=4, sy=5),
                        ),
                        unknown_attributes={
                            "unknown": "unknown_value"
                        },
                    ),
                )
            )
        )
    writer = SvgWriter()
    assert writer.write_svg_string(d) == dedent("""\
    <?xml version='1.0' encoding='UTF-8'?>
    <svg>
    <g id="grpid" transform="scale(4 5)" unknown="unknown_value" />
    </svg>
    """)

def test_write_group_with_children():
    d = Document(
            svg=Svg(
                children=(
                    Group(
                        children=(
                            Shape(
                                id="circleid",
                                geometry=Circle(
                                    center=Point(
                                        x=0,
                                        y=0,
                                    ),
                                    radius=2,
                                ),
                            ),
                        ),
                    ),
                )
            )
        )
    writer = SvgWriter()
    assert writer.write_svg_string(d) == dedent("""\
    <?xml version='1.0' encoding='UTF-8'?>
    <svg>
    <g>
      <circle id="circleid" cx="0" cy="0" r="2" />
    </g>
    </svg>
    """)

def test_write_rect_with_attributes():
    d = Document(
            svg=Svg(
                children=(
                    Shape(
                        id="rectid",
                        transformations=(
                             Scale(sx=4, sy=5),
                             Translate(dx=1, dy=2),
                             Rotate(theta=45, cx=1, cy=3),
                        ),
                        geometry=Rect(
                            top_left=Point(
                                x=4,
                                y=5,
                            ),
                            width=2,
                            height=1,
                        ),
                        unknown_attributes={
                            "unknown": "unknown_value",
                        }
                    ),
                )
            )
        )
    writer = SvgWriter()
    assert writer.write_svg_string(d) == dedent("""\
    <?xml version='1.0' encoding='UTF-8'?>
    <svg>
    <rect id="rectid" x="4" y="5" width="2" height="1" transform="scale(4 5) translate(1 2) rotate(45 1 3)" unknown="unknown_value" />
    </svg>
    """)

def test_write_rect_with_more_transformations():
    d = Document(
            svg=Svg(
                children=(
                    Shape(
                        id="rectid",
                        transformations=(
                             SkewX(theta=60),
                             SkewY(theta=30),
                             Affine(a=1, b=2, c=3, d=4, e=5, f=6),
                        ),
                        geometry=Rect(
                            top_left=Point(
                                x=4,
                                y=5,
                            ),
                            width=2,
                            height=1,
                        ),
                        unknown_attributes={
                            "unknown": "unknown_value",
                        }
                    ),
                )
            )
        )
    writer = SvgWriter()
    assert writer.write_svg_string(d) == dedent("""\
    <?xml version='1.0' encoding='UTF-8'?>
    <svg>
    <rect id="rectid" x="4" y="5" width="2" height="1" transform="skewX(60) skewY(30) matrix(1 2 3 4 5 6)" unknown="unknown_value" />
    </svg>
    """)

def test_write_circle_with_attributes():
    d = Document(
            svg=Svg(
                children=(
                    Shape(
                        id="circleid",
                        transformations=(
                             Translate(dx=-1, dy=-3),
                             Scale(sx=2, sy=1),
                        ),
                        geometry=Circle(
                            center=Point(
                                x=3,
                                y=2,
                            ),
                            radius=7,
                        ),
                        unknown_attributes={
                            "unknown": "unknown_value",
                        }
                    ),
                )
            )
        )
    writer = SvgWriter()
    assert writer.write_svg_string(d) == dedent("""\
    <?xml version='1.0' encoding='UTF-8'?>
    <svg>
    <circle id="circleid" cx="3" cy="2" r="7" transform="translate(-1 -3) scale(2 1)" unknown="unknown_value" />
    </svg>
    """)

def test_write_path():
    d = Document(
        svg=Svg(
            children=(
                Shape (
                    id="mypath",
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
                            ClosePath(
                                representation = 'z',
                            ),
                            QuadraticBezier(
                                control1 = Point (
                                    x = 7,
                                    y = 8,
                                ),
                                end = Point (
                                    x = 10,
                                    y = 11,
                                ),
                                representation = 't',
                            ),
                            CubicBezier(
                                control1 = Point (
                                    x = 20,
                                    y = 21,
                                ),
                                control2 = Point (
                                    x = 22,
                                    y = 23,
                                ),
                                end = Point (
                                    x = 24,
                                    y = 25,
                                ),
                                representation = 's',
                            ),
                            Arc(
                                rx = 30,
                                ry = 31,
                                phi = 60,
                                large_arc_flag = 0,
                                sweep_flag = 1,
                                end = Point (
                                    x = 35,
                                    y = 36,
                                ),
                                representation = 'a'
                            ),
                        ),
                    ),
                ),
            ),
        ),
    )
    writer = SvgWriter()
    assert writer.write_svg_string(d) == dedent("""\
    <?xml version='1.0' encoding='UTF-8'?>
    <svg>
    <path id="mypath" d="M 3 4 L 4 5 Z Q 7 8 10 11 C 20 21 22 23 24 25 A 30 31 60 0 1 35 36" />
    </svg>
    """)


def test_write_use():
    d = Document(
            svg=Svg(
                children=(
                    Defs(
                        children=(
                            Shape(
                                id="rectid",
                                geometry=Rect(
                                    top_left=Point(
                                        x=0,
                                        y=0,
                                    ),
                                    width=2,
                                    height=1,
                                ),
                            ),
                        ),
                    ),
                    Use(
                        href="#rectid",
                        transformations=(
                            Translate(
                                dx=1,
                                dy=1,
                            ),
                        ),
                        unknown_attributes={
                            "unknown": "unknown_value",
                        }
                    ),
                )
            )
        )
    writer = SvgWriter()
    assert writer.write_svg_string(d) == dedent("""\
    <?xml version='1.0' encoding='UTF-8'?>
    <svg>
    <defs>
      <rect id="rectid" x="0" y="0" width="2" height="1" />
    </defs>
    <use href="#rectid" transform="translate(1 1)" unknown="unknown_value" />
    </svg>
    """)
