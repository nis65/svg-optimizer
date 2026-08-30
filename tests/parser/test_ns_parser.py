import pytest
from svgtools.parser.ns_parser import (
    parse_attr,
    parse_tag,
    split_clark_name,
    XML_NAMESPACE,
    SVG_NAMESPACE,
    XLINK_NAMESPACE,
)


def test_ns_parser():
    assert ("bli", "bla") == split_clark_name("{bli}bla")
    assert ("", "bla") == split_clark_name("bla")


def test_parse_tag():
    assert ("testtag", None) == parse_tag("testtag")
    assert ("testtag", SVG_NAMESPACE) == parse_tag(
        "{" + SVG_NAMESPACE + "}" + "testtag"
    )
    assert ("xml:testtag", XML_NAMESPACE) == parse_tag(
        "{" + XML_NAMESPACE + "}" + "testtag"
    )
    assert (None, "othernamespace") == parse_tag("{othernamespace}anytag")


def test_parse_attr():
    assert "testattr" == parse_attr("testattr")
    assert "xml:testattr" == parse_attr("{" + XML_NAMESPACE + "}" + "testattr")
    assert "href" == parse_attr("{" + XLINK_NAMESPACE + "}" + "href")


def test_parse_attr_warnings(capsys):
    assert None == parse_attr("{unknown_ns}any")
    captured = capsys.readouterr()
    assert "WARNING: dropping attribute {unknown_ns}any" in captured.err
    assert None == parse_attr("{" + XLINK_NAMESPACE + "}" + "anything")
    captured = capsys.readouterr()
    assert (
        "WARNING: dropping xlink attribute {http://www.w3.org/1999/xlink}anything"
        in captured.err
    )


def test_parse_attr_raises():
    with pytest.raises(ValueError):
        parse_attr("{" + SVG_NAMESPACE + "}" + "sthelse")
