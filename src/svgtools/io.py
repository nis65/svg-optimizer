from pathlib import Path

from svgtools.writer.svg_writer import SvgWriter
from svgtools.parser.svg_parser import parse_svg_string

from svgtools.svg.document import Document

def parse_svg_file(path: str | Path) -> Document:
    path = Path(path)
    with path.open("r", encoding="utf-8") as f:
        return parse_svg_string(f.read())

def write_svg_file(document: Document, path: str | Path ) -> None:
    path = Path(path)
    writer = SvgWriter()
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(writer.write_svg_string(document))

