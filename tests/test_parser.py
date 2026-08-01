import pytest

from svgtools.parser import parse_string
from svgtools.model.scene.document import Document
from svgtools.model.scene.svg import Svg
from svgtools.model.scene.defs import Defs
from svgtools.model.scene.group import Group
from svgtools.model.scene.use import Use
from svgtools.model.scene.rect import Rect
from svgtools.model.scene.circle import Circle
from svgtools.model.geometry.rect import Rect as GeometryRect
from svgtools.model.geometry.circle import Circle as GeometryCircle
from svgtools.model.geometry.point import Point as GeometryPoint

def test_parse_empty_svg():
    svg_text = "<svg/>"

    assert parse_string(svg_text) == Document(
        svg=Svg(
            children=(),
        )
    )

def test_parse_empty_svg_with_id():
    svg_text = """
    <svg id="svgid">
    </svg>
    """
    assert parse_string(svg_text) == Document(
        svg=Svg(
            id="svgid",
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
        <defs id="defsid">
        </defs>
    </svg>
    """
    d_one = Document(
        svg=Svg(
            children=(
                Defs(
                    children=(),
                ),
            ),
        ),
    )
    d_two = Document(
        svg=Svg(
            children=(
                Defs(
                    id="defsid",
                    children=(),
                ),
            ),
        ),
    )
    assert parse_string(svg_text_one_tag) == d_one
    assert parse_string(svg_text_two_tags) == d_two

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
            <g id="gid">
            </g>
        </defs>
    </svg>
    """
    d_one = Document(
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

    d_two = Document(
        svg=Svg(
            children=(
                Defs(
                    children=(
                        Group(
                            id="gid",
                            children=(),
                        ),
                    ),
                ),
            ),
        ),
    )

    assert parse_string(svg_text_one_tag) == d_one
    assert parse_string(svg_text_two_tags) == d_two

def test_parse_group_with_elements():
    svg_text = """
    <svg>
        <g>
            <circle cx="1" cy="2" r="3.5"/>
            <use href="#arrow"/>
            <rect x="1" y="2" width="3.5" height="4"/>
        </g>
    </svg>
    """
    assert parse_string(svg_text) == Document(
        svg=Svg(
            children=(
                Group(
                    children=(
                        Circle(
                            geometry=GeometryCircle(
                                center=GeometryPoint(
                                    x=1,
                                    y=2,
                                ),
                                radius=3.5,
                            ),
                        ),
                        Use(
                            href="#arrow",
                        ),
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
            ),
        ),
    )

def test_parse_use():
    svg_text = """
    <svg>
        <use id="useid" href="#arrow"/>
    </svg>
    """
    d = Document(
        svg=Svg(
            children=(
                Use(
                    id="useid",
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
        <rect id="rectid" x="1" y="2" width="3.5" height="4"/>
    </svg>
    """
    assert parse_string(svg_text) == Document(
        svg=Svg(
            children=(
                Rect(
                    id="rectid",
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

def test_circle():

    svg_text = """
    <svg>
        <circle id="circleid" cx="1" cy="2" r="3.5"/>
    </svg>
    """
    assert parse_string(svg_text) == Document(
        svg=Svg(
            children=(
                Circle(
                    id="circleid",
                    geometry=GeometryCircle(
                        center=GeometryPoint(
                            x=1,
                            y=2,
                        ),
                        radius=3.5,
                    ),
                ),
            ),
        ),
    )
