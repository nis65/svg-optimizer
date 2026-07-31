from xml.etree import ElementTree as ET

from svgtools.model.scene.document import Document
from svgtools.model.scene.svg import Svg
from svgtools.model.scene.defs import Defs

def parse_string(svg_text: str) -> Document:

    xml_root = ET.fromstring(svg_text)

    if xml_root.tag != "svg":
        raise ValueError(f"Root element must be <svg>, not '{xml_root.tag}'")

    scene_children = []

    for xml_child in xml_root:
        scene_children.append(_parse_xml_element(xml_child))

    return Document(
        svg=Svg(
            children=( tuple(scene_children) ),
        )
    )

def _parse_xml_element(xml_element: ET.Element):

    if xml_element.tag == "defs":
         return Defs(children=())
    raise NotImplementedError("can parse only defs yet")
