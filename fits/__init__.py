"""Common classes and functions for scripts."""

import numpy as np
from dag_modelling.core import NodeStorage
from dgm_fit.minimizer_base import MinimizerBase
from dag_modelling.parameters import Parameter
from numpy.typing import NDArray
from yaml import add_representer

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
        List of groups of parameters to be added to dict_parameters.
    model_parameters : NodeStorage
        Storage of model parameters.

    Returns
    -------
    None
    """
    for group in groups:
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
    model : model_dayabay_v0x
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
