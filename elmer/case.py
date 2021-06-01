import tempfile

from .runners.docker import run
from .mesh import to_file


class Case:

    def __init__(self, mesh, sif):

        self.mesh = mesh
        self.sif = sif

    def run(self,
            verbose: bool = False,
            image: str = 'elmer',
            tag: str = 'latest'):

        with tempfile.TemporaryDirectory() as dirpath:
            to_file(self.mesh, "{}/tmpmesh".format(dirpath))
            if verbose:
                print(self.sif)
            run("{}/tmpmesh".format(dirpath),
                self.sif,
                verbose=verbose,
                image=image,
                tag=tag)
