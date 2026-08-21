import argparse
import sys

from svgtools.parser.svg_parser import parse_svg_string
from svgtools.writer.svg_writer import SvgWriter
from svgtools.writer.transform_write_strategy import TransformWriteStrategy

parser = argparse.ArgumentParser()

parser.add_argument("--in", dest="input")
parser.add_argument("--out", dest="output")
parser.add_argument("--transform-strategy",
                    dest="transform_strategy",
                    type=TransformWriteStrategy.__getitem__,
                    choices=TransformWriteStrategy,
                    default=TransformWriteStrategy.KEEP
                   )

args = parser.parse_args()

infile = open(args.input, encoding="utf-8") if args.input else sys.stdin
outfile = open(args.output, "w", encoding="utf-8") if args.output else sys.stdout

try:
    svg_input_text = infile.read()
    svg_doc = parse_svg_string(svg_input_text)
    writer = SvgWriter(transform_strategy = args.transform_strategy)
    outfile.write(writer.write_svg_string(svg_doc))
    if args.transform_strategy == TransformWriteStrategy.CANONICAL_CONSERVATIVE:
       print(f"conservative stats (exact, forced): {writer.conservative_stats}", file=sys.stderr)

finally:
    if infile is not sys.stdin:
        infile.close()
    if outfile is not sys.stdout:
        outfile.close()
