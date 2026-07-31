from xml.etree import ElementTree as ET

from svgtools.model.scene.document import Document
from svgtools.model.scene.svg import Svg

def parse_string(svg_text: str) -> Document:

    xml_root = ET.fromstring(svg_text)

    if xml_root.tag != "svg":
        raise ValueError("Root element must be <svg>")

    scene_children = []

    for xml_child in xml_root:
        raise NotImplementedError

    return Document(
        svg=Svg(
            children=( tuple(scene_children) ),
        )
    )
