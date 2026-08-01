
import pytest
from dataclasses import FrozenInstanceError
from svgtools.model.scene.svg import Svg

def test_svg_construction():
    svg = Svg(id="svgid", children=("x", 2))
    assert svg.id == "svgid"
    assert svg.children == ( "x", 2 )
    assert svg.children[0] == "x"
    assert svg.children[1] == 2

def test_svgs_are_equal():
    assert Svg(id="svgid", children=("y", 1)) == Svg(id="svgid", children=("y", 1))

def test_svg_is_immutable():
    svg = Svg(id="svgid", children=("x", 2))
    with pytest.raises(FrozenInstanceError):
        svg.children = ("x", 3)

def test_empty_svg():
    svg = Svg(children=())
    assert svg.children == ()

