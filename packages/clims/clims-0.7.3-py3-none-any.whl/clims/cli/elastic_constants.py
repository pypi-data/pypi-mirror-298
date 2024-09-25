import click
from ase.io import read
import elastic
from pathlib import Path
from ase.units import GPa
from clims.cli.citations import cite_and_print
import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning)


@click.group()
def clims_elastic():
    """
    Simple wrapper around Elastic for FHI-aims to compute the elastic tensor and/or the
    equation of state.
    """


@clims_elastic.command()
@click.option(
    "--action",
    type=click.Choice(["cij", "eos"]),
    default="cij",
    help="Generate deformations for elastic constants (cij) or equation of state (eos).",
)
@click.option(
    "--n_deformations",
    default=5,
    type=int,
    help="Number of generated deformations per axis (default: 5)",
)
@click.option(
    "--volume_change",
    default=0.02,
    type=int,
    help="Maximum relative volume change w.r.t V_0.",
)
@click.option(
    "--size",
    default=2.0,
    type=float,
    show_default=True,
    help="Deformation size for Cij scan (% or deg., default: 2.0)",
)
def initialize(action, n_deformations, volume_change, size):
    """
    Generate deformed structures for the computation of the elastic constants and the
    equation of motion with the package 'Elastic'.
    """

    c = read("geometry.in")
    p = Path(".")
    _, brav, sg, _ = elastic.elastic.get_lattice_type(c)
    click.echo(f"{brav} lattice ({sg}): {c.get_chemical_formula()}")
    if action == "cij":
        systems = elastic.get_elementary_deformations(c, n=n_deformations, d=size)
    elif action == "eos":
        systems = elastic.scan_volumes(
            c, n=n_deformations, lo=1 - volume_change, hi=1 + volume_change
        )
    systems.insert(0, c)
    click.echo(f"Writing {len(systems)} deformation files.")
    for n, s in enumerate(systems):
        d = p / f"{action}_{n:03}"
        d.mkdir()
        s.write(d / "geometry.in", scaled=False)

    cite_and_print(["elastic"])


@clims_elastic.command()
@click.option(
    "--action",
    type=click.Choice(["cij", "eos"]),
    default="cij",
    help="Generate deformations for elastic constants (cij) or equation of state (eos).",
)
@click.option("--pwd", type=click.Path(exists=True), default=".")
def postprocess(action, pwd):
    """
    Read the FHI-aims output files from the subdirectories and compute the elastic tensor
    (cij) of the equation of state (eos).
    """

    def reader(f):
        print(f"Reading file {f}")
        return read(f)

    p = Path(pwd)
    outputs = sorted(
        [
            (d / "aims.out").as_posix()
            for d in p.iterdir()
            if d.is_dir() and action in d.as_posix()
        ]
    )
    outputs = [reader(o) for o in outputs]

    if action == "cij":
        cij = elastic.get_elastic_tensor(outputs[0], systems=outputs[1:])
        msv = cij[1][3].max()
        eps = 1e-4
        click.echo("\nCij solution\n" + 30 * "-")
        click.echo(
            f" Solution rank: {cij[1][2]:2d}{' (undetermined)' if cij[1][2] < len(cij[0]) else ''}"
        )
        if cij[1][2] == len(cij[0]):
            click.echo(f" Square of residuals: {cij[1][1]:7.2g}")
        click.echo(" Relative singular values:")
        for sv in cij[1][3] / msv:
            click.echo(f"{sv:7.4f}{'* ' if (sv) < eps else '  '}", nl=False)
        click.echo("\n\nElastic tensor (GPa):")
        for dsc in elastic.elastic.get_cij_order(outputs[0]):
            click.echo(f"{dsc:>7}  ".format(dsc), nl=False)
        click.echo("\n" + 30 * "-")
        for c, sv in zip(cij[0], cij[1][3] / msv):
            click.echo(f"{c / GPa:7.2f}{'* ' if sv < eps else '  '}", nl=False)
        click.echo()
    elif action == "eos":
        eos = elastic.get_BM_EOS(outputs[0], systems=outputs[1:])
        eos[1] /= GPa
        click.echo("# %7s (A^3)  %7s (GPa)   %7s" % ("V0", "B0", "B0'"))
        click.echo("    %7.2f        %7.2f        %7.2f" % tuple(eos))

    cite_and_print(["ase", "elastic"])
