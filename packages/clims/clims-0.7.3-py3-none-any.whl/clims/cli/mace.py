import click
import spglib  # We need to import spglib here to suppress the warnings


@click.command()
@click.option(
    "--filein",
    type=click.Path(exists=True),
    default="geometry.in",
    show_default=True,
    help="File name of input structure.",
)
@click.option(
    "--format",
    type=str,
    default="aims",
    show_default=True,
    help="Format of input structure.",
)
@click.option(
    "--fmax",
    type=float,
    default=0.01,
    show_default=True,
    help="Maximum residual force.",
)
@click.option(
    "--fix-symmetry",
    is_flag=True,
    help="Fix spacegroup symmetry for relaxation.",
)
@click.option(
    "--relax-unit-cell",
    is_flag=True,
    help="Also relax the lattice vectors.",
)
@click.option(
    "--trajectory",
    type=str,
    default="bfgs.traj",
    show_default=True,
    help="Name of the ASE trajectory file.",
)
def clims_prerelax(filein, format, fmax, fix_symmetry, relax_unit_cell, trajectory):
    """
    Relaxation of input structure FILEIN with the mace-mp-0 force field up to residual
    forces of FMAX. Here, only the atomic positions are relaxed, while the lattice
    vectors are kept fixed. The force field should work well for most non-magnetic bulk
    systems.
    """
    import warnings

    warnings.filterwarnings("ignore")

    from ase.optimize import BFGS
    from ase.io import read
    from ase.constraints import FixSymmetry, UnitCellFilter
    from clims.cli.citations import cite_and_print

    try:
        from mace.calculators import mace_mp
    except:
        print(
            "*** Mace is not installed. ***\nPlease install with the following command:\n\n  pip install 'clims[mace]'\n"
        )
        return

    macemp = mace_mp(default_dtype="float64")  # return ASE calculator
    atoms = read(filein, format=format)

    atoms.calc = macemp

    atoms_relax = atoms
    if fix_symmetry:
        atoms.set_constraint(FixSymmetry(atoms))
        atoms_relax = atoms
    if relax_unit_cell and atoms.pbc.all():
        atoms_relax = UnitCellFilter(atoms)

    relax = BFGS(atoms_relax, trajectory=trajectory)

    for ii, _ in enumerate(relax.irun(fmax=fmax)):
        atoms.write(f"geometry.in.next_step.{ii:03}", "aims", scaled=atoms.pbc.all())

    cite_and_print(["ase", "mace-mp-0"])
