import argparse
import sys
from dataclasses import replace

from svgtools.parser.svg_parser import parse_svg_string
from svgtools.semantic.bounding_box_visitor import BoundingBoxVisitor
from svgtools.writer.svg_writer import SvgWriter

parser = argparse.ArgumentParser()
parser.add_argument("--in", dest="input")
parser.add_argument("--out", dest="output")


def margin(value):
    value = int(value)
    if not 0 <= value <= 40:
        raise argparse.ArgumentTypeError(
            f"margin must be between 0 and 40 percent, not {value}"
        )
    return value


parser.add_argument("--margin", type=margin, default=5)

args = parser.parse_args()


if args.input:
    with open(args.input, encoding="utf-8") as infile:
        svg_input_text = infile.read()
else:
    svg_input_text = sys.stdin.read()

# get original document and viewBox width and height
svg_doc = parse_svg_string(svg_input_text)
viewbox_width = svg_doc.svg.viewBox[2]
viewbox_height = svg_doc.svg.viewBox[3]

# get boundingbox width and height
bbvisitor = BoundingBoxVisitor()
bbvisitor.visit(svg_doc)
bbwidth = bbvisitor.bounding_box.max.x - bbvisitor.bounding_box.min.x
bbheight = bbvisitor.bounding_box.max.y - bbvisitor.bounding_box.min.y

# compute new viewbox width and height, keeping aspect ratio of old viewBox
framefactor = 1 + ((2 * args.margin) / 100)
minimal_viewbox_width = bbwidth * framefactor
minimal_viewbox_height = bbheight * framefactor
if bbwidth / bbheight > viewbox_width / viewbox_height:
    new_viewbox_width = minimal_viewbox_width
    new_viewbox_height = new_viewbox_width * viewbox_height / viewbox_width
else:
    new_viewbox_height = minimal_viewbox_height
    new_viewbox_width = new_viewbox_height * viewbox_width / viewbox_height

# compute new viewbox topleft corner
new_viewbox_topleft_x = bbvisitor.bounding_box.min.x - (new_viewbox_width - bbwidth) / 2
new_viewbox_topleft_y = (
    bbvisitor.bounding_box.min.y - (new_viewbox_height - bbheight) / 2
)

# replace viewbox in document
new_svg = replace(
    svg_doc.svg,
    viewBox=(
        new_viewbox_topleft_x,
        new_viewbox_topleft_y,
        new_viewbox_width,
        new_viewbox_height,
    ),
)
new_svg_doc = replace(svg_doc, svg=new_svg)

writer = SvgWriter()
svg_output_text = writer.write_svg_string(new_svg_doc)

# and finally write result
if args.output:
    with open(args.output, "w", encoding="utf-8") as outfile:
        outfile.write(svg_output_text)
else:
    sys.stdout.write(svg_output_text)
