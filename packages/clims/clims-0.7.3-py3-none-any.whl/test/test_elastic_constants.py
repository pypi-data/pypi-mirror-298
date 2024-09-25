from pathlib import Path
from click.testing import CliRunner
from ase.io import read
from ase.build import bulk
from test.file_comparison import compare_geo_files
from clims.cli.elastic_constants import clims_elastic


parent = Path(__file__).parent

elastic_constants_output = """Cij solution
------------------------------
 Solution rank:  3
 Square of residuals: 4.5e-05
 Relative singular values:
 1.0000   0.7071   0.6354  

Elastic tensor (GPa):
   C_11     C_12     C_44  
------------------------------
 277.49    85.71   143.26  

Please consider to cite the following publications:

[ase]       Larsen, Ask Hjorth, et al.
            The Atomic Simulation Environment—A Python library for working with atoms
            J. Phys.: Condens. Matter 29, 273002 (2017)
            https://doi.org/10.1088/1361-648X/aa680e

[elastic]   Jochym, Pawel T.
            Module for calculating elastic tensor of crystals
            software, https://github.com/jochym/Elastic
            https://doi.org/10.5281/zenodo.593721
"""


def test_elastic_constants():
    runner = CliRunner()
    with runner.isolated_filesystem():
        print(f"{parent / 'elastic'}")
        c = read(parent / "elastic" / "geometry.in")
        c.write("geometry.in")
        result = runner.invoke(clims_elastic, "initialize")
        assert result.exit_code == 0
        dirlist = sorted([d for d in Path(".").iterdir() if d.is_dir()])
        rlist = sorted([d for d in (parent / "elastic").iterdir() if d.is_dir()])
        print(dirlist)
        assert len(rlist) == len(dirlist)
        for d, r in zip(dirlist, rlist):
            compare_geo_files(d / "geometry.in", r / "geometry.in")
        result = runner.invoke(
            clims_elastic, ["postprocess", "--pwd", f"{parent / 'elastic'}"]
        )
        assert result.exit_code == 0
        assert "\n".join(result.output.splitlines()[-24:]) == elastic_constants_output
