import argparse
import sys

from svgtools.parser.svg_parser import parse_svg_string
from svgtools.model.scene.document import Document
from svgtools.semantic.bounding_box_visitor import BoundingBoxVisitor
from svgtools.model.geometry.bounding_box import BoundingBox as GeometryBoundingBox
from svgtools.model.geometry.point import Point as GeometryPoint

parser = argparse.ArgumentParser()

parser.add_argument("--in", dest="input")

args = parser.parse_args()

infile = open(args.input, encoding="utf-8") if args.input else sys.stdin

try:
    svg_input_text = infile.read()
    svg_doc = parse_svg_string(svg_input_text)
    visitor = BoundingBoxVisitor()
    visitor.visit(svg_doc)
    print(f"Bounding Box min: {visitor.bounding_box.min.x}, {visitor.bounding_box.min.y}")
    print(f"Bounding Box max: {visitor.bounding_box.max.x}, {visitor.bounding_box.max.y}")

finally:
    if infile is not sys.stdin:
        infile.close()


