from re import escape
import pytest

from svgtools.parser.transform_parser import parse_transform_string
from svgtools.model.scene.transform import Translate, Scale

def test_parse_empty_transform():
    ttext0=""
    ttext1=None
    assert parse_transform_string(ttext0) == ()
    assert parse_transform_string(ttext1) == ()

def test_parse_scale_transform():
    ttext0="scale(3)"
    ttext1="scale(4,5)"
    assert parse_transform_string(ttext0) == (Scale (sx = 3, sy = 3 ),)
    assert parse_transform_string(ttext0)[0] == Scale (sx = 3, sy = 3 )
    assert parse_transform_string(ttext1)[0] == Scale (sx = 4, sy = 5 )

def test_parse_invalid_syntax_transform():
    text_no_closing="scale("
    text_no_opening="scaleX"
    text_not_implemented="rotate"
    text_invalid_number="scale(4.5 xz)"
    with pytest.raises(ValueError, match=escape("expected ')'")):
        parse_transform_string(text_no_closing)
    with pytest.raises(ValueError, match=escape("expected '('")):
        parse_transform_string(text_no_opening)
    with pytest.raises(ValueError, match="only scale and translate supported"):
        parse_transform_string(text_not_implemented)
    with pytest.raises(ValueError, match="Expected number, found xz"):
        parse_transform_string(text_invalid_number)

def test_parse_invalid_scale_semantics():
    ttext0="scale()"
    ttext1="scale(3 4 5)"
    with pytest.raises(ValueError, match="scale needs 1 or 2 parameters, not"):
        parse_transform_string(ttext0)
    with pytest.raises(ValueError, match="scale needs 1 or 2 parameters, not"):
        parse_transform_string(ttext1)

def test_parse_two_scales():
    ttext0="scale(4,5) scale(1  2  )"
    assert parse_transform_string(ttext0) == (
        Scale (sx = 4, sy = 5 ),
        Scale (sx = 1, sy = 2 ),
    )

def test_parse_translate_transform():
    ttext0="translate(15 12)"
    assert parse_transform_string(ttext0) == (Translate (dx = 15, dy = 12),)

def test_parse_invalid_translate_semantics():
    ttext0="translate(1)"
    ttext1="translate(3 4 5)"
    with pytest.raises(ValueError, match="translate needs exactly 2 parameters, not"):
        parse_transform_string(ttext0)
    with pytest.raises(ValueError, match="translate needs exactly 2 parameters, not"):
        parse_transform_string(ttext1)

def test_parse_3_transforms():
    ttext0="scale(4,5) translate (  3 ,  7  ) scale(  1  2  )"
    assert parse_transform_string(ttext0) == (
        Scale (sx = 4, sy = 5 ),
        Translate (dx = 3, dy = 7 ),
        Scale (sx = 1, sy = 2 ),
    )
