from enum import Enum, auto
import re
import sys
from dataclasses import dataclass

from svgtools.geometry.point import Point
from svgtools.geometry.path import Path
from svgtools.geometry.path_elements.moveto import MoveTo
from svgtools.geometry.path_elements.lineto import LineTo

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

def parse_path_string(text: str) -> tuple:
    tokens = _lexer(text)
    token_iterator = TokenIterator(tokens)

    path_element_list = []
    current_point = Point(0,0)
    current_subpath_start = current_point
    
    while True:
        token = token_iterator.get()
        if token is None:
            break
        if token.kind != TokenKind.COMMAND:
            raise ValueError(f"Expected a COMMAND, found {token}")
        command = token.value
        match command:
            case 'm'|'M':
                current_point, parsed_elements = _parse_mM_list(command, current_point, token_iterator)
            case 'l'|'L':
                current_point, parsed_elements = _parse_any_list(command, current_point, token_iterator,
                                                 LineTo.parameter_counts[command], _parse_lL)
            case 'h'|'H':
                current_point, parsed_elements = _parse_any_list(command, current_point, token_iterator,
                                                 LineTo.parameter_counts[command], _parse_hH)
            case 'v'|'V':
                current_point, parsed_elements = _parse_any_list(command, current_point, token_iterator,
                                                 LineTo.parameter_counts[command], _parse_vV)
        for element in parsed_elements:
            path_element_list.append(element)
    return Path(children = tuple(path_element_list))
                
def _parse_mM_list(command: str, current_point: Point, iterator: TokenIterator) -> tuple:
    expected_numbers = MoveTo.parameter_counts[command]
    if not iterator.has_numbers(expected_numbers):
        raise ValueError(f"Not enough numbers {expected_numbers} for command {command}")
    else:
        current_point, parsed_element = _parse_mM(command, current_point, iterator)
        match command:
            case 'm':
                replaced_command = 'l'
            case 'M':
                replaced_command = 'L'
        expected_numbers = LineTo.parameter_counts[replaced_command]
        other_elements = ()
        while iterator.peek() is not None and iterator.peek().kind == TokenKind.NUMBER:
            if iterator.has_numbers(expected_numbers):
                current_point, other_elements = _parse_any_list(replaced_command, current_point, iterator,
                                                                expected_numbers, _parse_lL)
            else:
                print_stderr(f"WARNING: dropping extra number {iterator.get().value} in {command} command")
    return current_point, (parsed_element, *other_elements)

def _parse_any_list(command: str, current_point: Point, iterator: TokenIterator,
                   expected_numbers, parse_element_function):
    parsed_path_elements = []
    if not iterator.has_numbers(expected_numbers):
        raise ValueError(f"Not enough numbers {expected_numbers} for command {command}")
    else:
        current_point, parsed_element = parse_element_function(command, current_point, iterator)
        parsed_path_elements.append(parsed_element)
        while iterator.peek() is not None and iterator.peek().kind == TokenKind.NUMBER:
            if iterator.has_numbers(LineTo.parameter_counts[command]):
                current_point, parsed_element = parse_element_function(command, current_point, iterator)
                parsed_path_elements.append(parsed_element)
            else:
               print_stderr(f"WARNING: dropping extra number {iterator.get().value} in {command} command")
    return current_point, tuple(parsed_path_elements)

def _parse_mM(command: str, current_point: Point, iterator: TokenIterator) -> (Point, MoveTo):
    match command:
        case 'm': 
            new_x = current_point.x + float(iterator.get().value)
            new_y = current_point.y + float(iterator.get().value)
        case 'M':
            new_x = float(iterator.get().value)
            new_y = float(iterator.get().value)
    end_point = Point(new_x, new_y) 
    return (end_point,
        MoveTo(
            target = end_point,
            representation = command,
        ))

def _parse_lL(command: str, current_point: Point, iterator: TokenIterator) -> (Point, LineTo):
    match command:
        case 'l': 
            new_x = current_point.x + float(iterator.get().value)
            new_y = current_point.y + float(iterator.get().value)
        case 'L':
            new_x = float(iterator.get().value)
            new_y = float(iterator.get().value)
    end_point = Point(new_x, new_y) 
    return (end_point,
        LineTo(
            target = end_point,
            representation = command,
        ))

def _parse_hH(command: str, current_point: Point, iterator: TokenIterator) -> (Point, LineTo):
    match command:
        case 'h': 
            new_x = current_point.x + float(iterator.get().value)
        case 'H':
            new_x = float(iterator.get().value)
    new_y = current_point.y
    end_point = Point(new_x, new_y)
    return (end_point,
        LineTo(
            target = end_point,
            representation = command,
        ))

def _parse_vV(command: str, current_point: Point, iterator: TokenIterator) -> (Point, LineTo):
    new_x = current_point.x
    match command:
        case 'v': 
            new_y = current_point.y + float(iterator.get().value)
        case 'V':
            new_y = float(iterator.get().value)
    end_point = Point(new_x, new_y)
    return (end_point,
        LineTo(
            target = end_point,
            representation = command,
        ))

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
