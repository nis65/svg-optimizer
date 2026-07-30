
import pytest
from dataclasses import FrozenInstanceError
from svgtools.model.scene.group import Group

def test_group_construction():
    g = Group(("x", 2))
    assert g.children == ( "x", 2 )
    assert g.children[0] == "x"
    assert g.children[1] == 2

def test_groups_are_equal():
    assert Group(("y", 1)) == Group(("y", 1))

def test_group_is_immutable():
    g = Group(("x", 2))
    with pytest.raises(FrozenInstanceError):
        g.children = ("x", 3)

def test_empty_group():
    g = Group(children=())
    assert g.children == ()

