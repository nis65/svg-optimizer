import pytest
from dataclasses import FrozenInstanceError

from svgtools.model.geometry.matrix3 import Matrix3
from svgtools.model.geometry.point import Point

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

def test_identity_matrix():
    assert Matrix3.identity() == Matrix3(
        1, 0, 0,
        0, 1, 0,
        0, 0, 1,
    )

def test_matrix_multiplication_not_implemented():
    m = Matrix3(
        1, 2, 3,
        4, 5, 6,
        7, 8, 9,
    )
    with pytest.raises(TypeError):
        n = m * 3.5

def test_identity_multiplication():
    m = Matrix3(
        1, 2, 3,
        4, 5, 6,
        7, 8, 9,
    )

    assert Matrix3.identity() * m == m
    assert m * Matrix3.identity() == m

def test_identity_point_multiplication():
    p = Point(3, 4)

    assert Matrix3.identity() * p == Point(3, 4)

def test_matrix_point_multiplication_translate():
    a = Matrix3(
        1, 0, 1,
        0, 1, 2,
        0, 0, 1
    )
    p = Point(3, 4)

    assert a * p == Point(4, 6)

def test_matrix_point_multiplication_scale():
    a = Matrix3(
        2, 0, 0,
        0, 3, 0,
        0, 0, 1
    )
    p = Point(3, 4)

    assert a * p == Point(6, 12)

def test_matrix_matrix_multiplication():
    a = Matrix3(
        1, 2, 3,
        4, 5, 6,
        7, 8, 9,
    )

    b = Matrix3(
        9, 8, 7,
        6, 5, 4,
        3, 2, 1,
    )

    assert a * b == Matrix3(
        30, 24, 18,
        84, 69, 54,
        138, 114, 90,
    )

def test_matrix_multiplication_is_not_commutative():
    a = Matrix3(
        1, 2, 3,
        4, 5, 6,
        7, 8, 9,
    )

    b = Matrix3(
        9, 8, 7,
        6, 5, 4,
        3, 2, 1,
    )

    assert a * b != b * a
