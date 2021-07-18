import elmer

from skfem import MeshTri


def test_elmer():
    m = MeshTri()
    case = elmer.Case(m, "")
    assert case.sif == ""
