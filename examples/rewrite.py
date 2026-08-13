import argparse
import sys

#from svgtools.io import write_svg_file, parse_svg_file

from svgtools.parser.svg_parser import parse_svg_string
from svgtools.model.scene.document import Document
from svgtools.writer.svg_writer import SvgWriter
from svgtools.writer.transform_write_strategy import TransformWriteStrategy


parser = argparse.ArgumentParser()

parser.add_argument("--in", dest="input")
parser.add_argument("--out", dest="output")
parser.add_argument("--strategy",
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
    writer = SvgWriter(args.strategy)
    outfile.write(writer.write_svg_string(svg_doc))

finally:
    if infile is not sys.stdin:
        infile.close()
    if outfile is not sys.stdout:
        outfile.close()
