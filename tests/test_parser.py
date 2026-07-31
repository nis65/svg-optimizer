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

def test_parse_empty_defs_one_tag():
    svg_text_one_tag = """
    <svg>
        <defs/>
    </svg>
    """
    svg_text_two_tags = """
    <svg>
        <defs>
        </defs>
    </svg>
    """
    d = Document(
        svg=Svg(
            children=(
                Defs(
                    children=(),
                ),
            ),
        ),
    )
    assert parse_string(svg_text_one_tag) == d
    assert parse_string(svg_text_two_tags) == d
