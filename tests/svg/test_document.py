
import pytest
from dataclasses import FrozenInstanceError
from svgtools.svg.document import Document
from svgtools.svg.svg import Svg

def test_document_construction():
    doc = Document(Svg(("x", 2)))
    assert doc.svg.children == ( "x", 2 )
    assert doc.svg.children[0] == "x"
    assert doc.svg.children[1] == 2

def test_documents_are_equal():
    assert Document(Svg(("y", 1))) == Document(Svg(("y", 1)))

def test_document_is_immutable():
    doc = Document(Svg(("x", 2)))
    with pytest.raises(FrozenInstanceError):
        doc.svg.children = ("x", 3)
