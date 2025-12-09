#!/usr/bin/env python
from __future__ import annotations

import itertools
from argparse import Namespace
from pprint import pprint
from typing import TYPE_CHECKING, Any

import numpy as np
from dayabay_data_official import get_path_data
from dayabay_model import model_dayabay
from dgm_fit.iminuit_minimizer import IMinuitMinimizer

from fits import update_dict_parameters

if TYPE_CHECKING:
    from dag_modelling.parameters.gaussian_parameter import Parameter
    from numpy.typing import NDArray


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


def cartesian_product(
    grid_opts: list[tuple[str, float, float, int]],
) -> tuple[list[str], list[NDArray], NDArray]:
    """Create cartesian products of several axes.

    Parameters
    ----------
    grid_opts : list[tuple[str, float, float, int]]
        Tuple of parameter name, left and right bounds,
        and the number of points with equal distance between the bounds.

    Returns
    -------
    tuple[list[str], NDArray]
        List of parameter names, list of arrays for cartersian product, and cartesian products of arrays.
    """
    parameters = []
    grids = []
    for parameter, l_bound, r_bound, num in grid_opts:
        parameters.append(parameter)
        grids.append(np.linspace(float(l_bound), float(r_bound), int(num)))
    grid = np.array(list(itertools.product(*grids)))
    return parameters, grids, grid


def main(args: Namespace) -> None:
    model = model_dayabay(
        path_data=get_path_data(args.source_type) if args.source_type else None,
        concatenation_mode=args.concatenation_mode)

    storage = model.storage
    model.switch_data(args.data)

    parameters_free = storage["parameters.free"]
    parameters_constrained = storage["parameters.constrained"]
    statistic = storage["outputs.statistic"]

    stat_chi2 = statistic[f"{args.statistic}"]
    minimization_parameters: dict[str, Parameter] = {}
    update_dict_parameters(minimization_parameters, args.free_parameters, parameters_free)
    if "covmat" not in args.statistic:
        update_dict_parameters(
            minimization_parameters,
            args.constrained_parameters,
            parameters_constrained,
        )
    elif args.constrained_parameters:
        raise Exception(f"Statistic {args.statistic} can not be used with constrained parameters")

    model.next_sample(mc_parameters=False, mc_statistics=False)
    minimizer = IMinuitMinimizer(stat_chi2, parameters=minimization_parameters, nbins=model.nbins)
    global_fit = minimizer.fit()
    pprint(global_fit)
    bf_x_dict = global_fit["xdict"]
    model.set_parameters(bf_x_dict)

    parameters, grids, xy_grid = cartesian_product(args.scan_par)
    grid_parameters = []
    minimization_parameters_2d = minimization_parameters.copy()
    for parameter in parameters:
        minimization_parameters_2d.pop(parameter)
        grid_parameters.append(parameter)

    model.next_sample(mc_parameters=False, mc_statistics=False)
    minimizer_scan_2d = IMinuitMinimizer(stat_chi2, parameters=minimization_parameters_2d)
    chi2_map = np.zeros(xy_grid.shape[0])
    for idx, grid_values in enumerate(xy_grid):
        model.set_parameters(dict(zip(grid_parameters, grid_values)))
        fit = minimizer_scan_2d.fit()
        minimizer_scan_2d.push_initial_values()
        chi2_map[idx] = fit["fun"]

    chi2_map_1d: dict[str, NDArray | Any] = dict.fromkeys(grid_parameters)
    if args.scan_1d:
        for parameter, grid_1d in zip(grid_parameters, grids):
            model.set_parameters(bf_x_dict)
            model.next_sample(mc_parameters=False, mc_statistics=False)
            chi2_map_1d[parameter] = np.zeros_like(grid_1d)
            minimization_parameters_1d = minimization_parameters.copy()
            minimization_parameters_1d.pop(parameter)
            minimizer_scan_1d = IMinuitMinimizer(stat_chi2, parameters=minimization_parameters_1d)
            for idx, grid_value in enumerate(grid_1d):
                model.set_parameters({parameter: grid_value})
                fit = minimizer_scan_1d.fit()
                minimizer_scan_1d.push_initial_values()
                chi2_map_1d[parameter][idx] = fit["fun"]
    else:
        parameter_x, parameter_y = grid_parameters
        best_fit_x = global_fit["xdict"][parameter_x]
        best_fit_y = global_fit["xdict"][parameter_y]
        fun = global_fit["fun"]
        grid_x, chi2_map_1d[parameter_x] = get_profile_of_chi2(
            xy_grid[:, 0],
            xy_grid[:, 1],
            chi2_map,
            best_fit_x,
            fun,
        )

        grid_y, chi2_map_1d[parameter_y] = get_profile_of_chi2(
            xy_grid[:, 1],
            xy_grid[:, 0],
            chi2_map,
            best_fit_y,
            fun,
        )

    if args.output:
        parameter_x, parameter_y = grid_parameters
        np.savez(
            args.output,
            **{
                "chi2map2d": np.stack((*xy_grid.T, chi2_map), axis=1),
                "chi2map1d_x": np.stack((grids[0], chi2_map_1d[parameter_x]), axis=1),
                "chi2map1d_y": np.stack((grids[1], chi2_map_1d[parameter_y]), axis=1),
                "best_fit_values": np.array(
                    [
                        (
                            global_fit["xdict"][parameter_x],
                            global_fit["xdict"][parameter_y],
                            global_fit["fun"],
                        )
                    ],
                    dtype=np.dtype(
                        [(parameter_x, np.float64), (parameter_y, np.float64), ("fun", np.float64)]
                    ),
                ),
                "best_fit_errors": global_fit.get("errorsdict_profiled", global_fit["errorsdict"]),
            },
        )


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument(
        "--source-type",
        default=None,
        help="Source type of dataset loaded from dayabay-data-official",
    )
    parser.add_argument(
        "--concatenation-mode",
        default="detector_period",
        choices=["detector", "detector_period"],
        help="Choose type of concatenation for final observation: by detector or by detector and period",
    )
    parser.add_argument(
        "--par",
        nargs=2,
        action="append",
        default=[],
        help="set parameter value",
    )
    parser.add_argument(
        "--data",
        default="asimov",
        choices=["asimov", "real"],
        help="Choose data for fit: 0th and 1st output",
    )
    parser.add_argument(
        "--scan-par",
        nargs=4,
        action="append",
        default=[],
        help="linspace of parameter",
    )
    parser.add_argument(
        "--scan-1d",
        action="store_true",
        help="provide 1d profiling with minos algorithm",
    )
    parser.add_argument(
        "--statistic",
        default="full.pull.chi2cnp",
        choices=[
            "stat.chi2p_iterative",
            "stat.chi2n",
            "stat.chi2p",
            "stat.chi2cnp",
            "stat.chi2p_unbiased",
            "stat.chi2poisson",
            "full.covmat.chi2p_iterative",
            "full.covmat.chi2n",
            "full.covmat.chi2p",
            "full.covmat.chi2p_unbiased",
            "full.covmat.chi2cnp",
            "full.pull.chi2p_iterative",
            "full.pull.chi2p",
            "full.pull.chi2cnp",
            "full.pull.chi2p_unbiased",
            "full.pull.chi2poisson",
        ],
        help="Choose chi-squared function for minimizer",
    )
    parser.add_argument(
        "--n-iterations",
        default=0,
        help="number of iterations of fit procedure, usefull only for iterative chi-squared",
    )
    parser.add_argument(
        "--free-parameters",
        default=[],
        nargs="*",
        help="Add free parameters to minimization process",
    )
    parser.add_argument(
        "--constrained-parameters",
        default=[],
        nargs="*",
        help="Add constrained parameters to minimization process",
    )
    parser.add_argument(
        "--output",
        help="path to save contour data, supports npz",
    )

    args = parser.parse_args()

    main(args)
