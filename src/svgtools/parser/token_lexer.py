import re
import sys
from dataclasses import dataclass
from enum import Enum, auto


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


def token_lexer(text: str, commands: str) -> tuple:

    NUMBER_RE = re.compile(r"[+-]?(?:(?:\d+(?:\.\d*)?)|(?:\.\d+))(?:[eE][+-]?\d+)?")

    tokens = []

    i = 0
    while i < len(text):
        char = text[i]

        if char in commands:
            tokens.append(Token(TokenKind.COMMAND, char))
            i += 1

        elif char in " ,\t\r\n":
            i += 1

        else:
            match = NUMBER_RE.match(text, i)

            if not match:
                raise ValueError(
                    f"Cannot lex this (is neither a command, nor a separator, nor a number): {text[i:]}"
                )

            tokens.append(Token(TokenKind.NUMBER, match.group()))
            i = match.end()

    return tuple(tokens)


def print_stderr(text: str):
    print(f"{text}", file=sys.stderr)
