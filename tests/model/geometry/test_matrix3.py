import pytest
from dataclasses import FrozenInstanceError

from svgtools.model.geometry.matrix3 import Matrix3

def test_matrix3_construction():
    m = Matrix3(
        1, 2, 3,
        4, 5, 6,
        7, 8, 9,
    )
    assert m.m11 == 1
    assert m.m12 == 2
    assert m.m13 == 3

    assert m.m21 == 4
    assert m.m22 == 5
    assert m.m23 == 6

    assert m.m31 == 7
    assert m.m32 == 8
    assert m.m33 == 9

def test_matrix3_equality():
    assert Matrix3(
        1, 2, 3,
        4, 5, 6,
        7, 8, 9,
    ) == Matrix3(
        1, 2, 3,
        4, 5, 6,
        7, 8, 9,
    )

def test_matrix3_is_immutable():
    m = Matrix3(
        1, 2, 3,
        4, 5, 6,
        7, 8, 9,
    )
    with pytest.raises(FrozenInstanceError):
        m.m11 = 42
