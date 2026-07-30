
import pytest
from dataclasses import FrozenInstanceError
from svgtools.model.scene.document import Document

def test_document_construction():
    doc = Document(("x", 2))
    assert doc.elements == ( "x", 2 )
    assert doc.elements[0] == "x"
    assert doc.elements[1] == 2

def test_documents_are_equal():
    assert Document(("y", 1)) == Document(("y", 1))

def test_document_is_immutable():
    doc = Document(("x", 2))
    with pytest.raises(FrozenInstanceError):
        doc.elements = ("x", 3)

def test_empty_document():
    doc = Document(elements=())
    assert doc.elements == ()

