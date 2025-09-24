#!/usr/bin/env python
r"""Script for creating covariance matrix via Monte-Carlo approach.

Examples
--------
Example of call

.. code-block:: shell

    ./covariances/covmatrix_mc.py \
        --par oscprob.DeltaMSq32 2.5e-3 \
        --systematic-parameters-groups survival_probability background \
        "--seed 1 \
        "--num 500
"""
from __future__ import annotations
from argparse import Namespace
import numpy as np
from matplotlib import pyplot as plt
from dag_modelling.tools.logger import set_verbosity
from dayabay_model_official import model_dayabay
from dag_modelling.parameters import Parameter
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from numpy.typing import NDArray
    from dag_modelling.core import NodeStorage
    from dag_modelling.core.output import Output


SYSTEMATIC_UNCERTAINTIES_GROUPS = {
    "all",
    "survival_probability",
    "detector",
    "reactor",
    "background",
    "reactor_antineutrino",
}


def variate_parameters(parameters: list[Parameter], generator: np.random.Generator) -> None:
    """Randomize value of parameters via normal unit distribution N(0, 1).

    Parameters
    ----------
    parameters : list[Parameter]
        List of normalized parameters.
    generator : np.random.Generator
        Numpy generator of pseudo-random numbers.

    Returns
    -------
    None
    """
    for parameter in parameters:
        parameter.value = generator.normal(0, 1)


def create_list_of_variation_parameters(
    model,
    storage: NodeStorage,
    groups: list[str],
) -> list[Parameter]:
    """Create a list of parameters.

    Parameters
    ----------
    model : model_dayabay_v0x
        Object of model.
    storage : NodeStorage
        Storage of model where all necessary items are stored.
    groups : list[str]
        List of parameters groups that will be used for Monte-Carlo method.

    Returns
    -------
    list[Parameter]
        List of normalized parameters.
    """
    parameters = []
    if "all" in groups:
        groups = model.systematic_uncertainties_groups().values()
    for group in groups:
        if isinstance(storage[f"parameters.normalized.{group}"], Parameter):
            parameters.append(storage[f"parameters.normalized.{group}"])
        else:
            parameters.extend(
                [parameter for parameter in storage[f"parameters.normalized.{group}"].walkvalues()]
            )
    return parameters


def covariance_matrix_calculation(
    parameters: list[Parameter],
    generator: np.random.Generator,
    observation: Output,
    N: int,
    asimov: NDArray | None = None,
) -> NDArray:
    r"""Calculate absolute covariance matrix.

    Parameters
    ----------
    parameters : list[Parameter]
        List of normalized parameters.
    generator : np.random.Generator
        Numpy generator of pseudo-random numbers.
    observation : Output
        Observation of model that depends on parameters.
    N : int
        Number of samples for calculation covariance matrices.
    asimov : NDArray, optional
        Asimov observation (no fluctuation of parameters).

    Returns
    -------
    NDArray
        Two dimensional square array, absolute covariance matrix.

    Notes
    -----
    For the calculation used the next formula

    .. math:: cov_{ij} = \frac{1}{N}\sum_{k = 1}^{N}(x_i^k - \overline{x_i})(x_j^k - \overline{x_j}),

    where `x_i^k` is `i`-th bin value of `k`-th sample, `\overline{x_i}` is mean
    value of `i`-th bin, $N$ is normalization factor

    Here we are using simplified formula

    .. math:: cov_{ij} = \frac{1}{\text{norm}} \overline{x_i x_j} - \overline{x_i}\overline{x_j^A} - \overline{x_j}\overline{x_i^A} + \overline{x_i^A}\overline{x_i^A},

    where we averaging over all MC samples

    If Asimov observation is passed, the next formula is used

    .. math:: cov_{ij} = \frac{1}{\text{norm}} \overline{x_i x_j} - \overline{x_i}\overline{x_j^A} - \overline{x_j}\overline{x_i^A} + \overline{x_i^A}\overline{x_j^A},
    """
    observation_size = observation.data.shape[0]
    product_mean = np.zeros((observation_size, observation_size))
    observation_sum = np.zeros(observation_size)
    for _ in range(N):
        variate_parameters(parameters, generator)
        observation_sum += observation.data
        product_mean += np.outer(observation.data, observation.data)
    if asimov is not None:
        product_mean /= N
        observation_mean_asimov = np.outer(observation_sum, asimov) / N
        observation_product_mean = (
            observation_mean_asimov + observation_mean_asimov.T - np.outer(asimov, asimov)
        )
    else:
        product_mean /= N - 1
        observation_product_mean = np.outer(observation_sum, observation_sum) / ((N - 1) * N)
    covariance_matrix_absolute = product_mean - observation_product_mean
    return covariance_matrix_absolute


def covariance_matrix_calculation_alternative(
    parameters: list[Parameter],
    generator: np.random.Generator,
    observation: Output,
    N: int,
    asimov: NDArray | None = None,
) -> NDArray:
    r"""Calculate absolute matrix (alternative method).

    Parameters
    ----------
    parameters : list[Parameter]
        List of normalized parameters.
    generator : np.random.Generator
        Numpy generator of pseudo-random numbers.
    observation : Output
        Observation of model that depends on parameters.
    N : int
        Number of samples for calculation covariance matrices.
    asimov : NDArray, optional
        Two dimensional square array, absolute covariance matrix.

    Returns
    -------
    NDArray
        Absolute covariance matrix.

    Notes
    -----
    For the calculation used simplified formula

    .. math:: cov_{ij} = \frac{1}{\text{norm}} \overline{x_i x_j} - \overline{x_i}\overline{x_j^A} - \overline{x_j}\overline{x_i^A} + \overline{x_i^A}\overline{x_j^A},

    where `S` is `Nx(observation size)` matrix that contains all Monte-Carlo samples.

    Here we use a lot of memory to store every Monte-Carlo sample and we provide
    calculations via matrix product

    If Asimov observation is passed, the next formula is used

    .. math:: cov_{ij} = \frac{1}{\text{norm}} \overline{x_i x_j} - \overline{x_i}\overline{x_j^A} - \overline{x_j}\overline{x_i^A} + \overline{x_i^A}\overline{x_j^A},
    """
    observation_size = observation.data.shape[0]
    samples = np.zeros((N, observation_size))
    for i in range(N):
        variate_parameters(parameters, generator)
        samples[i] = observation.data
    if asimov is not None:
        samples_mean = asimov
        covariance_normalization_factor = N
    else:
        samples_mean = samples.mean(axis=0)
        covariance_normalization_factor = N - 1
    samples_diff = samples - samples_mean
    covariance_matrix_absolute = samples_diff.T @ samples_diff / covariance_normalization_factor
    return covariance_matrix_absolute


def calculate_correlation_matrix(covariance_matrix: NDArray) -> NDArray:
    r"""Calculate correlation matrix from covariance matrix.

    Parameters
    ----------
    covariance_matrix : NDArray
        Covariance matrix.

    Returns
    -------
    NDArray
        Correlation matrix.

    Notes
    -----

    .. math:: \mathrm{corr}_{ij} = \frac{\mathrm{cov}_{ij}}{\sqrt{\mathrm{cov}_{ii}\mathrm{cov}_{jj}}}
    """
    diagonal = np.diagonal(covariance_matrix)
    return covariance_matrix / np.outer(diagonal, diagonal) ** 0.5


def main(opts: Namespace) -> None:
    if opts.verbose:
        set_verbosity(opts.verbose)

    model = model_dayabay(
        source_type=opts.source_type,
        parameter_values=opts.par,
    )

    storage: NodeStorage = model.storage

    observation = storage["outputs.eventscount.final.concatenated.selected"]
    asimov = observation.data.copy()
    generator = np.random.Generator(np.random.MT19937(opts.seed))

    parameters = create_list_of_variation_parameters(
        model,
        storage,
        opts.systematic_parameters_groups,
    )

    if opts.alternative:
        covariance_absolute = covariance_matrix_calculation_alternative(
            parameters,
            generator,
            observation,
            opts.num,
            asimov if opts.asimov_as_mean else None,
        )
    else:
        covariance_absolute = covariance_matrix_calculation(
            parameters,
            generator,
            observation,
            opts.num,
            asimov if opts.asimov_as_mean else None,
        )

    covariance_relative = covariance_absolute / np.outer(asimov, asimov)
    correlation_matrix = calculate_correlation_matrix(covariance_absolute)

    cs = plt.matshow(covariance_absolute)
    plt.title("Covariance matrix (absolute)")
    plt.colorbar(cs)
    plt.tight_layout()

    plt.figure()
    plt.plot(np.diagonal(covariance_absolute))
    plt.title("Covariance matrix (absolute, diagonal)")
    plt.xlabel("Bin index")
    plt.ylabel("Entries")
    plt.tight_layout()

    cs = plt.matshow(covariance_relative)
    plt.title("Covariance matrix (relative)")
    plt.colorbar(cs)
    plt.tight_layout()

    cs = plt.matshow(correlation_matrix)
    plt.title("Correlation matrix")
    plt.colorbar(cs)
    plt.tight_layout()

    plt.show()


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument("-v", "--verbose", default=1, action="count", help="verbosity level")

    model = parser.add_argument_group("model", "model related options")
    model.add_argument(
        "-s",
        "--source-type",
        "--source",
        choices=("tsv", "hdf5", "root", "npz"),
        default="default:hdf5",
        help="Data source type",
    )
    model.add_argument("--par", nargs=2, action="append", default=[], help="Set parameter value")

    cov = parser.add_argument_group("cov", "covariance parameters")
    cov.add_argument(
        "--systematic-parameters-groups",
        "--cov",
        default=[],
        choices=SYSTEMATIC_UNCERTAINTIES_GROUPS,
        nargs="+",
        help="Choose systematic parameters for building covariance matrix",
    )
    cov.add_argument(
        "--asimov-as-mean",
        action="store_true",
        help="Use Asimov data as mean",
    )
    cov.add_argument(
        "--alternative",
        action="store_true",
        help="Use alternative method for calculation (much memory-intensive)",
    )
    cov.add_argument(
        "--seed",
        default=0,
        help="Choose seed of randomization algorithm",
    )
    cov.add_argument(
        "-N",
        "--num",
        default=1000,
        help="Choose number of samples",
    )
    args = parser.parse_args()

    main(args)
