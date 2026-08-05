
from textwrap import dedent

from svgtools.writer.svg_writer import SvgWriter

from svgtools.model.scene.document import Document
from svgtools.model.scene.svg import Svg
from svgtools.model.scene.defs import Defs
from svgtools.model.scene.group import Group
#from svgtools.model.scene.use import Use
from svgtools.model.scene.rect import Rect
#from svgtools.model.scene.circle import Circle
from svgtools.model.scene.transform import Translate, Scale
from svgtools.model.geometry.rect import Rect as GeometryRect
#from svgtools.model.geometry.circle import Circle as GeometryCircle
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
