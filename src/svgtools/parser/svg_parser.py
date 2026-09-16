from collections.abc import Callable, Collection
from typing import TypedDict
from xml.etree import ElementTree as ET

from svgtools.geometry import Circle, Ellipse, Line, Point, Polygon, Polyline, Rect
from svgtools.svg import (
    Defs,
    Group,
    PreservedSubtree,
    Shape,
    SvgChildren,
    Use,
)
from svgtools.svg.document import Document
from svgtools.svg.svg import Svg

from .float_list_parser import parse_float_list
from .ns_parser import (
    SVG_NAMESPACE,
    XLINK_NAMESPACE,
    parse_attr,
    parse_tag,
)
from .parse_utils import print_stderr
from .path_parser import parse_path_string
from .token_lexer import TokenIterator, token_lexer
from .transform_parser import parse_transform_string

type AttributeGetter = Callable[[ET.Element], str]
type OptionalAttributeGetter = Callable[[ET.Element], str | None]


def _get_convert_href(xml_element: ET.Element) -> str | None:
    xml_href = xml_element.get("href")
    if xml_href is None:
        xml_href = xml_element.get("{" + XLINK_NAMESPACE + "}href")
    return xml_href


def _get_convert_mandatory_href(xml_element: ET.Element) -> str:
    xml_href = _get_convert_href(xml_element)
    if xml_href is None:
        raise ValueError(f"<{xml_element.tag}> requires a href attribute")
    return xml_href


# defines all tags to parse and all their attributes, but
# NOT the children and NOT the preserved_attributes


class DefsAttributes(TypedDict):
    id: OptionalAttributeGetter


_DEFS_ATTRIBUTES: DefsAttributes = {"id": lambda element: element.get("id")}


class GroupAttributes(TypedDict):
    id: OptionalAttributeGetter
    href: OptionalAttributeGetter
    transform: OptionalAttributeGetter


_GROUP_ATTRIBUTES: GroupAttributes = {
    "id": lambda element: element.get("id"),
    "href": _get_convert_href,
    "transform": lambda element: element.get("transform"),
}


class UseAttributes(TypedDict):
    id: OptionalAttributeGetter
    href: AttributeGetter
    x: AttributeGetter
    y: AttributeGetter
    transform: OptionalAttributeGetter


_USE_ATTRIBUTES: UseAttributes = {
    "id": lambda element: element.get("id"),
    "href": _get_convert_mandatory_href,
    "x": lambda element: _get_with_default(element, "x", "0"),
    "y": lambda element: _get_with_default(element, "y", "0"),
    "transform": lambda element: element.get("transform"),
}


class RectAttributes(TypedDict):
    id: OptionalAttributeGetter
    x: AttributeGetter
    y: AttributeGetter
    width: AttributeGetter
    height: AttributeGetter
    transform: OptionalAttributeGetter


_RECT_ATTRIBUTES: RectAttributes = {
    "id": lambda element: element.get("id"),
    "x": lambda element: _get_with_default(element, "x", "0"),
    "y": lambda element: _get_with_default(element, "y", "0"),
    "width": lambda element: _get_required(element, "width"),
    "height": lambda element: _get_required(element, "height"),
    "transform": lambda element: element.get("transform"),
}


class CircleAttributes(TypedDict):
    id: OptionalAttributeGetter
    cx: AttributeGetter
    cy: AttributeGetter
    r: AttributeGetter
    transform: OptionalAttributeGetter


_CIRCLE_ATTRIBUTES: CircleAttributes = {
    "id": lambda element: element.get("id"),
    "cx": lambda element: _get_with_default(element, "cx", "0"),
    "cy": lambda element: _get_with_default(element, "cy", "0"),
    "r": lambda element: _get_required(element, "r"),
    "transform": lambda element: element.get("transform"),
}


class EllipseAttributes(TypedDict):
    id: OptionalAttributeGetter
    cx: AttributeGetter
    cy: AttributeGetter
    rx: AttributeGetter
    ry: AttributeGetter
    transform: OptionalAttributeGetter


_ELLIPSE_ATTRIBUTES: EllipseAttributes = {
    "id": lambda element: element.get("id"),
    "cx": lambda element: _get_with_default(element, "cx", "0"),
    "cy": lambda element: _get_with_default(element, "cy", "0"),
    "rx": lambda element: _get_required(element, "rx"),
    "ry": lambda element: _get_required(element, "ry"),
    "transform": lambda element: element.get("transform"),
}


class PathAttributes(TypedDict):
    id: OptionalAttributeGetter
    d: AttributeGetter
    transform: OptionalAttributeGetter


_PATH_ATTRIBUTES: PathAttributes = {
    "id": lambda element: element.get("id"),
    "d": lambda element: _get_required(element, "d"),
    "transform": lambda element: element.get("transform"),
}


class LineAttributes(TypedDict):
    id: OptionalAttributeGetter
    x1: AttributeGetter
    y1: AttributeGetter
    x2: AttributeGetter
    y2: AttributeGetter
    transform: OptionalAttributeGetter


_LINE_ATTRIBUTES: LineAttributes = {
    "id": lambda element: element.get("id"),
    "x1": lambda element: _get_required(element, "x1"),
    "y1": lambda element: _get_required(element, "y1"),
    "x2": lambda element: _get_required(element, "x2"),
    "y2": lambda element: _get_required(element, "y2"),
    "transform": lambda element: element.get("transform"),
}


class PolyAttributes(TypedDict):
    id: OptionalAttributeGetter
    points: AttributeGetter
    transform: OptionalAttributeGetter


_POLY_ATTRIBUTES: PolyAttributes = {
    "id": lambda element: element.get("id"),
    "points": lambda element: _get_required(element, "points"),
    "transform": lambda element: element.get("transform"),
}


def parse_svg_string(svg_text: str) -> Document:

    xml_root = ET.fromstring(svg_text)

    # namespace needs special handling
    root_tag, namespace = parse_tag(xml_root.tag)
    if (namespace == SVG_NAMESPACE or namespace is None) and root_tag == "svg":
        pass
    else:
        raise ValueError(
            f"Root element must be 'svg', not '{root_tag}' in namespace {namespace}"
        )

    return Document(
        svg=Svg(
            id=xml_root.get("id"),
            xmlnamespace=namespace,
            width=xml_root.get("width"),
            height=xml_root.get("height"),
            viewBox=parse_float_list(xml_root.get("viewBox")),
            children=_parse_xml_children(xml_root),
            transformations=parse_transform_string(xml_root.get("transform")),
            preserved_attributes=_collect_preserved_attributes(
                xml_root, {"id", "width", "height", "viewBox", "transform"}
            ),
        )
    )


def _get_required(xml_element: ET.Element, name: str) -> str:
    value = xml_element.get(name)
    if value is None:
        raise ValueError(f"<{xml_element.tag}> requires a {name} attribute")
    return value


def _get_with_default(xml_element: ET.Element, name: str, default: str) -> str:
    value = xml_element.get(name)
    if value is None:
        value = default
    return value


def _parse_xml_element(xml_element: ET.Element) -> SvgChildren | None:  # noqa: PLR0911 PLR0912

    tag, namespace = parse_tag(xml_element.tag)
    if namespace == SVG_NAMESPACE or namespace is None:
        pass
    else:
        print_stderr(f"WARNING: dropping tag {xml_element.tag}")
        return None

    match tag:
        case "defs":
            getters = _DEFS_ATTRIBUTES
            return Defs(
                id=getters["id"](xml_element),
                children=_parse_xml_children(xml_element),
                preserved_attributes=_collect_preserved_attributes(
                    xml_element, getters.keys()
                ),
            )
        case "g" | "a":
            getters = _GROUP_ATTRIBUTES
            return Group(
                id=getters["id"](xml_element),
                href=getters["href"](xml_element),
                children=_parse_xml_children(xml_element),
                transformations=parse_transform_string(
                    getters["transform"](xml_element)
                ),
                preserved_attributes=_collect_preserved_attributes(
                    xml_element, getters.keys()
                ),
            )
        case "use":
            getters = _USE_ATTRIBUTES
            return Use(
                id=getters["id"](xml_element),
                href=getters["href"](xml_element),
                x=float(getters["x"](xml_element)),
                y=float(getters["y"](xml_element)),
                children=_parse_xml_children(xml_element),
                transformations=parse_transform_string(
                    getters["transform"](xml_element)
                ),
                preserved_attributes=_collect_preserved_attributes(
                    xml_element, getters.keys()
                ),
            )
        case "rect":
            getters = _RECT_ATTRIBUTES
            return Shape(
                id=getters["id"](xml_element),
                children=_parse_xml_children(xml_element),
                geometry=Rect(
                    top_left=Point(
                        x=float(getters["x"](xml_element)),
                        y=float(getters["y"](xml_element)),
                    ),
                    width=float(getters["width"](xml_element)),
                    height=float(getters["height"](xml_element)),
                ),
                transformations=parse_transform_string(
                    getters["transform"](xml_element)
                ),
                preserved_attributes=_collect_preserved_attributes(
                    xml_element, getters.keys()
                ),
            )
        case "circle":
            getters = _CIRCLE_ATTRIBUTES
            return Shape(
                id=getters["id"](xml_element),
                children=_parse_xml_children(xml_element),
                geometry=Circle(
                    center=Point(
                        x=float(getters["cx"](xml_element)),
                        y=float(getters["cy"](xml_element)),
                    ),
                    radius=float(getters["r"](xml_element)),
                ),
                transformations=parse_transform_string(
                    getters["transform"](xml_element)
                ),
                preserved_attributes=_collect_preserved_attributes(
                    xml_element, getters.keys()
                ),
            )
        case "ellipse":
            getters = _ELLIPSE_ATTRIBUTES
            return Shape(
                id=getters["id"](xml_element),
                children=_parse_xml_children(xml_element),
                geometry=Ellipse(
                    center=Point(
                        x=float(getters["cx"](xml_element)),
                        y=float(getters["cy"](xml_element)),
                    ),
                    radiusx=float(getters["rx"](xml_element)),
                    radiusy=float(getters["ry"](xml_element)),
                ),
                transformations=parse_transform_string(
                    getters["transform"](xml_element)
                ),
                preserved_attributes=_collect_preserved_attributes(
                    xml_element, getters.keys()
                ),
            )
        case "path":
            getters = _PATH_ATTRIBUTES
            return Shape(
                id=getters["id"](xml_element),
                children=_parse_xml_children(xml_element),
                geometry=parse_path_string(getters["d"](xml_element)),
                transformations=parse_transform_string(
                    getters["transform"](xml_element)
                ),
                preserved_attributes=_collect_preserved_attributes(
                    xml_element, getters.keys()
                ),
            )

        case "line":
            getters = _LINE_ATTRIBUTES
            return Shape(
                id=getters["id"](xml_element),
                children=_parse_xml_children(xml_element),
                geometry=Line(
                    start=Point(
                        float(getters["x1"](xml_element)),
                        float(getters["y1"](xml_element)),
                    ),
                    end=Point(
                        float(getters["x2"](xml_element)),
                        float(getters["y2"](xml_element)),
                    ),
                ),
                transformations=parse_transform_string(
                    getters["transform"](xml_element)
                ),
                preserved_attributes=_collect_preserved_attributes(
                    xml_element, getters.keys()
                ),
            )

        case "polyline":
            getters = _POLY_ATTRIBUTES
            points = _parse_poly_points(getters["points"](xml_element), "polyline")
            return Shape(
                id=getters["id"](xml_element),
                children=_parse_xml_children(xml_element),
                geometry=Polyline(children=tuple(points)),
                transformations=parse_transform_string(
                    getters["transform"](xml_element)
                ),
                preserved_attributes=_collect_preserved_attributes(
                    xml_element, getters.keys()
                ),
            )

        case "polygon":
            getters = _POLY_ATTRIBUTES
            points = _parse_poly_points(getters["points"](xml_element), "polygon")
            return Shape(
                id=getters["id"](xml_element),
                children=_parse_xml_children(xml_element),
                geometry=Polygon(children=tuple(points)),
                transformations=parse_transform_string(
                    getters["transform"](xml_element)
                ),
                preserved_attributes=_collect_preserved_attributes(
                    xml_element, getters.keys()
                ),
            )
        case _:
            return PreservedSubtree(
                ET.tostring(xml_element, encoding="unicode").strip()
            )


def _parse_poly_points(points_string: str | None, name: str) -> tuple[Point, ...]:
    tokens = token_lexer(points_string, commands="")
    token_iterator = TokenIterator(tokens)
    points: list[Point] = []
    while token_iterator.has_numbers(2):
        points.append(
            Point(
                x=float(token_iterator.get_unwrapped().value),
                y=float(token_iterator.get_unwrapped().value),
            )
        )
    if token_iterator.peek() is not None:
        print_stderr(
            f"WARNING: dropping extra number {token_iterator.get_unwrapped().value} in {name}"
        )
    return tuple(points)


def _parse_xml_children(
    xml_element: ET.Element,
) -> tuple[SvgChildren, ...]:

    children: list[SvgChildren] = []

    for xml_child in xml_element:
        child = _parse_xml_element(xml_child)
        if child:
            children.append(child)

    return tuple(children)


def _collect_preserved_attributes(
    xml_element: ET.Element, known_list: Collection[str]
) -> dict[str, str]:

    preserved_attributes: dict[str, str] = {}
    for key, value in xml_element.attrib.items():
        attr = parse_attr(key)
        if attr in known_list:
            continue
        if attr:
            preserved_attributes[attr] = value
    return preserved_attributes
