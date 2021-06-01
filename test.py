import skfem as fem
import elmer

from skfem.visuals.matplotlib import plot, show, draw

mesh = fem.MeshTri().refined(3)

case = elmer.Case(mesh, """
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

Body 2
  Equation = 1
  Body Force = 1
End

Body Force 1 :: Source = Real 1
Equation 1 :: Active Solvers(1) = 1

Solver 1
  Equation = "Poisson"

  Variable = "Potential"
  Variable DOFs = 1
  Procedure = "Poisson" "PoissonSolver"

  Element = "p:2"

  Linear System Solver = "Direct"
  Linear System Direct Method = UMFPack
  Steady State Convergence Tolerance = 1e-09
End

Boundary Condition 1
  Target Boundaries(4) = 1 2 3 4
  Potential = Real 0
End
""")

results = case.run(image='elmer-66fb3dda',
                   verbose=True,
                   fetch='results_t0001.vtu')


ax = draw(mesh)
plot(mesh, results.point_data['potential'].flatten(), ax=ax, shading='gouraud')
show()
