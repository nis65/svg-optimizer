from svgtools.geometry.circle import Circle
from svgtools.geometry.ellipse import Ellipse
from svgtools.geometry.line import Line
from svgtools.geometry.path import Path
from svgtools.geometry.polygon import Polygon
from svgtools.geometry.polyline import Polyline
from svgtools.geometry.rect import Rect
from svgtools.svg.defs import Defs
from svgtools.svg.document import Document
from svgtools.svg.group import Group
from svgtools.svg.shape import Shape
from svgtools.svg.svg import Svg
from svgtools.svg.use import Use

from .path_writer import (
    PathCommandSet,
    PathCompactness,
    PathCoordinates,
    PathWriter,
)
from .transform_writer import TransformStrategy, TransformWriter
from .write_utils import number_to_string, numberlist_to_string


class SvgWriter:
    XML_HEADER = "<?xml version='1.0' encoding='UTF-8'?>\n"
    INDENT = "  "

    def __init__(
        self,
        transform_strategy: TransformStrategy = TransformStrategy.KEEP,
        path_coordinates: PathCoordinates = PathCoordinates.ABSOLUTE,
        path_compactness: PathCompactness = PathCompactness.CANONICAL,
        path_command_set: PathCommandSet = PathCommandSet.BASE,
    ):
        self._parts: list[str] = []
        self.transform_strategy = transform_strategy
        self.path_coordinates = path_coordinates
        self.path_compactness = path_compactness
        self.path_command_set = path_command_set
        self.total_aggregated_chains = 0
        self.total_aggressive_chains = 0

    @property
    def conservative_stats(self) -> tuple[int, int]:
        return (
            self.total_aggregated_chains,
            self.total_aggressive_chains,
        )

    def write_svg_string(self, document: Document) -> str:
        self._write_document(document)
        return self.XML_HEADER + "".join(self._parts)

    def _write_document(self, document: Document):
        self._walk_svg(document.svg)

    def _walk_svg(self, svg: Svg):
        self._parts.append("<svg")
        self._append_attributes(svg)
        if svg.children == ():
            self._parts.append(" />\n")
        else:
            self._parts.append(">\n")
            for child in svg.children:
                self._walk_element(child, "")
            self._parts.append("</svg>\n")

    def _walk_element(self, element, indent: str):
        match element:
            case Defs():
                self._walk_defs(element, indent)
            case Group():
                self._walk_group(element, indent)
            case Use():
                self._walk_use(element, indent)
            case Shape():
                self._walk_shape(element, indent)
            case _:  # pragma: no cover
                raise NotImplementedError(type(element))

    def _walk_group(self, group: Group, indent: str):
        self._parts.append(indent + "<g")
        self._append_attributes(group)
        if group.children == ():
            self._parts.append(" />\n")
        else:
            self._parts.append(">\n")
            for child in group.children:
                self._walk_element(child, self.INDENT + indent)
            self._parts.append(indent + "</g>\n")

    def _walk_defs(self, defs: Defs, indent: str):
        self._parts.append(indent + "<defs")
        self._append_attributes(defs)
        if defs.children == ():
            self._parts.append(" />\n")
        else:
            self._parts.append(">\n")
            for child in defs.children:
                self._walk_element(child, self.INDENT + indent)
            self._parts.append(indent + "</defs>\n")

    def _walk_use(self, use: Use, indent: str):
        self._parts.append(indent + "<use")
        self._append_attributes(use)
        self._parts.append(" />\n")

    def _walk_shape(self, shape: Shape, indent: str):
        match shape.geometry:
            case Rect():
                self._parts.append(indent + "<rect")
            case Circle():
                self._parts.append(indent + "<circle")
            case Ellipse():
                self._parts.append(indent + "<ellipse")
            case Path():
                self._parts.append(indent + "<path")
            case Line():
                self._parts.append(indent + "<line")
            case Polyline():
                self._parts.append(indent + "<polyline")
            case Polygon():
                self._parts.append(indent + "<polygon")
        self._append_attributes(shape)
        self._parts.append(" />\n")

    def _append_attributes(self, element) -> None:  # noqa: PLR0912
        if xmlnamespace := getattr(element, "xmlnamespace", None):
            self._parts.append(f' xmlns="{xmlnamespace}"')
        if element_id := getattr(element, "id", None):
            self._parts.append(f' id="{element_id}"')
        if href := getattr(element, "href", None):
            self._parts.append(f' href="{href}"')
        if geometry := getattr(element, "geometry", None):
            match geometry:
                case Rect():
                    self._parts.append(
                        f' x="{number_to_string(geometry.top_left.x)}"'
                        f' y="{number_to_string(geometry.top_left.y)}"'
                    )
                    self._parts.append(
                        f' width="{number_to_string(geometry.width)}"'
                        f' height="{number_to_string(geometry.height)}"'
                    )
                case Circle():
                    self._parts.append(
                        f' cx="{number_to_string(geometry.center.x)}"'
                        f' cy="{number_to_string(geometry.center.y)}"'
                    )
                    self._parts.append(f' r="{number_to_string(geometry.radius)}"')
                case Ellipse():
                    self._parts.append(
                        f' cx="{number_to_string(geometry.center.x)}"'
                        f' cy="{number_to_string(geometry.center.y)}"'
                    )
                    self._parts.append(
                        f' rx="{number_to_string(geometry.radiusx)}"'
                        f' ry="{number_to_string(geometry.radiusy)}"'
                    )
                case Path():
                    path_elements = geometry.children
                    pw = PathWriter(
                        path_coordinates=self.path_coordinates,
                        path_compactness=self.path_compactness,
                        path_command_set=self.path_command_set,
                    )
                    self._parts.append(
                        f' d="{pw.path_elements_to_string(path_elements)}"'
                    )
                case Line():
                    self._parts.append(
                        f' x1="{number_to_string(geometry.start.x)}"'
                        f' y1="{number_to_string(geometry.start.y)}"'
                        f' x2="{number_to_string(geometry.end.x)}"'
                        f' y2="{number_to_string(geometry.end.y)}"'
                    )
                case Polyline() | Polygon():
                    self._parts.append(
                        f' points="{self._polypoints_to_string(geometry.children)}"'
                    )
                case _:  # pragma: no cover
                    raise NotImplementedError(
                        "I know nothing but Rects, Circles, Ellipses, Lines, Polylines, Polygons and Paths"
                    )
        if width := getattr(element, "width", None):
            self._parts.append(f' width="{number_to_string(width)}"')
        if height := getattr(element, "height", None):
            self._parts.append(f' height="{number_to_string(height)}"')
        if viewBox := getattr(element, "viewBox", None):
            self._parts.append(f' viewBox="{numberlist_to_string(viewBox)}"')
        if transformations := getattr(element, "transformations", None):
            # output_transformations = self._transformations_to_write(transformations)
            tw = TransformWriter(self.transform_strategy)
            output_transformations = tw.apply(transformations)
            self.total_aggregated_chains += tw.total_aggregated_chains
            self.total_aggressive_chains += tw.total_aggressive_chains
            self._parts.append(
                f' transform="{tw.transforms_to_string(output_transformations)}"'
            )
        for key, value in sorted(element.unknown_attributes.items()):
            self._parts.append(f' {key}="{value}"')

    @staticmethod
    def _polypoints_to_string(polypoints):
        result = ""
        for point in polypoints:
            coords = (point.x, point.y)
            result += f"{numberlist_to_string(coords)} "
        return result.strip()
