citations = {
    "aims": """\
Volker Blum, Ralf Gehrke, Felix Hanke, Paula Havu, Ville Havu,
Xinguo Ren, Karsten Reuter, and Matthias Scheffler
Ab initio molecular simulations with numeric atom-centered orbitals
Computer Physics Communications 180, 2175-2196 (2009)
http://doi.org/10.1016/j.cpc.2009.06.022
""",
    "ase": """\
Larsen, Ask Hjorth, et al.
The Atomic Simulation Environment—A Python library for working with atoms
J. Phys.: Condens. Matter 29, 273002 (2017)
https://doi.org/10.1088/1361-648X/aa680e
""",
    "elastic": """\
Jochym, Pawel T.
Module for calculating elastic tensor of crystals
software, https://github.com/jochym/Elastic
https://doi.org/10.5281/zenodo.593721
""",
    "mace-mp-0": """\
Batatia, Ilyes, et al. 
A foundation model for atomistic materials chemistry 
arXiv preprint arXiv:2401.00096 (2023)
https://doi.org/10.48550/arXiv.2401.00096
""",
    "phonopy": """\
Togo, Atsushi and Chaput, Laurent and Tadano, Terumasa and Tanaka, Isao
Implementation strategies in phonopy and phono3py
J. Phys. Condens. Matter 35, 353001-1-22 (2023)
https://dx.doi.org/10.1088/1361-648X/acd831
""",
    "spglib": """\
Togo, Atsushi  and Tanaka, Isao 
Spglib: a software library for crystal symmetry search
arXiv preprint arXiv:1808.01590 (2018)
https://arxiv.org/abs/1808.01590
""",
}


def cite_and_print(refs):
    print("\nPlease consider to cite the following publications:\n")
    for ref in refs:
        lines = citations[ref].splitlines()
        cite_text = f"{f'[{ref}]':11} " + lines[0] + "\n"
        for l in lines[1:]:
            cite_text += " " * (12) + l + "\n"
        print(cite_text)
