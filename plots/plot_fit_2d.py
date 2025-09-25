#!/usr/bin/env python
r"""Script for 2d fit plot.

Examples
--------
Example of call

.. code-block:: shell

    ./scripts/plot_fit_2d.py \

"""
from argparse import Namespace

import numpy as np
from matplotlib import pyplot as plt
from yaml import safe_load as yaml_load


plt.rcParams.update(
    {
        "xtick.top": True,
        "xtick.minor.top": True,
        "xtick.minor.visible": True,
        "axes.grid": True,
        "ytick.left": True,
        "ytick.minor.left": True,
        "ytick.right": True,
        "ytick.minor.right": True,
        "ytick.minor.visible": True,
    }
)


def get_parameter_fit(
    xdict: dict[str, float], errorsdict: dict[str, float | tuple[float, float]], key: str
) -> tuple[float, float, float]:
    """Get value, left/right error of chosen.

    Parameters
    ----------
    xdict : dict[str, float]
        Dictionary with central values of fitted parameters.
    errorsdict : dict[str, float | tuple[float, float]]
        Dictionary with errors of fitted parameters.
    key : str
        Name of fitted parameter.

    Returns
    -------
    tuple[float, float, float, str]
        Return tuple (central value, left error, right error, string with an additional information).
    """
    if key in xdict.keys():
        if isinstance(errorsdict[key], float):
            return xdict[key], errorsdict[key], errorsdict[key]
        elif isinstance(errorsdict[key], (tuple, list)):
            return xdict[key], -1 * errorsdict[key][0], errorsdict[key][1]
    elif key == "detector.global_normalization":
        names = [
            name for name in xdict if name.startswith("neutrino_per_fission_factor.spec_scale")
        ]
        scale = np.array([xdict[name] for name in names])
        unc = np.array([errorsdict[name] for name in names])
        w = unc**-2
        wsum = w.sum()
        res = (scale * w).sum() / wsum
        return 1 + res, 0.0, 0.0
    raise KeyError(f"No key {key} in fit information.")


def main(args: Namespace) -> None:

    with open(args.input, "r") as f:
        fit = yaml_load(f)



    fig, ax,  = plt.subplots(1, 1)


    xdict = fit["xdict"]
    errorsdict = fit.get("errorsdict_profiled", fit["errorsdict"])

    dm_value, dm_error_left, dm_error_right = get_parameter_fit(
        xdict, errorsdict, "survival_probability.DeltaMSq32"
    )
    sin_value, sin_error_left, sin_error_right = get_parameter_fit(
        xdict, errorsdict, "survival_probability.SinSq2Theta13"
    )

    ax.errorbar(
        sin_value,
        dm_value,
        xerr=[[sin_error_left], [sin_error_right]],
        yerr=[[dm_error_left], [dm_error_right]],
        label="best fit",
    )
    label = r"$0.1\sigma$"
    ax.axvspan(
        sin_value - 0.1 * sin_error_left,
        sin_value + 0.1 * sin_error_right,
        -10,
        10,
        color="0.9",
        label=label,
    )
    ax.axhspan(
        dm_value - 0.1 * dm_error_left,
        dm_value + 0.1 * dm_error_right,
        -10,
        10,
        color="0.9",
    )

    plt.legend()

    if args.output:
        plt.savefig(args.output, metadata={"creationDate": None})

    if args.show:
        plt.show()


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()

    comparison = parser.add_argument_group("comparison", "Comparison options")
    comparison.add_argument(
        "--input",
        help="Path to file with reference fit values",
    )

    outputs = parser.add_argument_group("outputs", "set outputs")
    outputs.add_argument(
        "--output",
        help="Path to save plot",
    )
    outputs.add_argument(
        "--show",
        action="store_true",
        help="Show output plot",
    )

    args = parser.parse_args()

    main(args)
