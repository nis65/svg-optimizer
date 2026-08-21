from enum import Enum, auto
import re
import sys
from dataclasses import dataclass

from svgtools.geometry.geometry_abc import Geometry
from svgtools.geometry.point import Point
from svgtools.geometry.path import Path
from svgtools.geometry.path_elements.moveto import MoveTo
from svgtools.geometry.path_elements.lineto import LineTo
from svgtools.geometry.path_elements.closepath import ClosePath
from svgtools.geometry.path_elements.quadraticbezier import QuadraticBezier
from svgtools.geometry.path_elements.cubicbezier import CubicBezier
from svgtools.geometry.path_elements.arc import Arc

class TokenKind(Enum):
    COMMAND = auto()
    NUMBER = auto()

@dataclass(frozen=True, slots=True)
class Token:
    kind: TokenKind
    value: str

class TokenIterator:
    def __init__(self, tokens):
        self._iterator = iter(tokens)
        self._buffer = []

    def _lookahead(self, count=1):
        while len(self._buffer) < count:
            try:
                self._buffer.append(next(self._iterator))
            except StopIteration:
                return False
        return True

    def peek(self):
        if len(self._buffer) == 0:
            if self._lookahead(count=1): 
                return self._buffer[0]
            else:
                return None
        else:
            return self._buffer[0]

    def has_numbers(self, count: int):
        if self._lookahead(count):
            for token in self._buffer[:count]: 
                if token.kind != TokenKind.NUMBER:
                    return False
            return True
        else:
            return False

    def get(self):
        token = self.peek()
        if token is not None:
            del self._buffer[0]
        return token

def print_stderr(text: str):
    print(f"{text}", file=sys.stderr)

@dataclass
class PathParseState:
    current_point: Point = Point(0, 0)
    current_subpath_start: Point = Point(0, 0)
    previous_command: str | None = None
    previous_quadratic_control: Point | None = None
    previous_cubic_control: Point | None = None

def parse_path_string(text: str) -> Geometry:
    tokens = _lexer(text)
    token_iterator = TokenIterator(tokens)

    path_element_list = []
    current_state = PathParseState()
    
    while True:
        token = token_iterator.get()
        if token is None:
            break
        if token.kind != TokenKind.COMMAND:
            raise ValueError(f"Expected a COMMAND, found {token}")
        command = token.value
        match command:
            case 'm'|'M':
                current_state, parsed_elements = _parse_mM_list(command, current_state, token_iterator)
            case 'l'|'L':
                current_state, parsed_elements = _parse_any_list(command, current_state, token_iterator,
                                                 LineTo.parameter_counts[command], _parse_lL)
            case 'h'|'H':
                current_state, parsed_elements = _parse_any_list(command, current_state, token_iterator,
                                                 LineTo.parameter_counts[command], _parse_hH)
            case 'v'|'V':
                current_state, parsed_elements = _parse_any_list(command, current_state, token_iterator,
                                                 LineTo.parameter_counts[command], _parse_vV)
            case 'z'|'Z':
                current_state, parsed_elements = _parse_any_list(command, current_state, token_iterator,
                                                 ClosePath.parameter_counts[command], _parse_zZ)
            case 'q'|'Q':
                current_state, parsed_elements = _parse_any_list(command, current_state, token_iterator,
                                                 QuadraticBezier.parameter_counts[command], _parse_qQ)
            case 't'|'T':
                current_state, parsed_elements = _parse_any_list(command, current_state, token_iterator,
                                                 QuadraticBezier.parameter_counts[command], _parse_tT)
            case 'c'|'C':
                current_state, parsed_elements = _parse_any_list(command, current_state, token_iterator,
                                                 CubicBezier.parameter_counts[command], _parse_cC)
            case 's'|'S':
                current_state, parsed_elements = _parse_any_list(command, current_state, token_iterator,
                                                 CubicBezier.parameter_counts[command], _parse_sS)
            case 'a'|'A':
                current_state, parsed_elements = _parse_any_list(command, current_state, token_iterator,
                                                 Arc.parameter_counts[command], _parse_aA)
        for element in parsed_elements:
            path_element_list.append(element)
    return Path(children = tuple(path_element_list))
                
def _parse_mM_list(command: str, current_state: PathParseState, iterator: TokenIterator) -> (PathParseState, tuple):
    expected_numbers = MoveTo.parameter_counts[command]
    if not iterator.has_numbers(expected_numbers):
        raise ValueError(f"Not enough numbers {expected_numbers} for command {command}")
    else:
        current_state, parsed_element = _parse_mM(command, current_state, iterator)
        match command:
            case 'm':
                replaced_command = 'l'
            case 'M':
                replaced_command = 'L'
        expected_numbers = LineTo.parameter_counts[replaced_command]
        other_elements = ()
        while iterator.peek() is not None and iterator.peek().kind == TokenKind.NUMBER:
            if iterator.has_numbers(expected_numbers):
                current_state, other_elements = _parse_any_list(replaced_command, current_state, iterator,
                                                                expected_numbers, _parse_lL)
            else:
                print_stderr(f"WARNING: dropping extra number {iterator.get().value} in {command} command")
    return current_state, (parsed_element, *other_elements)

def _parse_any_list(command: str, current_state: PathParseState, iterator: TokenIterator,
                   expected_numbers, parse_element_function) -> (PathParseState, tuple):
    parsed_path_elements = []
    if not iterator.has_numbers(expected_numbers):
        raise ValueError(f"Not enough numbers {expected_numbers} for command {command}")
    else:
        current_state, parsed_element = parse_element_function(command, current_state, iterator)
        parsed_path_elements.append(parsed_element)
        while iterator.peek() is not None and iterator.peek().kind == TokenKind.NUMBER:
            if iterator.has_numbers(expected_numbers) and not expected_numbers == 0:
                current_state, parsed_element = parse_element_function(command, current_state, iterator)
                parsed_path_elements.append(parsed_element)
            else:
               print_stderr(f"WARNING: dropping extra number {iterator.get().value} in {command} command")
    return current_state, tuple(parsed_path_elements)

def _parse_mM(command: str, current_state: PathParseState, iterator: TokenIterator) -> (PathParseState, MoveTo):
    match command:
        case 'm': 
            new_x = current_state.current_point.x + float(iterator.get().value)
            new_y = current_state.current_point.y + float(iterator.get().value)
        case 'M':
            new_x = float(iterator.get().value)
            new_y = float(iterator.get().value)
    current_state.current_point = Point(new_x, new_y)
    current_state.current_subpath_start = current_state.current_point
    current_state.previous_command = command
    return (current_state,
        MoveTo(
            target = current_state.current_point,
            representation = command,
        ))

def _parse_lL(command: str, current_state: PathParseState, iterator: TokenIterator) -> (PathParseState, LineTo):
    match command:
        case 'l': 
            new_x = current_state.current_point.x + float(iterator.get().value)
            new_y = current_state.current_point.y + float(iterator.get().value)
        case 'L':
            new_x = float(iterator.get().value)
            new_y = float(iterator.get().value)
    current_state.current_point = Point(new_x, new_y)
    current_state.previous_command = command
    return (current_state,
        LineTo(
            target = current_state.current_point,
            representation = command,
        ))

def _parse_hH(command: str, current_state: PathParseState, iterator: TokenIterator) -> (PathParseState, LineTo):
    match command:
        case 'h': 
            new_x = current_state.current_point.x + float(iterator.get().value)
        case 'H':
            new_x = float(iterator.get().value)
    new_y = current_state.current_point.y
    current_state.current_point = Point(new_x, new_y)
    current_state.previous_command = command
    return (current_state,
        LineTo(
            target = current_state.current_point,
            representation = command,
        ))

def _parse_vV(command: str, current_state: PathParseState, iterator: TokenIterator) -> (PathParseState, LineTo):
    new_x = current_state.current_point.x
    match command:
        case 'v': 
            new_y = current_state.current_point.y + float(iterator.get().value)
        case 'V':
            new_y = float(iterator.get().value)
    current_state.current_point = Point(new_x, new_y)
    current_state.previous_command = command
    return (current_state,
        LineTo(
            target = current_state.current_point,
            representation = command,
        ))

def _parse_zZ(command: str, current_state: PathParseState, iterator: TokenIterator) -> (PathParseState, ClosePath):
    current_state.current_point = current_state.current_subpath_start
    return (current_state,
        ClosePath(
            representation = command
        ))

def _parse_qQ(command: str, current_state: PathParseState, iterator: TokenIterator) -> (PathParseState, QuadraticBezier):
    match command:
        case 'q':
            new_control1_x = current_state.current_point.x + float(iterator.get().value)
            new_control1_y = current_state.current_point.y + float(iterator.get().value)
            new_end_x = current_state.current_point.x + float(iterator.get().value)
            new_end_y = current_state.current_point.y + float(iterator.get().value)
        case 'Q':
            new_control1_x = float(iterator.get().value)
            new_control1_y = float(iterator.get().value)
            new_end_x = float(iterator.get().value)
            new_end_y = float(iterator.get().value)
    current_state.current_point = Point(new_end_x, new_end_y)
    current_state.previous_command = command
    current_state.previous_quadratic_control = Point(new_control1_x, new_control1_y)
    return (current_state,
        QuadraticBezier(
            control1 = current_state.previous_quadratic_control,
            end = current_state.current_point,
            representation = command,
        ))

def _parse_tT(command: str, current_state: PathParseState, iterator: TokenIterator) -> (PathParseState, QuadraticBezier):
    if current_state.previous_command in ('q', 'Q', 't', 'T'):
        new_control1 = _mirror_point(current_state.current_point, current_state.previous_quadratic_control)
    else:
        new_control1 = current_state.current_point
    match command:
        case 't':
            new_end_x = current_state.current_point.x + float(iterator.get().value)
            new_end_y = current_state.current_point.y + float(iterator.get().value)
        case 'T':
            new_end_x = float(iterator.get().value)
            new_end_y = float(iterator.get().value)
    current_state.current_point = Point(new_end_x, new_end_y)
    current_state.previous_command = command
    current_state.previous_quadratic_control = new_control1
    return (current_state,
        QuadraticBezier(
            control1 = current_state.previous_quadratic_control,
            end = current_state.current_point,
            representation = command,
        ))

def _parse_cC(command: str, current_state: PathParseState, iterator: TokenIterator) -> (PathParseState, CubicBezier):
    match command:
        case 'c':
            new_control1_x = current_state.current_point.x + float(iterator.get().value)
            new_control1_y = current_state.current_point.y + float(iterator.get().value)
            new_control2_x = current_state.current_point.x + float(iterator.get().value)
            new_control2_y = current_state.current_point.y + float(iterator.get().value)
            new_end_x = current_state.current_point.x + float(iterator.get().value)
            new_end_y = current_state.current_point.y + float(iterator.get().value)
        case 'C':
            new_control1_x = float(iterator.get().value)
            new_control1_y = float(iterator.get().value)
            new_control2_x = float(iterator.get().value)
            new_control2_y = float(iterator.get().value)
            new_end_x = float(iterator.get().value)
            new_end_y = float(iterator.get().value)
    current_state.current_point = Point(new_end_x, new_end_y)
    current_state.previous_command = command
    current_state.previous_cubic_control = Point(new_control2_x, new_control2_y)
    return (current_state,
        CubicBezier(
            control1 = Point(new_control1_x, new_control1_y),
            control2 = current_state.previous_cubic_control,
            end = current_state.current_point,
            representation = command,
        ))

def _parse_sS(command: str, current_state: PathParseState, iterator: TokenIterator) -> (PathParseState, CubicBezier):
    if current_state.previous_command in ('c', 'C', 's', 'S'):
        new_control1 = _mirror_point(current_state.current_point, current_state.previous_cubic_control)
    else:
        new_control1 = current_state.current_point
    match command:
        case 's':
            new_control2_x = current_state.current_point.x + float(iterator.get().value)
            new_control2_y = current_state.current_point.y + float(iterator.get().value)
            new_end_x = current_state.current_point.x + float(iterator.get().value)
            new_end_y = current_state.current_point.y + float(iterator.get().value)
        case 'S':
            new_control2_x = float(iterator.get().value)
            new_control2_y = float(iterator.get().value)
            new_end_x = float(iterator.get().value)
            new_end_y = float(iterator.get().value)
    current_state.current_point = Point(new_end_x, new_end_y)
    current_state.previous_command = command
    current_state.previous_cubic_control = Point(new_control2_x, new_control2_y)
    return (current_state,
        CubicBezier(
            control1 = new_control1,
            control2 = current_state.previous_cubic_control,
            end = current_state.current_point,
            representation = command,
        ))

def _parse_aA(command: str, current_state: PathParseState, iterator: TokenIterator) -> (PathParseState, Arc):
    new_rx = float(iterator.get().value)
    new_ry = float(iterator.get().value)
    new_phi = float(iterator.get().value)
    new_large_arc_flag = int(iterator.get().value)
    new_sweep_flag = int(iterator.get().value)
    match command:
        case 'a': 
            new_x = current_state.current_point.x + float(iterator.get().value)
            new_y = current_state.current_point.y + float(iterator.get().value)
        case 'A':
            new_x = float(iterator.get().value)
            new_y = float(iterator.get().value)
    current_state.current_point = Point(new_x, new_y)
    current_state.previous_command = command
    return (current_state,
        Arc(
            rx = new_rx,
            ry = new_ry,
            phi = new_phi,
            large_arc_flag = new_large_arc_flag,
            sweep_flag = new_sweep_flag,
            end = current_state.current_point,
            representation = command,
        ))

def _mirror_point(center: Point, point_to_mirror: Point) -> Point:
    return Point(
            x = 2 * center.x - point_to_mirror.x,
            y = 2 * center.y - point_to_mirror.y,
    )

def _lexer(text: str) -> tuple:

    COMMANDS = "mMlLhHvVzZqQtTcCsSaA"
    NUMBER_RE = re.compile(
        r"[+-]?(?:(?:\d+(?:\.\d*)?)|(?:\.\d+))(?:[eE][+-]?\d+)?"
        )

    tokens=[]

    i = 0
    while i < len(text):
        char = text[i]
    
        if char in COMMANDS:
            tokens.append(Token(TokenKind.COMMAND, char))
            i += 1
    
        elif char in " ,\t\r\n":
            i += 1
    
        else:
            match = NUMBER_RE.match(text, i)
    
            if not match:
                raise ValueError(f"Cannot lex this (is neither a command, nor a separator, nor a number): {text[i:]}")
    
            tokens.append(Token(TokenKind.NUMBER, match.group()))
            i = match.end()

    return tuple(tokens)
