from dataclasses import FrozenInstanceError

import pytest

from svgtools.geometry.bounding_box import BoundingBox
from svgtools.geometry.point import Point


def test_bounding_box_construction():
    bbox = BoundingBox(
        min=Point(1, 2),
        max=Point(10, 20),
    )

    assert bbox.min == Point(1, 2)
    assert bbox.max == Point(10, 20)


def test_bounding_boxes_are_equal():
    assert BoundingBox(
        Point(1, 2),
        Point(10, 20),
    ) == BoundingBox(
        Point(1, 2),
        Point(10, 20),
    )


def test_bounding_box_is_immutable():
    bbox = BoundingBox(
        Point(1, 2),
        Point(10, 20),
    )
    with pytest.raises(FrozenInstanceError):
        bbox.min = Point(0, 0)


def test_invalid_bounding_box_x_raises():
    with pytest.raises(ValueError):
        BoundingBox(
            Point(10, 2),
            Point(1, 20),
        )


def test_invalid_bounding_box_y_raises():
    with pytest.raises(ValueError):
        BoundingBox(
            Point(1, 20),
            Point(10, 2),
        )


def test_include_point_inside():

    bbox = BoundingBox(
        min=Point(1, 2),
        max=Point(5, 6),
    )
    assert bbox.include(Point(3, 4)) == bbox


def test_include_point_left_outside():
    bbox = BoundingBox(
        min=Point(1, 2),
        max=Point(5, 6),
    )
    assert bbox.include(Point(0, 4)) == BoundingBox(min=Point(0, 2), max=Point(5, 6))


def test_include_point_right_outside():
    bbox = BoundingBox(
        min=Point(1, 2),
        max=Point(5, 6),
    )
    assert bbox.include(Point(6, 4)) == BoundingBox(min=Point(1, 2), max=Point(6, 6))


def test_include_point_above_outside():
    bbox = BoundingBox(
        min=Point(1, 2),
        max=Point(5, 6),
    )
    assert bbox.include(Point(3, 1)) == BoundingBox(min=Point(1, 1), max=Point(5, 6))


def test_include_point_below_outside():
    bbox = BoundingBox(
        min=Point(1, 2),
        max=Point(5, 6),
    )
    assert bbox.include(Point(3, 7)) == BoundingBox(min=Point(1, 2), max=Point(5, 7))


def test_union_identity():
    bbox = BoundingBox(
        min=Point(1, 2),
        max=Point(5, 6),
    )
    assert bbox.union(bbox) == bbox


def test_add_identity():
    bbox = BoundingBox(
        min=Point(1, 2),
        max=Point(5, 6),
    )
    assert bbox + bbox == bbox


def test_add_inner():
    bbox_big = BoundingBox(
        min=Point(1, 2),
        max=Point(11, 12),
    )
    bbox_inner = BoundingBox(
        min=Point(5, 5),
        max=Point(6, 6),
    )
    assert bbox_big + bbox_inner == bbox_big


def test_add_grow_right():
    bbox_big = BoundingBox(
        min=Point(1, 2),
        max=Point(11, 12),
    )
    bbox_right = BoundingBox(
        min=Point(5, 5),
        max=Point(20, 6),
    )
    assert bbox_big + bbox_right == BoundingBox(min=Point(1, 2), max=Point(20, 12))


def test_add_grow_left():
    bbox_big = BoundingBox(
        min=Point(1, 2),
        max=Point(11, 12),
    )
    bbox_left = BoundingBox(
        min=Point(0, 5),
        max=Point(6, 6),
    )
    assert bbox_big + bbox_left == BoundingBox(min=Point(0, 2), max=Point(11, 12))


def test_add_grow_top():
    bbox_big = BoundingBox(
        min=Point(1, 2),
        max=Point(11, 12),
    )
    bbox_top = BoundingBox(
        min=Point(5, 1),
        max=Point(6, 6),
    )
    assert bbox_big + bbox_top == BoundingBox(min=Point(1, 1), max=Point(11, 12))


def test_add_grow_bottom():
    bbox_big = BoundingBox(
        min=Point(1, 2),
        max=Point(11, 12),
    )
    bbox_bottom = BoundingBox(
        min=Point(5, 5),
        max=Point(6, 13),
    )
    assert bbox_big + bbox_bottom == BoundingBox(min=Point(1, 2), max=Point(11, 13))


def test_add_commutative():
    bbox1 = BoundingBox(
        min=Point(1, 2),
        max=Point(5, 6),
    )
    bbox2 = BoundingBox(
        min=Point(-1, 3),
        max=Point(4, 7),
    )
    assert bbox1 + bbox2 == bbox2 + bbox1
