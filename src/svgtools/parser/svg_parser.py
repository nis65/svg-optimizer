from xml.etree import ElementTree as ET
from collections.abc import Collection
import re

from .transform_parser import parse_transform_string
from .float_list_parser import parse_float_list
from .token_lexer import TokenIterator, token_lexer, print_stderr
from .path_parser import parse_path_string
from svgtools.svg.document import Document
from svgtools.svg.svg import Svg
from svgtools.svg.defs import Defs
from svgtools.svg.group import Group
from svgtools.svg.use import Use
from svgtools.svg.shape import Shape
from svgtools.geometry.rect import Rect
from svgtools.geometry.circle import Circle
from svgtools.geometry.ellipse import Ellipse
from svgtools.geometry.path import Path
from svgtools.geometry.line import Line
from svgtools.geometry.polyline import Polyline
from svgtools.geometry.polygon import Polygon
from svgtools.geometry.point import Point

def parse_svg_string(svg_text: str) -> Document:

    xml_root = ET.fromstring(svg_text)

    # namespace needs special handling
    namespace = None
    if xml_root.tag == 'svg':
        pass
    else:
        match = re.match(r"^\{([^}]+)\}svg", xml_root.tag)
        if match:
            namespace = match.group(1)
        else:
            raise ValueError(f"Root element must end with 'svg', not '{xml_root.tag}'")
    if namespace:
        namespace_str = f"{{{namespace}}}"
    else:
        namespace_str = ""

    return Document(
        svg=Svg(
            id = xml_root.get("id"),
            xmlnamespace = namespace,
            width = xml_root.get("width"),
            height = xml_root.get("height"),
            viewBox = parse_float_list(xml_root.get("viewBox")),
            children = _parse_xml_children(xml_root, namespace_str),
            transformations = parse_transform_string(xml_root.get("transform")),
            unknown_attributes = _collect_unknown_attributes(
                xml_root, {"id", "width", "height", "viewBox", "transform"})
        )
    )

def _parse_xml_element(xml_element: ET.Element, namespace_str: str):

    tag = xml_element.tag.removeprefix(namespace_str)

    match tag:
        case "defs":
            defs_id = xml_element.get("id")
            return Defs(
                    id=defs_id, 
                    children=_parse_xml_children(xml_element, namespace_str),
                    unknown_attributes = _collect_unknown_attributes(
                        xml_element, {"id"})
                )

        case "g":
            g_id = xml_element.get("id")
            return Group(
                    id=g_id,
                    children=_parse_xml_children(xml_element, namespace_str),
                    transformations=parse_transform_string(xml_element.get("transform")),
                    unknown_attributes = _collect_unknown_attributes(
                        xml_element, {"id", "transform"})
                )
        case "use":
            use_id = xml_element.get("id")
            xml_href=xml_element.get("href")
            if xml_href is None:
                raise ValueError("<use> requires a href attribute")
            return Use(id=use_id,
                       href=xml_href,
                       transformations=parse_transform_string(xml_element.get("transform")),
                       unknown_attributes = _collect_unknown_attributes(
                           xml_element, {"id", "href", "transform"})
                      )
        case "rect":
            rect_id = xml_element.get("id")
            xml_x=xml_element.get("x", "0")
            xml_y=xml_element.get("y", "0")
            xml_width=xml_element.get("width")
            xml_height=xml_element.get("height")
            return Shape(
                id = rect_id,
                geometry=Rect(
                    top_left=Point(
                        x=float(xml_x),
                        y=float(xml_y),
                    ),
                    width=float(xml_width),
                    height=float(xml_height),
                ),
                transformations=parse_transform_string(xml_element.get("transform")),
                unknown_attributes = _collect_unknown_attributes(
                    xml_element, {"id", "x", "y", "width", "height", "transform"})
            )
        case "circle":
            circle_id = xml_element.get("id")
            xml_cx=xml_element.get("cx", "0")
            xml_cy=xml_element.get("cy", "0")
            xml_r=xml_element.get("r")
            return Shape(
                id = circle_id,
                geometry=Circle(
                    center=Point(
                        x=float(xml_cx),
                        y=float(xml_cy),
                    ),
                    radius=float(xml_r),
                ),
                transformations=parse_transform_string(xml_element.get("transform")),
                unknown_attributes = _collect_unknown_attributes(
                    xml_element, {"id", "cx", "cy", "r", "transform"})
            )
        case "ellipse":
            ellipse_id = xml_element.get("id")
            xml_cx=xml_element.get("cx", "0")
            xml_cy=xml_element.get("cy", "0")
            xml_rx=xml_element.get("rx")
            xml_ry=xml_element.get("ry")
            return Shape(
                id = ellipse_id,
                geometry=Ellipse(
                    center=Point(
                        x=float(xml_cx),
                        y=float(xml_cy),
                    ),
                    radiusx=float(xml_rx),
                    radiusy=float(xml_ry),
                ),
                transformations=parse_transform_string(xml_element.get("transform")),
                unknown_attributes = _collect_unknown_attributes(
                    xml_element, {"id", "cx", "cy", "rx", "ry", "transform"})
            )
        case "path":
            path_id = xml_element.get("id")
            p_geometry = parse_path_string(xml_element.get("d"))
            return Shape(
                id = path_id,
                geometry = p_geometry,
                transformations=parse_transform_string(xml_element.get("transform")),
                unknown_attributes = _collect_unknown_attributes(
                    xml_element, {"id", "d", "transform"})
            )

        case "line":
            line_id = xml_element.get("id")
            line_x1 = xml_element.get("x1")
            line_y1 = xml_element.get("y1")
            line_x2 = xml_element.get("x2")
            line_y2 = xml_element.get("y2")
            return Shape(
                id = line_id,
                geometry = Line(
                    start = Point(float(line_x1), float(line_y1)),
                    end   = Point(float(line_x2), float(line_y2)),
                ),
                transformations=parse_transform_string(xml_element.get("transform")),
                unknown_attributes = _collect_unknown_attributes(
                    xml_element, {"id", "x1", "y1", "x2", "y2", "transform"}),
            )

        case "polyline":
            polyline_id = xml_element.get("id")
            points_string = xml_element.get("points")
            points = _parse_poly_points(points_string, "polyline")
            return Shape(
                id = polyline_id,
                geometry = Polyline(
                    children = tuple(points)
                ),
                transformations=parse_transform_string(xml_element.get("transform")),
                unknown_attributes = _collect_unknown_attributes(
                    xml_element, {"id", "points", "transform"}),
            )

        case "polygon":
            polygon_id = xml_element.get("id")
            points_string = xml_element.get("points")
            points = _parse_poly_points(points_string, "polygon")
            return Shape(
                id = polygon_id,
                geometry = Polygon(
                    children = tuple(points)
                ),
                transformations=parse_transform_string(xml_element.get("transform")),
                unknown_attributes = _collect_unknown_attributes(
                    xml_element, {"id", "points", "transform"}),
            )

    raise NotImplementedError(f"can parse only defs, g, use, rect, circle, path, line and polyline yet, not '{tag}' in namespace '{namespace_str}'")

def _parse_poly_points(points_string: str, name: str):
    tokens = token_lexer(points_string, commands="")
    token_iterator = TokenIterator(tokens)
    points = []
    while token_iterator.has_numbers(2):
        points.append(Point(
            x = float(token_iterator.get().value),
            y = float(token_iterator.get().value),
            )
        )
    if token_iterator.peek() is not None:
        print_stderr(f"WARNING: dropping extra number {token_iterator.get().value} in {name}")
    return tuple(points)

def _parse_xml_children(xml_element: ET.Element, namespace_str: str) -> tuple:

    children = []

    for xml_child in xml_element:
        children.append(_parse_xml_element(xml_child, namespace_str))

    return tuple(children)

def _collect_unknown_attributes(xml_element: ET.Element, known_list: Collection[str]) -> dict[str, str]:

    XML_NAMESPACE="http://www.w3.org/XML/1998/namespace"
    xml_namespace_prefix = "{" + XML_NAMESPACE + "}"

    unknown_attributes = {}
    for key, value in xml_element.attrib.items():
        if key in known_list:
            continue
        if key.startswith("{"):
            if key.startswith(xml_namespace_prefix):
                key = "xml:" + key.removeprefix(xml_namespace_prefix)
            else:
                print_stderr(
                        f'WARNING: dropping attribute with unsupported namespace: {key}="{value}"'
                    )
                continue
        unknown_attributes[key] = value
    return unknown_attributes
