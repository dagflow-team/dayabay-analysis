import iminuit
from argparse import ArgumentParser
from dag_modelling.tools.make_fcn import make_fcn
from dayabay_model_official import model_dayabay


def dump_pickle(data):
    pass


def dump_json(data):
    pass


def dump_yaml(data):
    pass


def main(args) -> None:
    model = model_dayabay()
    storage = model.storage

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
    if "covmat" not in args.statistic:
        parameters.update(constrained_parameters)
    print(len(parameters))

    fcn = make_fcn(
        storage[f"outputs.statistic.{args.statistic}"],
        parameters=list(parameters.values()),
        safe=False,
    )

    minimizer = iminuit.Minuit(
        fcn, name=parameters.keys(), **{name: par.value for name, par in parameters.items()}
    )
    result = minimizer.migrad()
    print(result)


if __name__ == "__main__":
    parser = ArgumentParser()
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
    args = parser.parse_args()

    main(args)
