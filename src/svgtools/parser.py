from xml.etree import ElementTree as ET

from svgtools.model.scene.document import Document
from svgtools.model.scene.svg import Svg
from svgtools.model.scene.defs import Defs

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

    if xml_element.tag == "defs":
         return Defs(children=_parse_xml_children(xml_element))
    raise NotImplementedError("can parse only defs yet")

def _parse_xml_children(xml_element: ET.Element) -> tuple:

    scene_children = []

    for xml_child in xml_element:
        scene_children.append(_parse_xml_element(xml_child))

    return tuple(scene_children)
