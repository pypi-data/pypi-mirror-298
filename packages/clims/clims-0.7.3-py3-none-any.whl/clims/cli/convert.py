import click
from ase.io import read, write
from ase.io.formats import filetype
from clims.cli.citations import cite_and_print


@click.command()
@click.option(
    "--filein",
    type=click.Path(exists=True),
    default="geometry.in",
    show_default=True,
    help="File of input structure",
)
@click.option(
    "--formatin",
    type=str,
    show_default=True,
    help="Format of input file.",
)
@click.option(
    "--fileout",
    type=str,
    default="geometry-converted.in",
    show_default=True,
    help="File name for converted structure",
)
@click.option(
    "--formatout",
    type=str,
    show_default=True,
    help="Format of output file.",
)
@click.option(
    "--fractional", is_flag=True, help="Convert input file to fractional coordinates."
)
@click.option("--cartesian", is_flag=True, help="Convert input file to cartesian coordinates.")
def convert(filein, formatin, fileout, formatout, fractional, cartesian):
    """Convert input file to specified output file."""
    structure = read(filein, formatin)
    scaled = None
    kwargs = {}
    if (fractional is False) and (cartesian is False) and all(structure.pbc):
        scaled = True
    if fractional:
        scaled = True
    if formatout is None:
        if filetype(fileout, read=False) == "aims":
            kwargs["scaled"] = scaled
        if filetype(fileout, read=False) == "vasp":
            kwargs["direct"] = scaled
    write(fileout, structure, format=formatout, **kwargs)

    cite_and_print(["ase"])
