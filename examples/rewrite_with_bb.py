import argparse
import sys
from dataclasses import replace

from svgtools.parser.svg_parser import parse_svg_string
from svgtools.model.scene.document import Document
from svgtools.model.scene.shape import Shape

from svgtools.semantic.bounding_box_visitor import BoundingBoxVisitor

from svgtools.model.geometry.bounding_box import BoundingBox as GeometryBoundingBox
from svgtools.model.geometry.rect import Rect as GeometryRect
from svgtools.model.geometry.point import Point as GeometryPoint

from svgtools.writer.svg_writer import SvgWriter

# Warning: this only works when the top svg tag does NOT do any transformation
def build_rect_from_bb(bb: GeometryBoundingBox) -> Shape:
    return Shape(
        id="bbrect",
        geometry=GeometryRect(
            top_left=GeometryPoint(
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

infile = open(args.input, encoding="utf-8") if args.input else sys.stdin
outfile = open(args.output, "w", encoding="utf-8") if args.output else sys.stdout

try:
    svg_input_text = infile.read()
    svg_doc = parse_svg_string(svg_input_text)
    visitor = BoundingBoxVisitor()
    visitor.visit(svg_doc)
    bbrect = build_rect_from_bb(visitor.bounding_box)
    new_svg = replace(svg_doc.svg, children=(bbrect, *svg_doc.svg.children))
    new_svg_doc = replace(svg_doc, svg=new_svg)
    writer = SvgWriter()
    outfile.write(writer.write_svg_string(new_svg_doc))

finally:
    if infile is not sys.stdin:
        infile.close()
    if outfile is not sys.stdout:
        outfile.close()

