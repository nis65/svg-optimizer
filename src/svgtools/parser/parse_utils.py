import sys


def print_stderr(text: str):
    print(f"{text}", file=sys.stderr)
