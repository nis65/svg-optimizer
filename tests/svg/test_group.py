from dataclasses import FrozenInstanceError

import pytest

from svgtools.svg.group import Group
from svgtools.svg.transform import Scale


def test_group_construction():
    g = Group(id="gid", children=("x", 2))
    assert g.id == "gid"
    assert g.transformations == ()
    assert g.children == ("x", 2)
    assert g.children[0] == "x"
    assert g.children[1] == 2


def test_group_transformations():
    g = Group(children=(), transformations=(Scale(2, 3)))
    assert g.transformations == (Scale(2, 3))


def test_groups_are_equal():
    assert Group(id="gid", children=("y", 1)) == Group(id="gid", children=("y", 1))


def test_group_is_immutable():
    g = Group(id="gid", children=("x", 2))
    with pytest.raises(FrozenInstanceError):
        g.children = ("x", 3)


def test_empty_group():
    g = Group(children=())
    assert g.children == ()
