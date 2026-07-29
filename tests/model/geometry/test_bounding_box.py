import pytest
from dataclasses import FrozenInstanceError
from svgtools.model.geometry.bounding_box import BoundingBox
from svgtools.model.geometry.point import Point

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

def test_invalid_bounding_box_raises():
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
