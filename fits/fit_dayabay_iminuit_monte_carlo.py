#!/usr/bin/env python
r"""
Simple script for fit Daya Bay model to Monte-Carlo data with Minuit from iminuit package.

Examples
--------
Example of call

.. code-block:: shell

    ./fits/fit_dayabay_iminuit_monte_carlo.py \
        --statistic full.pull.chi2cnp \
        --free-spectrum-shape \
        --monte_carlo_mode poisson \
        --seed 1 \
        --use-hubber-mueller-spectral-uncertainties
"""
from __future__ import annotations

from argparse import ArgumentParser
from pprint import pprint

import iminuit
from dag_modelling.tools.make_fcn import make_fcn
from dayabay_model_official import model_dayabay

from fits import filter_save_fit

ASIMOV_OUTPUT_INDEX = 0


def main(args) -> None:
    # Load Daya Bay model
    model = model_dayabay(
        path_data=args.path_data,
        concatenation_mode=args.concatenation_mode,
        monte_carlo_mode=args.monte_carlo_mode,
        seed=args.seed,
    )
    storage = model.storage

    # Switch output for data from observed data to Asimov data
    model.switch_data("asimov")

    # Create dictionary of free parameters: [parameter name, parameter]
    # If user put --free-spectrum-shape flag, it will add parameters
    # to variate electron antineutrino spectrum shape
    # Otherwise, it will add global normalization paramter to simultaniously
    # variate rate in each detector
    if args.free_spectrum_shape:
        free_parameters = {
            par.name: par
            for par in filter(
                lambda x: "global_normalization" not in x.name,
                storage["parameters.free"].walkvalues(),
            )
        }
    else:
        free_parameters = {
            par.name: par
            for par in filter(
                lambda x: "neutrino_per_fission" not in x.name,
                storage["parameters.free"].walkvalues(),
            )
        }
    # Create dictionary of constrained parameters: [parameter name, parameter]
    # If user put --use-hubber-mueller-spectral-uncertainties flag, it will add
    # parameters of uncertainties for each isotope (more than 1000 parameters)
    # Usually, these parameters are used for fit with observed data
    if args.use_hubber_mueller_spectral_uncertainties:
        constrained_parameters = {
            par.name: par for par in storage["parameters.constrained"].walkvalues()
        }
    else:
        constrained_parameters = {
            par.name: par
            for par in filter(
                lambda x: "reactor_antineutrino" not in x.name,
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

    minos_result = {}
    if args.profile_parameters:
        minos_result = minimizer.minos(*args.profile_parameters).merrors

    if args.output:
        filter_save_fit(result, args.output, minos_result)


if __name__ == "__main__":
    parser = ArgumentParser()
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
        "--monte-carlo-mode",
        "--mc",
        default="poisson",
        choices=["poisson", "normal-stats"],
        help="Choose Monte-Carlo option",
    )
    parser.add_argument(
        "--seed",
        default=0,
        type=int,
        help="Choose seed for random generation",
    )
    parser.add_argument(
        "--free-spectrum-shape", action="store_true", help="Minimize spectrum shape"
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
            "full.covmat.chi2cnp_alt",
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
        "--output",
        type=str,
        help="Path to save output",
    )
    args = parser.parse_args()

    main(args)
