import numpy as np

from .run import run

from skfem import Mesh, MeshTri, MeshTet, MeshQuad, MeshHex


def mesh(arg1=None, arg2=None):

    if arg2 is None:
        if isinstance(arg1, str):
            return Mesh.load(arg1)

    if isinstance(arg1, list) and isinstance(arg2, list):
        arg1 = np.array(arg1, np.float64)
        arg2 = np.array(arg2, np.int64)

    assert isinstance(arg1, np.ndarray)
    assert isinstance(arg2, np.ndarray)

    if arg1.shape[0] > arg1.shape[1]:
        arg1 = arg1.T
        arg2 = arg2.T

    if arg1.shape[0] == 2:
        if arg2.shape[0] == 3:
            m = MeshTri(arg1, arg2)
        elif arg2.shape[0] == 4:
            m = MeshQuad(arg1, arg2)
    elif arg1.shape[0] == 3:
        if arg2.shape[0] == 4:
            m = MeshTet(arg1, arg2)
        elif arg2.shape[0] == 8:
            m = MeshHex(arg1, arg2)

    return m


def target_boundaries(mesh, *keys):

    boundaries = list(mesh.boundaries.keys())
    keylist = []
    for key in keys:
        keylist.append(str(boundaries.index(key) + 1))
    return "Target Boundaries({}) = {}".format(
        len(keylist),
        ' '.join(keylist)
    )


def targets(mesh):

    targets = {}

    if mesh.boundaries is not None:
        boundaries = list(mesh.boundaries.keys())
        targets['boundaries'] = {}
        for key in boundaries:
            targets['boundaries'][key] = "Target Boundaries({}) = {}".format(
                1,
                boundaries.index(key) + 1,
            )

    if mesh.subdomains is not None:
        subdomains = list(mesh.subdomains.keys())
        targets['bodies'] = {}
        for key in subdomains:
            targets['bodies'][key] = "Target Bodies({}) = {}".format(
                1,
                subdomains.index(key) + 1,
            )

    return targets


def plot(mesh, x, edges=False):
    from skfem.visuals.matplotlib import plot, draw
    if len(x.shape) > 1:
        x = x.flatten()
    if edges:
        ax = draw(mesh)
        return plot(mesh, x, ax=ax, shading='gouraud')
    return plot(mesh, x, shading='gouraud')
