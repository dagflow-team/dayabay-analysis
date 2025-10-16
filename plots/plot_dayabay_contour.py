#!/usr/bin/env python

from argparse import Namespace

import numpy as np
from matplotlib import pyplot as plt
from numpy.typing import NDArray
from scipy.stats import chi2, norm


def convert_sigmas_to_chi2(df: int, sigmas: list[float] | NDArray) -> NDArray:
    """Convert deviation of normal unit distribution N(0, 1) to critical value
    of chi-squared.

    Parameters
    ----------
    df : int
        Degree of freedom of chi-squared distribution.
    sigmas : list[float] | NDArray
        List or array deviations from 0 in terms of standard deviation of normal unit distribution N(0, 1).

    Returns
    -------
    NDArray
        Array of critical values of chi-squared.
    """
    percentiles = 2 * norm(0, 1).cdf(sigmas) - 1
    return chi2(df).ppf(percentiles)


def get_profile_of_chi2(
    parameter_grid: NDArray,
    profile_grid: NDArray,
    chi2_map: NDArray,
    best_fit_value: float,
    best_fit_fun: float,
) -> tuple[NDArray, NDArray]:
    """Make a profile of the chi-squared map using thee minimum value. Works
    with 2-dimensional maps.

    Parameters
    ----------
    parameter_grid : NDArray
        Array of grid to look for best fit value of parameter.
    profile_grid : NDArray
        Array of grid to create profile grid.
    chi2_map : NDArray
        Map of chi-squared values.
    best_fit_value : float
        Value of parameter in best fit point.
    best_fit_fun : float
        Value of the chi-squared in best fit point.

    Returns
    -------
    tuple[NDArray, NDArray]
        Array of profile grid values and array of chi-squared values.
    """
    abs_difference = np.abs(parameter_grid - best_fit_value)
    closest_value = abs_difference.min()
    mask = abs_difference == closest_value
    chi2_profile = chi2_map[mask] - best_fit_fun
    return profile_grid[mask], chi2_profile


def prepare_axes(
    ax: plt.Axes,
    limits: list[tuple[float, float]],
    profile: tuple[NDArray, NDArray],
    xlabel: str = "",
    ylabel: str = "",
    ticks: list[float] = [5, 10, 15, 20],
    levels: list[float] = [1, 4, 9, 16],
):
    """Update axis labels, limits, ticks, and plot levels.

    Parameters
    ----------
    ax : plt.Axes
        Element of (sub-)plot.
    limits : list[tuple[float, float], tuple[float, float]]
        Tuples of xlimits and ylimits.
    profile : tuple[NDArray, NDArray]
        Array of x values and y values (profile grid and chi-squared values or reversed).
    xlabel : str, optional
        Label of x axis.
    ylabel : str, optional
        Label of y axis.
    ticks : list[float], optional
        Ticks of chi-squared axis.
    levels : list[float], optional
        Levels of constant chi-squared.
    """
    xlim, ylim = limits
    if xlabel:
        ax.set_xticks(ticks, ticks)
        ax.set_yticks([], [])
        ax.set_xlabel(xlabel)
        ax.vlines(levels, *ylim, linestyle="--", alpha=0.25, colors="black")
    elif ylabel:
        ax.set_xticks([], [])
        ax.set_yticks(ticks, ticks)
        ax.set_ylabel(ylabel)
        ax.hlines(levels, *xlim, linestyle="--", alpha=0.25, colors="black")
    ax.plot(profile[0], profile[1], color="black")
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.minorticks_on()


def main(args: Namespace) -> None:
    data = np.load(args.chi2map)
    xy_grid = data["chi2map2d"][:, :2]
    chi2_map = data["chi2map2d"][:, 2]
    best_fit_values = data["best_fit_values"]
    best_fit_x = best_fit_values["survival_probability.SinSq2Theta13"]
    best_fit_y = best_fit_values["survival_probability.DeltaMSq32"]
    fun = best_fit_values["fun"]
    

    fig, axes = plt.subplots(2, 2, gridspec_kw={"width_ratios": [3, 1], "height_ratios": [1, 3]})
    sinSqD13_profile, chi2_profile = get_profile_of_chi2(
        xy_grid[:, 1], xy_grid[:, 0], chi2_map, best_fit_y, fun
    )

    # TODO: profile 1d
    label = r"$\Delta\chi^2$"
    prepare_axes(
        axes[0, 0],
        limits=[(xy_grid[:, 0].min(), xy_grid[:, 0].max()), (0, 20)],
        ylabel=label,
        profile=(sinSqD13_profile, chi2_profile),
    )

    dm32_profile, chi2_profile = get_profile_of_chi2(
        xy_grid[:, 0],
        xy_grid[:, 1],
        chi2_map,
        best_fit_x,
        fun,
    )
    prepare_axes(
        axes[1, 1],
        limits=[(0, 20), (xy_grid[:, 1].min(), xy_grid[:, 1].max())],
        xlabel=label,
        profile=(chi2_profile, dm32_profile),
    )

    ndof = 2  # len(parameters)
    levels = convert_sigmas_to_chi2(ndof, [0, 1, 2, 3])
    axes[1, 0].grid(linestyle="--")
    axes[1, 0].tricontourf(xy_grid[:, 0], xy_grid[:, 1], chi2_map - fun, levels=levels, cmap="GnBu")
    # axes[1, 0].errorbar(
    #     best_fit_x,
    #     best_fit_y,
    #     xerr=best_fit_x_error,
    #     yerr=best_fit_y_error,
    #     color="black",
    #     marker="o",
    #     markersize=3,
    #     capsize=3,
    # )

    axes[1, 0].set_ylabel(r"$\Delta m^2_{32}$, [eV$^2$]")
    axes[1, 0].set_xlabel(r"$\sin^22\theta_{13}$")
    axes[1, 0].minorticks_on()
    fig.delaxes(axes[0, 1])
    plt.tight_layout()
    plt.subplots_adjust(wspace=0, hspace=0)
    if args.output:
        plt.savefig(args.output)
    plt.show()


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("--chi2map")

    parser.add_argument(
        "--output",
        help="path to save plot",
    )

    args = parser.parse_args()

    main(args)
