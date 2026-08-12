from re import escape
import pytest

from svgtools.parser.transform_parser import parse_transform_string
from svgtools.model.scene.transform import Translate, Scale, Rotate, SkewX, SkewY, Affine

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
    text_not_implemented="unsupported"
    text_invalid_number="scale(4.5 xz)"
    with pytest.raises(ValueError, match=escape("expected ')'")):
        parse_transform_string(text_no_closing)
    with pytest.raises(ValueError, match=escape("expected '('")):
        parse_transform_string(text_no_opening)
    with pytest.raises(ValueError, match="not supported transformation"):
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

def test_parse_rotate_transform():
    ttext0="rotate(60)"
    ttext1="rotate(20 3 4)"
    assert parse_transform_string(ttext0) == ( Rotate(theta=60, cx=0, cy=0), )
    assert parse_transform_string(ttext1) == ( Rotate(theta=20, cx=3, cy=4), )

def test_parse_invalid_rotate_semantics():
    ttext0="rotate(60 2)"
    with pytest.raises(ValueError, match="rotate needs 1 or 3 parameters, not 2"):
        parse_transform_string(ttext0)

def test_parse_skewX():
    ttext0="skewX(60)"
    assert parse_transform_string(ttext0) == ( SkewX(theta=60,),)

def test_parse_invalid_skewX_semantics():
    ttext0="skewX(1 3)"
    with pytest.raises(ValueError, match="skewX needs exactly 1 parameter, not 2"):
         parse_transform_string(ttext0)

def test_parse_skewY():
    ttext0="skewY(60)"
    assert parse_transform_string(ttext0) == ( SkewY(theta=60,),)

def test_parse_invalid_skewY_semantics():
    ttext0="skewY(1 3)"
    with pytest.raises(ValueError, match="skewY needs exactly 1 parameter, not 2"):
        parse_transform_string(ttext0)

def test_parse_affine():
    ttext0="matrix(1 2 3 4 5 6)"
    assert parse_transform_string(ttext0) == ( Affine(a=1, b=2, c=3, d=4, e=5, f=6,),)

def test_parse_invalid_affine_semantics():
    ttext0="matrix(1 2 3)"
    with pytest.raises(ValueError, match="matrix needs exactly 6 parameters, not 3"):
        parse_transform_string(ttext0)
