from pathlib import Path
DATA = Path(__file__).parent / "testdata"

from svgtools.io import write_svg_file, parse_svg_file

def test_io_document_roundtrip(tmp_path):

    start = DATA / "logo.svg"

    gen1 = tmp_path / "gen1.svg"
    write_svg_file(parse_svg_file(start), gen1)

    gen2 = tmp_path / "gen2.svg"
    write_svg_file(parse_svg_file(gen1), gen2)

    assert gen1.read_bytes() == gen2.read_bytes()
