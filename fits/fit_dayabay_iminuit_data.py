#!/usr/bin/env python
r"""
Simple script for fit Daya Bay model to observed data with Minuit from iminuit package.

Examples
--------
Example of call

.. code-block:: shell

    ./fits/fit_dayabay_iminuit_data.py \
        --statistic full.pull.chi2cnp \
        --free-spectrum-shape \
        --use-hubber-mueller-spectral-uncertainties
"""
from __future__ import annotations
import iminuit
from json import dump as json_dump
from yaml import safe_dump as yaml_dump
from pickle import dump as pickle_dump
from argparse import ArgumentParser
from typing import TYPE_CHECKING
from dag_modelling.tools.make_fcn import make_fcn
from dayabay_model_official import model_dayabay


if TYPE_CHECKING:
    from typing import Any, Callable


def save_json(data, filename: str) -> None:
    with open(filename, "w") as f:
        json_dump(data, f, indent=4)


def save_pickle(data, filename: str) -> None:
    with open(filename, "wb") as f:
        pickle_dump(data, f)


def save_yaml(data: dict[str, Any], filename: str) -> None:
    with open(filename, "w") as f:
        yaml_dump(data, f)


_save_data: dict[str, Callable] = {
    "json": save_json,
    "yaml": save_yaml,
    "pickle": save_pickle,
}


def main(args) -> None:
    # Load Daya Bay model
    model = model_dayabay()
    storage = model.storage

    # Create dictionary of free parameters: [parameter name, parameter]
    # If user put --free-spectrum-shape flag, it will add parameters
    # to variate electron antineutrino spectrum shape
    # Otherwise, it will add global normalization paramter to simultaniously
    # variate rate in each detector
    if args.free_spectrum_shape:
        free_parameters = {
            "free." + par.name: par
            for par in filter(
                lambda x: "global_normalization" not in x.name,
                storage["parameters.free"].walkvalues(),
            )
        }
    else:
        free_parameters = {
            "free." + par.name: par
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
            "constrained." + par.name: par for par in storage["parameters.constrained"].walkvalues()
        }
    else:
        constrained_parameters = {
            "constrained." + par.name: par
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

    print(result)

    if args.output:
        *filename, ext = args.output.split(".")
        _save_data[ext](result, args.output)


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
        "--output",
        type=str,
        help="Path to save output",
    )
    args = parser.parse_args()

    main(args)
