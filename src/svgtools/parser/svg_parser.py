from xml.etree import ElementTree as ET
import re

from .transform_parser import parse_transform_string
from .float_list_parser import parse_float_list
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

def parse_svg_string(svg_text: str) -> Document:

    xml_root = ET.fromstring(svg_text)

    namespace = None
    if xml_root.tag == 'svg':
        pass
    else:
        match = re.match(r"^\{([^}]+)\}svg", xml_root.tag)
        if match:
            namespace = match.group(1)
        else:
            raise ValueError(f"Root element must end with 'svg', not '{xml_root.tag}'")
    return Document(
        svg=Svg(
            id = xml_root.get("id"),
            xmlnamespace = namespace,
            width = xml_root.get("width"),
            height = xml_root.get("height"),
            viewBox = parse_float_list(xml_root.get("viewBox")),
            children = _parse_xml_children(xml_root),
            transformations = parse_transform_string(xml_root.get("transform")),
        )
    )

def _parse_xml_element(xml_element: ET.Element):

    match xml_element.tag:
        case "defs":
            defs_id = xml_element.get("id")
            return Defs(id=defs_id, children=_parse_xml_children(xml_element))
        case "g":
            g_id = xml_element.get("id")
            return Group(
                    id=g_id,
                    children=_parse_xml_children(xml_element),
                    transformations=parse_transform_string(xml_element.get("transform")),
                )
        case "use":
            use_id = xml_element.get("id")
            xml_href=xml_element.get("href")
            if xml_href is None:
                raise ValueError("<use> requires a href attribute")
            return Use(id=use_id,
                       href=xml_href,
                       transformations=parse_transform_string(xml_element.get("transform")),
                      )
        case "rect":
            rect_id = xml_element.get("id")
            xml_x=xml_element.get("x", "0")
            xml_y=xml_element.get("y", "0")
            xml_width=xml_element.get("width")
            xml_height=xml_element.get("height")
            return Rect(
                id = rect_id,
                geometry=GeometryRect(
                    top_left=GeometryPoint(
                        x=float(xml_x),
                        y=float(xml_y),
                    ),
                    width=float(xml_width),
                    height=float(xml_height),
                ),
                transformations=parse_transform_string(xml_element.get("transform")),
            )
        case "circle":
            circle_id = xml_element.get("id")
            xml_cx=xml_element.get("cx", "0")
            xml_cy=xml_element.get("cy", "0")
            xml_r=xml_element.get("r")
            return Circle(
                id = circle_id,
                geometry=GeometryCircle(
                    center=GeometryPoint(
                        x=float(xml_cx),
                        y=float(xml_cy),
                    ),
                    radius=float(xml_r),
                ),
                transformations=parse_transform_string(xml_element.get("transform")),
            )
    raise NotImplementedError("can parse only defs, g, use, rect and circle yet")

def _parse_xml_children(xml_element: ET.Element) -> tuple:

    scene_children = []

    for xml_child in xml_element:
        scene_children.append(_parse_xml_element(xml_child))

    return tuple(scene_children)
