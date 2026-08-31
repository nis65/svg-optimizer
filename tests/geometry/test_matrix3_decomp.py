import pytest

from svgtools.geometry.matrix3 import Matrix3, TRHxSDecomposition


def test_matrix3_decomp_scale_0():
    mt = Matrix3.scaling(0.0000000000000001, 3)
    with pytest.raises(ValueError):
        md = Matrix3.TRHxS_decompose(mt)  # noqa: F841


def test_matrix_decomp_det_is_0():
    mt = Matrix3.affine(1, 1, 1, 1.0000000000001, 0, 0)
    with pytest.raises(ValueError):
        md = Matrix3.TRHxS_decompose(mt)  # noqa: F841


def test_matrix3_decomp_translate():
    mt = Matrix3.translation(2, 3)
    md = Matrix3.TRHxS_decompose(mt)
    assert md == TRHxSDecomposition(
        tx=2,
        ty=3,
        theta_rotate=0,
        h_skew_x=0,
        sx=1,
        sy=1,
    )


def test_matrix3_decomp_rotate():
    mr = Matrix3.rotation(60, 0, 0)
    md = Matrix3.TRHxS_decompose(mr)
    assert md.isclose(
        TRHxSDecomposition(
            tx=0,
            ty=0,
            theta_rotate=60,
            h_skew_x=0,
            sx=1,
            sy=1,
        )
    )


def test_matrix3_decomp_translate_and_rotate():
    mt = Matrix3.translation(2, 3)
    mr = Matrix3.rotation(60, 0, 0)
    md = Matrix3.TRHxS_decompose(mt * mr)
    assert md.isclose(
        TRHxSDecomposition(
            tx=2,
            ty=3,
            theta_rotate=60,
            h_skew_x=0,
            sx=1,
            sy=1,
        )
    )


def test_matrix3_decomp_scale():
    ms = Matrix3.scaling(3, 4)
    md = Matrix3.TRHxS_decompose(ms)
    assert md.isclose(
        TRHxSDecomposition(
            tx=0,
            ty=0,
            theta_rotate=0,
            h_skew_x=0,
            sx=3,
            sy=4,
        )
    )


def test_matrix3_decomp_skewX():
    mh = Matrix3.skew_x(45)
    md = Matrix3.TRHxS_decompose(mh)
    assert md.isclose(
        TRHxSDecomposition(
            tx=0,
            ty=0,
            theta_rotate=0,
            h_skew_x=1,
            sx=1,
            sy=1,
        )
    )


def test_matrix3_decomp_any():
    # fmt: off
    m = Matrix3(
        1, 2, 3, 
        4, 5, 6, 
        0, 0, 1)
    # fmt: on
    m = Matrix3(1, 2, 3, 4, 5, 6, 0, 0, 1)
    md = Matrix3.TRHxS_decompose(m)
    assert m.isclose(
        Matrix3.translation(dx=md.tx, dy=md.ty)
        * Matrix3.rotation(theta_degree=md.theta_rotate, cx=0, cy=0)
        * Matrix3.skew_x(theta_degree=md.theta_skew_x)
        * Matrix3.scaling(sx=md.sx, sy=md.sy)
    )
