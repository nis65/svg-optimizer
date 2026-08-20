import pytest
from svgtools.parser.path_parser import parse_path_string, Token, TokenKind, TokenIterator
from svgtools.geometry.point import Point
from svgtools.geometry.path import Path
from svgtools.geometry.path_elements.moveto import MoveTo
from svgtools.geometry.path_elements.lineto import LineTo

def test_iterator_empty(): 
    tokens=[]
    token_iterator = TokenIterator(tokens)
    assert token_iterator.peek() is None
    assert not token_iterator.has_numbers(1)
    assert token_iterator.get() is None

def test_iterator_one():
    numbertoken1=Token(kind = TokenKind.NUMBER, value=1)
    tokens=[numbertoken1]
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
    commandtokenx = Token(kind = TokenKind.COMMAND, value='x')
    commandtokeny = Token(kind = TokenKind.COMMAND, value='y')
    numbertoken = Token(kind = TokenKind.NUMBER, value=1)
    tokens=[ commandtokenx, numbertoken, commandtokeny, numbertoken ]
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

def test_parser_with_mM(capsys):
    p = parse_path_string("M 1 2 3 4 m 5 6 7")
    assert p == Path(
            children = (
                MoveTo(
                    target = Point(
                        x = 1,
                        y = 2,
                    ),
                    representation='M',
                ),
                LineTo(
                    target = Point(
                        x = 3,
                        y = 4,
                    ),
                    representation='L',
                ),
                MoveTo(
                    target = Point(
                        x = 8,
                        y = 10,
                    ),
                    representation='m',
                ),
            )
        )
    captured = capsys.readouterr()
    assert "WARNING: dropping extra number 7 in m command" in captured.err

def test_parser_with_mM_and_lL():
    p = parse_path_string("M1 2l3 4-5-6L 7 8")
    assert p == Path(
            children = (
                MoveTo(
                    target = Point(
                        x = 1,
                        y = 2,
                    ),
                    representation='M',
                ),
                LineTo(
                    target = Point(
                        x = 4,
                        y = 6,
                    ),
                    representation='l',
                ),
                LineTo(
                    target = Point(
                        x = -1,
                        y = 0,
                    ),
                    representation='l',
                ),
                LineTo(
                    target = Point(
                        x = 7,
                        y = 8,
                    ),
                    representation='L',
                ),
            )
        )

def test_parser_with_hH():
    p = parse_path_string("h 1 h 3 4 H 5")
    assert p == Path(
            children = (
                LineTo(
                    target = Point(
                        x = 1,
                        y = 0,
                    ),
                    representation='h',
                ),
                LineTo(
                    target = Point(
                        x = 4,
                        y = 0,
                    ),
                    representation='h',
                ),
                LineTo(
                    target = Point(
                        x = 8,
                        y = 0,
                    ),
                    representation='h',
                ),
                LineTo(
                    target = Point(
                        x = 5,
                        y = 0,
                    ),
                    representation='H',
                ),
            )
        )

def test_parser_with_vV():
    p = parse_path_string("v 1 2 V 4")
    assert p == Path(
            children = (
                LineTo(
                    target = Point(
                        x = 0,
                        y = 1,
                    ),
                    representation='v',
                ),
                LineTo(
                    target = Point(
                        x = 0,
                        y = 3,
                    ),
                    representation='v',
                ),
                LineTo(
                    target = Point(
                        x = 0,
                        y = 4,
                    ),
                    representation='V',
                ),
            )
        )

