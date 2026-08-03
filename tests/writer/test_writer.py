
from textwrap import dedent

from svgtools.writer.svg_writer import SvgWriter

from svgtools.model.scene.document import Document
from svgtools.model.scene.svg import Svg
#from svgtools.model.scene.defs import Defs
#from svgtools.model.scene.group import Group
#from svgtools.model.scene.use import Use
#from svgtools.model.scene.rect import Rect
#from svgtools.model.scene.circle import Circle
from svgtools.model.scene.transform import Translate, Scale
#from svgtools.model.geometry.rect import Rect as GeometryRect
#from svgtools.model.geometry.circle import Circle as GeometryCircle
#from svgtools.model.geometry.point import Point as GeometryPoint

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

