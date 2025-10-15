#!/usr/bin/env python
r""" """

from __future__ import annotations

from argparse import Namespace
from typing import TYPE_CHECKING

import numpy as np
from dayabay_model_official import model_dayabay
from matplotlib import pyplot as plt
from matplotlib import ticker
from yaml import safe_load as yaml_load

if TYPE_CHECKING:
    from collections.abc import Generator
    from typing import Any

    from numpy.typing import NDArray


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


def get_obs(
    storage_generator: Generator[tuple[str, Any], None, None], width: NDArray = np.array([1.0])
) -> dict[str, NDArray]:
    """Get observable scaled or not by width of bins.

    Parameters
    ----------
    storage_generator : Generator[tuple[str, Any], None, None]
        Storage that contains observables.
    width : NDArray
        Array of widths of bins.

    Returns
    -------
    None
    """
    result = {}
    for key, obs in storage_generator:
        result[key] = obs.data.copy() / width
    return result


def main(args: Namespace) -> None:
    with open(args.input, "r") as f:
        fit = yaml_load(f)

    if not fit["success"]:
        print("Fit is not succeed")
        exit()

    model = model_dayabay()
    storage = model.storage

    model.switch_data("asimov")

    data_obs = get_obs(storage[f"outputs.eventscount.final.{args.concatenation}"].walkjoineditems())
    model.set_parameters(fit["xdict"])
    fit_obs = get_obs(storage[f"outputs.eventscount.final.{args.concatenation}"].walkjoineditems())

    edges = storage["outputs.edges.energy_final"].data
    xerr = (edges[1:] - edges[:-1]) / 2
    centers = (edges[1:] + edges[:-1]) / 2
    borders_plot = [edges[0], *edges]
    for obs_name, data in data_obs.items():
        if args.concatenation == "detector_period":
            title = "{}, {} period".format(*obs_name.split("."))
        else:
            title = f"{obs_name}, all periods"
        fig, axs = plt.subplots(2, 1, height_ratios=[2, 1], sharex=True)
        axs[0].step(borders_plot, [0, *fit_obs[obs_name], 0], where="post", label="fit", color="C0")
        axs[0].errorbar(
            centers,
            data,
            yerr=data**0.5,
            xerr=xerr,
            marker="o",
            markersize=4,
            linestyle="none",
            label="data",
            color="black",
        )
        ratio = data / fit_obs[obs_name]
        yerr_ratio = 1 / fit_obs[obs_name] * (ratio * (data + fit_obs[obs_name])) ** 0.5
        axs[1].errorbar(
            centers, ratio - 1, xerr=xerr, marker="o", markersize=4, yerr=yerr_ratio, color="C0"
        )
        formatter = ticker.ScalarFormatter()
        formatter.set_powerlimits((0, 2))
        axs[0].yaxis.set_major_formatter(formatter)
        axs[0].set_title(title)
        axs[0].set_ylabel("Entries")
        axs[1].set_xlabel("E, MeV")
        axs[1].set_ylabel("data / fit - 1")
        plt.subplots_adjust(hspace=0.0, left=0.15, right=0.95, bottom=0.125, top=0.925)
        if args.output:
            plt.savefig(
                args.output.format(obs_name.replace(".", "-")),
                metadata={"creationDate": None},
            )

    if args.show:
        plt.show()


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()

    model = parser.add_argument_group("model", "model related options")
    model.add_argument(
        "--concatenation",
        choices=["detector", "detector_period"],
        default="detector_period",
        help="Choose concatenation mode for plotting observation",
    )
    input = parser.add_argument_group("input", "input options")
    input.add_argument(
        "--input",
        help="Path to file with fit data",
    )

    outputs = parser.add_argument_group("outputs", "set outputs")
    outputs.add_argument(
        "--output",
        help="Path to save full plot of fits, needs placeholder for observation name",
    )
    outputs.add_argument(
        "--show",
        action="store_true",
        help="Show plots",
    )

    args = parser.parse_args()

    main(args)
