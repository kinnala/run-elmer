import pytest
import run_elmer as elmer

poisson = """
Check Keywords "Warn"

Header
  Mesh DB "." "."
End

Simulation
  Max Output Level = 5
  Coordinate System = Cartesian
  Simulation Type = Steady
  Output Intervals(1) = 1
  Steady State Max Iterations = 1
  Post File = "results.vtu"
End

Body 1
  Equation = 1
  Body Force = 1
End

Body Force 1 :: Source = Real 1.0
Equation 1 :: Active Solvers(1) = 1

Solver 1
  Equation = "Poisson"
  Variable = "Potential"
  Variable DOFs = 1
  Procedure = "Poisson" "PoissonSolver"
  Linear System Solver = "Direct"
  Linear System Direct Method = UMFPack
  Steady State Convergence Tolerance = 1e-09
End

Boundary Condition 1
  Target Boundaries(1) = -1
  Potential = Real 0
End

"""

def test_poisson():
    m = elmer.MeshTri().refined(3)
    out = elmer.run(
        m,
        poisson,
        # verbose=True,
    )
    assert 'potential' in out.point_data
    assert len(out.points) == m.p.shape[1]
    x = out.point_data['potential'].flatten()
    assert x.min() >= 0.
    assert x.max() <= 0.073
    assert x.max() >= 0.072
