from xml.etree import ElementTree as ET

from svgtools.model.scene.document import Document
from svgtools.model.scene.svg import Svg
from svgtools.model.scene.defs import Defs
from svgtools.model.scene.group import Group
from svgtools.model.scene.use import Use
from svgtools.model.scene.rect import Rect
from svgtools.model.scene.circle import Circle
from svgtools.model.geometry.rect import Rect as GeometryRect
from svgtools.model.geometry.circle import Circle as GeometryCircle
from svgtools.model.geometry.point import Point as GeometryPoint

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
        case "rect":
            xml_x=xml_element.get("x")
            xml_y=xml_element.get("y")
            xml_width=xml_element.get("width")
            xml_height=xml_element.get("height")
            return Rect(
                geometry=GeometryRect(
                    top_left=GeometryPoint(
                        x=float(xml_x),
                        y=float(xml_y),
                    ),
                    width=float(xml_width),
                    height=float(xml_height),
                )
            )
        case "circle":
            xml_cx=xml_element.get("cx")
            xml_cy=xml_element.get("cy")
            xml_r=xml_element.get("r")
            return Circle(
                geometry=GeometryCircle(
                    center=GeometryPoint(
                        x=float(xml_cx),
                        y=float(xml_cy),
                    ),
                    radius=float(xml_r),
                )
            )
    raise NotImplementedError("can parse only defs, g, use, rect and circle yet")

def _parse_xml_children(xml_element: ET.Element) -> tuple:

    scene_children = []

    for xml_child in xml_element:
        scene_children.append(_parse_xml_element(xml_child))

    return tuple(scene_children)
