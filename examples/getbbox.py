import argparse
import sys

from svgtools.parser.svg_parser import parse_svg_string
from svgtools.semantic.bounding_box_visitor import BoundingBoxVisitor

parser = argparse.ArgumentParser()

parser.add_argument("--in", dest="input")

args = parser.parse_args()

if args.input:
    with open(args.input, encoding="utf-8") as infile:
        svg_input_text = infile.read()
else:
    svg_input_text = sys.stdin.read()

svg_doc = parse_svg_string(svg_input_text)
visitor = BoundingBoxVisitor()
visitor.visit(svg_doc)
print(f"Bounding Box min: {visitor.bounding_box.min.x}, {visitor.bounding_box.min.y}")
print(f"Bounding Box max: {visitor.bounding_box.max.x}, {visitor.bounding_box.max.y}")
