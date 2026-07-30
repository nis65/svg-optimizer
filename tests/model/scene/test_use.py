
import pytest
from dataclasses import FrozenInstanceError
from svgtools.model.scene.use import Use

def test_use_construction():
    u = Use("abcde")
    assert u.href == "abcde"

def test_uses_are_equal():
    assert Use("abcd") == Use('abcd')

def test_use_is_immutable():
    u = Use("abcde")
    with pytest.raises(FrozenInstanceError):
        u.href = "newref"

