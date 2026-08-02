
import pytest
from dataclasses import FrozenInstanceError
from svgtools.model.geometry.point import Point as GeometryPoint
from svgtools.model.geometry.circle import Circle as GeometryCircle
from svgtools.model.scene.circle import Circle
from svgtools.model.scene.transform import Translate, Scale

def test_circle_construction():
    c = Circle(id="circle",
               geometry=GeometryCircle(center=GeometryPoint(1.5, -2.0), radius=2),
               transformations=Translate ( 2, 3),
              )
    assert c.geometry.center.x == 1.5
    assert c.geometry.center.y == -2.0
    assert c.geometry.radius == 2
    assert c.id == "circle"
    assert c.transformations == Translate ( 2, 3)

def test_minimal_circle_construction():
    c = Circle(geometry=GeometryCircle(center=GeometryPoint(1.5, -2.0), radius=2))
    assert c.geometry.center.x == 1.5
    assert c.geometry.center.y == -2.0
    assert c.geometry.radius == 2
    assert c.id is None
    assert c.transformations == ()

def test_circles_are_equal():
    assert (Circle(id="circle",
                   geometry=GeometryCircle(center=GeometryPoint(1.5, -2.0), radius=2),
                   transformations=Scale(3,3)
                  ) ==
            Circle(id="circle",
                   geometry=GeometryCircle(center=GeometryPoint(1.5, -2.0), radius=2),
                   transformations=Scale(3,3)
                  )
    )

def test_circle_is_immutable():
    c = Circle(id="circle", geometry=GeometryCircle(center=GeometryPoint(1.5, -2.0), radius=2))
    with pytest.raises(FrozenInstanceError):
       c.geometry.radius = 3
