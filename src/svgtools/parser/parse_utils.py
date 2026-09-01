import sys


def print_stderr(text: str) -> None:
    print(f"{text}", file=sys.stderr)
