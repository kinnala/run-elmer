import tempfile

from typing import Optional

from numpy import ndarray

from .runners.docker import run
from .mesh import to_file


class Case:

    def __init__(self, mesh, sif):

        self.mesh = mesh
        self.sif = sif.format(**self._sif_mapping())

    def _sif_mapping(self):

        return {
            **{key: ix + 2 for ix, key in enumerate(self.mesh.subdomains)},
            **{key: ix + 2 for ix, key in enumerate(self.mesh.boundaries)},
        }

    def run(self,
            verbose: bool = False,
            image: str = 'ghcr.io/kinnala/elmer',
            tag: str = 'devel-ba15974',
            fetch: Optional[str] = None):

        retval = None

        with tempfile.TemporaryDirectory() as dirpath:
            to_file(
                self.mesh,
                "{}/tmpmesh".format(dirpath),
            )
            retval = run(
                "{}/tmpmesh".format(dirpath),
                self.sif,
                verbose=verbose,
                image=image,
                tag=tag,
                fetch=fetch,
            )

        return retval
