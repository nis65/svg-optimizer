from .transform_write_strategy import TransformWriteStrategy
from .path_write_options import PathCoordinates, PathCompactness, PathCommandSet, PathCommand, PathWriteState
from svgtools.svg.document import Document
from svgtools.svg.svg import Svg
from svgtools.svg.defs import Defs
from svgtools.svg.group import Group
from svgtools.svg.use import Use
from svgtools.svg.shape import Shape
from svgtools.svg.transform import Translate, Scale, Rotate, SkewX, SkewY, Affine
from svgtools.svg.get_matrix import get_matrix, transforms_to_matrix
from svgtools.geometry.rect import Rect
from svgtools.geometry.circle import Circle
from svgtools.geometry.ellipse import Ellipse
from svgtools.geometry.line import Line
from svgtools.geometry.polyline import Polyline
from svgtools.geometry.polygon import Polygon
from svgtools.geometry.path import Path
from svgtools.geometry.path_elements.moveto import MoveTo
from svgtools.geometry.path_elements.lineto import LineTo
from svgtools.geometry.path_elements.closepath import ClosePath
from svgtools.geometry.path_elements.quadraticbezier import QuadraticBezier
from svgtools.geometry.path_elements.cubicbezier import CubicBezier
from svgtools.geometry.path_elements.arc import Arc
from svgtools.geometry.point import Point
from svgtools.geometry.matrix3 import Matrix3, TRHxSDecomposition
from svgtools.geometry.isclose import geometry_isclose

class SvgWriter:

    XML_HEADER = "<?xml version='1.0' encoding='UTF-8'?>\n"
    INDENT = "  "
    PRECISION = 3

    def __init__(
            self,
            transform_strategy: TransformWriteStrategy = TransformWriteStrategy.KEEP,
            path_coordinates: PathCoordinates = PathCoordinates.ABSOLUTE,
            path_compactness: PathCompactness = PathCompactness.CANONICAL,
            path_command_set: PathCommandSet = PathCommandSet.BASE
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
            case _:
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

    def _walk_shape(self, shape: Shape, indent:str):
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

    def _append_attributes(self, element) -> None:
        if xmlnamespace := getattr(element, "xmlnamespace", None):
            self._parts.append(f' xmlns="{xmlnamespace}"')
        if element_id := getattr(element, "id", None):
            self._parts.append(f' id="{element_id}"')
        if href := getattr(element, "href", None):
            self._parts.append(f' href="{href}"')
        if geometry := getattr(element, "geometry", None):
            match geometry:
                case Rect():
                    self._parts.append(f' x="{self._number_to_string(geometry.top_left.x)}"'
                                       f' y="{self._number_to_string(geometry.top_left.y)}"'
                                      )
                    self._parts.append(f' width="{self._number_to_string(geometry.width)}"'
                                       f' height="{self._number_to_string(geometry.height)}"'
                                      )
                case Circle():
                    self._parts.append(f' cx="{self._number_to_string(geometry.center.x)}"'
                                       f' cy="{self._number_to_string(geometry.center.y)}"'
                                      )
                    self._parts.append(f' r="{self._number_to_string(geometry.radius)}"')
                case Ellipse():
                    self._parts.append(f' cx="{self._number_to_string(geometry.center.x)}"'
                                       f' cy="{self._number_to_string(geometry.center.y)}"'
                                      )
                    self._parts.append(f' rx="{self._number_to_string(geometry.radiusx)}"'
                                       f' ry="{self._number_to_string(geometry.radiusy)}"'
                                      )
                case Path():
                    path_elements = geometry.children
                    self._parts.append(f' d="{self._path_elements_to_string(path_elements)}"')
                case Line():
                    self._parts.append(f' x1="{self._number_to_string(geometry.start.x)}"'
                                       f' y1="{self._number_to_string(geometry.start.y)}"'
                                       f' x2="{self._number_to_string(geometry.end.x)}"'
                                       f' y2="{self._number_to_string(geometry.end.y)}"'
                                      )
                case Polyline() | Polygon() :
                    self._parts.append(f' points="{self._polypoints_to_string(geometry.children)}"')
                case _:
                    raise NotImplementedError("I know nothing but Rects, Circles, Ellipses, Lines, Polylines, Polygons and Paths")
        if width := getattr(element, "width", None):
            self._parts.append(f' width="{self._number_to_string(width)}"')
        if height := getattr(element, "height", None):
            self._parts.append(f' height="{self._number_to_string(height)}"')
        if viewBox := getattr(element, "viewBox", None):
            self._parts.append(f' viewBox="{self._numberlist_to_string(viewBox)}"')
        if transformations := getattr(element, "transformations", None):
            output_transformations = self._transformations_to_write(transformations)
            self._parts.append(f' transform="{self._transforms_to_string(output_transformations)}"')
        for key, value in sorted(element.unknown_attributes.items()):
            self._parts.append(f' {key}="{value}"')

    def _polypoints_to_string(self, polypoints):
        result = ""
        for point in polypoints:
            coords = ( point.x, point.y )
            result += f'{SvgWriter._numberlist_to_string(coords)} '
        return result.strip()

    def _path_elements_to_string(self, path_elements):
        path_command_list = self._path_elements_to_path_commands(path_elements)
        result = ""
        match self.path_compactness:
            case PathCompactness.CANONICAL:
                for command in path_command_list:
                    if command.parameters:
                       result += f"{command.command} {command.parameters} "
                    else:
                       result += f"{command.command} "
            case _:
                raise ValueError(f"path_compactness {self.path_compactness} not implemented")
        return result.strip()

    def _path_elements_to_path_commands(self, path_elements):
        current_state = PathWriteState()
        path_command_list = []
        for element in path_elements:
            match element:
                case MoveTo():
                    current_state, path_command = self._build_path_command_moveto(current_state, element)
                case LineTo():
                    current_state, path_command = self._build_path_command_lineto(current_state, element)
                case ClosePath():
                    current_state, path_command = self._build_path_command_closepath(current_state, element)
                case QuadraticBezier():
                    current_state, path_command = self._build_path_command_qbezier(current_state, element)
                case CubicBezier():
                    current_state, path_command = self._build_path_command_cbezier(current_state, element)
                case Arc():
                    current_state, path_command = self._build_path_command_arc(current_state, element)
            path_command_list.append(path_command)
        return path_command_list

    def _get_command(self, representation: str) -> str:

        match self.path_coordinates:
            case PathCoordinates.KEEP:
                new_representation = representation
            case PathCoordinates.ABSOLUTE:
                new_representation = representation.upper()
            case PathCoordinates.RELATIVE:
                new_representation = representation.lower()
        base_commands = {
                "h": "l",
                "v": "l",
                "H": "L",
                "V": "L",
                "t": "q",
                "T": "Q",
                "s": "c",
                "S": "C",
                }
        if self.path_command_set is PathCommandSet.BASE:
            new_representation = base_commands.get(new_representation, new_representation)
        return new_representation

    def _build_path_command_moveto(self, current_state, moveto):

        new_command = self._get_command(moveto.representation)
        if new_command.isupper():
            new_x = moveto.target.x
            new_y = moveto.target.y
        else:
            new_x = moveto.target.x - current_state.current_point.x
            new_y = moveto.target.y - current_state.current_point.y
        current_state.current_point = moveto.target
        current_state.current_subpath_start = current_state.current_point
        number_string = self._numberlist_to_string((new_x, new_y))
        return current_state, PathCommand(command=new_command, parameters=number_string)

    def _build_path_command_lineto(self, current_state, lineto):

        new_command = self._get_command(lineto.representation)
        if new_command.isupper():
            new_x = lineto.target.x
            new_y = lineto.target.y
        else:
            new_x = lineto.target.x - current_state.current_point.x
            new_y = lineto.target.y - current_state.current_point.y
        current_state.current_point = lineto.target
        match new_command:
            case 'L' | 'l':
               number_string = self._numberlist_to_string((new_x, new_y))
            case 'H' | 'h':
               number_string = self._numberlist_to_string((new_x,))
            case 'V' | 'v':
               number_string = self._numberlist_to_string((new_y,))
        return current_state, PathCommand(command=new_command, parameters=number_string)

    def _build_path_command_closepath(self, current_state, closepath):

        new_command = self._get_command(closepath.representation)
        current_state.current_point = current_state.current_subpath_start

        return current_state, PathCommand(command=new_command, parameters="")

    def _build_path_command_qbezier(self, current_state, qbezier):

        new_command = self._get_command(qbezier.representation)
        if new_command.isupper():
            new_control1_x = qbezier.control1.x
            new_control1_y = qbezier.control1.y
            new_end_x = qbezier.end.x
            new_end_y = qbezier.end.y
        else:
            new_control1_x = qbezier.control1.x - current_state.current_point.x
            new_control1_y = qbezier.control1.y - current_state.current_point.y
            new_end_x = qbezier.end.x - current_state.current_point.x
            new_end_y = qbezier.end.y - current_state.current_point.y
        current_state.current_point = qbezier.end
        match new_command:
            case 'Q' | 'q':
                number_string = self._numberlist_to_string(
                                      (new_control1_x, new_control1_y,
                                       new_end_x, new_end_y)
                                      )
            case 'T' | 't':
                number_string = self._numberlist_to_string((new_end_x, new_end_y))
        return current_state, PathCommand(command=new_command, parameters=number_string)

    def _build_path_command_cbezier(self, current_state, cbezier):
        new_command = self._get_command(cbezier.representation)
        if new_command.isupper():
            new_control1_x = cbezier.control1.x
            new_control1_y = cbezier.control1.y
            new_control2_x = cbezier.control2.x
            new_control2_y = cbezier.control2.y
            new_end_x = cbezier.end.x
            new_end_y = cbezier.end.y
        else:
            new_control1_x = cbezier.control1.x - current_state.current_point.x
            new_control1_y = cbezier.control1.y - current_state.current_point.y
            new_control2_x = cbezier.control2.x - current_state.current_point.x
            new_control2_y = cbezier.control2.y - current_state.current_point.y
            new_end_x = cbezier.end.x - current_state.current_point.x
            new_end_y = cbezier.end.y - current_state.current_point.y
        current_state.current_point = cbezier.end
        match new_command:
            case 'C' | 'c':
                number_string = self._numberlist_to_string(
                                      (new_control1_x, new_control1_y,
                                       new_control2_x, new_control2_y,
                                       new_end_x, new_end_y)
                                      )
            case 'S' | 's':
                number_string = self._numberlist_to_string(
                                      (new_control2_x, new_control2_y,
                                       new_end_x, new_end_y)
                                      )
        return current_state, PathCommand(command=new_command, parameters=number_string)

    def _build_path_command_arc(self, current_state, arc):
        new_command = self._get_command(arc.representation)
        if new_command.isupper():
            new_end_x = arc.end.x
            new_end_y = arc.end.y
        else:
            new_end_x = arc.end.x - current_state.current_point.x
            new_end_y = arc.end.y - current_state.current_point.y
        current_state.current_point = arc.end
        number_string = self._numberlist_to_string(
            ( arc.rx, arc.ry, arc.phi, arc.large_arc_flag, arc.sweep_flag,
              new_end_x, new_end_y )
            )
        return current_state, PathCommand(command=new_command, parameters=number_string)

    def _transformations_to_write(self, transformations):
        match self.transform_strategy:
            case TransformWriteStrategy.KEEP:
                return transformations
            case TransformWriteStrategy.AGGREGATE:
                return self._transform_strategy_aggregate(transformations)
            case TransformWriteStrategy.DECOMPOSE_MATRIX:
                return self._transform_strategy_decompose_matrix(transformations)
            case TransformWriteStrategy.DECOMPOSE_MATRIX_AND_AGGREGATE:
                decomposed=self._transform_strategy_decompose_matrix(transformations)
                return self._transform_strategy_aggregate(decomposed)
            case TransformWriteStrategy.CANONICAL_CONSERVATIVE :
                return self._transform_strategy_conservative(transformations)
            case TransformWriteStrategy.CANONICAL_AGGRESSIVE:
                return self._transform_strategy_aggressive(transformations)
            case _:
                raise ValueError(f"transform_strategy {self.transform_strategy} not implemented")

    @staticmethod
    def _is_canonical(transformations) -> bool:
        _CANONICAL_ORDER = (Translate, Rotate, SkewX, Scale)
        reference = iter(_CANONICAL_ORDER)
        for t in transformations:
            if type(t) == Rotate:
                if not (t.cx == 0 and t.cy == 0):
                    return False
            for expected in reference:
                if type(t) == expected:
                    break
            else:
                return False
        return True

    @staticmethod
    def _transform_strategy_aggregate(transformations):
        if len(transformations) == 0:
            raise ValueError(f"should not be called with 0 transformations")
        t_list = []
        agg_t = None
        for t in transformations:
            if agg_t is None:
                agg_t = t
            elif type(t) == type(agg_t):
                match t:
                    case Translate():
                        agg_t = Translate(dx = agg_t.dx + t.dx, dy = agg_t.dy + t.dy)
                    case Scale():
                        agg_t = Scale(sx = agg_t.sx * t.sx, sy = agg_t.sy * t.sy)
                    case Rotate():
                        if agg_t.cx == t.cx and agg_t.cy == t.cy:
                            agg_t = Rotate(theta = agg_t.theta + t.theta, cx = t.cx, cy = t.cy)
                        else:
                            # rotate can only be aggregated exactly with the same rotation center
                            t_list.append(agg_t)
                            agg_t = t
                    case SkewX() | SkewY():
                        # skew cannot be aggregated in an exact way
                        t_list.append(agg_t)
                        agg_t = t
                    case Affine():
                        agg_m = get_matrix(agg_t) * get_matrix(t)
                        agg_t= Affine(a=agg_m.m11, b=agg_m.m21, c=agg_m.m12,
                                      d=agg_m.m22, e=agg_m.m13, f=agg_m.m23)
            else:
                t_list.append(agg_t)
                agg_t = t
        t_list.append(agg_t)
        return tuple(t_list)

    @staticmethod
    def _transform_strategy_decompose_matrix(transformations):
        t_list = []
        for t in transformations:
            match t:
                case Affine():
                    md = Matrix3.TRHxS_decompose(
                            Matrix3.affine(a=t.a, b=t.b, c=t.c,
                                           d=t.d, e=t.e, f=t.f
                        )
                    )
                    if not (md.tx == 0 and md.ty == 0):
                        t_list.append(Translate(dx=md.tx, dy=md.ty))
                    if not geometry_isclose(md.theta_rotate, 0):
                        t_list.append(Rotate(theta=md.theta_rotate, cx=0, cy=0))
                    if not geometry_isclose(md.theta_skew_x, 0):
                        t_list.append(SkewX(theta=md.theta_skew_x))
                    if not (md.sx == 1 and md.sy == 1):
                        t_list.append(Scale(sx=md.sx, sy=md.sy))
                case _:
                    t_list.append(t)
        return tuple(t_list)

    def _transform_strategy_conservative(self, transformations):
        # attempt aggregate
        aggregated = self._transform_strategy_aggregate(transformations)
        if self._is_canonical(aggregated):
            self.total_aggregated_chains +=1
            return aggregated
        else:
            self.total_aggressive_chains +=1
            return self._transform_strategy_aggressive(transformations)

    @staticmethod
    def _transform_strategy_aggressive(transformations):
        m = transforms_to_matrix(transformations)
        return SvgWriter._transform_strategy_decompose_matrix((Affine(a=m.m11, b=m.m21, c=m.m12, d=m.m22, e=m.m13, f=m.m23),))

    @staticmethod
    def _number_to_string(number: float | str) -> str:
        if isinstance(number, str):
            return number
        number = round(number, SvgWriter.PRECISION)
        if number.is_integer():
            return str(int(number))
        return f"{number:.3f}"
        #return f"{number:.3f}".rstrip("0").rstrip(".")

    @staticmethod
    def _numberlist_to_string(numbers) -> str:
        str_numbers = []
        for number in numbers:
            str_numbers.append(SvgWriter._number_to_string(number))
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
                case Rotate():
                    numberlist=(trans.theta, trans.cx, trans.cy, )
                    result += f' rotate({SvgWriter._numberlist_to_string(numberlist)})'
                case SkewX():
                    numberlist=(trans.theta, )
                    result += f' skewX({SvgWriter._numberlist_to_string(numberlist)})'
                case SkewY():
                    numberlist=(trans.theta, )
                    result += f' skewY({SvgWriter._numberlist_to_string(numberlist)})'
                case Affine():
                    numberlist=(trans.a, trans.b, trans.c, trans.d, trans.e, trans.f, )
                    result += f' matrix({SvgWriter._numberlist_to_string(numberlist)})'

        return result.strip()
