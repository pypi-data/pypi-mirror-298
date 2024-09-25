import numpy as np
from clims.elements import colors as element_colors
import re
from ase.symbols import symbols2numbers
from ase.data import atomic_numbers
import sys
from matplotlib.colors import is_color_like


def read_and_plot_mulliken_bands(
    band_data,
    ax_bands,
    n_atoms,
    l_index,
    PLOT_SOC,
    masks,
    groups,
    group_colors,
    scale_mulliken_marker,
    no_legend,
    fontsize,
    legend_offset,
):
    for iband, segment in enumerate(band_data.values()):
        for spin, sb in enumerate(segment):
            filename = "bandmlk%i%03i.out" % (spin + 1, iband + 1)
            scatters = read_mulliken_bands(
                filename,
                ax_bands,
                n_atoms,
                l_index,
                PLOT_SOC,
                sb,
                masks,
                groups,
                group_colors,
                scale_mulliken_marker,
            )

    if not no_legend:
        lg = ax_bands.legend(
            scatters,
            groups,
            scatterpoints=1,
            fontsize=fontsize,
            loc="lower right",
            bbox_to_anchor=legend_offset,
        )
        for lh in lg.legend_handles:
            lh.set_alpha(1)
            lh.set_sizes([100])


def read_mulliken_bands(
    filename,
    ax_bands,
    n_atoms,
    l_index,
    is_SOC,
    segments,
    masks,
    groups,
    group_colors,
    scale_marker,
):

    markersizeunit = 24
    factor_atoms = 1
    total_atom_ind = 4 + l_index

    if is_SOC:
        factor_atoms = 2
        total_atom_ind += 1

    with open(filename) as f:
        output = f.read()
    print("Parsing " + filename)
    k_points = output.split("k point number:")[1:]
    # print("Number of k_points", len(k_points))
    len_k = len(k_points)

    # Find out actual number of states:
    start_state = int(re.search(r"\n *State *([0-9]*)\n", k_points[0]).group(1)) - 1
    states = re.split(r"\n *State *[0-9]*\n", k_points[0])[1:]
    n_states = len(states)
    mulliken_k = np.zeros((len(groups), n_states * len_k))
    x_vals = np.zeros(n_states * len_k)
    y_vals = np.zeros(n_states * len_k)
    raise_index_warning = False
    for i_k, k in enumerate(k_points):
        start_state = int(re.search(r"\n *State *([0-9]*)\n", k).group(1)) - 1
        states = re.split(r"\n *State *[0-9]*\n", k)[1:]
        end_state = start_state + n_states
        mulliken = np.zeros((n_states, factor_atoms * n_atoms))
        for i_state, state in enumerate(states):
            lines = state.splitlines()
            for i, line in enumerate(lines):
                try:
                    mulliken[i_state, i] = float(line.split()[total_atom_ind])
                except IndexError:
                    mulliken[i_state, i] = 0.0
                    raise_index_warning = True

        for i_s, s in enumerate(groups):
            spec_mlk = mulliken[:, masks[s]].sum(axis=1)
            mulliken_k[i_s, i_k * n_states : (i_k + 1) * n_states] = spec_mlk
            x_vals[i_k * n_states : (i_k + 1) * n_states] = [segments["xvals"][i_k]] * n_states
            y_vals[i_k * n_states : (i_k + 1) * n_states] = segments["band_energies"][i_k][
                start_state:end_state
            ]
    if raise_index_warning:
        print("WARNING: The requested l-projection was not available for at least one atom!")
    scatters = ()

    for i_s, color in enumerate(group_colors):
        sc = ax_bands.scatter(
            x_vals,
            y_vals,
            s=(markersizeunit * np.abs(mulliken_k[i_s])) * scale_marker,
            c=color,
            alpha=1,
            edgecolors="none",
        )
        scatters += (sc,)

    return scatters


def get_groups_for_projections(is_SOC, species, atoms, structure, colors):
    masks = {}
    group_colors = []
    groups = []

    if species is not None:
        for s in species:
            groups += [" ".join(s)]
            for x in s:
                if not x in structure.get_chemical_symbols():
                    print(f"Error: Species '{x}' is not in the structure. Stopping.")
                    sys.exit()
            group_colors += [element_colors[symbols2numbers(s[0])[0] - 1]]
            if is_SOC:
                # There are double the number of states for SOC.
                masks[groups[-1]] = [
                    np.any(np.array(s) == x)
                    for x in structure.get_chemical_symbols()
                    for _ in (0, 1)
                ]
            else:
                masks[groups[-1]] = [
                    np.any(np.array(s) == x) for x in structure.get_chemical_symbols()
                ]
    elif atoms is not None:
        for a in atoms:
            groups += ["Atom No: " + ", ".join([str(x) for x in a])]
            group_colors += [
                element_colors[
                    symbols2numbers(structure.get_chemical_symbols()[a[0] - 1])[0] - 1
                ]
            ]
            if is_SOC:
                masks[groups[-1]] = [
                    (i + 1) in a for i in range(len(structure)) for _ in (0, 1)
                ]
            else:
                masks[groups[-1]] = [(i + 1) in a for i in range(len(structure))]

    if colors:
        colors = [c.strip() for c in colors.split(",")]
        for c in colors:
            if not is_color_like(c):
                print(
                    f"Error: The color '{c}' is not recognized as color by matplotlib. Stopping."
                )
                sys.exit()
        if len(colors) == len(group_colors):
            group_colors = colors
        else:
            print("Error: Number of colors does not equal the number of groups. Stopping.")
            sys.exit()

    return groups, group_colors, masks
