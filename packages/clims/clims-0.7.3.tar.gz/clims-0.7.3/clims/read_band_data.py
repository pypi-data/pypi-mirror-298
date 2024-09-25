import numpy as np
from matplotlib.lines import Line2D


def read_and_plot_bands(
    ax_bands,
    controlin_bands,
    output_x_axis,
    PLOT_SOC,
    PLOT_GW,
    max_spin_channel,
    soc,
    no_soc,
    dos_plot,
    bandmlk,
    sr_spin_collinear,
    rlatvec,
    emin,
    emax,
):

    band_segments = []
    band_totlength = 0.0  # total length of all band segments

    for band in controlin_bands:
        start = np.asarray(band[:3], dtype=float)
        end = np.asarray(band[3:6], dtype=float)
        length = np.linalg.norm(np.dot(end, rlatvec) - np.dot(start, rlatvec))
        band_totlength += length
        npoint = int(band[6])
        startname, endname = "", ""
        if len(band) > 7:
            startname = band[7]
        if len(band) > 8:
            endname = band[8]
        band_segments += [(start, end, length, npoint, startname, endname)]

    band_no_soc_suffix = [False]
    max_spin_channels = [max_spin_channel]
    plot_labels = [None]
    if PLOT_SOC:
        if not soc and not no_soc and not dos_plot and not bandmlk:
            # Plotting both SOC and NO_SOC band data
            band_no_soc_suffix = [True, False]
            if sr_spin_collinear:
                max_spin_channels = [2, 1]
                plot_labels = [["SR spin up", "SR spin down"], ["SOC"]]
            else:
                max_spin_channels = [1, 1]
                plot_labels = [["SR"], ["SOC"]]
        elif no_soc:
            band_no_soc_suffix = [True]
            if sr_spin_collinear:
                max_spin_channels = [2]
                plot_labels = [["SR spin up", "SR spin down"]]
            else:
                max_spin_channels = [1]
    else:
        if sr_spin_collinear:
            plot_labels = [["SR spin up", "SR spin down"]]

    print("Plotting %i band segments..." % len(band_segments))

    if output_x_axis:
        ax_bands.axhline(0, color=(0.0, 0.0, 0.0), linestyle=":")

    handles, _ = ax_bands.get_legend_handles_labels()

    for msp, no_soc_suffix, plot_label in zip(
        max_spin_channels, band_no_soc_suffix, plot_labels
    ):
        band_data, labels, e_shift = read_bands(
            band_segments, band_totlength, msp, PLOT_GW, no_soc=no_soc_suffix
        )

        for spin in range(msp):
            if plot_label:
                line = Line2D(
                    [0], [0], label=plot_label[spin], color=band_data[1][spin]["color"]
                )
                handles.extend([line])

        for iband, segment in enumerate(band_data.values()):
            for sb in segment:  # iterating over spin
                ax_bands.plot(sb["xvals"], sb["band_energies"], color=sb["color"])

    tickx, tickl = [], []
    for xpos, l in labels:
        ax_bands.axvline(xpos, color="k", linestyle=":")
        tickx += [xpos]
        if l == "Gamma" or l == "G":
            l = "$\\Gamma$"
        tickl += [l]
        print("| %8.3f %s" % (xpos, repr(l)))

    ax_bands.set_xlim(labels[0][0], labels[-1][0])
    ax_bands.set_xticks(tickx)
    ax_bands.set_xticklabels(tickl)
    ax_bands.set_ylim(emin, emax)

    if plot_labels[0]:
        ax_bands.legend(handles=handles, loc="upper right")

    return band_data, e_shift


def read_bands(band_segments, band_totlength, max_spin_channel, gw, no_soc=False):
    band_data = {}

    prev_end = band_segments[0][0]
    distance = band_totlength / 30.0  # distance between line segments that do not coincide

    xpos = 0.0
    labels = [(0.0, band_segments[0][4])]

    prefix = ""
    if gw:
        prefix = "GW_"
    suffix = ".out"
    if no_soc:
        suffix += ".no_soc"
    if max_spin_channel == 1 and not no_soc:
        band_colors = ["black"]
    elif max_spin_channel == 1 and no_soc:
        band_colors = ["tomato"]
    else:
        band_colors = ["tomato", "darkgoldenrod"]

    for iband, (start, end, length, npoint, startname, endname) in enumerate(band_segments):
        band_data[iband + 1] = []
        if any(start != prev_end):
            xpos += distance
            labels += [(xpos, startname)]

        xvals = xpos + np.linspace(0, length, npoint)
        xpos = xvals[-1]

        labels += [(xpos, endname)]

        prev_end = end

        for spin in range(max_spin_channel):
            data = np.loadtxt(prefix + "band%i%03i%s" % (spin + 1, iband + 1, suffix))
            idx = data[:, 0].astype(int)
            kvec = data[:, 1:4]
            band_occupations = data[:, 4::2]
            band_energies = data[:, 5::2]
            assert (npoint) == len(idx)
            band_data[iband + 1] += [
                {
                    "xvals": xvals,
                    "band_energies": band_energies,
                    "color": band_colors[spin],
                    "band_occupations": band_occupations,
                }
            ]
    shift = shift_band_data(band_data, max_spin_channel)

    return band_data, labels, shift


def shift_band_data(band_data, max_spin_channel):

    vbm = -1000000000
    for n, segment in band_data.items():
        for spin in range(max_spin_channel):
            occs = segment[spin]["band_occupations"]
            for k in range(len(occs)):
                occ_diff = occs[k][1:] - occs[k][:-1]
                fermi_inds = np.nonzero(occ_diff != 0)[0]
                # print(fermi_inds)
                if len(fermi_inds) == 1:
                    tmp_vbm = segment[spin]["band_energies"][k][fermi_inds]
                    if vbm < tmp_vbm:
                        vbm = tmp_vbm
                else:
                    print("Your system is probably a metal. Not shifting bands.")
                    return 0

    # Shift all bands
    for n in band_data.keys():
        for spin in range(max_spin_channel):
            band_data[n][spin]["band_energies"] -= vbm[0]

    return -vbm[0]
