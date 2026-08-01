from enum import Enum

from svgtools.model.geometry.bounding_box import BoundingBox
from svgtools.model.scene.document import Document
from svgtools.model.scene.svg import Svg
from svgtools.model.scene.defs import Defs
from svgtools.model.scene.group import Group
from svgtools.model.scene.use import Use
from svgtools.model.scene.rect import Rect
from svgtools.model.scene.circle import Circle

class _Phase(Enum):
    BUILD_DEFINITION_TABLE = 0
    VISIT = 1

class BoundingBoxVisitor:

    def __init__(self):

        self.bounding_box = None
        self.definition_table = {}  # Maps object ids to reusable scene elements.
        self.rectangles_visited = 0
        self.circles_visited = 0

    def visit(self, document: Document):

        self._walk_svg(document.svg, _Phase.BUILD_DEFINITION_TABLE)
        self._walk_svg(document.svg, _Phase.VISIT)

    def _accumulate_bbox(self, bbox: BoundingBox) -> None:
        if self.bounding_box is None:
            self.bounding_box = bbox
        else:
            self.bounding_box += bbox

    def _walk_svg(self, svg: Svg, phase: _Phase):

        for child in svg.children:
            self._walk_element(child, phase)

    def _walk_element(self, element, phase: _Phase):

        match element:
            case Defs():
                self._walk_defs(element,phase)
            case Group():
                self._walk_group(element,phase)
            case Use():
                self._walk_use(element,phase)
            case Rect():
                self._walk_rect(element,phase)
            case Circle():
                self._walk_circle(element,phase)
            case _:
                raise NotImplementedError(type(element))

    def _walk_group(self, group: Group, phase: _Phase):
        match phase:
            case _Phase.BUILD_DEFINITION_TABLE:
                if group.id:
                    self.definition_table[group.id] = group
            case _Phase.VISIT:
                pass
        for child in group.children:
            self._walk_element(child, phase)

    def _walk_defs(self, defs: Defs, phase: _Phase):

        match phase:
            case _Phase.BUILD_DEFINITION_TABLE:
                for child in defs.children:
                    if child.id is None:
                        raise ValueError("Definitions must have an id.")
                    self._walk_element(child, phase)
            case _Phase.VISIT:
                pass

    def _walk_use(self, use: Use, phase: _Phase):

        match phase:
            case _Phase.BUILD_DEFINITION_TABLE:
                pass
            case _Phase.VISIT:
                label = use.href.removeprefix("#")
                if label not in self.definition_table:
                    raise ValueError(f"Use references unknown label {label}")
                self._walk_element(self.definition_table[label], phase)

    def _walk_rect(self, rect: Rect, phase: _Phase):

        match phase:
            case _Phase.BUILD_DEFINITION_TABLE:
                if rect.id:
                    self.definition_table[rect.id] = rect
            case _Phase.VISIT:
                self.rectangles_visited += 1
                self._accumulate_bbox(rect.geometry.bounding_box())

    def _walk_circle(self, circle: Circle, phase: _Phase):

        match phase:
            case _Phase.BUILD_DEFINITION_TABLE:
                if circle.id:
                    self.definition_table[circle.id] = circle
            case _Phase.VISIT:
                self.circles_visited += 1
                self._accumulate_bbox(circle.geometry.bounding_box())
