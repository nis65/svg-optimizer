import re
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
    def __init__(self, tokens: tuple[Token, ...]):
        self._iterator = iter(tokens)
        self._buffer: list[Token] = []

    def _lookahead(self, count: int = 1) -> bool:
        while len(self._buffer) < count:
            try:
                self._buffer.append(next(self._iterator))
            except StopIteration:
                return False
        return True

    def peek(self) -> Token | None:
        if len(self._buffer) == 0:
            if self._lookahead(count=1):
                return self._buffer[0]
            else:
                return None
        else:
            return self._buffer[0]

    def has_numbers(self, count: int) -> bool:
        if self._lookahead(count):
            for token in self._buffer[:count]:
                if token.kind != TokenKind.NUMBER:
                    return False
            return True
        else:
            return False

    def get(self) -> Token | None:
        token = self.peek()
        if token is not None:
            del self._buffer[0]
        return token

    def get_unwrapped(self) -> Token:
        token = self.get()
        if token is None:
            raise RuntimeError(
                "Internal Error: should not be called when no token is left"
            )
        return token


def token_lexer(text: str | None, commands: str) -> tuple[Token, ...]:

    NUMBER_RE = re.compile(r"[+-]?(?:(?:\d+(?:\.\d*)?)|(?:\.\d+))(?:[eE][+-]?\d+)?")

    tokens: list[Token] = []

    i = 0
    while text is not None and i < len(text):
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
