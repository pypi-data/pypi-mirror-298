from ase.io import read, write
from ase import Atoms
from phonopy.structure.atoms import PhonopyAtoms
from phonopy import Phonopy
from pathlib import Path
import numpy as np


def write_phonopy_disp_yaml(phonon, calculator, supercell_matrix):

    from phonopy.interface.calculator import get_default_physical_units
    from phonopy.interface.phonopy_yaml import PhonopyYaml

    filename = "phonopy_disp.yaml"
    yaml_settings = {
        "force_sets": False,
        "force_constants": False,
        "born_effective_charge": False,
        "dielectric_constant": False,
        "displacements": True,
    }
    adim = [str(x) for x in np.array(supercell_matrix).flatten()]
    dim = " ".join(adim)

    phonopy_confs = {
        "dim": dim,
        "calculator": calculator,
        "create_displacements": ".true.",
    }

    units = get_default_physical_units(calculator)

    phpy_yaml = PhonopyYaml(
        configuration=phonopy_confs, physical_units=units, settings=yaml_settings
    )
    phpy_yaml.set_phonon_info(phonon)
    with open(filename, "w") as w:
        w.write(str(phpy_yaml))


def initialize_phonopy(
    structure,
    structure_file="geometry.in",
    structure_format="aims",
    supercell_matrix=[[1, 0, 0], [0, 1, 0], [0, 0, 1]],
    primitive_matrix="auto",
    displacement=0.01,
):

    atoms = PhonopyAtoms(
        symbols=structure.get_chemical_symbols(),
        cell=structure.get_cell(),
        scaled_positions=structure.get_scaled_positions(),
    )

    phonon = Phonopy(atoms, supercell_matrix, primitive_matrix=primitive_matrix)
    phonon.generate_displacements(distance=displacement)
    supercells = phonon.get_supercells_with_displacements()

    n_digits = len(str(len(supercells))) + 1
    p = Path(".")
    for i, supercell in enumerate(supercells):
        atoms = Atoms(
            symbols=supercell.get_chemical_symbols(),
            scaled_positions=supercell.get_scaled_positions(),
            cell=supercell.get_cell(),
            pbc=True,
        )
        displacement = p / f"displacement-{str(i).zfill(n_digits)}"
        displacement.mkdir(exist_ok=True)
        print(f"Creating displacement in directory: {displacement.as_posix()}")
        write(displacement / structure_file, atoms, format=structure_format)

    write_phonopy_disp_yaml(phonon, structure_format, supercell_matrix)


def parse_forces(num_atoms, outfile):
    from phonopy.interface.aims import parse_set_of_forces

    p = Path(".")
    output_files = [str(s) for s in p.glob(f"**/{outfile}")]
    print("Found following output files:")
    for output_file in output_files:
        print(output_file)
    forces = parse_set_of_forces(num_atoms, output_files)
    return forces


def post_process_phonopy(mesh=[20, 20, 20], outfile="aims.out", show=False, born=False):
    from phonopy import load
    from phonopy.file_IO import get_born_parameters
    from phonopy.phonon.band_structure import get_band_qpoints_and_path_connections
    from ase.dft.kpoints import resolve_kpt_path_string

    phonon = load(phonopy_yaml="phonopy_disp.yaml", produce_fc=False, is_nac=False)
    primitive = phonon.primitive

    # Parse forces from aims.out files
    n_atoms = phonon.supercell.get_number_of_atoms()
    forces = parse_forces(n_atoms, outfile)
    n_atoms_supercell = len(forces[0])
    assert n_atoms == n_atoms_supercell

    # Do we need non-analytic correction (polar materials)? Yes -> read BORN file
    if born:
        nac_params = get_born_parameters(open("BORN"), primitive, phonon.primitive_symmetry)
        if nac_params is None:
            print("\n***ERROR***: Please correct BORN file. Stopping.\n")
            return
        phonon.set_nac_params(nac_params)

    # Prepare displacement_dataset for phonopy and produce force constants
    first_atoms = []
    for fs, disp in zip(forces, phonon.get_displacements()):
        first_atoms.append({"number": disp[0], "displacement": disp[1:], "forces": fs})
    displacement_dataset = {"natom": n_atoms_supercell, "first_atoms": first_atoms}
    phonon.dataset = displacement_dataset
    phonon.produce_force_constants()

    # Run and write phonon DOS
    phonon.run_mesh(mesh)
    phonon.run_total_dos()
    phonon.write_total_dos()

    # Run and write phonon band structure
    # We are using tools from ASE, which is why we construct atoms object first
    atoms = Atoms(
        symbols=primitive.get_chemical_symbols(),
        cell=primitive.get_cell(),
        positions=primitive.get_positions(),
        pbc=True,
    )
    bp = atoms.cell.bandpath()
    labels, bands = resolve_kpt_path_string(bp.path, bp.special_points)
    labels = [
        l if l != "G" else "$\\Gamma$" for label in labels for l in label
    ]  # need to flatten the array and replace G with Latex Gamma
    print(labels)
    qpoints, connections = get_band_qpoints_and_path_connections(bands, npoints=51)
    phonon.run_band_structure(qpoints, path_connections=connections, labels=labels)
    phonon.write_yaml_band_structure()

    # Show phonon DOS and band structure
    if show:
        phonon.plot_band_structure_and_dos().show()
    phonon.save()
