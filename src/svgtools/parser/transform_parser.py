"""
very simple parser for very simple language:
* input is just one line
* a transformation is always "name( number1, number2, ...)"
* there can be any number of transformations in the string
* order is relevant
all parser funcions
* read as much of the string as needed
* return the rest that is still to parse
* until nothing is left
* spaces are ignored everywhere, except within parentheses where at least
  a space (or a comma) is separator
"""

from svgtools.model.scene.transform import Translate, Scale

def parse_transform_string(tstring: str) -> tuple:

    transformation_list = []

    if tstring is None:
        rest = ""
    else:
        rest = tstring.strip()

    while rest:
        if rest.startswith("scale"):
            rest = rest.removeprefix("scale")
            rest, transformation = _parse_scale(rest)
        elif rest.startswith("translate"):
            rest = rest.removeprefix("translate")
            rest, transformation = _parse_translate(rest)
        else:
            raise ValueError("only scale and translate supported")
        transformation_list.append(transformation)
        rest = _skip_spaces(rest)
    return tuple(transformation_list)
        
def _skip_spaces(text: str) -> str:
    return text.lstrip()

def _parse_translate(text: str):
    numbers, rest = _parse_parentheses(text)
    if len(numbers) == 2:
        t = Translate(
                dx=numbers[0],
                dy=numbers[1]
            )
    else:
        raise ValueError(f"translate needs exactly 2 parameters, not {len(numbers)}")
    return rest, t

def _parse_scale(text: str):
    numbers, rest = _parse_parentheses(text)
    match len(numbers):
        case 1: 
            t = Scale(
                    sx=numbers[0],
                    sy=numbers[0]
                )
        case 2:
            t = Scale(
                    sx=numbers[0],
                    sy=numbers[1]
                )
        case _:
            raise ValueError(f"scale needs 1 or 2 parameters, not {len(numbers)}")
    return rest, t

def _parse_parentheses(text: str) -> tuple[tuple[float, ...], str]:
    rest = _skip_spaces(text)
    before = rest
    rest = rest.removeprefix("(")
    if rest == before:
        raise ValueError(f"expected '(' - found {rest}")
    end_pos = rest.find(")")
    if end_pos == -1:
        raise ValueError(f"expected ')' - found {rest}")
    inside = rest[:end_pos]
    rest = rest[end_pos+1:]
    # inside contains now everything within parentheses (without the parentheses themselves)
    # rest contains now everything after the closing parenthese
    inside = inside.replace(",", " ")
    tokens = inside.split()
    numbers = []
    for token in tokens:
        try:
            numbers.append(float(token))
        except ValueError:
            raise ValueError(
                f"Expected number, found {token}" 
            )
    return tuple(numbers), rest
