"""Elmer import and export."""

import numpy as np
from numpy import ndarray

from typing import Optional
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
    npts = mesh.nvertices
    nt = mesh.nelements
    nfacets = mesh.nfacets
    mesh_type = type(mesh)

    # build t_id and boundary_id
    t_id = None
    boundary_id = None

    if mesh.subdomains is not None:
        t_id = np.ones(nt, dtype=np.int64)
        for ix, key in enumerate(mesh.subdomains):
            t_id[mesh.subdomains[key]] = ix + 2

    if mesh.boundaries is not None:
        boundary_id = np.ones(nfacets, dtype=np.int64)
        for ix, key in enumerate(mesh.boundaries):
            boundary_id[mesh.boundaries[key]] = ix + 2

    if isinstance(mesh, MeshHex):
        mesh = replace(mesh, t=mesh.t[[1, 5, 3, 0, 4, 7, 6, 2]])

    # filename.header
    with open(filename + '.header', 'w') as handle:
        handle.write("{} {} {}\n".format(npts,
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
        for itr in range(npts):
            handle.write("{} -1 {} {} {}\n".format(
                itr + 1,
                mesh.p[0, itr],
                mesh.p[1, itr],
                mesh.p[2, itr] if mesh.p.shape[0] > 2 else 0.
            ))

    # filename.elements
    with open(filename + '.elements', 'w') as handle:
        for itr in range(nt):
            handle.write(("{} {} {}"
                          + (" {}" * mesh.t.shape[0])
                          + "\n").format(
                              itr + 1,
                              1 if t_id is None else t_id[itr],
                              MESH_TYPE_MAPPING[mesh_type],
                              *(mesh.t[:, itr] + 1)
                          ))

    # filename.boundary
    with open(filename + '.boundary', 'w') as handle:
        for itr in mesh.boundary_facets():
            handle.write(("{} {} {} {} {}"
                          + " {}" * mesh.facets.shape[0]
                          + "\n").format(
                itr + 1,
                1 if boundary_id is None else boundary_id[itr],
                mesh.f2t[0, itr] + 1,
                mesh.f2t[1, itr] + 1,
                BOUNDARY_TYPE_MAPPING[mesh_type],
                *(mesh.facets[:, itr] + 1)
            ))
