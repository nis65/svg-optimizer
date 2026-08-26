from collections import Counter
from enum import Enum

from svgtools.geometry.bounding_box import BoundingBox
from svgtools.geometry.matrix3 import Matrix3
from svgtools.geometry.path import Path
from svgtools.geometry.point import Point
from svgtools.geometry.tolerance import GEOMETRY_NUMBER_OF_SAMPLES
from svgtools.svg.defs import Defs
from svgtools.svg.document import Document
from svgtools.svg.get_matrix import transforms_to_matrix
from svgtools.svg.group import Group
from svgtools.svg.shape import Shape
from svgtools.svg.svg import Svg
from svgtools.svg.use import Use


class _Phase(Enum):
    BUILD_DEFINITION_TABLE = 0
    VISIT = 1


class BoundingBoxVisitor:
    def __init__(self):

        self.bounding_box = None
        self.definition_table = {}  # Maps object ids to reusable svg elements.
        self.visited = Counter()

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
            current_matrix *= transforms_to_matrix(svg.transformations)
        for child in svg.children:
            self._walk_element(child, phase, current_matrix)

    def _walk_element(self, element, phase: _Phase, current_matrix: Matrix3):

        match element:
            case Defs():
                self._walk_defs(element, phase)
            case Group():
                self._walk_group(element, phase, current_matrix)
            case Use():
                self._walk_use(element, phase, current_matrix)
            case Shape():
                self._walk_shape(element, phase, current_matrix)
            case _:  # pragma: no cover
                raise NotImplementedError(type(element))

    def _walk_group(self, group: Group, phase: _Phase, current_matrix: Matrix3):
        match phase:
            case _Phase.BUILD_DEFINITION_TABLE:
                if group.id:
                    self.definition_table[group.id] = group
            case _Phase.VISIT:
                current_matrix *= transforms_to_matrix(group.transformations)
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
                current_matrix *= transforms_to_matrix(use.transformations)
                self._walk_element(self.definition_table[label], phase, current_matrix)

    def _walk_shape(self, shape: Shape, phase: _Phase, current_matrix: Matrix3):

        match phase:
            case _Phase.BUILD_DEFINITION_TABLE:
                if shape.id:
                    self.definition_table[shape.id] = shape
            case _Phase.VISIT:
                self.visited[type(shape.geometry).__name__] += 1
                current_matrix *= transforms_to_matrix(shape.transformations)
                if type(shape.geometry) is Path:
                    pathstats, points = (
                        shape.geometry.points_for_bounding_box_with_stats(
                            GEOMETRY_NUMBER_OF_SAMPLES
                        )
                    )
                    self.visited.update(
                        {f"path_{key}": value for key, value in pathstats.items()}
                    )
                else:
                    points = shape.geometry.points_for_bounding_box(
                        GEOMETRY_NUMBER_OF_SAMPLES
                    )
                self._accumulate_bbox(
                    self._transformed_points_bounding_box(points, current_matrix)
                )

    @staticmethod
    def _transformed_points_bounding_box(
        points: set[Point], matrix: Matrix3
    ) -> BoundingBox:
        if len(points) < 1:
            raise ValueError(
                f"need at least one point to create a BoundingBox, not {len(points)}"
            )
        if len(points) == 1:
            moved_point = matrix * next(iter(points))
            bb = BoundingBox(moved_point, moved_point)
        else:
            points_iterator = iter(points)
            first = matrix * next(points_iterator)
            second = matrix * next(points_iterator)
            bb = BoundingBox(
                Point(min(first.x, second.x), min(first.y, second.y)),
                Point(max(first.x, second.x), max(first.y, second.y)),
            )
            for p in points_iterator:
                bb = bb.include(matrix * p)
        return bb
