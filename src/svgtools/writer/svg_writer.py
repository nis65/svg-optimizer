from svgtools.model.scene.document import Document
from svgtools.model.scene.svg import Svg
#from svgtools.model.scene.defs import Defs
#from svgtools.model.scene.group import Group
#from svgtools.model.scene.use import Use
#from svgtools.model.scene.rect import Rect
#from svgtools.model.scene.circle import Circle
from svgtools.model.scene.transform import Translate, Scale
#from svgtools.model.geometry.rect import Rect as GeometryRect
#from svgtools.model.geometry.circle import Circle as GeometryCircle
#from svgtools.model.geometry.point import Point as GeometryPoint

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
        if svg.children == ():
            self._parts.append("<svg")
            self._append_attributes(svg)
            self._parts.append(" />\n")
        else:
            # indent
            raise NotImplemented("can only write empty svg")

    def _walk_element(self, element, indent: str):
        indent = INDENT + indent
        match element:
            case Defs():
                self._walk_defs(element,indent)
            #case Group():
            #    self._walk_group(element,indent)
            #case Use():
            #    self._walk_use(element,indent)
            #case Rect():
            #    self._walk_rect(element,indent)
            #case Circle():
            #    self._walk_circle(element,indent)
            case _:
                raise NotImplementedError(type(element))

    #def _walk_defs(defs: Defs, indent: str)

    def _append_attributes(self, element) -> None:
        if element.xmlnamespace:
            self._parts.append(f' xmlns="{element.xmlnamespace}"')
        if element.id:
            self._parts.append(f' id="{element.id}"')
        if element.width:
            self._parts.append(f' width="{element.width}"')
        if element.height:
            self._parts.append(f' height="{element.height}"')
        if element.viewBox:
            self._parts.append(f' viewBox="{self._numberlist_to_string(element.viewBox)}"')
        if element.transformations:
            self._parts.append(f' transform="{self._transforms_to_string(element.transformations)}"')

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


