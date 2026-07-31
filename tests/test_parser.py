import pytest

from svgtools.parser import parse_string
from svgtools.model.scene.document import Document
from svgtools.model.scene.svg import Svg
from svgtools.model.scene.defs import Defs
from svgtools.model.scene.group import Group
from svgtools.model.scene.use import Use
from svgtools.model.scene.rect import Rect
from svgtools.model.geometry.rect import Rect as GeometryRect
from svgtools.model.geometry.point import Point as GeometryPoint

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

def test_parse_defs_with_empty_group():
    svg_text_one_tag = """
    <svg>
        <defs>
            <g/>
        </defs>
    </svg>
    """
    svg_text_two_tags = """
    <svg>
        <defs>
            <g>
            </g>
        </defs>
    </svg>
    """
    d = Document(
        svg=Svg(
            children=(
                Defs(
                    children=(
                        Group(
                            children=(),
                        ),
                    ),
                ),
            ),
        ),
    )

    assert parse_string(svg_text_one_tag) == d
    assert parse_string(svg_text_two_tags) == d

def test_parse_use():
    svg_text = """
    <svg>
        <use href="#arrow"/>
    </svg>
    """
    d = Document(
        svg=Svg(
            children=(
                Use(
                    href="#arrow",
                ),
            ),
        ),
    )
    assert parse_string(svg_text) == d

def test_parse_use_without_href():
    svg_text = """
    <svg>
        <use/>
    </svg>
    """
    with pytest.raises(ValueError, match="<use> requires a href attribute"):
        parse_string(svg_text)

def test_rect():
    svg_text = """
    <svg>
        <rect x="1" y="2" width="3.5" height="4"/>
    </svg>
    """
    assert parse_string(svg_text) == Document(
        svg=Svg(
            children=(
                Rect(
                    geometry=GeometryRect(
                        top_left=GeometryPoint(
                            x=1,
                            y=2,
                        ),
                        width=3.5,
                        height=4,
                    ),
                ),
            ),
        ),
    )
