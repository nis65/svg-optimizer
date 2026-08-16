import pytest

from dataclasses import FrozenInstanceError
from svgtools.svg.transform.translate import Translate

def test_translate_construction():
    t = Translate(dx=3, dy=4)
    assert t.dx == 3
    assert t.dy == 4

def test_translates_are_equal():
    assert Translate(dx=3, dy=4) == Translate(dx=3, dy=4)

def test_translate_is_immutable():
    t = Translate(dx=3, dy=4)
    with pytest.raises(FrozenInstanceError):
        t.dx = 4
