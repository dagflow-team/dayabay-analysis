import iminuit
from argparse import ArgumentParser
from dag_modelling.core.make_fcn import make_fcn
from dayabay_model_official import model_dayabay


def main(args) -> None:
    model = model_dayabay()
    storage = model.storage

    if args.free_spec:
        free_parameters = {"parameters.all." + par.name: par.value for par in filter(lambda x: "global_normalization" not in x.name, storage["parameters.free"].walkvalues())}
    else:
        free_parameters = {"parameters.all." + par.name: par.value for par in filter(lambda x: "neutrino_per_fission" not in x.name, storage["parameters.free"].walkvalues())}
    if args.use_hm_unc:
        constrained_parameters = {"parameters.all." + par.name: par.value for par in storage["parameters.constrained"].walkvalues()}
    else:
        constrained_parameters = {"parameters.all." + par.name: par.value for par in filter(lambda x: "reactor_antineutrino_spectrum_uncertainty" not in x.name, storage["parameters.constrained"].walkvalues())}
    constrained_errors = {"error_" + par.name: par.sigma for par in storage["parameters.constrained"].walkvalues()}

    parameters = free_parameters.copy()
    if "covmat" not in args.statistic:
        parameters.update(constrained_parameters)

    fcn = make_fcn(
        storage[f"outputs.statistic.{args.statistic}"],
        storage,
        safe=False,
        par_names=parameters.keys(),
    )

    minimizer = iminuit.Minuit(fcn, name=parameters.keys(), **parameters)
    result = minimizer.migrad()
    print(result)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--free-spec", action="store_true", help="Minimize spectrum shape")
    parser.add_argument("--use-hm-unc", action="store_true", help="Add Hubber-Mueller uncertainties to fit parameters")
    parser.add_argument("--statistic", default="full.pull.chi2cnp", help="Choose statistic for fit")
    args = parser.parse_args()

    main(args)
