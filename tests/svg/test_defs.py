
from dataclasses import FrozenInstanceError

import pytest

from svgtools.svg.defs import Defs


def test_defs_construction():
    d = Defs(id="defid", children=("x", 2))
    assert d.id == "defid"
    assert d.children == ( "x", 2 )
    assert d.children[0] == "x"
    assert d.children[1] == 2

def test_defs_are_equal():
    assert Defs(id="defid", children=("y", 1)) == Defs(id="defid", children=("y", 1))

def test_defs_is_immutable():
    d = Defs(id="defid", children=("x", 2))
    with pytest.raises(FrozenInstanceError):
        d.children = ("x", 3)

def test_empty_defs():
    d = Defs(children=())
    assert d.children == ()

