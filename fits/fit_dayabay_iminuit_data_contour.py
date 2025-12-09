#!/usr/bin/env python
r"""
Simple script for fit Daya Bay model to observed data with Minuit from iminuit package.

Examples
--------
Example of call

.. code-block:: shell

    ./fits/fit_dayabay_iminuit_data.py \
        --statistic full.pull.chi2cnp \
        --use-hubber-mueller-spectral-uncertainties
"""
from __future__ import annotations

from argparse import ArgumentParser
from pprint import pprint

import iminuit
import numpy as np
from dag_modelling.tools.make_fcn import make_fcn
from dayabay_data_official import get_path_data
from dayabay_model import model_dayabay

from fits import convert_minuit_to_dict


def main(args) -> None:
    # Load Daya Bay model
    model = model_dayabay(
        path_data=get_path_data(args.source_type),
        concatenation_mode=args.concatenation_mode
    )
    storage = model.storage

    # Switch output for data from observed data to Asimov data
    model.switch_data("real")

    # Create dictionary of free parameters: [parameter name, parameter]
    free_parameters = {
        par.name: par
        for par in filter(
            lambda x: "global_normalization" not in x.name,
            storage["parameters.free"].walkvalues(),
        )
    }
    # Create dictionary of constrained parameters: [parameter name, parameter]
    # If user put --use-hubber-mueller-spectral-uncertainties flag, it will add
    # parameters of uncertainties for each isotope (more than 1000 parameters)
    # Usually, these parameters are used for fit with observed data
    if args.use_hubber_mueller_spectral_uncertainties:
        constrained_parameters = {
            par.name: par for par in filter(
                lambda x: "nominal_thermal_power" not in x.name,
                storage["parameters.constrained"].walkvalues(),
            )
        }
    else:
        constrained_parameters = {
            par.name: par
            for par in filter(
                lambda x: not ("reactor_antineutrino" in x.name or "nominal_thermal_power" in x.name),
                storage["parameters.constrained"].walkvalues(),
            )
        }

    parameters = free_parameters.copy()
    # We do not use constrained parameters, if the chi-squared function based on covariance matrix
    if "covmat" not in args.statistic:
        parameters.update(constrained_parameters)

    # Create wrapper for statistic, put parameters
    # safe=False disables returning of parameters to the initial values
    fcn = make_fcn(
        storage[f"outputs.statistic.{args.statistic}"],
        parameters=parameters,
        safe=False,
    )

    # Initialize minimizer
    minimizer = iminuit.Minuit(
        fcn, name=parameters.keys(), **{name: par.value for name, par in parameters.items()}
    )
    # Do fit
    result = minimizer.migrad()

    pprint(result)

    contours = []
    for cl in args.confidence_levels:
        contours.append(result.mncontour(*args.profile_parameters, cl=cl))

    profiles = []
    for parameter in args.profile_parameters:
        profiles.append(result.mnprofile(parameter, subtract_min=True)[:2])

    result_dict = convert_minuit_to_dict(result)
    final_result = {
        f"sigma{idx}": contour for idx, contour in zip(args.confidence_levels, contours)
    }
    final_result.update(
        {parameter: profile for parameter, profile in zip(args.profile_parameters, profiles)}
    )
    parameter_x, parameter_y = args.profile_parameters
    final_result.update(
        {
            "best-fit": np.array(
                [(result_dict[parameter_x], result_dict[parameter_y], result_dict["fun"])],
                dtype=np.dtype(
                    [(parameter_x, np.float64), (parameter_y, np.float64), ("fun", np.float64)]
                ),
            )
        }
    )

    if args.output:
        np.savez(args.output, **final_result)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--source-type",
        default=None,
        help="Source type of dataset loaded from dayabay-data-official",
    )
    parser.add_argument(
        "--path-data",
        default=None,
        help="Path to data",
    )
    parser.add_argument(
        "--concatenation-mode",
        default="detector_period",
        choices=["detector", "detector_period"],
        help="Choose type of concatenation for final observation: by detector or by detector and period",
    )
    parser.add_argument(
        "--use-hubber-mueller-spectral-uncertainties",
        action="store_true",
        help="Add Hubber-Mueller uncertainties to fit parameters",
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
        help="Choose statistic for fit",
    )
    parser.add_argument(
        "--profile-parameters",
        action="extend",
        nargs="*",
        default=[],
        help="choose parameters for Minos profiling",
    )
    parser.add_argument(
        "--confidence-levels",
        action="extend",
        nargs="*",
        type=int,
        required=True,
        help="choose CL for contours",
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Path to save output, supports only npz",
    )
    args = parser.parse_args()

    main(args)
