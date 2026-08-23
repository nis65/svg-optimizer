from textwrap import dedent

from svgtools.geometry.path import Path
from svgtools.geometry.path_elements.arc import Arc
from svgtools.geometry.path_elements.closepath import ClosePath
from svgtools.geometry.path_elements.cubicbezier import CubicBezier
from svgtools.geometry.path_elements.lineto import LineTo
from svgtools.geometry.path_elements.moveto import MoveTo
from svgtools.geometry.path_elements.quadraticbezier import QuadraticBezier
from svgtools.geometry.point import Point
from svgtools.svg.document import Document
from svgtools.svg.shape import Shape
from svgtools.svg.svg import Svg
from svgtools.writer.path_writer import (
    PathCommandSet,
    PathCompactness,
    PathCoordinates,
)
from svgtools.writer.svg_writer import SvgWriter

# {{{ document "d" for PathCoordinates / PathCommandSet
d = Document(
    svg=Svg(
        children=(
            Shape (
                id="mypath",
                geometry = Path (
                    children = (
                        MoveTo(target = Point(x = 30, y = 50,), representation = 'm',),
                        LineTo(target = Point(x = 70, y = 30,), representation = 'l',),
                        LineTo(target = Point(x = 70, y = 40,), representation = 'v',),
                        LineTo(target = Point(x = 80, y = 40,), representation = 'h',),
                        ClosePath(representation = 'z',),
                        LineTo(target = Point(x = 50, y = 80,), representation = 'l',),
                        QuadraticBezier(control1 = Point(x = 70, y = 110,), end = Point(x = 90, y = 80,), representation = 'q',),
                        QuadraticBezier(control1 = Point(x = 110, y = 50,), end = Point(x = 130, y = 80,), representation = 't',),
                        LineTo(target = Point(x = 50, y = 150,), representation = 'l',),
                        CubicBezier(control1 = Point(x = 90, y = 170,), control2 = Point(x = 30, y = 170,), end = Point(x = 70, y = 150,), representation = 'c',),
                        CubicBezier(control1 = Point(x = 110, y = 130,), control2 = Point(x = 50, y = 130,), end = Point(x = 90, y = 150,), representation = 's',),
                        LineTo(target = Point(x = 130, y = 170,), representation = 'l',),
                        Arc(rx = 50, ry = 40, phi = 135, large_arc_flag = 0, sweep_flag = 0, end = Point(x = 170, y = 90,), representation = 'a'),
                    ),
                ),
            ),
        ),
    ),
)

# }}}
# {{{ def test_write_absolute_canonical_base():
def test_write_absolute_canonical_base():
    writer = SvgWriter(path_coordinates = PathCoordinates.ABSOLUTE,
                       path_compactness = PathCompactness.CANONICAL,
                       path_command_set = PathCommandSet.BASE
                      )
    assert writer.write_svg_string(d) == dedent("""\
    <?xml version='1.0' encoding='UTF-8'?>
    <svg>
    <path id="mypath" d="M 30 50 L 70 30 L 70 40 L 80 40 Z L 50 80 Q 70 110 90 80 Q 110 50 130 80 L 50 150 C 90 170 30 170 70 150 C 110 130 50 130 90 150 L 130 170 A 50 40 135 0 0 170 90" />
    </svg>
    """)
# }}}
# {{{ def test_write_absolute_canonical_full():
def test_write_absolute_canonical_full():
    writer = SvgWriter(path_coordinates = PathCoordinates.ABSOLUTE,
                       path_compactness = PathCompactness.CANONICAL,
                       path_command_set = PathCommandSet.FULL
                      )
    assert writer.write_svg_string(d) == dedent("""\
    <?xml version='1.0' encoding='UTF-8'?>
    <svg>
    <path id="mypath" d="M 30 50 L 70 30 V 40 H 80 Z L 50 80 Q 70 110 90 80 T 130 80 L 50 150 C 90 170 30 170 70 150 S 50 130 90 150 L 130 170 A 50 40 135 0 0 170 90" />
    </svg>
    """)
# }}}
# {{{ def test_write_relative_canonical_base():
def test_write_relative_canonical_base():
    writer = SvgWriter(path_coordinates = PathCoordinates.RELATIVE,
                       path_compactness = PathCompactness.CANONICAL,
                       path_command_set = PathCommandSet.BASE
                      )
    assert writer.write_svg_string(d) == dedent("""\
    <?xml version='1.0' encoding='UTF-8'?>
    <svg>
    <path id="mypath" d="m 30 50 l 40 -20 l 0 10 l 10 0 z l 20 30 q 20 30 40 0 q 20 -30 40 0 l -80 70 c 40 20 -20 20 20 0 c 40 -20 -20 -20 20 0 l 40 20 a 50 40 135 0 0 40 -80" />
    </svg>
    """)
# }}}
# {{{ def test_write_keep_canonical_base():
def test_write_keep_canonical_base():
    writer = SvgWriter(path_coordinates = PathCoordinates.KEEP,
                       path_compactness = PathCompactness.CANONICAL,
                       path_command_set = PathCommandSet.BASE
                      )
    assert writer.write_svg_string(d) == dedent("""\
    <?xml version='1.0' encoding='UTF-8'?>
    <svg>
    <path id="mypath" d="m 30 50 l 40 -20 l 0 10 l 10 0 z l 20 30 q 20 30 40 0 q 20 -30 40 0 l -80 70 c 40 20 -20 20 20 0 c 40 -20 -20 -20 20 0 l 40 20 a 50 40 135 0 0 40 -80" />
    </svg>
    """)
# }}}

# {{{ document "e" for PathCompactness
e = Document(
    svg=Svg(
        children=(
            Shape (
                id="mypath",
                geometry = Path (
                    children = (
                        MoveTo(target = Point(x = 30, y = 50,), representation = 'm',),
                        LineTo(target = Point(x = 70, y = 30,), representation = 'l',),
                        LineTo(target = Point(x = 70, y = 40,), representation = 'l',),
                        LineTo(target = Point(x = 80, y = 40,), representation = 'l',),
                        ClosePath(representation = 'z',),
                        LineTo(target = Point(x = 50, y = 80,), representation = 'l',),
                        QuadraticBezier(control1 = Point(x = 70, y = 110,), end = Point(x = 90, y = 80,), representation = 'q',),
                        QuadraticBezier(control1 = Point(x = 110, y = 50,), end = Point(x = 130, y = 80,), representation = 'q',),
                        LineTo(target = Point(x = 50, y = 150,), representation = 'l',),
                        CubicBezier(control1 = Point(x = 90, y = 170,), control2 = Point(x = 30, y = 170,), end = Point(x = 70, y = 150,), representation = 'c',),
                        CubicBezier(control1 = Point(x = 110, y = 130,), control2 = Point(x = 50, y = 130,), end = Point(x = 90, y = 150,), representation = 'c',),
                        LineTo(target = Point(x = 130, y = 170,), representation = 'l',),
                        Arc(rx = 50, ry = 40, phi = 135, large_arc_flag = 0, sweep_flag = 0, end = Point(x = 170, y = 90,), representation = 'a'),
                    ),
                ),
            ),
        ),
    ),
)



# }}}
# {{{ def test_write_absolute_compact_base():
def test_write_absolute_compact_base():
    writer = SvgWriter(path_coordinates = PathCoordinates.ABSOLUTE,
                       path_compactness = PathCompactness.COMPACT,
                       path_command_set = PathCommandSet.BASE
                      )
    assert writer.write_svg_string(e) == dedent("""\
    <?xml version='1.0' encoding='UTF-8'?>
    <svg>
    <path id="mypath" d="M 30 50 70 30 70 40 80 40 Z L 50 80 Q 70 110 90 80 110 50 130 80 L 50 150 C 90 170 30 170 70 150 110 130 50 130 90 150 L 130 170 A 50 40 135 0 0 170 90" />
    </svg>
    """)
# }}}
# {{{ def test_write_relative_compact_base():
def test_write_relative_compact_base():
    writer = SvgWriter(path_coordinates = PathCoordinates.RELATIVE,
                       path_compactness = PathCompactness.COMPACT,
                       path_command_set = PathCommandSet.BASE
                      )
    assert writer.write_svg_string(e) == dedent("""\
    <?xml version='1.0' encoding='UTF-8'?>
    <svg>
    <path id="mypath" d="m 30 50 40 -20 0 10 10 0 z l 20 30 q 20 30 40 0 20 -30 40 0 l -80 70 c 40 20 -20 20 20 0 40 -20 -20 -20 20 0 l 40 20 a 50 40 135 0 0 40 -80" />
    </svg>
    """)
# }}}

