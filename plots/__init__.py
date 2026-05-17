from __future__ import annotations

from collections.abc import Generator
from typing import Any

import numpy as np
from matplotlib import ticker
from numpy.typing import NDArray

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


def get_observation(
    storage_generator: Generator[tuple[str, Any], None, None], width: NDArray = np.array([1.0])
) -> dict[str, NDArray]:
    """Get observable scaled or not by width of bins.

    Parameters
    ----------
    storage_generator : Generator[tuple[str, Any], None, None]
        Storage that contains observables.
    width : NDArray
        Array of widths of bins.

    Returns
    -------
    None
    """
    result = {}
    for key, obs in storage_generator:
        result[key] = obs.data.copy() / width
    return result


def calculate_ratio_error(data_a: NDArray | float, data_b: NDArray | float) -> NDArray | float:
    r"""Calculate error of ratio of two observables.

    .. math::
        \sigma\left(\dfrac{a}{b}\right) = \sqrt{\left(\dfrac{\sigma_a}{a}\right)^2 + \left(\dfrac{\sigma_b}{b}\right)^2}
        = \dfrac{1}{b}\sqrt{\dfrac{a}{b}\left(a + b\right)}

    Parameters
    ----------
    data_a : NDArray | float
        Numerator.
    data_b : NDArray | float
        Denominator.

    Returns
    -------
    NDArray
        Error of ratio.
    """
    ratio = data_a / data_b
    return 1 / data_b * (ratio * (data_a + data_b)) ** 0.5


class FFormatter(ticker.ScalarFormatter):
    """FFormatter class for pretty formatting of x-/y-axis tick labels.

    Parameters
    ----------
    fformat : str
        Format of labels.
    useOffset : bool
        Use offset value.
    useMathText : bool
        Use LaTeX for formatting.
    *args : list
        Other arguments to be delivered to parent class.
    **kwargs : dict
        Other keyword arguments to be delivered to parent class.
    """

    def __init__(
        self,
        fformat: str = "%3.1f",
        useOffset: bool = True,
        useMathText: bool = True,
        *args: list,
        **kwargs: dict,
    ):
        self.fformat = fformat
        ticker.ScalarFormatter.__init__(
            self, useOffset=useOffset, useMathText=useMathText, *args, **kwargs
        )

    def _set_format(self) -> None:
        """Set format field.

        Returns
        -------
        None
        """
        self.format = self.fformat
