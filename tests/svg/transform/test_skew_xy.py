from dataclasses import FrozenInstanceError

import pytest

from svgtools.svg.transform.skew_x import SkewX
from svgtools.svg.transform.skew_y import SkewY


def test_skew_x_construction():
    s = SkewX(theta=60)
    assert s.theta == 60


def test_skew_y_construction():
    s = SkewY(theta=60)
    assert s.theta == 60


def test_skews_are_equal():
    assert SkewX(theta=21) == SkewX(theta=21)
    assert SkewY(theta=22) == SkewY(theta=22)


def test_skews_are_immutable():
    s = SkewX(theta=60)
    with pytest.raises(FrozenInstanceError):
        s.theta = 61
    s = SkewY(theta=60)
    with pytest.raises(FrozenInstanceError):
        s.theta = 61
