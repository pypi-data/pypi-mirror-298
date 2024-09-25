import numpy as np
from pathlib import Path
import re


files = [x for x in Path(".").iterdir() if not x.is_dir()]


def get_file_name(pattern, files):
    for file in files:
        filename = file.as_posix()
        if pattern.match(filename):
            print(file)
            return file
    raise FileNotFoundError


def get_mu(filename):
    f = open(filename)
    for _ in range(3):
        line = f.readline()
        if "chemical potential" in line:
            return float(line.split()[-2])
    raise


def read_species_dos(species, max_spin_channel, no_soc=False):
    dos_species = {}
    maxdos = 0.0
    energy_lim = [100000, -100000]

    spinstrs = [""]
    if max_spin_channel == 2:
        spinstrs = ["_spin_up", r"_spin_d(ow)?n"]
    suffix = ".dat"
    if no_soc:
        suffix += ".no_soc"
    print("\nReading species projected DOS from files:")
    for s in species:
        dos_species[s] = []
        for ss in spinstrs:
            pattern = re.compile(s + r"_l_proj_dos(\_tetrahedron)?" + ss + suffix + "$")
            filename = get_file_name(pattern, files)
            mu = get_mu(filename)
            data = np.loadtxt(filename)
            maxdos = max(maxdos, data[:, 1].max())
            dos_species[s].append(data)
            energy_lim = [
                min(data[:, 0][0], energy_lim[0]),
                max(data[:, 0][-1], energy_lim[1]),
            ]
    dos_species["maxdos"] = maxdos
    dos_species["energy_lim"] = energy_lim

    return dos_species


def get_dos_groups(groups, dos_species, max_spin_channel):
    dos_groups = {}
    for g in groups:
        species_in_g = g.split()
        max_l = 0
        for sg in species_in_g:
            max_l = max(max_l, dos_species[sg][0].shape[1])
        max_l -= 1  # First column is x axis. We store separately.
        dos_groups[g] = [
            np.zeros((dos_species[sg][0].shape[0], max_l))
            for i_spin in range(max_spin_channel)
        ]
        dos_groups["x"] = dos_species[sg][0][:, 0]
        for sg in species_in_g:
            tmp_max_l = dos_species[sg][0].shape[1] - 1
            for i_spin in range(max_spin_channel):
                dos_groups[g][i_spin][:, :tmp_max_l] += dos_species[sg][i_spin][:, 1:]
    return dos_groups


def read_total_dos(no_soc=False):
    suffix = ".dat"
    if no_soc:
        suffix += ".no_soc"
    print("\nReading total DOS from files:")
    pattern = re.compile("KS_DOS_total(\_tetrahedron)?" + suffix + "$")
    filename = get_file_name(pattern, files)
    mu = get_mu(filename)
    data = np.loadtxt(filename)
    energy = data[:, 0]
    dos = data[:, 1:]
    maxdos = dos.max()
    energy_lim = [energy[0], energy[-1]]
    return energy, dos, maxdos, energy_lim
