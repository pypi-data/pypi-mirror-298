import click
from clims.structure import Structure
from ase.io.formats import read, ioformats
from clims.cli.citations import cite_and_print


@click.command()
@click.option(
    "--filein",
    default="geometry.in",
    type=click.Path(exists=True),
    show_default=True,
    help="Name of the input file",
)
@click.option(
    "--format",
    default="aims",
    show_default=True,
    help="In- and output format of structure files",
)
@click.option("--symthresh", default=1e-5, help="Threshold for crystal symmetry detection")
@click.option("--primitive", is_flag=True, help="Write primitive to file.")
@click.option("--conventional", is_flag=True, help="Write conventional to file.")
def unit_cell_info(filein, format, symthresh, primitive, conventional):
    """
    Show information for the input structure. Mainly intended for periodic structures. The following quantities are written:

    * Number of atoms in the input structure.

    * Chemical formula of the input structure (alphabetically ordered).

    * The unit cell parameters (lattice constants and angles) of the input structure.

    * Name of the Bravais lattice of the refined (= symmetrized + standardized) structure (from spglib).

    * The spacegroup number and Hall symbol of the refined structure.

    * The Wyckoff positions of the refined structure (if spacegroup number > 1). The numbers in parenthesis denote the indeces of the unique atoms that occupy this position.

    * Whether the refined structure is primitive.

    * The used symmetry threshold.

    The input structure can be converted to the standardized primitive and conventional cell (using spglib).
    """
    try:
        c = read(filein, format=format)
    except:
        click.echo(f'ERROR: Could not identify format of input file "{filein}"')
        click.echo('Please specify the format of input file by "--format".')
        click.echo("Available formats are:")
        ase_formats = list(ioformats.keys())
        for a, b, c in zip(ase_formats[::3], ase_formats[1::3], ase_formats[2::3]):
            print("{:<30}{:<30}{:<}".format(a, b, c))
        raise
    si = Structure(c, symthresh)
    if (conventional or primitive) and not all(c.pbc):
        click.echo(
            f'ERROR: "{filein}" is not a periodic structure. Cannot write conventional or primitive cell.'
        )
        return
    if conventional:
        click.echo("Writing conventional unit cell (refined)")
        si.write_refined()
    if primitive:
        click.echo("Writing primitive unit cell (refined)")
        si.write_primitive()
    click.echo(si)

    cite_and_print(["ase", "spglib"])
