import pytest

from dataclasses import FrozenInstanceError
from svgtools.svg.transform.scale import Scale

def test_scale_construction():
    s = Scale(sx=3, sy=4)
    assert s.sx == 3
    assert s.sy == 4

def test_scales_are_equal():
    assert Scale(sx=3, sy=4) == Scale(sx=3, sy=4) 

def test_scale_is_immutable():
    s = Scale(sx=3, sy=4)
    with pytest.raises(FrozenInstanceError):
        s.sy = 5
