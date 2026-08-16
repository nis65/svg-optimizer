import math

def geometry_isclose(a: float, b: float):
    return math.isclose(a, b, rel_tol=1e-9, abs_tol=1e-9)
