import click
from clims.prepare_input import write_control
from pathlib import Path
from clims.cli.configure import get_config_value
from clims.prepare_submission import write_submission_file
from ase.io import read
from clims.cli.citations import cite_and_print


@click.command()
@click.option("--species", default="light", help="Specify species defaults", show_default=True)
@click.option("--relax", is_flag=True, help="Set relaxation flag.")
@click.option("--bands", is_flag=True, help="Attach band path.")
@click.option("--bands_mulliken", is_flag=True, help="Attach Mulliken-decomposed band path.")
@click.option("--dos", is_flag=True, help="Attach DOS output.")
@click.option("--submit-file", is_flag=True, help="Write submission file.")
@click.option("--hse06", is_flag=True, help="Use xc HSE06.")
@click.option("--vdwTS", is_flag=True, help="Use vdW-TS corrections.")
@click.option("--forces", is_flag=True, help="Compute forces.")
@click.option("--stress", is_flag=True, help="Compute (analytical) stress.")
@click.option(
    "--keyword", type=(str, str), multiple=True, help="Add additional keywords to control.in."
)
def prepare_run(
    species,
    relax,
    bands,
    bands_mulliken,
    dos,
    submit_file,
    hse06,
    vdwts,
    forces,
    stress,
    keyword,
):
    """Prepares control.in template file in the CWD, if geometry.in is in CWD

    Provides only a minimum of needed flags to make it run. Following scenarios are coverd:

    1. No control.in file: Creates a new file with minimum flags and species attached\n
    2. control.in file with flags: Attaches the needed species\n
    3. control.in file with species: do nothing\n
    """
    try:
        AIMS_SPECIES = Path(get_config_value("species_path"))
    except:
        return
    species_dir = AIMS_SPECIES / species
    print(species_dir)
    try:
        geo = read("geometry.in", format="aims")
        print("-- Found geometry.in file")
    except:
        print("**ERROR**: No control.in file generated: No geometry.in found!")
        raise
    CWD = Path(".")
    # more kw
    if keyword:
        kw = dict(keyword)
    else:
        kw = {}
    if vdwts:
        kw.update({"vdw_correction_hirshfeld": True})
    if forces:
        kw.update({"compute_forces": True})
    if stress:
        kw.update({"compute_analytical_stress": True})
    write_control(
        geo,
        CWD,
        species_dir,
        relax=relax,
        bands=bands,
        bands_mulliken=bands_mulliken,
        dos=dos,
        hse06=hse06,
        **kw
    )

    if submit_file:
        header = get_config_value("submission_header")
        mpi_command = get_config_value("mpi_command")
        aims_executable = get_config_value("aims_executable")
        output_name = get_config_value("output_name")
        error_name = get_config_value("error_name")
        if all([header, mpi_command, aims_executable, output_name, error_name]):
            write_submission_file(
                header, mpi_command, aims_executable, output_name, error_name
            )
        else:
            print(
                "Some configurations missing. Please check if you have configured the following:"
            )
            print("  submission_header, mpi_command, aims_executable, output_name, error_name")

    cite_and_print(["ase"])
