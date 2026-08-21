from enum import Enum, auto
import re
from dataclasses import dataclass

class TokenKind(Enum):
    COMMAND = auto()
    NUMBER = auto()

@dataclass(frozen=True, slots=True)
class Token:
    kind: TokenKind
    value: str

def token_lexer(text: str, commands: str) -> tuple:

    NUMBER_RE = re.compile(
        r"[+-]?(?:(?:\d+(?:\.\d*)?)|(?:\.\d+))(?:[eE][+-]?\d+)?"
        )

    tokens=[]

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
                raise ValueError(f"Cannot lex this (is neither a command, nor a separator, nor a number): {text[i:]}")
    
            tokens.append(Token(TokenKind.NUMBER, match.group()))
            i = match.end()

    return tuple(tokens)
