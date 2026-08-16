
import pytest
from dataclasses import FrozenInstanceError
from svgtools.svg.use import Use
from svgtools.svg.transform import Translate, Scale

def test_use_construction():
    u = Use(id="useid", href="#abcde")
    assert u.href == "#abcde"
    assert u.transformations == ()
    assert u.id == "useid"

def test_use_transformations():
    u = Use(href="#ref", transformations = ( Scale ( 2, 3)) )
    assert u.transformations == ( Scale ( 2, 3) )

def test_use_id_optional():
    u = Use(href="#abcde")

def test_uses_are_equal():
    assert Use(id="useid", href="#abcd") == Use(id="useid", href='#abcd')

def test_use_is_immutable():
    u = Use(id="useid", href="#abcde")
    with pytest.raises(FrozenInstanceError):
        u.href = "#newref"

