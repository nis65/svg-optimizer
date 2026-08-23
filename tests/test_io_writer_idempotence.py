from pathlib import Path

import pytest

from svgtools.io import parse_svg_file, write_svg_file

DATA = Path(__file__).parent / "testdata"

@pytest.mark.parametrize("start", DATA.glob("*.svg"), ids=lambda p: p.name)

def test_io_writer_idempotence(start, tmp_path):

    gen1 = tmp_path / "gen1.svg"
    write_svg_file(parse_svg_file(start), gen1)

    gen2 = tmp_path / "gen2.svg"
    write_svg_file(parse_svg_file(gen1), gen2)

    assert gen1.read_bytes() == gen2.read_bytes()
