import pytest

from svgtools.geometry.path import Path
from svgtools.geometry.path_elements.arc import Arc
from svgtools.geometry.path_elements.closepath import ClosePath
from svgtools.geometry.path_elements.cubicbezier import CubicBezier
from svgtools.geometry.path_elements.lineto import LineTo
from svgtools.geometry.path_elements.moveto import MoveTo
from svgtools.geometry.path_elements.quadraticbezier import QuadraticBezier
from svgtools.geometry.point import Point
from svgtools.parser.path_parser import parse_path_string
from svgtools.parser.token_lexer import Token, TokenIterator, TokenKind


def test_iterator_empty():
    tokens = []
    token_iterator = TokenIterator(tokens)
    assert token_iterator.peek() is None
    assert not token_iterator.has_numbers(1)
    assert token_iterator.get() is None
    with pytest.raises(
        RuntimeError, match="Internal Error: should not be called when no token is left"
    ):
        token_iterator.get_unwrapped()


def test_iterator_one():
    numbertoken1 = Token(kind=TokenKind.NUMBER, value=1)
    tokens = [numbertoken1]
    token_iterator = TokenIterator(tokens)
    assert token_iterator._lookahead(count=1)
    assert not token_iterator._lookahead(count=2)
    assert token_iterator.peek() == numbertoken1
    assert token_iterator.has_numbers(1)
    assert not token_iterator.has_numbers(2)
    peeked = token_iterator.peek()
    assert peeked == numbertoken1
    assert token_iterator._lookahead(count=1)
    consumed = token_iterator.get()
    assert consumed == numbertoken1
    assert not token_iterator._lookahead(count=1)
    peeked = token_iterator.peek()
    assert peeked is None
    consumed = token_iterator.get()
    assert consumed is None


def test_iterator_four():
    commandtokenx = Token(kind=TokenKind.COMMAND, value="x")
    commandtokeny = Token(kind=TokenKind.COMMAND, value="y")
    numbertoken = Token(kind=TokenKind.NUMBER, value=1)
    tokens = [commandtokenx, numbertoken, commandtokeny, numbertoken]
    token_iterator = TokenIterator(tokens)
    assert token_iterator.peek() == commandtokenx
    assert not token_iterator.has_numbers(1)
    consumed = token_iterator.get()
    assert consumed == commandtokenx
    assert token_iterator.has_numbers(1)
    assert not token_iterator.has_numbers(2)
    consumed = token_iterator.get()
    assert consumed == numbertoken
    assert not token_iterator.has_numbers(1)
    consumed = token_iterator.get()
    assert consumed == commandtokeny
    assert token_iterator.has_numbers(1)
    assert not token_iterator.has_numbers(2)


def test_lexer_exception():
    with pytest.raises(ValueError, match="Cannot lex this"):
        parse_path_string("a1 2c3+3-2 1e-e9 2")


def test_parser_does_not_start_with_command():
    with pytest.raises(ValueError, match="Expected a COMMAND, found Token"):
        parse_path_string("1 2 3")


def test_parser_not_enough_numbers():
    with pytest.raises(ValueError, match="Not enough numbers"):
        parse_path_string("M 1")
    with pytest.raises(ValueError, match="Not enough numbers"):
        parse_path_string("C 1")


def test_parser_with_mM_and_warning(capsys):
    p = parse_path_string("M 1 2 3 4 m 5 6 7")
    assert p == Path(
        children=(
            MoveTo(
                target=Point(
                    x=1,
                    y=2,
                ),
                representation="M",
            ),
            LineTo(
                target=Point(
                    x=3,
                    y=4,
                ),
                representation="L",
            ),
            MoveTo(
                target=Point(
                    x=8,
                    y=10,
                ),
                representation="m",
            ),
        )
    )
    captured = capsys.readouterr()
    assert "WARNING: dropping extra number 7 in m command" in captured.err


def test_parser_with_mM_and_lL():
    p = parse_path_string("M1 2l3 4-5-6L 7 8")
    assert p == Path(
        children=(
            MoveTo(
                target=Point(
                    x=1,
                    y=2,
                ),
                representation="M",
            ),
            LineTo(
                target=Point(
                    x=4,
                    y=6,
                ),
                representation="l",
            ),
            LineTo(
                target=Point(
                    x=-1,
                    y=0,
                ),
                representation="l",
            ),
            LineTo(
                target=Point(
                    x=7,
                    y=8,
                ),
                representation="L",
            ),
        )
    )


def test_parser_with_hH():
    p = parse_path_string("h 1 h 3 4 H 5")
    assert p == Path(
        children=(
            LineTo(
                target=Point(
                    x=1,
                    y=0,
                ),
                representation="h",
            ),
            LineTo(
                target=Point(
                    x=4,
                    y=0,
                ),
                representation="h",
            ),
            LineTo(
                target=Point(
                    x=8,
                    y=0,
                ),
                representation="h",
            ),
            LineTo(
                target=Point(
                    x=5,
                    y=0,
                ),
                representation="H",
            ),
        )
    )


def test_parser_with_vV():
    p = parse_path_string("v 1 2 V 4")
    assert p == Path(
        children=(
            LineTo(
                target=Point(
                    x=0,
                    y=1,
                ),
                representation="v",
            ),
            LineTo(
                target=Point(
                    x=0,
                    y=3,
                ),
                representation="v",
            ),
            LineTo(
                target=Point(
                    x=0,
                    y=4,
                ),
                representation="V",
            ),
        )
    )


def test_parser_with_zZ():
    p = parse_path_string("M 1 2 l 3 4 z l 5 6")
    assert p == Path(
        children=(
            MoveTo(
                target=Point(
                    x=1,
                    y=2,
                ),
                representation="M",
            ),
            LineTo(
                target=Point(
                    x=4,
                    y=6,
                ),
                representation="l",
            ),
            ClosePath(
                representation="z",
            ),
            LineTo(
                target=Point(
                    x=6,
                    y=8,
                ),
                representation="l",
            ),
        )
    )


def test_parser_with_zZ_and_warning(capsys):
    p = parse_path_string("Z 123 m 3 3")
    assert p == Path(
        children=(
            ClosePath(
                representation="Z",
            ),
            MoveTo(
                target=Point(
                    x=3,
                    y=3,
                ),
                representation="m",
            ),
        )
    )
    captured = capsys.readouterr()
    assert "WARNING: dropping extra number 123 in Z command" in captured.err


def test_parser_with_qbezier_and_warning(capsys):
    p = parse_path_string("M 1 2 q 3 4 5 6 7")
    assert p == Path(
        children=(
            MoveTo(
                target=Point(
                    x=1,
                    y=2,
                ),
                representation="M",
            ),
            QuadraticBezier(
                control1=Point(
                    x=4,
                    y=6,
                ),
                end=Point(
                    x=6,
                    y=8,
                ),
                representation="q",
            ),
        )
    )
    captured = capsys.readouterr()
    assert "WARNING: dropping extra number 7 in q command" in captured.err


def test_parser_with_qbezier_q_and_t():
    p = parse_path_string("M 1 2 q 3 4 5 6 t 7 8")
    assert p == Path(
        children=(
            MoveTo(
                target=Point(
                    x=1,
                    y=2,
                ),
                representation="M",
            ),
            QuadraticBezier(
                control1=Point(
                    x=4,
                    y=6,
                ),
                end=Point(
                    x=6,
                    y=8,
                ),
                representation="q",
            ),
            QuadraticBezier(
                control1=Point(
                    x=8,
                    y=10,
                ),
                end=Point(
                    x=13,
                    y=16,
                ),
                representation="t",
            ),
        )
    )


def test_parser_with_qbezier_q_l_and_t():
    p = parse_path_string("M 1 2 q 3 4 5 6 l 1 1 t 7 8")
    assert p == Path(
        children=(
            MoveTo(
                target=Point(
                    x=1,
                    y=2,
                ),
                representation="M",
            ),
            QuadraticBezier(
                control1=Point(
                    x=4,
                    y=6,
                ),
                end=Point(
                    x=6,
                    y=8,
                ),
                representation="q",
            ),
            LineTo(
                target=Point(
                    x=7,
                    y=9,
                ),
                representation="l",
            ),
            QuadraticBezier(
                control1=Point(
                    x=7,
                    y=9,
                ),
                end=Point(
                    x=14,
                    y=17,
                ),
                representation="t",
            ),
        )
    )


def test_parser_with_cbezier_with_c_and_s():
    p = parse_path_string("M 1 2 c 3 4 5 6 7 8 s 10 11 12 13")
    assert p == Path(
        children=(
            MoveTo(
                target=Point(
                    x=1,
                    y=2,
                ),
                representation="M",
            ),
            CubicBezier(
                control1=Point(
                    x=4,
                    y=6,
                ),
                control2=Point(x=6, y=8),
                end=Point(
                    x=8,
                    y=10,
                ),
                representation="c",
            ),
            CubicBezier(
                control1=Point(
                    x=10,
                    y=12,
                ),
                control2=Point(
                    x=18,
                    y=21,
                ),
                end=Point(
                    x=20,
                    y=23,
                ),
                representation="s",
            ),
        )
    )


def test_parser_with_cbezier_with_m_and_arc():
    p = parse_path_string("M 1 2 a 10 20 45 0 1 30 35")
    assert p == Path(
        children=(
            MoveTo(
                target=Point(
                    x=1,
                    y=2,
                ),
                representation="M",
            ),
            Arc(
                rx=10,
                ry=20,
                phi=45,
                large_arc_flag=0,
                sweep_flag=1,
                end=Point(
                    x=31,
                    y=37,
                ),
                representation="a",
            ),
        )
    )
