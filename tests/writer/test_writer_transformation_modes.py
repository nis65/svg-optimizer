
from textwrap import dedent

from svgtools.geometry.point import Point
from svgtools.geometry.rect import Rect
from svgtools.svg.document import Document
from svgtools.svg.shape import Shape
from svgtools.svg.svg import Svg
from svgtools.svg.transform import Affine, Rotate, Scale, SkewX, Translate
from svgtools.writer.svg_writer import SvgWriter
from svgtools.writer.transform_write_strategy import TransformWriteStrategy


def test_write_mode_keep():
    d = Document(
            svg=Svg(
                children=(
                    Shape(
                        id="rectid",
                        transformations=(
                             Scale(sx=4, sy=5),
                             Translate(dx=1, dy=2),
                             Rotate(theta=45, cx=1, cy=3),
                        ),
                        geometry=Rect(
                            top_left=Point(
                                x=4,
                                y=5,
                            ),
                            width=2,
                            height=1,
                        ),
                        unknown_attributes={
                            "unknown": "unknown_value",
                        }
                    ),
                )
            )
        )
    writer = SvgWriter(TransformWriteStrategy.KEEP)
    assert writer.write_svg_string(d) == dedent("""\
    <?xml version='1.0' encoding='UTF-8'?>
    <svg>
    <rect id="rectid" x="4" y="5" width="2" height="1" transform="scale(4 5) translate(1 2) rotate(45 1 3)" unknown="unknown_value" />
    </svg>
    """)

def test_write_mode_aggregate():
    d = Document(
            svg=Svg(
                children=(
                    Shape(
                        id="rectid",
                        transformations=(
                             Translate(dx=2, dy=10),
                             Translate(dx=-1, dy=2),
                             Rotate(theta=30, cx=0, cy=0),
                             Rotate(theta=30, cx=0, cy=0),
                             Rotate(theta=-10, cx=1, cy=1),
                             Scale(sx=2, sy=3),
                             Scale(sx=4, sy=2),
                             Affine(a=1, b=2, c=3, d=4, e=5, f=6),
                             Affine(a=6, b=5, c=4, d=3, e=2, f=1),
                        ),
                        geometry=Rect(
                            top_left=Point(
                                x=4,
                                y=5,
                            ),
                            width=2,
                            height=1,
                        ),
                        unknown_attributes={
                            "unknown": "unknown_value",
                        }
                    ),
                )
            )
        )
    writer = SvgWriter(TransformWriteStrategy.AGGREGATE)
    assert writer.write_svg_string(d) == dedent("""\
    <?xml version='1.0' encoding='UTF-8'?>
    <svg>
    <rect id="rectid" x="4" y="5" width="2" height="1" transform="translate(1 12) rotate(60 0 0) rotate(-10 1 1) scale(8 6) matrix(21 32 13 20 10 14)" unknown="unknown_value" />
    </svg>
    """)

def test_write_mode_decompose_matrix():
    d = Document(
            svg=Svg(
                children=(
                    Shape(
                        id="rectid",
                        transformations=(
                             Affine(a=0, b=2, c=-3, d=3, e=2, f=10),
                        ),
                        geometry=Rect(
                            top_left=Point(
                                x=4,
                                y=5,
                            ),
                            width=2,
                            height=1,
                        ),
                        unknown_attributes={
                            "unknown": "unknown_value",
                        }
                    ),
                )
            )
        )
    writer = SvgWriter(TransformWriteStrategy.DECOMPOSE_MATRIX)
    assert writer.write_svg_string(d) == dedent("""\
    <?xml version='1.0' encoding='UTF-8'?>
    <svg>
    <rect id="rectid" x="4" y="5" width="2" height="1" transform="translate(2 10) rotate(90 0 0) skewX(45) scale(2 3)" unknown="unknown_value" />
    </svg>
    """)

def test_write_mode_decompose_matrix_and_aggregate():
    d = Document(
            svg=Svg(
                children=(
                    Shape(
                        id="rectid",
                        transformations=(
                             Translate(dx=3, dy=1),
                             Affine(a=0, b=2, c=-3, d=3, e=2, f=10),
                             Scale(1,2)
                        ),
                        geometry=Rect(
                            top_left=Point(
                                x=4,
                                y=5,
                            ),
                            width=2,
                            height=1,
                        ),
                        unknown_attributes={
                            "unknown": "unknown_value",
                        }
                    ),
                )
            )
        )
    writer = SvgWriter(TransformWriteStrategy.DECOMPOSE_MATRIX_AND_AGGREGATE)
    assert writer.write_svg_string(d) == dedent("""\
    <?xml version='1.0' encoding='UTF-8'?>
    <svg>
    <rect id="rectid" x="4" y="5" width="2" height="1" transform="translate(5 11) rotate(90 0 0) skewX(45) scale(2 6)" unknown="unknown_value" />
    </svg>
    """)

def test_write_mode_canonical_conservative():
    d = Document(
            svg=Svg(
                children=(
                    Shape(
                        id="rectid",
                        transformations=(
                             Translate(dx=2, dy=10),
                             Rotate(theta=90, cx=0, cy=0),
                             SkewX(theta=45),
                             Scale(sx=2, sy=3),
                        ),
                        geometry=Rect(
                            top_left=Point(
                                x=4,
                                y=5,
                            ),
                            width=2,
                            height=1,
                        ),
                        unknown_attributes={
                            "unknown": "unknown_value",
                        }
                    ),
                )
            )
        )
    writer = SvgWriter(TransformWriteStrategy.CANONICAL_CONSERVATIVE)
    assert writer.write_svg_string(d) == dedent("""\
    <?xml version='1.0' encoding='UTF-8'?>
    <svg>
    <rect id="rectid" x="4" y="5" width="2" height="1" transform="translate(2 10) rotate(90 0 0) skewX(45) scale(2 3)" unknown="unknown_value" />
    </svg>
    """)
    assert writer.conservative_stats == (1, 0)

def test_write_mode_canonical_aggressive():
    d = Document(
            svg=Svg(
                children=(
                    Shape(
                        id="rectid",
                        transformations=(
                             Translate(dx=2, dy=10),
                             Rotate(theta=90, cx=0, cy=0),
                             SkewX(theta=45),
                             Scale(sx=2, sy=3),
                        ),
                        geometry=Rect(
                            top_left=Point(
                                x=4,
                                y=5,
                            ),
                            width=2,
                            height=1,
                        ),
                        unknown_attributes={
                            "unknown": "unknown_value",
                        }
                    ),
                )
            )
        )
    writer = SvgWriter(TransformWriteStrategy.CANONICAL_AGGRESSIVE)
    assert writer.write_svg_string(d) == dedent("""\
    <?xml version='1.0' encoding='UTF-8'?>
    <svg>
    <rect id="rectid" x="4" y="5" width="2" height="1" transform="translate(2 10) rotate(90 0 0) skewX(45) scale(2 3)" unknown="unknown_value" />
    </svg>
    """)

# Translate(dx=2, dy=10), Rotate(theta=90, cx=0, cy=0), SkewX(theta=45), Scale(sx=2, sy=3),
# <rect id="rectid" x="4" y="5" width="2" height="1" transform="matrix(0 2 -3 3 2 10)" unknown="unknown_value" />
#                        transformations=(
#                             SkewX(theta=60),
#                             SkewY(theta=30),
#                             Affine(a=1, b=2, c=3, d=4, e=5, f=6),
