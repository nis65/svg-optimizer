# from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, auto

from svgtools.geometry.path_elements.arc import Arc
from svgtools.geometry.path_elements.closepath import ClosePath
from svgtools.geometry.path_elements.cubicbezier import CubicBezier
from svgtools.geometry.path_elements.lineto import LineTo
from svgtools.geometry.path_elements.moveto import MoveTo
from svgtools.geometry.path_elements.path_element_abc import PathElement
from svgtools.geometry.path_elements.quadraticbezier import QuadraticBezier
from svgtools.geometry.point import Point

from .write_utils import numberlist_to_string


class PathCoordinates(Enum):
    ABSOLUTE = auto()
    RELATIVE = auto()
    KEEP = auto()


class PathCompactness(Enum):
    CANONICAL = auto()
    COMPACT = auto()


class PathCommandSet(Enum):
    BASE = auto()
    FULL = auto()


@dataclass(frozen=True, slots=True)
class PathCommand:
    command: str
    parameters: str


@dataclass
class PathWriteState:
    current_point: Point = field(default_factory=lambda: Point(0, 0))
    current_subpath_start: Point = field(default_factory=lambda: Point(0, 0))


class PathWriter:
    def __init__(
        self,
        path_coordinates: PathCoordinates = PathCoordinates.ABSOLUTE,
        path_compactness: PathCompactness = PathCompactness.CANONICAL,
        path_command_set: PathCommandSet = PathCommandSet.BASE,
    ):
        self.path_coordinates = path_coordinates
        self.path_compactness = path_compactness
        self.path_command_set = path_command_set

    def path_elements_to_string(self, path_elements: tuple[PathElement, ...]):
        path_command_list = self._path_elements_to_path_commands(path_elements)
        match self.path_compactness:
            case PathCompactness.CANONICAL:
                new_path_command_list = path_command_list
            case PathCompactness.COMPACT:
                new_path_command_list = self._compact_command_list(path_command_list)
            case _:  # pragma: no cover
                raise ValueError(
                    f"path_compactness {self.path_compactness} not implemented"
                )
        result = ""
        for command in new_path_command_list:
            if command.parameters:
                result += f"{command.command} {command.parameters} "
            else:
                result += f"{command.command} "
        return result.strip()

    @staticmethod
    def _can_aggregate(previous: PathCommand, current: PathCommand) -> bool:
        if previous.command == current.command:
            return True
        if previous.command == "m" and current.command == "l":
            return True
        if previous.command == "M" and current.command == "L":  # noqa: SIM103
            return True
        return False

    @classmethod
    def _compact_command_list(
        cls, command_list: list[PathCommand]
    ) -> list[PathCommand]:
        result: list[PathCommand] = []
        for c in command_list:
            if not result:
                result.append(c)
            elif cls._can_aggregate(result[-1], c):
                new_command = PathCommand(
                    command=result[-1].command,
                    parameters=result[-1].parameters + f" {c.parameters}",
                )
                result[-1] = new_command
            else:
                result.append(c)
        return result

    def _path_elements_to_path_commands(
        self, path_elements: tuple[PathElement, ...]
    ) -> list[PathCommand]:
        current_state = PathWriteState()
        path_command_list: list[PathCommand] = []
        for element in path_elements:
            match element:
                case MoveTo():
                    current_state, path_command = self._build_path_command_moveto(
                        current_state, element
                    )
                case LineTo():
                    current_state, path_command = self._build_path_command_lineto(
                        current_state, element
                    )
                case ClosePath():
                    current_state, path_command = self._build_path_command_closepath(
                        current_state, element
                    )
                case QuadraticBezier():
                    current_state, path_command = self._build_path_command_qbezier(
                        current_state, element
                    )
                case CubicBezier():
                    current_state, path_command = self._build_path_command_cbezier(
                        current_state, element
                    )
                case Arc():
                    current_state, path_command = self._build_path_command_arc(
                        current_state, element
                    )
                case _:  # pragma: no cover
                    raise RuntimeError(f"Internal Error: PathElement {element}")
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
            new_representation = base_commands.get(
                new_representation, new_representation
            )
        return new_representation

    def _build_path_command_moveto(
        self, current_state: PathWriteState, moveto: MoveTo
    ) -> tuple[PathWriteState, PathCommand]:

        new_command = self._get_command(moveto.representation)
        if new_command.isupper():
            new_x = moveto.target.x
            new_y = moveto.target.y
        else:
            new_x = moveto.target.x - current_state.current_point.x
            new_y = moveto.target.y - current_state.current_point.y
        current_state.current_point = moveto.target
        current_state.current_subpath_start = current_state.current_point
        number_string = numberlist_to_string((new_x, new_y))
        return current_state, PathCommand(command=new_command, parameters=number_string)

    def _build_path_command_lineto(
        self, current_state: PathWriteState, lineto: LineTo
    ) -> tuple[PathWriteState, PathCommand]:

        new_command = self._get_command(lineto.representation)
        if new_command.isupper():
            new_x = lineto.target.x
            new_y = lineto.target.y
        else:
            new_x = lineto.target.x - current_state.current_point.x
            new_y = lineto.target.y - current_state.current_point.y
        current_state.current_point = lineto.target
        match new_command:
            case "L" | "l":
                number_string = numberlist_to_string((new_x, new_y))
            case "H" | "h":
                number_string = numberlist_to_string((new_x,))
            case "V" | "v":
                number_string = numberlist_to_string((new_y,))
            case _:  # pragma: no cover
                raise RuntimeError(f"Internal Error: unexpected command {new_command}")
        return current_state, PathCommand(command=new_command, parameters=number_string)

    def _build_path_command_closepath(
        self, current_state: PathWriteState, closepath: ClosePath
    ) -> tuple[PathWriteState, PathCommand]:

        new_command = self._get_command(closepath.representation)
        current_state.current_point = current_state.current_subpath_start

        return current_state, PathCommand(command=new_command, parameters="")

    def _build_path_command_qbezier(
        self, current_state: PathWriteState, qbezier: QuadraticBezier
    ) -> tuple[PathWriteState, PathCommand]:

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
            case "Q" | "q":
                number_string = numberlist_to_string(
                    (new_control1_x, new_control1_y, new_end_x, new_end_y)
                )
            case "T" | "t":
                number_string = numberlist_to_string((new_end_x, new_end_y))
            case _:  # pragma: no cover
                raise RuntimeError(f"Internal Error: unexpected command {new_command}")
        return current_state, PathCommand(command=new_command, parameters=number_string)

    def _build_path_command_cbezier(
        self, current_state: PathWriteState, cbezier: CubicBezier
    ) -> tuple[PathWriteState, PathCommand]:
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
            case "C" | "c":
                number_string = numberlist_to_string(
                    (
                        new_control1_x,
                        new_control1_y,
                        new_control2_x,
                        new_control2_y,
                        new_end_x,
                        new_end_y,
                    )
                )
            case "S" | "s":
                number_string = numberlist_to_string(
                    (new_control2_x, new_control2_y, new_end_x, new_end_y)
                )
            case _:  # pragma: no cover
                raise RuntimeError(f"Internal Error: unexpected command {new_command}")
        return current_state, PathCommand(command=new_command, parameters=number_string)

    def _build_path_command_arc(
        self, current_state: PathWriteState, arc: Arc
    ) -> tuple[PathWriteState, PathCommand]:
        new_command = self._get_command(arc.representation)
        if new_command.isupper():
            new_end_x = arc.end.x
            new_end_y = arc.end.y
        else:
            new_end_x = arc.end.x - current_state.current_point.x
            new_end_y = arc.end.y - current_state.current_point.y
        current_state.current_point = arc.end
        number_string = numberlist_to_string(
            (
                arc.rx,
                arc.ry,
                arc.phi,
                arc.large_arc_flag,
                arc.sweep_flag,
                new_end_x,
                new_end_y,
            )
        )
        return current_state, PathCommand(command=new_command, parameters=number_string)
