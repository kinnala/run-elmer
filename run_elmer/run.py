import tempfile

from typing import Optional

from numpy import ndarray

from .runners.docker import run as run_docker
from .export import to_file


def run(mesh,
        sif,
        verbose=False,
        runner=None,
        outfile='results_t0001.vtu',
        **kwargs):
    """Run the case.

    Parameters
    ----------
    mesh
    sif
    verbose
    runner
    outfile

    Rest of the keyword arguments are passed to ``runner``.

    """

    if runner is None:
        runner = run_docker

    mio = None

    if mesh.subdomains is None:
        mesh = mesh.with_subdomains({'domain': lambda x: 0 * x[0] + 1})

    with tempfile.TemporaryDirectory() as dirpath:
        to_file(
            mesh,
            dirpath,
        )
        mio = runner(
            "{}/mesh".format(dirpath),
            sif,
            outfile,
            verbose,
            **kwargs,
        )

    return mio
