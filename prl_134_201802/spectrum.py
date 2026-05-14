from argparse import ArgumentParser, Namespace
from typing import Iterable

import numpy as np
from dayabay_data_official import get_path_data
from dayabay_model import model_dayabay
from matplotlib import pyplot as plt
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


CM2_PER_FISSION_SCALE = 1.0e43
DEFAULT_EDGES = np.concatenate([[0.700000], np.arange(1.25, 7.01, 0.25), [8.000000]], dtype=float)


def load_dayabay_201802_data(path):
    arr = np.loadtxt(path, unpack=True)
    return {
        "edges": np.concatenate((arr[0], [8.0])),
        "y": arr[2],
        "ey": arr[3],
    }


def sum_detector_period_data(storage, observation: str, detectors: Iterable[str], periods: Iterable[str]) -> NDArray:
    total = np.zeros_like(next(storage[observation].walkvalues()).data)
    for key, obs in storage[observation].walkjoineditems():
        if any([detector in key for detector in detectors]) and any([period in key for period in periods]):
            arr = np.array(obs.data, dtype=float)
            total = arr.copy() if total is None else total + arr
    return total


def main(args: Namespace) -> None:

    detectors = args.detectors or ("AD11", "AD12", "AD21", "AD22")
    periods = args.periods or ("6AD", "8AD", "7AD")
    prl_data = load_dayabay_201802_data(args.official_spectrum_file)

    model = model_dayabay(
        path_data=get_path_data(),
        final_erec_bin_edges=DEFAULT_EDGES,
        concatenation_mode="detector",
    )
    storage = model.storage["outputs"]

    widths = DEFAULT_EDGES[1:] - DEFAULT_EDGES[:-1]
    centers = 0.5 * (DEFAULT_EDGES[:-1] + DEFAULT_EDGES[1:])

    # Real data counts in final reconstructed-energy bins
    data_counts = sum_detector_period_data(storage, "data.real.final.detector_period", detectors, periods)

    # Background estimate in the same bins
    background_counts = sum_detector_period_data(storage, "eventscount.final.background", detectors, periods)

    # IBD model spectra in the same bins
    full_ibd_counts = sum_detector_period_data(storage, "eventscount.final.ibd", detectors, periods)

    model.set_parameters(
        {
            "reactor.neq_factor": 0.0,
            "reactor.snf_factor": 0.0,
        }
    )
    main_osc_counts = sum_detector_period_data(storage, "eventscount.final.ibd", detectors, periods)

    model.set_parameters(
        {
            "survival_probability.SinSq2Theta13": 0.0,
            "survival_probability.SinSq2Theta12": 0.0,
        }
    )
    main_noosc_counts = sum_detector_period_data(storage, "eventscount.final.ibd", detectors, periods)
    model.set_parameters(
        {
            "survival_probability.SinSq2Theta13": 0.0856,
            "survival_probability.SinSq2Theta12": 0.8510,
        }
    )

    # NEQ+SNF contribution to subtract from data-like points
    neq_snf_counts = full_ibd_counts - main_osc_counts

    # Oscillation correction factor applied bin-by-bin
    osc_correction = np.divide(
        main_noosc_counts,
        main_osc_counts,
        out=np.ones_like(main_noosc_counts),
        where=main_osc_counts != 0.0,
    )

    corrected_data_counts = (data_counts - background_counts - neq_snf_counts) * osc_correction

    # Effective fission denominator from Eq. (1)-like normalization in the model
    denominator = sum_detector_period_data(
        storage, "reactor_detector.n_fissions_n_protons_per_cm2_scaled", detectors, periods
    )

    data_like_yield = corrected_data_counts / (denominator * widths) * CM2_PER_FISSION_SCALE

    ratio = prl_data["y"] / data_like_yield
    corrected_data_counts_err = data_like_yield * (1.0 / (corrected_data_counts * CM2_PER_FISSION_SCALE) + 1.0 / (denominator * widths))**0.5

    ratio_err = ratio * ((corrected_data_counts_err / corrected_data_counts)**2 + (prl_data["ey"] / prl_data["y"])**2)**0.5

    total_flux = (data_like_yield * widths).sum()

    fig, axs = plt.subplots(2, 1, height_ratios=[3, 1], sharex=True, figsize=(5, 5.5))
    axs[0].stairs(data_like_yield, DEFAULT_EDGES, label="model")
    axs[0].stairs(prl_data["y"], DEFAULT_EDGES, label="official")

    axs[0].errorbar(y=data_like_yield, x=centers, linestyle="none", xerr=widths / 2, yerr=corrected_data_counts_err)
    axs[0].errorbar(y=prl_data["y"],   x=centers, linestyle="none", xerr=widths / 2, yerr=prl_data["ey"])

    axs[1].errorbar(y=ratio - 1.0, x=centers, xerr=widths / 2, yerr=ratio_err, linestyle="none")
    axs[1].hlines(0, 12, -1, color="black", alpha=0.5, linestyle="--")
    axs[1].set_xlim(0.6, 8.1)
    axs[1].set_xlabel("Reconstructed energy [MeV]")
    axs[1].set_ylabel("official / model - 1")
    axs[0].set_ylabel(r"$\times 10^{-43}\text{cm}^2/\text{fission}/\text{MeV}$")
    axs[0].set_title(f"Total flux is {total_flux:1.2f} " r"$\times 10^{-43}\text{cm}^2/\text{fission}$")
    plt.tight_layout()
    plt.subplots_adjust(hspace=0)
    plt.savefig("results/prl_134_201802/spectrum.pdf")
    plt.savefig("results/prl_134_201802/spectrum.png")
    plt.show()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--path-data", default=None, help="Path to Daya Bay dataset directory")
    parser.add_argument(
        "--detectors",
        default=["AD11", "AD12", "AD21", "AD22"],
        nargs="*",
        help="Comma-separated detector list. Default: near ADs only",
    )
    parser.add_argument(
        "--periods",
        default=["6AD", "8AD", "7AD"],
        nargs="*",
        help="Comma-separated periods to aggregate",
    )
    parser.add_argument(
        "--official-spectrum-file",
        default="prl_134_201802/official-spectrum.dat",
        help="Path to published 2501 total prompt IBD yield table (Emin Emax Ec y ey)",
    )
    args = parser.parse_args()

    main(args)
