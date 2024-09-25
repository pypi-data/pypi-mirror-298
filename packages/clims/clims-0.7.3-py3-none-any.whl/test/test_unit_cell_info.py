from ase.spacegroup import crystal
from click.testing import CliRunner
from clims.cli.unit_cell_info import unit_cell_info
from ase.io import write, read
import numpy as np
from pathlib import Path

Fe2O3 = crystal(
    ("Fe", "O"),
    basis=[
        (0.3333333333333334, 0.6666666666666667, 0.3116866666666667),
        (0.0251333333333334, 0.3584666666666668, 0.4166666666666667),
    ],
    cellpar=[5.0342021271, 5.0342021271, 13.75191, 90.0, 90.0, 120.0],
    spacegroup=167,
    primitive_cell=True,
)

unit_cell_info_output = """Writing conventional unit cell (refined)
Writing primitive unit cell (refined)

Structure Info
--------------
Number of atoms                 : 10
Chemical formula                : Fe4O6
Unit cell parameters (original) : 5.4277538 5.4277538 5.4277538 55.2582374093 55.2582374093 55.2582374093 
Bravais lattice (symmetrized)   : primitive rhombohedral RHL(a=5.42775, alpha=55.2582)
Spacegroup number               : 167
Hall symbol                     : -R 3 2"c
Occupied Wyckoff positions      : 4*c (1, 2, 7, 8)
                                  6*e (3, 4, 5, 6, 9, 10)
Is primitive cell?              : True
Symmetry threshold              : 1e-05


Please consider to cite the following publications:

[ase]       Larsen, Ask Hjorth, et al.
            The Atomic Simulation Environment—A Python library for working with atoms
            J. Phys.: Condens. Matter 29, 273002 (2017)
            https://doi.org/10.1088/1361-648X/aa680e

[spglib]    Togo, Atsushi  and Tanaka, Isao 
            Spglib: a software library for crystal symmetry search
            arXiv preprint arXiv:1808.01590 (2018)
            https://arxiv.org/abs/1808.01590

"""


def test_unit_cell_info():
    runner = CliRunner()
    with runner.isolated_filesystem():
        write("geometry.in", Fe2O3, scaled=True)
        result = runner.invoke(unit_cell_info, ["--conventional", "--primitive"])
        assert result.exit_code == 0
        assert Path("geometry-primitive.in").exists()
        assert Path("geometry-conventional.in").exists()
        conventional = read("geometry-conventional.in")
        primitive = read("geometry-primitive.in")
        assert len(conventional) == 30
        assert len(primitive) == 10
        assert result.output == unit_cell_info_output
