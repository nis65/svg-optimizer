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
    ttext0="scale()"
    ttext1="scale(3 4 5)"
    ttext2="scale("
    ttext3="scaleX"
    ttext4="rotate"
    ttext5="scale(4.5 xz)"
    with pytest.raises(ValueError, match="scale needs 1 or 2 parameters, not"):
        parse_transform_string(ttext0)
    with pytest.raises(ValueError, match="scale needs 1 or 2 parameters, not"):
        parse_transform_string(ttext1)
    with pytest.raises(ValueError, match=escape("expected ')'")):
        parse_transform_string(ttext2)
    with pytest.raises(ValueError, match=escape("expected '('")):
        parse_transform_string(ttext3)
    with pytest.raises(ValueError, match="only scale implemented"):
        parse_transform_string(ttext4)
    with pytest.raises(ValueError, match="Expected number, found xz"):
        parse_transform_string(ttext5)

def test_parse_two_scales():
    ttext0="scale(4,5) scale(1  2  )"
    assert parse_transform_string(ttext0) == (
        Scale (sx = 4, sy = 5 ),
        Scale (sx = 1, sy = 2 ),
    )


