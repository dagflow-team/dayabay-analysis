#!/usr/bin/env python
# TODO: update doc
r"""Script for fit model to observed/model data.

Examples
--------
Example of call

.. code-block:: shell

    ./scripts/plot_fit_article.py --version v0e --data model \
      --mo "{dataset: a}" \
      --input-fit fit.yaml \
      --output "fit-{}.pdf" \
      --output-show
"""
from argparse import Namespace

import numpy as np
from dag_modelling.tools.logger import set_verbosity
from dayabay_model import model_dayabay
from matplotlib import pyplot as plt
from matplotlib.axes import Axes
from numpy.typing import NDArray
from yaml import safe_load as yaml_load

from plots import get_obs, FFormatter, calculate_ratio_error

DATA_INDICES = {"model": 0, "loaded": 1}
AD_TO_EH = {
    "AD11": "EH1",
    "AD12": "EH1",
    "AD21": "EH2",
    "AD22": "EH2",
    "AD31": "EH3",
    "AD32": "EH3",
    "AD33": "EH3",
    "AD34": "EH3",
}


plt.rcParams.update(
    {
        "xtick.top": True,
        "xtick.minor.top": True,
        "xtick.minor.visible": True,
        "axes.grid": True,
        "ytick.left": True,
        "ytick.minor.left": True,
        "ytick.right": True,
        "ytick.minor.right": True,
        "ytick.minor.visible": True,
    }
)

BKG_LABELS = {
    "fast_neutrons": r"Fast n",
    "fast_neutrons+muonx": r"Fast n + $\mu$ decay",
    "alpha_neutron": r"$^{13}$C($\alpha$,n)$^{16}$O",
    "amc": r"$^{241}$Am-$^{13}$C",
    "lithium_helium": r"$^{9}$Li/$^{8}$He",
    "accidentals": r"Accidental",
}

bkg_label_filter = lambda bkg_type, bkg_types: (
    BKG_LABELS[bkg_type + "+muonx"]
    if bkg_type == "fast_neutrons" and "muonx" in bkg_types
    else BKG_LABELS[bkg_type]
)


def sum_by_eh(dict_obs: dict[str, NDArray]) -> dict:
    """Summarize observations by experimental hall.

    Parameters
    ----------
    dict_obs : dict[str, NDArray]
        Dictionary with (AD, observation) items.

    Returns
    -------
    dict
        Dictionary with (EH, observation) items.
    """
    result = dict(zip(["EH1", "EH2", "EH3"], [0, 0, 0]))
    for detector, obs in dict_obs.items():
        result[AD_TO_EH[detector]] += obs
    return result


def plot(
    ax: Axes,
    hall: str,
    edges: NDArray,
    no_osc_obs: dict[str, NDArray],
    data_obs: dict[str, NDArray],
    fit_obs: dict[str, NDArray],
    bkg_obs: dict[str, dict[str, NDArray]],
    markersize: int = 3,
):
    """Plot observations, backgrounds, fits, etc.

    Parameters
    ----------
    ax : Axes
        Axes where to plot.
    hall : str
        Experimental hall.
    edges : NDArray
        Edges of bins.
    no_osc_obs : dict[str, NDArray]
        Dictionary with (EH, model observation without oscillation effects) items.
    data_obs : dict[str, NDArray]
        Dictionary with (EH, real observation) items.
    fit_obs : dict[str, NDArray]
        Dictionary with (EH, fitted model observation) items.
    bkg_obs : dict[str, dict[str, NDArray]]
        Dictionary with (EH, fitted model background) items.
    markersize : int
        Marker size for data points.
    """
    centers = (edges[1:] + edges[:-1]) / 2
    ax.step([edges[0], *edges], [0, *no_osc_obs[hall], 0], where="post", label="No oscillation")
    ax.step([edges[0], *edges], [0, *data_obs[hall], 0], where="post", label="Best fit")
    ax.errorbar(
        centers,
        data_obs[hall],
        yerr=fit_obs[hall] ** 0.5,
        linestyle="none",
        label="Data",
        marker="o",
        markersize=markersize,
        color="black",
    )
    bkg = 0
    for bkg_source in bkg_obs.values():
        bkg += bkg_source[hall]
    for color, bkg_type in zip(["C4", "C8", "C7", "C6", "C2"], ["accidentals", "lithium_helium", "fast_neutrons", "amc", "alpha_neutron"]):
        ax.stairs(bkg, edges, color=color)
        ax.fill_between(
            [edges[0], *edges],
            [0, *bkg, 0],
            step="post",
            color=color,
            label=bkg_label_filter(bkg_type, bkg_obs.keys()),
        )
        bkg -= bkg_obs[bkg_type][hall]
        if bkg_type == "fastn" and "muonx" in bkg_obs.keys():
            bkg -= bkg_obs["muonx"][hall]


def main(args: Namespace) -> None:
    if args.verbose:
        set_verbosity(args.verbose)

    with open(args.input, "r") as f:
        fit = yaml_load(f)

    if not fit["success"]:
        print("Fit is not succeed")
        exit()

    model = model_dayabay(
        path_data=args.path_data,
    )

    storage = model.storage
    outputs = storage["outputs"]
    eventscount = outputs["eventscount.final"]

    edges = outputs["edges.energy_final"].data
    centers = (edges[:-1] + edges[1:]) / 2
    widths = edges[1:] - edges[:-1]
    xerrs = widths / 2

    data_obs = get_obs(outputs["data.real.final.detector"].walkjoineditems(), widths)
    model.set_parameters(fit["xdict"])
    fit_obs = get_obs(eventscount["detector"].walkjoineditems(), widths)
    model.set_parameters({"survival_probability.SinSq2Theta12": 0, "survival_probability.SinSq2Theta13": 0})
    no_osc_obs = get_obs(eventscount["detector"].walkjoineditems(), widths)
    data_obs = sum_by_eh(data_obs)
    fit_obs = sum_by_eh(fit_obs)
    no_osc_obs = sum_by_eh(no_osc_obs)

    bkg_obs = dict.fromkeys(eventscount["background_by_source"].keys())
    for bkg_source in bkg_obs.keys():
        bkg_obs[bkg_source] = sum_by_eh(
            get_obs(eventscount[f"background_by_source.{bkg_source}"].walkjoineditems(), widths)
        )

    for hall in ["EH1", "EH2", "EH3"]:
        fig, axs = plt.subplots(2, 1, figsize=[5.5, 6.0], height_ratios=[3, 1], sharex=True)
        plot(axs[0], hall, edges, no_osc_obs, data_obs, fit_obs, bkg_obs)
        axs[1].hlines(1, 0, 12, linestyle=":")
        subax = fig.add_axes([0.53, 0.685, 0.40, 0.25], facecolor="white")
        plot(subax, hall, edges, no_osc_obs, data_obs, fit_obs, bkg_obs, markersize=1)
        subax.set_yscale("log")
        subax.set_xlim(0.7, 12.0)
        # subax.set_ylim(bkg_obs["fast_neutrons"][hall].max() * 0.9, no_osc_obs[hall].max() * 1.2)
        subax.set_ylim(10, 1e+6)
        subax.set_xticks([2, 4, 6, 8, 10, 12], [2, 4, 6, 8, 10, 12])
        subax.tick_params(axis="x", which="both", top=False, bottom=True)
        subax.tick_params(axis="y", which="both", right=False, left=True)
        for label in subax.get_xticklabels() + subax.get_yticklabels():
            label.set_bbox(
                dict(
                    facecolor="white",
                    edgecolor="None",
                    alpha=0.85,
                    pad=0,
                    boxstyle="round,rounding_size=0.5",
                )
            )
        plt.setp(axs[0].get_xticklabels(), visible=False)

        ratio = np.array([0, *(fit_obs[hall] / no_osc_obs[hall])])
        axs[1].step(
            edges,
            ratio,
            color="C1",
            where="pre",
        )
        axs[1].errorbar(
            centers,
            data_obs[hall] / no_osc_obs[hall],
            xerr=xerrs,
            yerr=calculate_ratio_error(data_obs[hall], no_osc_obs[hall]),
            color="black",
            linestyle="none",
        )

        formatter = FFormatter()
        formatter.set_powerlimits((0, 3))
        axs[0].yaxis.set_major_formatter(formatter)
        axs[1].set_ylim(0.90, 1.065)
        axs[0].set_title(hall)
        axs[1].hlines(1, 0, 12, linestyle=":")
        axs[0].set_xlim(0.7, 12.0)
        axs[0].set_ylim(0.0, no_osc_obs[hall].max() * 1.26)

        axs[0].set_ylabel("Entries [MeV$^{-1}$]")
        axs[1].set_xlabel("Reconstructed prompt energy [MeV]")
        axs[1].set_ylabel(r"$N^{\mathrm{obs}} / N^{\mathrm{pred}}_{\mathrm{no-osc.}}$")
        leg = axs[0].legend(loc="lower right")
        leg.get_frame().set_linewidth(0.0)
        leg.get_frame().set_alpha(1.0)

        plt.subplots_adjust(hspace=0.0, left=0.125, right=0.95, bottom=0.1, top=0.95)
        if args.output:
            plt.savefig(args.output.format(hall), metadata={"creationDate": None})

    if args.show:
        plt.show()


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("-v", "--verbose", default=1, action="count", help="verbosity level")

    model = parser.add_argument_group("model", "model related options")
    model.add_argument(
        "--path-data",
        default=None,
        help="Path to data",
    )

    comparison = parser.add_argument_group("comparison", "Comparison options")
    comparison.add_argument(
        "--input",
        help="path to file which load as expected",
    )

    outputs = parser.add_argument_group("outputs", "set outputs")
    outputs.add_argument(
        "--show",
        action="store_true",
    )
    outputs.add_argument(
        "--output",
    )

    args = parser.parse_args()

    main(args)
