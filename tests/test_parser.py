from svgtools.parser import parse_string

from svgtools.model.scene.document import Document
from svgtools.model.scene.svg import Svg


def test_parse_empty_svg():
    svg_text = "<svg/>"

    assert parse_string(svg_text) == Document(
        svg=Svg(
            children=(),
        )
    )
