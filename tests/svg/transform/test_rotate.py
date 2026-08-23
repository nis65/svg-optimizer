from dataclasses import FrozenInstanceError

import pytest

from svgtools.svg.transform.rotate import Rotate


def test_rotate_construction():
    r = Rotate(theta=60, cx=3, cy=4)
    assert r.theta == 60
    assert r.cx == 3
    assert r.cy == 4

def test_rotates_are_equal():
    assert Rotate(theta=60, cx=3, cy=4) == Rotate(theta=60, cx=3, cy=4)

def test_rotate_is_immutable():
    r = Rotate(theta=60, cx=3, cy=4)
    with pytest.raises(FrozenInstanceError):
        r.theta = 30
