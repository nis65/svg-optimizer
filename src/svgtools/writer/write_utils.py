WRITE_PRECISION = 3


def number_to_string(number: float | str) -> str:
    if isinstance(number, str):
        return number
    number = round(number, WRITE_PRECISION)
    if number.is_integer():
        return str(int(number))
    return f"{number:.{WRITE_PRECISION}f}"
    # return f"{number:.3f}".rstrip("0").rstrip(".")


def numberlist_to_string(numbers) -> str:
    str_numbers = []
    for number in numbers:
        str_numbers.append(number_to_string(number))
    return " ".join(str_numbers)
