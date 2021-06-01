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

        to_file(self.mesh, "tmptest")
        if verbose:
            print(self.sif)
        run("tmptest",
            self.sif,
            verbose=verbose,
            image=image,
            tag=tag)
