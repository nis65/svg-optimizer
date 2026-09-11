from dataclasses import FrozenInstanceError

import pytest

from svgtools.svg.transform import Scale
from svgtools.svg.use import Use


def test_use_construction():
    u = Use(
        id="useid",
        href="#abcde",
        x=12,
        y=13,
        children=(),
    )
    assert u.href == "#abcde"
    assert u.transformations == ()
    assert u.id == "useid"
    assert u.x == 12
    assert u.y == 13
    assert u.children == ()


def test_use_transformations():
    u = Use(
        href="#ref",
        transformations=(Scale(2, 3)),
        x=0,
        y=0,
        children=(),
    )
    assert u.transformations == (Scale(2, 3))


def test_use_id_optional():
    u = Use(
        href="#abcde",
        x=0,
        y=0,
        children=(),
    )  # noqa: F841


def test_uses_are_equal():
    assert Use(
        id="useid",
        href="#abcd",
        x=1,
        y=2,
        children=(),
    ) == Use(
        id="useid",
        x=1,
        y=2,
        href="#abcd",
        children=(),
    )


def test_use_is_immutable():
    u = Use(
        id="useid",
        href="#abcde",
        x=0,
        y=0,
        children=(),
    )
    with pytest.raises(FrozenInstanceError):
        u.href = "#newref"
