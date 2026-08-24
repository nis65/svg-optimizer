"""
a simple parser for lists of numbers a used in an svg. All these are valid number lists:

1 2 3 4
1,2,3,4
1 2,3 4

"""


def parse_float_list(text: str) -> tuple[float, ...]:

    numbers = []
    if text is not None:
        tokens = text.strip().replace(",", " ").split()
        numbers = []
        for token in tokens:
            try:
                numbers.append(float(token))
            except ValueError:
                raise ValueError(f"Expected number, found {token}")
    return tuple(numbers)
