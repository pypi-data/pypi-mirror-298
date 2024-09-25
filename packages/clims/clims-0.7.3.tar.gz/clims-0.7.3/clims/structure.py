from ase.io import read, write
import spglib as spg
import numpy as np
from ase.atoms import Atoms
from ase.cell import Cell


class Structure:
    c_info = []

    def __init__(self, c, sym_thresh=1e-5):

        self.add("Number of atoms", len(c))
        self.add("Chemical formula", c.get_chemical_formula())

        if all(c.pbc):
            lattice = c.get_cell()[:]
            positions = c.get_scaled_positions()
            numbers = c.get_atomic_numbers()
            magmoms = c.get_initial_magnetic_moments()
            cell = (lattice, positions, numbers, magmoms)
            dataset = spg.get_symmetry_dataset(cell, symprec=sym_thresh)
            # Get primitive unit cell
            plattice, pscaled_positions, pnumbers = spg.find_primitive(
                cell, symprec=sym_thresh
            )
            self.primitive = Atoms(
                cell=plattice, pbc=True, scaled_positions=pscaled_positions, numbers=pnumbers
            )
            # Refine cell
            rlattice, rscaled_positions, rnumbers = spg.refine_cell(cell, symprec=sym_thresh)
            self.refined = Atoms(
                cell=rlattice, pbc=True, scaled_positions=rscaled_positions, numbers=rnumbers
            )
            self.add("Unit cell parameters (original)", np.around(c.cell.cellpar(), 10))
            bravais = Cell(lattice).get_bravais_lattice(eps=sym_thresh)
            self.add(
                "Bravais lattice (symmetrized)", "{} {}".format(bravais.longname, bravais)
            )
            self.add("Spacegroup number", dataset.number)
            self.add("Hall symbol", dataset.hall)
            wy = dataset.wyckoffs
            unique_atoms, count = np.unique(dataset.equivalent_atoms, return_counts=True)
            e_atoms = {}
            for ua in unique_atoms:
                e_atoms[ua] = [
                    str(i + 1) for i, ea in enumerate(dataset.equivalent_atoms) if ea == ua
                ]
            if dataset.number > 1:
                self.add(
                    "Occupied Wyckoff positions",
                    f"\n{' '*34}".join(
                        f"{c}*{wy[w]} ({', '.join(e_atoms[w])})"
                        for (w, c) in zip(unique_atoms, count)
                    ),
                )
            self.add("Is primitive cell?", len(c) == len(pnumbers))
            self.add("Symmetry threshold", sym_thresh)

    def __str__(self):
        str_str = "\nStructure Info\n" + "-" * 14 + "\n"
        for info in self.c_info:
            if isinstance(info[1], (list, np.ndarray)):
                fmt_str = "{:32}: " + "{} " * len(info[1]) + "\n"
                str_str += fmt_str.format(info[0], *info[1])
            else:
                fmt_str = "{:32}: {}\n"
                str_str += fmt_str.format(info[0], info[1])
        return str_str

    def add(self, info_str, info_value):
        self.c_info.append([info_str, info_value])

    def write_primitive(self):
        write("geometry-primitive.in", self.primitive, format="aims", scaled=True)

    def write_refined(self):
        write("geometry-conventional.in", self.refined, format="aims", scaled=True)
