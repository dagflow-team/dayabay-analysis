#!/usr/bin/env python
r"""Script for fit model to observed/model data.

Examples
--------
Example of call

.. code-block:: shell

    ./fits/fit_dayabay.py --version v0e \
      --mo "{dataset: b, monte_carlo_mode: poisson, seed: 1}" \
      --chi2 full.pull.chi2p \
      --free-parameters oscprob neutrino_per_fission_factor \
      --constrained-parameters oscprob detector reactor bkg reactor_anue \
      --constrain-osc-parameters \
      --output fit-result.yaml
"""
from argparse import ArgumentParser, Namespace
from pprint import pprint
from typing import TYPE_CHECKING

from dag_modelling.tools.logger import DEBUG as INFO4
from dag_modelling.tools.logger import INFO1, INFO2, INFO3, set_level
from dgm_dayabay_dev.models import available_models, load_model
from dgm_fit.iminuit_minimizer import IMinuitMinimizer
from yaml import dump as yaml_dump

from fits import convert_numpy_to_lists, do_fit, filter_fit, update_dict_parameters

if TYPE_CHECKING:
    from dag_modelling.parameters import Parameter


DATA_INDICES = {"model": 0, "loaded": 1}


def main(args: Namespace) -> None:
    # Set verbosity level
    if args.verbose:
        args.verbose = min(args.verbose, 3)
        set_level(globals()[f"INFO{args.verbose}"])

    # Initialize model
    model = load_model(
        args.version,
        source_type=args.source_type,
        model_options=args.model_options,
        parameter_values=args.par,
    )

    # Initialize helpful variables and switch output of model
    # to Asimov (output 0) or Real data (output 1).
    storage = model.storage
    storage["nodes.data.proxy"].switch_input(DATA_INDICES[args.data])

    parameters_free = storage("parameters.free")
    parameters_constrained = storage("parameters.constrained")
    statistic = storage("outputs.statistic")

    # Choose statistic for minimization
    chi2 = statistic[f"{args.chi2}"]
    # Fill variable `minimization_parameters` free and constrained parameters,
    # if they are given
    minimization_parameters: dict[str, Parameter] = {}
    update_dict_parameters(minimization_parameters, args.free_parameters, parameters_free)
    if "covmat" not in args.chi2:
        update_dict_parameters(
            minimization_parameters,
            args.constrained_parameters,
            parameters_constrained,
        )
    elif args.constrained_parameters:
        raise Exception(f"Statistic {args.chi2} can not be used with constrained parameters")

    # Sometimes fit is unstable. And constraining of free parameters
    # might improve robustness of fit
    if args.constrain_osc_parameters:
        # Initialize minimizer object
        minimizer = IMinuitMinimizer(
            chi2,
            parameters=minimization_parameters,
            limits={"oscprob.SinSq2Theta13": (0, 1), "oscprob.DeltaMSq32": (2e-3, 3e-3)},
            nbins=model.nbins,
            verbose=args.verbose > 1,
        )
        # Start fitting
        fit = do_fit(minimizer, model, args.n_iterations)
        # Errors from IMinuit are not good?. Errors can be improved,
        # if we profile them with minos algorithm
        if args.profile_parameters:
            minos_profile = minimizer.profile_errors(args.profile_parameters)
            fit["errorsdict_profiled"] = minos_profile["errorsdict"]
        # Filter fit output before saving in yaml format
        filter_fit(fit, ["summary"])
        # Convert all arrays in lists
        convert_numpy_to_lists(fit)
        if args.output:
            with open(f"{args.output}.constrained_osc", "w") as f:
                yaml_dump(fit, f)
        if not fit["success"]:
            exit()

    # Initialize minimizer object
    minimizer = IMinuitMinimizer(
        chi2, parameters=minimization_parameters, nbins=model.nbins, verbose=args.verbose > 1
    )

    fit = do_fit(minimizer, model, args.n_iterations)
    # Start fitting
    if args.profile_parameters:
        minos_profile = minimizer.profile_errors(args.profile_parameters)
        fit["errorsdict_profiled"] = minos_profile["errorsdict"]

    filter_fit(fit, ["summary"])
    convert_numpy_to_lists(fit)
    if args.output:
        with open(f"{args.output}", "w") as f:
            yaml_dump(fit, f)
    pprint(fit)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("-v", "--verbose", default=0, action="count", help="verbosity level")

    model = parser.add_argument_group("model", "model related options")
    model.add_argument(
        "--version",
        default="v0",
        choices=available_models(),
        help="model version",
    )
    model.add_argument(
        "-s",
        "--source-type",
        "--source",
        choices=("tsv", "hdf5", "root", "npz"),
        default="hdf5",
        help="data source type",
    )
    model.add_argument(
        "--par",
        nargs=2,
        action="append",
        default=[],
        help="set parameter value",
    )
    model.add_argument("--model-options", "--mo", default={}, help="model options as yaml dict")

    fit_options = parser.add_argument_group("fit", "Set fit procedure")
    fit_options.add_argument(
        "--data",
        default="model",
        choices=DATA_INDICES.keys(),
        help="choose data for fit",
    )
    fit_options.add_argument(
        "--constrain-osc-parameters",
        action="store_true",
        help="constrain oscillation parameters",
    )
    fit_options.add_argument(
        "--profile-parameters",
        action="extend",
        nargs="*",
        default=[],
        help="choose parameters for Minos profiling",
    )
    fit_options.add_argument(
        "--chi2",
        default="stat.chi2p",
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
        help="choose chi-squared function for minimizer",
    )
    fit_options.add_argument(
        "--n-iterations",
        default=0,
        help="number of iterations of fit procedure, usefull only for iterative chi-squared",
    )
    fit_options.add_argument(
        "--free-parameters",
        default=[],
        nargs="*",
        help="add free parameters to minimization process",
    )
    fit_options.add_argument(
        "--constrained-parameters",
        default=[],
        nargs="*",
        help="add constrained parameters to minimization process",
    )

    outputs = parser.add_argument_group("outputs", "set outputs")
    outputs.add_argument(
        "--output",
        help="path to save full fit, yaml format",
    )

    args = parser.parse_args()

    main(args)
