import pytest

from svgtools.geometry.path import Path
from svgtools.geometry.path_elements.moveto import MoveTo

def test_path_construction():
    p = Path(children=())
    assert len(p.children) == 0

def test_path_with_moveto():
    p = Path(
            children = (
                MoveTo(
                    x = 1,
                    y = 2,
                    representation='m',
                ),
            )
        )
    assert p.children[0].x == 1
    assert p.children[0].y == 2
    assert p.children[0].representation == 'm'

def test_path_with_moveto_invalid():
    with pytest.raises(ValueError):
        p = Path(
                children = (
                    MoveTo(
                        x = 1,
                        y = 2,
                        representation='f',
                    ),
                )
            )


