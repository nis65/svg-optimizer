from svgtools.parser.float_list_parser import parse_float_list

def test_float_list_parser():
    assert parse_float_list("1 2 3") == (1, 2, 3)
    assert parse_float_list("1 2,3") == (1, 2, 3)
    assert parse_float_list("1,2,3") == (1, 2, 3)
    assert parse_float_list("   1  ,  2  3   ") == (1, 2, 3)
