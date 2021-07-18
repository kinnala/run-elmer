import elmer


def test_elmer():
    m = elmer.MeshTri()
    case = elmer.Case(m, "")
    assert case.sif == ""
