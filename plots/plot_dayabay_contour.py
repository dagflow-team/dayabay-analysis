#!/usr/bin/env python

import os
from argparse import Namespace

import numpy as np
from matplotlib import pyplot as plt
from numpy.typing import NDArray
from scipy.interpolate import interp1d
from scipy.optimize import bisect
from scipy.stats import chi2, norm

sin_sq_2theta12 = 0.851
cos_sq_2theta12 = 1 - sin_sq_2theta12
cos_2theta12 = cos_sq_2theta12**0.5
sin_sq_theta12 = (1.0 - cos_2theta12) / 2.0
cos_sq_theta12 = 1.0 - sin_sq_theta12
delta_m_sq21 = 7.53e-05


def convert_to_dm_ee(dm32: NDArray | float):
    r"""Convert $`\Delta m^2_{32}`$ to $`\Delta m^2_{ee}`$.

    $`\Delta m^2_{ee} = \cos^2\theta_{12} \Delta m^2_{31} + \sin^2\theta_{12} \Delta m^2_{32}`$.

    Parameters
    ----------
    dm32 : NDArray | float
        Array or value of dm32
    """

    return cos_sq_theta12 * (delta_m_sq21 + dm32) + sin_sq_theta12 * dm32


def calculate_errors(x: NDArray, y: NDArray, bf: float) -> tuple[float, float]:
    """Calculate errors for best fit point based on 1d profile

    Parameters
    ----------
    x : NDArray
        X-axis of profile
    y : NDArray
        Y-axis of profile
    bf : float
        Best fit value of chosen parameter

    Returns
    -------
    tuple[float, float]
        Values of left and right errors
    """

    interp = interp1d(x, y - 1, kind="quadratic")
    return (bf - bisect(interp, x.min(), x.mean()), bisect(interp, x.mean(), x.max()) - bf)


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
    ax.plot(profile[0], profile[1], color="black", alpha=0.25)
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

    if not args.dm32:
        xy_grid[:, 1] = convert_to_dm_ee(xy_grid[:, 1])
        best_fit_y = convert_to_dm_ee(best_fit_y)

    fig, axes = plt.subplots(2, 2, gridspec_kw={"width_ratios": [3, 1], "height_ratios": [1, 3]})

    sin_sq2theta13, chi2_profile = data["chi2map1d_x"].T
    best_fit_x_errors = calculate_errors(sin_sq2theta13, chi2_profile, best_fit_x)
    label = r"$\Delta\chi^2$"
    prepare_axes(
        axes[0, 0],
        limits=[(xy_grid[:, 0].min(), xy_grid[:, 0].max()), (0, 20)],
        ylabel=label,
        profile=(sin_sq2theta13, chi2_profile),
    )

    dm, chi2_profile = data["chi2map1d_y"].T
    if not args.dm32:
        dm = convert_to_dm_ee(dm)
    best_fit_y_errors = calculate_errors(dm, chi2_profile, best_fit_y)
    prepare_axes(
        axes[1, 1],
        limits=[(0, 20), (xy_grid[:, 1].min(), xy_grid[:, 1].max())],
        xlabel=label,
        profile=(chi2_profile, dm),
    )

    ndof = 2
    levels = convert_sigmas_to_chi2(ndof, [0, 1, 2, 3])
    axes[1, 0].grid(linestyle="--")
    axes[1, 0].tricontourf(xy_grid[:, 0], xy_grid[:, 1], chi2_map - fun, levels=levels, cmap="GnBu")
    axes[1, 0].errorbar(
        best_fit_x,
        best_fit_y,
        xerr=best_fit_x_errors,
        yerr=best_fit_y_errors,
        color="black",
        marker="o",
        markersize=3,
        capsize=3,
    )

    axes[1, 0].set_ylabel(r"$\Delta m^2_{ee}$, [eV$^2$]")
    if args.dm32:
        axes[1, 0].set_ylabel(r"$\Delta m^2_{32}$, [eV$^2$]")
    axes[1, 0].set_xlabel(r"$\sin^22\theta_{13}$")
    axes[1, 0].minorticks_on()
    fig.delaxes(axes[0, 1])
    plt.tight_layout()
    plt.subplots_adjust(wspace=0, hspace=0)
    if args.output:
        plt.savefig(args.output)

    try:
        if args.show:
            plt.show()
    except UserWarning:
        print("it is not possible to show plot, it will be saved in tmp/tmp.pdf")
        os.makedirs("tmp/", exist_ok=True)
        plt.savefig(f"tmp/tmp.pdf", metadata={"creationDate": None})


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("--chi2map")

    parser.add_argument(
        "--output",
        help="path to save plot",
    )
    parser.add_argument(
        "--dm32",
        action="store_true",
        help=r"Switch plot y-axis from $\Delta m^2_{32}$ to $\Delta m^2_{ee}$",
    )
    parser.add_argument(
        "--show",
        action="store_true",
        help="show plot",
    )

    args = parser.parse_args()

    main(args)
