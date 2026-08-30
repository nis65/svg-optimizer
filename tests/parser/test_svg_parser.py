import pytest

from svgtools.geometry.circle import Circle
from svgtools.geometry.ellipse import Ellipse
from svgtools.geometry.line import Line
from svgtools.geometry.path import Path
from svgtools.geometry.path_elements.lineto import LineTo
from svgtools.geometry.path_elements.moveto import MoveTo
from svgtools.geometry.point import Point
from svgtools.geometry.polygon import Polygon
from svgtools.geometry.polyline import Polyline
from svgtools.geometry.rect import Rect
from svgtools.parser.svg_parser import parse_svg_string
from svgtools.svg.defs import Defs
from svgtools.svg.document import Document
from svgtools.svg.group import Group
from svgtools.svg.shape import Shape
from svgtools.svg.svg import Svg
from svgtools.svg.transform import Rotate, Scale, Translate
from svgtools.svg.use import Use


def test_parse_empty_svg():
    svg_text = "<svg/>"

    assert parse_svg_string(svg_text) == Document(
        svg=Svg(
            children=(),
        )
    )


def test_parse_empty_svg_with_id():
    svg_text = """
    <svg id="svgid">
    </svg>
    """
    assert parse_svg_string(svg_text) == Document(
        svg=Svg(
            id="svgid",
            children=(),
        )
    )


def test_parse_empty_svg_with_transform():
    svg_text = """
    <svg transform="translate(4 5)">
    </svg>
    """
    assert parse_svg_string(svg_text) == Document(
        svg=Svg(children=(), transformations=(Translate(dx=4, dy=5),))
    )


def test_parse_empty_svg_with_all_other_attrs():
    svg_text = """
    <svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024" xml:space="preserve">
    </svg>
    """
    assert parse_svg_string(svg_text) == Document(
        svg=Svg(
            children=(),
            transformations=(),
            xmlnamespace="http://www.w3.org/2000/svg",
            width="1024",
            height="1024",
            viewBox=(
                0,
                0,
                1024,
                1024,
            ),
            unknown_attributes={"xml:space": "preserve"},
        )
    )


def test_parse_svg_with_unknown_name_space_attribute(capsys):
    svg_text = """
    <svg xmlns="http://www.w3.org/2000/svg" xmlns:foo="http://i-dont-exist.com/">
       <rect foo:attr="hello" x="10" y="20" width="100" height="50" />
    </svg>
    """
    assert parse_svg_string(svg_text) == Document(
        svg=Svg(
            children=(
                Shape(
                    geometry=Rect(
                        top_left=Point(
                            x=10,
                            y=20,
                        ),
                        width=100,
                        height=50,
                    ),
                ),
            ),
            transformations=(),
            xmlnamespace="http://www.w3.org/2000/svg",
        )
    )
    captured = capsys.readouterr()
    assert "WARNING: dropping attribute {http://i-dont-exist.com/}attr" in captured.err


def test_parse_svg_with_namespace_and_rect():
    svg_text = """
    <svg xmlns="http://www.w3.org/2000/svg">
    <rect width="2" height="3" />
    </svg>
    """
    assert parse_svg_string(svg_text) == Document(
        svg=Svg(
            children=(
                Shape(
                    geometry=Rect(
                        top_left=Point(
                            x=0,
                            y=0,
                        ),
                        width=2,
                        height=3,
                    ),
                ),
            ),
            transformations=(),
            xmlnamespace="http://www.w3.org/2000/svg",
        )
    )


def test_root_element_must_be_svg():
    with pytest.raises(ValueError, match="Root element must be 'svg'"):
        parse_svg_string("<circle/>")


def test_parse_empty_svg_with_unknowns():
    svg_text = """
    <svg unknown="unknown_value" other="another_one">
    </svg>
    """
    assert parse_svg_string(svg_text) == Document(
        svg=Svg(
            children=(),
            unknown_attributes={
                "unknown": "unknown_value",
                "other": "another_one",
            },
        )
    )


def test_parse_svg_with_unknown_tag():
    svg_text = """
    <svg>
    <unknown />
    </svg>
    """
    with pytest.raises(NotImplementedError, match="can parse only defs, g, use, rect,"):
        parse_svg_string(svg_text)


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
    assert parse_svg_string(svg_text_one_tag) == d_one
    assert parse_svg_string(svg_text_two_tags) == d_two


def test_parse_empty_defs_with_unknowns():
    svg_text = """
    <svg>
        <defs unknown="unknown_value"/>
    </svg>
    """
    d = Document(
        svg=Svg(
            children=(
                Defs(
                    children=(),
                    unknown_attributes={
                        "unknown": "unknown_value",
                    },
                ),
            ),
        ),
    )
    assert parse_svg_string(svg_text) == d


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

    assert parse_svg_string(svg_text_one_tag) == d_one
    assert parse_svg_string(svg_text_two_tags) == d_two


def test_parse_empty_group_with_unknowns():
    svg_text = """
    <svg>
        <g unknown="unknown_value" />
    </svg>
    """
    d = Document(
        svg=Svg(
            children=(
                Group(
                    children=(),
                    unknown_attributes={
                        "unknown": "unknown_value",
                    },
                ),
            ),
        )
    )
    assert parse_svg_string(svg_text) == d


def test_parse_group_with_elements_and_transform():
    svg_text = """
    <svg>
        <g transform="scale(3)">
            <circle cx="1" cy="2" r="3.5"/>
            <use href="#arrow"/>
            <rect x="1" y="2" width="3.5" height="4"/>
        </g>
    </svg>
    """
    assert parse_svg_string(svg_text) == Document(
        svg=Svg(
            children=(
                Group(
                    children=(
                        Shape(
                            geometry=Circle(
                                center=Point(
                                    x=1,
                                    y=2,
                                ),
                                radius=3.5,
                            ),
                        ),
                        Use(
                            href="#arrow",
                            x=0,
                            y=0,
                        ),
                        Shape(
                            geometry=Rect(
                                top_left=Point(
                                    x=1,
                                    y=2,
                                ),
                                width=3.5,
                                height=4,
                            ),
                        ),
                    ),
                    transformations=(Scale(sx=3, sy=3),),
                ),
            ),
        ),
    )


def test_parse_use():
    svg_text = """
    <svg>
        <use id="useid" href="#arrow" x="3" y="4" transform="scale(3)"/>
    </svg>
    """
    d = Document(
        svg=Svg(
            children=(
                Use(
                    id="useid",
                    href="#arrow",
                    x=3,
                    y=4,
                    transformations=(Scale(sx=3, sy=3),),
                ),
            ),
        ),
    )
    assert parse_svg_string(svg_text) == d


def test_parse_use_with_unkonwns():
    svg_text = """
    <svg>
        <use id="useid" href="#arrow" unknown="unknown_value"/>
    </svg>
    """
    d = Document(
        svg=Svg(
            children=(
                Use(
                    id="useid",
                    href="#arrow",
                    x=0,
                    y=0,
                    unknown_attributes={
                        "unknown": "unknown_value",
                    },
                ),
            ),
        ),
    )
    assert parse_svg_string(svg_text) == d


def test_parse_use_with_xlink_href():
    svg_text = """
    <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">
        <use xlink:href="#myref"/>
    </svg>
    """
    d = Document(
        svg=Svg(
            xmlnamespace="http://www.w3.org/2000/svg",
            children=(
                Use(
                    href="#myref",
                    x=0,
                    y=0,
                ),
            ),
        ),
    )
    assert parse_svg_string(svg_text) == d


def test_parse_use_without_href():
    svg_text = """
    <svg>
        <use/>
    </svg>
    """
    with pytest.raises(ValueError, match="<use> requires a href attribute"):
        parse_svg_string(svg_text)


def test_rect():
    svg_text = """
    <svg>
        <rect id="rectid" x="1" y="2" width="3.5" height="4" transform="scale(2)"/>
    </svg>
    """
    assert parse_svg_string(svg_text) == Document(
        svg=Svg(
            children=(
                Shape(
                    id="rectid",
                    geometry=Rect(
                        top_left=Point(
                            x=1,
                            y=2,
                        ),
                        width=3.5,
                        height=4,
                    ),
                    transformations=(Scale(sx=2, sy=2),),
                ),
            ),
        ),
    )


def test_rect_with_defaults_and_unknowns():
    svg_text = """
    <svg>
        <rect id="rectid" width="3.5" height="4" transform="scale(2)" unknown="unknown_value"/>
    </svg>
    """
    assert parse_svg_string(svg_text) == Document(
        svg=Svg(
            children=(
                Shape(
                    id="rectid",
                    geometry=Rect(
                        top_left=Point(
                            x=0,
                            y=0,
                        ),
                        width=3.5,
                        height=4,
                    ),
                    transformations=(Scale(sx=2, sy=2),),
                    unknown_attributes={
                        "unknown": "unknown_value",
                    },
                ),
            ),
        ),
    )


def test_circle():

    svg_text = """
    <svg>
        <circle id="circleid" cx="1" cy="2" r="3.5" transform="scale(13 10)"/>
    </svg>
    """
    assert parse_svg_string(svg_text) == Document(
        svg=Svg(
            children=(
                Shape(
                    id="circleid",
                    geometry=Circle(
                        center=Point(
                            x=1,
                            y=2,
                        ),
                        radius=3.5,
                    ),
                    transformations=(Scale(sx=13, sy=10),),
                ),
            ),
        ),
    )


def test_circle_with_default_and_unknowns():

    svg_text = """
    <svg>
        <circle id="circleid" r="3.5" transform="rotate(30) scale(13)" unknown="unknown_value"/>
    </svg>
    """
    assert parse_svg_string(svg_text) == Document(
        svg=Svg(
            children=(
                Shape(
                    id="circleid",
                    geometry=Circle(
                        center=Point(
                            x=0,
                            y=0,
                        ),
                        radius=3.5,
                    ),
                    transformations=(
                        Rotate(theta=30, cx=0, cy=0),
                        Scale(sx=13, sy=13),
                    ),
                    unknown_attributes={
                        "unknown": "unknown_value",
                    },
                ),
            ),
        ),
    )


def test_ellipse():

    svg_text = """
    <svg>
        <ellipse id="eid" cx="1" cy="2" rx="3.5" ry="2.5" transform="scale(13 10)"/>
    </svg>
    """
    assert parse_svg_string(svg_text) == Document(
        svg=Svg(
            children=(
                Shape(
                    id="eid",
                    geometry=Ellipse(
                        center=Point(
                            x=1,
                            y=2,
                        ),
                        radiusx=3.5,
                        radiusy=2.5,
                    ),
                    transformations=(Scale(sx=13, sy=10),),
                ),
            ),
        ),
    )


def test_path():
    svg_text = """
    <svg>
        <path id="mypath" d="m 3 4 l 5+6" transform="rotate(30) scale(13)" unknown="unknown_value"/>
    </svg>
    """
    assert parse_svg_string(svg_text) == Document(
        svg=Svg(
            children=(
                Shape(
                    id="mypath",
                    geometry=Path(
                        children=(
                            MoveTo(
                                target=Point(
                                    x=3,
                                    y=4,
                                ),
                                representation="m",
                            ),
                            LineTo(
                                target=Point(
                                    x=8,
                                    y=10,
                                ),
                                representation="l",
                            ),
                        )
                    ),
                    transformations=(
                        Rotate(theta=30, cx=0, cy=0),
                        Scale(sx=13, sy=13),
                    ),
                    unknown_attributes={
                        "unknown": "unknown_value",
                    },
                ),
            ),
        ),
    )


def test_line():

    svg_text = """
    <svg>
        <line id="myline" x1="4" y1="5" x2="7" y2="8" transform="rotate(30) scale(13)" unknown="unknown_value"/>
    </svg>
    """
    assert parse_svg_string(svg_text) == Document(
        svg=Svg(
            children=(
                Shape(
                    id="myline",
                    geometry=Line(
                        start=Point(
                            x=4,
                            y=5,
                        ),
                        end=Point(
                            x=7,
                            y=8,
                        ),
                    ),
                    transformations=(
                        Rotate(theta=30, cx=0, cy=0),
                        Scale(sx=13, sy=13),
                    ),
                    unknown_attributes={
                        "unknown": "unknown_value",
                    },
                ),
            ),
        ),
    )


def test_polyline():

    svg_text = """
    <svg>
        <polyline id="mypoly" points="1 2 3 4 5 6 7" transform="rotate(30) scale(13)" unknown="unknown_value"/>
    </svg>
    """
    assert parse_svg_string(svg_text) == Document(
        svg=Svg(
            children=(
                Shape(
                    id="mypoly",
                    geometry=Polyline(
                        children=(
                            Point(
                                x=1,
                                y=2,
                            ),
                            Point(
                                x=3,
                                y=4,
                            ),
                            Point(
                                x=5,
                                y=6,
                            ),
                        ),
                    ),
                    transformations=(
                        Rotate(theta=30, cx=0, cy=0),
                        Scale(sx=13, sy=13),
                    ),
                    unknown_attributes={
                        "unknown": "unknown_value",
                    },
                ),
            ),
        ),
    )


def test_polygon():

    svg_text = """
    <svg>
        <polygon id="mypoly" points="1 2 3 4 5 6 7" transform="rotate(30) scale(13)" unknown="unknown_value"/>
    </svg>
    """
    assert parse_svg_string(svg_text) == Document(
        svg=Svg(
            children=(
                Shape(
                    id="mypoly",
                    geometry=Polygon(
                        children=(
                            Point(
                                x=1,
                                y=2,
                            ),
                            Point(
                                x=3,
                                y=4,
                            ),
                            Point(
                                x=5,
                                y=6,
                            ),
                        ),
                    ),
                    transformations=(
                        Rotate(theta=30, cx=0, cy=0),
                        Scale(sx=13, sy=13),
                    ),
                    unknown_attributes={
                        "unknown": "unknown_value",
                    },
                ),
            ),
        ),
    )
