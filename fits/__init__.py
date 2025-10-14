"""Common classes and functions for scripts."""

from __future__ import annotations

from json import dump as json_dump
from pickle import dump as pickle_dump
from typing import TYPE_CHECKING

import numpy as np
from dag_modelling.parameters import Parameter
from iminuit.minuit import Minuit
from iminuit.util import MErrors
from yaml import add_representer
from yaml import safe_dump as yaml_dump

if TYPE_CHECKING:
    from typing import Any

    from dag_modelling.core import NodeStorage
    from dgm_fit.minimizer_base import MinimizerBase
    from numpy.typing import NDArray

add_representer(
    np.ndarray,
    lambda representer, obj: representer.represent_str(np.array_repr(obj)),
)


def update_dict_parameters(
    dict_parameters: dict[str, Parameter],
    groups: list[str],
    model_parameters: NodeStorage,
) -> None:
    """Update dictionary of minimization parameters.

    Parameters
    ----------
    dict_parameters : dict[str, Parameter]
        Dictionary of parameters.
    groups : list[str]
        List of groups of parameters or parameters to be added to dict_parameters.
    model_parameters : NodeStorage
        Storage of model parameters.

    Returns
    -------
    None
    """
    for group in groups:
        if isinstance(model_parameters[group], Parameter):
            dict_parameters[group] = model_parameters[group]
        else:
            dict_parameters.update(
                {
                    f"{group}.{path}": parameter
                    for path, parameter in model_parameters[group].walkjoineditems()
                }
            )


def filter_fit(src: dict, keys_to_filter: list[str]) -> None:
    """Remove keys from fit dictionary.

    Parameters
    ----------
    src : dict
        Dictionary of fit.
    keys_to_filter : list[str]
        List of keys to be deleted from fit dictionary.

    Returns
    -------
    None
    """
    keys = list(src.keys())
    for key in keys:
        if key in keys_to_filter:
            del src[key]
            continue
        if isinstance(src[key], dict):
            filter_fit(src[key], keys_to_filter)


def convert_numpy_to_lists(src: dict[str, NDArray | dict]) -> None:
    """Convert recursively numpy array in dictionary.

    Parameters
    ----------
        src : dict
            Dictionary that may contains numpy arrays as value.

    Returns
    -------
    None
    """
    for key, value in src.items():
        if isinstance(value, np.ndarray):
            src[key] = value.tolist()
        elif isinstance(value, dict):
            convert_numpy_to_lists(value)


def do_fit(minimizer: MinimizerBase, model, is_iterative: bool = False) -> dict:
    """Do fit procedure obtain iterative statistics.

    Parameters
    ----------
    minimizer : MinimizerBase
        Minimization object.
    model : model_dayabay
        Object of model.
    is_iterative : bool
        Minimizable function is iterative statistics or not.

    Returns
    -------
    dict
        Fit result.
    """
    fit = minimizer.fit()
    if is_iterative:
        for _ in range(4):
            model.next_sample(mc_parameters=False, mc_statistics=False)
            fit = minimizer.fit()
            if not fit["success"]:
                break
    return fit


def _save_json(data: dict[str, Any], filename: str) -> None:
    """Save fit data in json-format.

    Parameters
    ----------
    data : dict[str, Any]
        Dictionary that contains lists, and dicts with strings or numbers
    filename : str
        Path to save output

    Returns
    -------
    None
    """
    with open(filename, "w") as f:
        json_dump(data, f)


def _save_pickle(data: dict[str, Any], filename: str) -> None:
    """Save fit data in pickle-format.

    Parameters
    ----------
    data : dict[str, Any]
        Dictionary that contains lists, and dicts with strings or numbers
    filename : str
        Path to save output

    Returns
    -------
    None
    """
    with open(filename, "wb") as f:
        pickle_dump(data, f)


def _save_yaml(data: dict[str, Any], filename: str) -> None:
    """Save fit data in yaml-format.

    Parameters
    ----------
    data : dict[str, Any]
        Dictionary that contains lists, and dicts with strings or numbers
    filename : str
        Path to save output

    Returns
    -------
    None
    """
    with open(filename, "w") as f:
        yaml_dump(data, f)


def convert_minuit_to_dict(data: Minuit) -> dict[str, Any]:
    names = [name for name in data.var2pos.keys()]
    x = [value for value in data.values]
    errors = [error for error in data.errors]
    return dict(
        covariance=data.covariance,
        errorsdict=dict(zip(names, errors)),
        fun=data.fval,
        names=names,
        nfev=data.nfcn,
        npars=data.npar,
        success=data.valid,
        x=np.array(x),
        xdict=dict(zip(names, x)),
    )


def filter_save_fit(data: dict[str, Any] | Minuit, filename: str, minos_result: MErrors | None = None) -> None:
    """Filter and save fit results.

    It filters fit data from undumpable objects
    and converts numpy arrays to simple python lists.

    Parameters
    ----------
    data : dict[str, Any] | Minuit
        Minuit object or dictionary that contains result of fit
    filename : str
        Path to save output
    minos_result : Minuit | None = None
        Results of profiling of parameters from Minos procedure

    Returns
    -------
    None

    """
    if isinstance(data, Minuit):
        result = convert_minuit_to_dict(data)
    else:
        result = data.copy()
    if minos_result:
        result["errorsdict_profiled"] = {parameter: [merror.lower, merror.upper] for parameter, merror in minos_result.items()}

    filter_fit(result, ["summary"])
    convert_numpy_to_lists(result)
    *rootparts, ext = filename.split(".")
    match ext:
        case "json":
            _save_json(result, filename)
        case "yaml":
            _save_yaml(result, filename)
        case "pickle":
            _save_pickle(result, filename)
        case "pkl":
            _save_pickle(result, filename)
        case _:
            raise RuntimeError(f"Couldn't dump result to `.{ext}`-type")
