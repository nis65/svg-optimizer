from dataclasses import FrozenInstanceError

import pytest

from svgtools.svg.transform.affine import Affine


def test_affine_construction():
    a = Affine(a=1, b=2, c=3, d=4, e=5, f=6)
    assert a.a == 1
    assert a.b == 2
    assert a.c == 3
    assert a.d == 4
    assert a.e == 5
    assert a.f == 6

def test_affines_are_equal():
    assert ( Affine(a=1, b=2, c=3, d=4, e=5, f=6) ==
             Affine(a=1, b=2, c=3, d=4, e=5, f=6)
           )

def test_affine_is_immutable():
    a = Affine(a=1, b=2, c=3, d=4, e=5, f=6)
    with pytest.raises(FrozenInstanceError):
        a.d = 5
