
from svgtools.io import write_svg_file, parse_svg_file

from svgtools.model.scene.document import Document
from svgtools.model.scene.svg import Svg

def test_io_document_roundtrip(tmp_path):

    filename = tmp_path / "test.svg"
    d_before = Document(
            svg=Svg(
                children=(),
            )
        )
    write_svg_file(d_before, filename)
    assert filename.exists()
    d_after = parse_svg_file(filename)
    assert d_before == d_after
