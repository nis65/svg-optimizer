from enum import Enum

from svgtools.model.geometry.bounding_box import BoundingBox
from svgtools.model.geometry.point import Point
from svgtools.model.geometry.matrix3 import Matrix3
from svgtools.model.scene.document import Document
from svgtools.model.scene.svg import Svg
from svgtools.model.scene.defs import Defs
from svgtools.model.scene.group import Group
from svgtools.model.scene.use import Use
from svgtools.model.scene.rect import Rect
from svgtools.model.scene.circle import Circle
from svgtools.model.scene.transform import Translate, Scale

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

        current_matrix = Matrix3.identity()
        if phase == _Phase.VISIT:
            current_matrix *= self._transforms_to_matrix(svg.transformations)
        for child in svg.children:
            self._walk_element(child, phase, current_matrix)

    def _walk_element(self, element, phase: _Phase, current_matrix: Matrix3):

        match element:
            case Defs():
                self._walk_defs(element,phase)
            case Group():
                self._walk_group(element,phase, current_matrix)
            case Use():
                self._walk_use(element,phase, current_matrix)
            case Rect():
                self._walk_rect(element,phase, current_matrix)
            case Circle():
                self._walk_circle(element,phase, current_matrix)
            case _:
                raise NotImplementedError(type(element))

    def _walk_group(self, group: Group, phase: _Phase, current_matrix: Matrix3):
        match phase:
            case _Phase.BUILD_DEFINITION_TABLE:
                if group.id:
                    self.definition_table[group.id] = group
            case _Phase.VISIT:
                current_matrix *= self._transforms_to_matrix(group.transformations)
        for child in group.children:
            self._walk_element(child, phase, current_matrix)

    def _walk_defs(self, defs: Defs, phase: _Phase):

        match phase:
            case _Phase.BUILD_DEFINITION_TABLE:
                for child in defs.children:
                    # we NEVER use a Matrix in the BUILD_DEFINITION_TABLE
                    # this is here to keep procedure calling syntax simple
                    # everywhere else.
                    self._walk_element(child, phase, Matrix3.identity())
            case _Phase.VISIT:
                pass

    def _walk_use(self, use: Use, phase: _Phase, current_matrix: Matrix3):

        match phase:
            case _Phase.BUILD_DEFINITION_TABLE:
                pass
            case _Phase.VISIT:
                label = use.href.removeprefix("#")
                if label not in self.definition_table:
                    raise ValueError(f"Use references unknown label {label}")
                current_matrix *= self._transforms_to_matrix(use.transformations)
                self._walk_element(self.definition_table[label], phase, current_matrix)

    def _walk_rect(self, rect: Rect, phase: _Phase, current_matrix: Matrix3):

        match phase:
            case _Phase.BUILD_DEFINITION_TABLE:
                if rect.id:
                    self.definition_table[rect.id] = rect
            case _Phase.VISIT:
                self.rectangles_visited += 1
                current_matrix *= self._transforms_to_matrix(rect.transformations)
                self._accumulate_bbox(self._transform_bounding_box(rect.geometry.bounding_box(), current_matrix))

    def _walk_circle(self, circle: Circle, phase: _Phase, current_matrix: Matrix3):

        match phase:
            case _Phase.BUILD_DEFINITION_TABLE:
                if circle.id:
                    self.definition_table[circle.id] = circle
            case _Phase.VISIT:
                self.circles_visited += 1
                current_matrix *= self._transforms_to_matrix(circle.transformations)
                self._accumulate_bbox(self._transform_bounding_box(circle.geometry.bounding_box(), current_matrix))

    @staticmethod
    def _transforms_to_matrix(transforms: tuple[Translate | Scale, ...],) -> Matrix3:
        matrix = Matrix3.identity()
        for transform in transforms:
            match transform:
                case Translate():
                    matrix = matrix * Matrix3.translation(transform.dx, transform.dy)
                case Scale():
                    matrix = matrix * Matrix3.scaling(transform.sx, transform.sy)
        return matrix

    @staticmethod
    def _transform_bounding_box(bbox: BoundingBox, matrix: Matrix3) -> BoundingBox:
        """
        This simple algorithm works reliably only as long as the matrix is composed of
        translate and scale transformations only. As soon as we have rotate, we will need
        to delegate the computation of the bounding box to the geometric elements themselves
        and only accumulate here.
        """
        return BoundingBox(
                min = matrix * bbox.min,
                max = matrix * bbox.max,
               )
