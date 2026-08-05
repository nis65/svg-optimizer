from svgtools.model.scene.document import Document
from svgtools.model.scene.svg import Svg
from svgtools.model.scene.defs import Defs
from svgtools.model.scene.group import Group
#from svgtools.model.scene.use import Use
from svgtools.model.scene.rect import Rect
from svgtools.model.scene.circle import Circle
from svgtools.model.scene.transform import Translate, Scale
from svgtools.model.geometry.rect import Rect as GeometryRect
from svgtools.model.geometry.circle import Circle as GeometryCircle
from svgtools.model.geometry.point import Point as GeometryPoint

class SvgWriter:

    XML_HEADER = "<?xml version='1.0' encoding='UTF-8'?>\n"
    INDENT = "  "

    def __init__(self):
        self._parts: list[str] = []

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
            #case Use():
            #    self._walk_use(element, indent)
            case Rect():
                self._walk_rect(element, indent)
            case Circle():
                self._walk_circle(element, indent)
            case _:
                raise NotImplementedError(type(element))

    def _walk_group(self, group: Group, indent: str):
        self._parts.append("<g")
        self._append_attributes(group)
        if group.children == ():
            self._parts.append(" />\n")
        else:
            raise NotImplementedError("Can parse empty group only")

    def _walk_defs(self, defs: Defs, indent: str):
        self._parts.append("<defs")
        self._append_attributes(defs)
        if defs.children == ():
            self._parts.append(" />\n")
        else:
            raise NotImplementedError("Can parse empty defs only")

    def _walk_rect(self, rect: Rect, indent:str):
        self._parts.append(indent + "<rect")
        self._append_attributes(rect)
        self._parts.append(" />\n")

    def _walk_circle(self, circle: Circle, indent:str):
        self._parts.append(indent + "<circle")
        self._append_attributes(circle)
        self._parts.append(" />\n")

    def _append_attributes(self, element) -> None:
        if xmlnamespace := getattr(element, "xmlnamespace", None):
            self._parts.append(f' xmlns="{xmlnamespace}"')
        if element_id := getattr(element, "id", None):
            self._parts.append(f' id="{element_id}"')
        if geometry := getattr(element, "geometry", None):
            match geometry:
                case GeometryRect():
                    self._parts.append(f' x="{geometry.top_left.x}" y="{geometry.top_left.y}"')
                    self._parts.append(f' width="{geometry.width}" height="{geometry.height}"')
                case GeometryCircle():
                    self._parts.append(f' cx="{geometry.center.x}" cy="{geometry.center.y}"')
                    self._parts.append(f' radius="{geometry.radius}"')
                case _:
                    raise NotImplementedError("I know nothing but Rects and Circles")
        if width := getattr(element, "width", None):
            self._parts.append(f' width="{width}"')
        if height := getattr(element, "height", None):
            self._parts.append(f' height="{height}"')
        if viewBox := getattr(element, "viewBox", None):
            self._parts.append(f' viewBox="{self._numberlist_to_string(viewBox)}"')
        if transformations := getattr(element, "transformations", None):
            self._parts.append(f' transform="{self._transforms_to_string(transformations)}"')

    @staticmethod
    def _numberlist_to_string(numbers) -> str:
        str_numbers = []
        for number in numbers:
            str_numbers.append(f'{number}')
        return " ".join(str_numbers)

    @staticmethod
    def _transforms_to_string(transformations) -> str:
        result = ""
        for trans in transformations:
            match trans:
                case Translate():
                    numberlist=(trans.dx, trans.dy, )
                    result += f' translate({SvgWriter._numberlist_to_string(numberlist)})'
                case Scale():
                    numberlist=(trans.sx, trans.sy, )
                    result += f' scale({SvgWriter._numberlist_to_string(numberlist)})'
        return result.strip()
