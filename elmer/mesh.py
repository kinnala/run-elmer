"""Elmer import and export."""

from skfem.mesh import Mesh, MeshTri, MeshQuad, MeshTet, MeshHex
from dataclasses import replace


MESH_TYPE_MAPPING = {
    MeshTet: '504',
    MeshHex: '808',
    MeshTri: '303',
    MeshQuad: '404',
}

BOUNDARY_TYPE_MAPPING = {
    MeshTet: '303',
    MeshHex: '404',
    MeshTri: '202',
    MeshQuad: '202',
}


def to_file(mesh: Mesh, filename: str):
    """The mesh is written to four files.

    The files are 'filename.{header,nodes,elements,boundary}'.

    Parameters
    ----------
    mesh
        The mesh object to export.
    filename
        The prefix of the filenames.

    """
    np = mesh.p.shape[1]
    nt = mesh.t.shape[1]
    mesh_type = type(mesh)

    if isinstance(mesh, MeshHex):
        mesh = replace(mesh, t=mesh.t[[1, 5, 3, 0, 4, 7, 6, 2]])

    # filename.header
    with open(filename + '.header', 'w') as handle:
        handle.write("{} {} {}\n".format(np,
                                         nt,
                                         len(mesh.boundary_facets())))
        handle.write("2\n")
        handle.write("{} {}\n".format(
            MESH_TYPE_MAPPING[mesh_type],
            nt
        ))
        handle.write("{} {}\n".format(
            BOUNDARY_TYPE_MAPPING[mesh_type],
            len(mesh.boundary_facets())
        ))

    # filename.nodes
    with open(filename + '.nodes', 'w') as handle:
        for itr in range(np):
            handle.write("{} -1 {} {} {}\n".format(
                itr + 1,
                mesh.p[0, itr],
                mesh.p[1, itr],
                mesh.p[2, itr] if mesh.p.shape[0] > 2 else 0.
            ))

    # filename.elements
    with open(filename + '.elements', 'w') as handle:
        for itr in range(nt):
            handle.write(("{} 1 {}"
                          + (" {}" * mesh.t.shape[0])
                          + "\n").format(
                itr + 1,
                MESH_TYPE_MAPPING[mesh_type],
                *(mesh.t[:, itr] + 1)
            ))

    # filename.boundary
    with open(filename + '.boundary', 'w') as handle:
        for itr in mesh.boundary_facets():
            handle.write(("{} 1 {} {} {}"
                          + " {}" * mesh.facets.shape[0]
                          + "\n").format(
                itr + 1,
                mesh.f2t[0, itr] + 1,
                mesh.f2t[1, itr] + 1,
                BOUNDARY_TYPE_MAPPING[mesh_type],
                *(mesh.facets[:, itr] + 1)
            ))
