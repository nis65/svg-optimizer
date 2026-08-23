import argparse
import sys
from dataclasses import replace

from svgtools.geometry.bounding_box import BoundingBox
from svgtools.geometry.point import Point
from svgtools.geometry.rect import Rect
from svgtools.parser.svg_parser import parse_svg_string
from svgtools.semantic.bounding_box_visitor import BoundingBoxVisitor
from svgtools.svg.shape import Shape
from svgtools.writer.svg_writer import SvgWriter


# Warning: this only works when the top svg tag does NOT do any transformation
def build_rect_from_bb(bb: BoundingBox) -> Shape:
    return Shape(
        id="bbrect",
        geometry=Rect(
            top_left=Point(
                bb.min.x,
                bb.min.y,
            ),
            width=bb.max.x - bb.min.x,
            height=bb.max.y - bb.min.y,
        ),
        unknown_attributes={
            "stroke": "red",
            "fill" : "none",
        },
    )

parser = argparse.ArgumentParser()

parser.add_argument("--in", dest="input")
parser.add_argument("--out", dest="output")

args = parser.parse_args()

#infile = open(args.input, encoding="utf-8") if args.input else sys.stdin
#outfile = open(args.output, "w", encoding="utf-8") if args.output else sys.stdout

if args.input:
    with open(args.input, encoding="utf-8") as infile:
        svg_input_text = infile.read()
else:
    svg_input_text = sys.stdin.read()

svg_doc = parse_svg_string(svg_input_text)
visitor = BoundingBoxVisitor()
visitor.visit(svg_doc)
bbrect = build_rect_from_bb(visitor.bounding_box)
new_svg = replace(svg_doc.svg, children=(bbrect, *svg_doc.svg.children))
new_svg_doc = replace(svg_doc, svg=new_svg)
writer = SvgWriter()
svg_output_text = writer.write_svg_string(new_svg_doc)

if args.output:
    with open(args.output, "w", encoding="utf-8") as outfile:
        outfile.write(svg_output_text)
else:
    sys.stdout.write(svg_output_text)
