from xml.etree import ElementTree as ET

from svgtools.model.scene.document import Document
from svgtools.model.scene.svg import Svg
from svgtools.model.scene.defs import Defs
from svgtools.model.scene.group import Group
from svgtools.model.scene.use import Use

def parse_string(svg_text: str) -> Document:

    xml_root = ET.fromstring(svg_text)

    if xml_root.tag != "svg":
        raise ValueError(f"Root element must be <svg>, not '{xml_root.tag}'")

    return Document(
        svg=Svg(
            children=_parse_xml_children(xml_root),
        )
    )

def _parse_xml_element(xml_element: ET.Element):

    match xml_element.tag:
        case "defs":
            return Defs(children=_parse_xml_children(xml_element))
        case "g":
            return Group(children=_parse_xml_children(xml_element))
        case "use":
            xml_href=xml_element.get("href")
            if xml_href is None:
                raise ValueError("<use> requires a href attribute")
            return Use(href=xml_href)
    raise NotImplementedError("can parse only defs, g, and use yet")

def _parse_xml_children(xml_element: ET.Element) -> tuple:

    scene_children = []

    for xml_child in xml_element:
        scene_children.append(_parse_xml_element(xml_child))

    return tuple(scene_children)
