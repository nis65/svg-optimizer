from svgtools.model.geometry.matrix3 import Matrix3

def test_matrix3_decomp_translate():
    mt = Matrix3.translation(2,3)
    (m_T, m_R, m_Hx, m_S) = Matrix3.decompose(mt)
    assert (m_T, m_R, m_Hx, m_S) == (
        mt,
        Matrix3.identity(),
        Matrix3.identity(),
        Matrix3.identity(),
    )

def test_matrix3_decomp_rotate():
    mr = Matrix3.rotation(60, 0, 0)
    (m_T, m_R, m_Hx, m_S) = Matrix3.decompose(mr)
    assert (m_T, m_R, m_Hx, m_S) == (
        Matrix3.identity(),
        mr,
        Matrix3.identity(),
        Matrix3.identity(),
    )

def test_matrix3_decomp_translate_and_rotate():
    mt = Matrix3.translation(2,3)
    mr = Matrix3.rotation(60, 0, 0)
    (m_T, m_R, m_Hx, m_S) = Matrix3.decompose(mt*mr)
    assert (m_T, m_R, m_Hx, m_S) == (
        mt,
        mr,
        Matrix3.identity(),
        Matrix3.identity(),
    )

def test_matrix3_decomp_scale():
    ms = Matrix3.scaling(3,4)
    (m_T, m_R, m_Hx, m_S) = Matrix3.decompose(ms)
    assert (m_T, m_R, m_Hx, m_S) == (
        Matrix3.identity(),
        Matrix3.identity(),
        Matrix3.identity(),
        ms
    )

def test_matrix3_decomp_skewX():
    mh = Matrix3.skew_x(45)
    (m_T, m_R, m_Hx, m_S) = Matrix3.decompose(mh)
    assert (m_T, m_R, m_Hx, m_S) == (
        Matrix3.identity(),
        Matrix3.identity(),
        mh,
        Matrix3.identity(),
    )

def test_matrix3_decomp_any():
    m = Matrix3(
        1,2,3,
        4,5,6,
        0,0,1
        )
    (m_T, m_R, m_Hx, m_S) = Matrix3.decompose(m)
    assert m.isclose(m_T * m_R * m_Hx * m_S)
