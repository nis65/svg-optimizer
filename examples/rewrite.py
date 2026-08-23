import argparse
import sys

from svgtools.parser.svg_parser import parse_svg_string
from svgtools.writer.path_write_options import (
    PathCommandSet,
    PathCompactness,
    PathCoordinates,
)
from svgtools.writer.svg_writer import SvgWriter
from svgtools.writer.transform_strategy import TransformWriteStrategy

parser = argparse.ArgumentParser()

parser.add_argument("--in", dest="input")
parser.add_argument("--out", dest="output")
parser.add_argument("--transform-strategy",
                    dest="transform_strategy",
                    type=TransformWriteStrategy.__getitem__,
                    choices=TransformWriteStrategy,
                    metavar="{" + ",".join(e.name for e in TransformWriteStrategy) + "}",
                    default=TransformWriteStrategy.KEEP,
                    help="transformation conversion strategy (default: KEEP)",
                   )
parser.add_argument("--path-coordinates",
                    dest="path_coordinates",
                    type=PathCoordinates.__getitem__,
                    choices=PathCoordinates,
                    metavar="{" + ",".join(e.name for e in PathCoordinates) + "}",
                    default=PathCoordinates.ABSOLUTE,
                    help="coordinate representation in path (default: ABSOLUTE)",
                   )
parser.add_argument("--path-compactness",
                    dest="path_compactness",
                    type=PathCompactness.__getitem__,
                    choices=PathCompactness,
                    metavar="{" + ",".join(e.name for e in PathCompactness) + "}",
                    default=PathCompactness.CANONICAL,
                    help="Compact adjacent identical commands in path (default: CANONICAL)",
                   )
parser.add_argument("--path-command-set",
                    dest="path_command_set",
                    type=PathCommandSet.__getitem__,
                    choices=PathCommandSet,
                    metavar="{" + ",".join(e.name for e in PathCommandSet) + "}",
                    default=PathCommandSet.BASE,
                    help="Command set used in path (default: BASE)"
                   )

args = parser.parse_args()

if args.input:
    with open(args.input, encoding="utf-8") as infile:
        svg_input_text = infile.read()
else:
    svg_input_text = sys.stdin.read()

svg_doc = parse_svg_string(svg_input_text)

writer = SvgWriter(transform_strategy = args.transform_strategy,
                   path_coordinates = args.path_coordinates,
                   path_compactness = args.path_compactness,
                   path_command_set = args.path_command_set,
                  )
svg_output_text = writer.write_svg_string(svg_doc)

if args.output:
    with open(args.output, "w", encoding="utf-8") as outfile:
        outfile.write(svg_output_text)
else:
    sys.stdout.write(svg_output_text)

if args.transform_strategy == TransformWriteStrategy.CANONICAL_CONSERVATIVE:
   print(f"conservative stats (exact, forced): {writer.conservative_stats}", file=sys.stderr)
