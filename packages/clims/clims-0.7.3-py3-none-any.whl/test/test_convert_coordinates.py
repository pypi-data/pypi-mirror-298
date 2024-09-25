from click.testing import CliRunner
from clims.cli.convert import convert
from ase.build import bulk
from ase.io import write
from test.file_comparison import compare_geo_files


GaAs = bulk("GaAs", crystalstructure="zincblende", a=5.65315)


def test_real2frac():
    runner = CliRunner()
    with runner.isolated_filesystem():
        write("geometry.in", GaAs, scaled=False)
        result = runner.invoke(convert)
        with open("geometry.out_ref", "w") as f:
            f.write(frac_coordinates)
        compare_geo_files("geometry-converted.in", "geometry.out_ref")


def test_frac2real():
    runner = CliRunner()
    with runner.isolated_filesystem():
        write("geometry.in", GaAs, scaled=True)
        result = runner.invoke(convert, args="--cartesian")
        with open("geometry.out_ref", "w") as f:
            f.write(real_coords)
        compare_geo_files("geometry-converted.in", "geometry.out_ref")


real_coords = """\
#===============================================================================
# Created using the Atomic Simulation Environment (ASE)

# Mon Sep  9 17:46:53 2024

#=======================================================
lattice_vector 0.0000000000000000 2.8265750000000001 2.8265750000000001
lattice_vector 2.8265750000000001 0.0000000000000000 2.8265750000000001
lattice_vector 2.8265750000000001 2.8265750000000001 0.0000000000000000
atom 0.0000000000000000 0.0000000000000000 0.0000000000000000 Ga
atom 1.4132875000000000 1.4132875000000000 1.4132875000000000 As
"""
frac_coordinates = """\
#===============================================================================
# Created using the Atomic Simulation Environment (ASE)

# Mon Sep  9 17:49:05 2024

#=======================================================
lattice_vector 0.0000000000000000 2.8265750000000001 2.8265750000000001
lattice_vector 2.8265750000000001 0.0000000000000000 2.8265750000000001
lattice_vector 2.8265750000000001 2.8265750000000001 0.0000000000000000
atom_frac 0.0000000000000000 0.0000000000000000 -0.0000000000000000 Ga
atom_frac 0.2500000000000000 0.2500000000000000 0.2499999999999999 As
"""
