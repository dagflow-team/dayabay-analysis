#!/usr/bin/env python
r""" """

from __future__ import annotations

from argparse import Namespace

from dayabay_model import model_dayabay
from matplotlib import pyplot as plt
from matplotlib import ticker
from yaml import safe_load as yaml_load

from plots import get_observation


def main(args: Namespace) -> None:
    with open(args.input, "r") as f:
        fit = yaml_load(f)

    if not fit["success"]:
        print("Fit is not succeed")
        exit()

    model = model_dayabay()
    outputs = model.storage["outputs"]

    # Switch between `asimov` and `real` data
    model.switch_data(args.data)
    if args.data == "asimov":
        observation = f"eventscount.final.{args.concatenation}"
    else:
        observation = f"data.real.final.{args.concatenation}"

    data_obs = get_observation(outputs[observation].walkjoineditems())
    model.set_parameters(fit["xdict"])
    fit_obs = get_observation(outputs[observation].walkjoineditems())

    edges = outputs["edges.energy_final"].data
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
    model.add_argument(
        "--data",
        choices=["asimov", "real"],
        default="asimov",
        help="Choose type of data which will be plotted: asimov or real",
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
