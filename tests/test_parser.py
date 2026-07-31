import pytest

from svgtools.parser import parse_string
from svgtools.model.scene.document import Document
from svgtools.model.scene.svg import Svg
from svgtools.model.scene.defs import Defs


def test_parse_empty_svg():
    svg_text = "<svg/>"

    assert parse_string(svg_text) == Document(
        svg=Svg(
            children=(),
        )
    )

def test_root_element_must_be_svg():
    with pytest.raises(ValueError, match="Root element must be <svg>, not"):
        parse_string("<circle/>")

def test_parse_empty_defs():
    svg_text = """
    <svg>
        <defs/>
    </svg>
    """

    assert parse_string(svg_text) == Document(
        svg=Svg(
            children=(
                Defs(
                    children=(),
                ),
            ),
        ),
    )
