
from textwrap import dedent

from svgtools.writer.svg_writer import SvgWriter

from svgtools.model.scene.document import Document
from svgtools.model.scene.svg import Svg
from svgtools.model.scene.defs import Defs
from svgtools.model.scene.group import Group
from svgtools.model.scene.use import Use
from svgtools.model.scene.rect import Rect
from svgtools.model.scene.circle import Circle
from svgtools.model.scene.transform import Translate, Scale
from svgtools.model.geometry.rect import Rect as GeometryRect
from svgtools.model.geometry.circle import Circle as GeometryCircle
from svgtools.model.geometry.point import Point as GeometryPoint

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
            )
        )
    writer = SvgWriter()
    assert writer.write_svg_string(d) == dedent("""\
    <?xml version='1.0' encoding='UTF-8'?>
    <svg xmlns="http://www.w3.org/2000/svg" id="svgid" width="1024" height="1024" viewBox="0 0 1024 1024" transform="translate(4 5)" />
    """)

def test_write_empty_defs_with_id():
    d = Document(
            svg=Svg(
                children=(
                    Defs(
                        children=(),
                        id="defid",
                    ),
                )
            )
        )
    writer = SvgWriter()
    assert writer.write_svg_string(d) == dedent("""\
    <?xml version='1.0' encoding='UTF-8'?>
    <svg>
    <defs id="defid" />
    </svg>
    """)

def test_write_defs_with_children():
    d = Document(
            svg=Svg(
                children=(
                    Defs(
                        children=(
                            Rect(
                                id="rectid",
                                geometry=GeometryRect(
                                    top_left=GeometryPoint(
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
                    ),
                )
            )
        )
    writer = SvgWriter()
    assert writer.write_svg_string(d) == dedent("""\
    <?xml version='1.0' encoding='UTF-8'?>
    <svg>
    <g id="grpid" transform="scale(4 5)" />
    </svg>
    """)

def test_write_group_with_children():
    d = Document(
            svg=Svg(
                children=(
                    Group(
                        children=(
                            Circle(
                                id="circleid",
                                geometry=GeometryCircle(
                                    center=GeometryPoint(
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
      <circle id="circleid" cx="0" cy="0" radius="2" />
    </g>
    </svg>
    """)

def test_write_rect_with_attributes():
    d = Document(
            svg=Svg(
                children=(
                    Rect(
                        id="rectid",
                        transformations=(
                             Scale(sx=4, sy=5),
                             Translate(dx=1, dy=2),
                        ),
                        geometry=GeometryRect(
                            top_left=GeometryPoint(
                                x=4,
                                y=5,
                            ),
                            width=2,
                            height=1,
                        ),
                    ),
                )
            )
        )
    writer = SvgWriter()
    assert writer.write_svg_string(d) == dedent("""\
    <?xml version='1.0' encoding='UTF-8'?>
    <svg>
    <rect id="rectid" x="4" y="5" width="2" height="1" transform="scale(4 5) translate(1 2)" />
    </svg>
    """)

def test_write_circle_with_attributes():
    d = Document(
            svg=Svg(
                children=(
                    Circle(
                        id="circleid",
                        transformations=(
                             Translate(dx=-1, dy=-3),
                             Scale(sx=2, sy=1),
                        ),
                        geometry=GeometryCircle(
                            center=GeometryPoint(
                                x=3,
                                y=2,
                            ),
                            radius=7,
                        ),
                    ),
                )
            )
        )
    writer = SvgWriter()
    assert writer.write_svg_string(d) == dedent("""\
    <?xml version='1.0' encoding='UTF-8'?>
    <svg>
    <circle id="circleid" cx="3" cy="2" radius="7" transform="translate(-1 -3) scale(2 1)" />
    </svg>
    """)

def test_write_use():
    d = Document(
            svg=Svg(
                children=(
                    Defs(
                        children=(
                            Rect(
                                id="rectid",
                                geometry=GeometryRect(
                                    top_left=GeometryPoint(
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
    <use href="#rectid" transform="translate(1 1)" />
    </svg>
    """)
