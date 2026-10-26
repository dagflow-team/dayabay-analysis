from argparse import ArgumentParser, Namespace

import numpy as np
from dayabay_data_official import get_path_data
from dayabay_model import model_dayabay
from matplotlib import pyplot as plt
from numpy.typing import NDArray
from scipy.interpolate import interp1d

from plots import FFormatter


def get_observation(storage, detectors) -> NDArray:
    return np.vstack(
        [obs.data for (period, detector), obs in storage.walkitems() if detector in detectors]
    ).sum(axis=0)


eh_events_energies = {
    "EH1": [],
    "EH2": [],
    "EH3": [],
}

eh_to_ads = {
    "EH1": ["AD11", "AD12"],
    "EH2": ["AD21", "AD22"],
    "EH3": ["AD31", "AD32", "AD33", "AD34"],
}

ad_to_eh = {
    "AD11": "EH1",
    "AD12": "EH1",
    "AD21": "EH2",
    "AD22": "EH2",
    "AD31": "EH3",
    "AD32": "EH3",
    "AD33": "EH3",
    "AD34": "EH3",
}


def main(args: Namespace) -> None:
    lsnl_data = np.load(get_path_data(source_type="npz") / "detector_lsnl_curves.npz")
    xcoarse = lsnl_data["nominal"]["E_MeV"]
    lsnl_nominal_relative = lsnl_data["nominal"]["f"]
    lsnl_nominal_absolute = lsnl_nominal_relative * xcoarse
    lsnl_nominal_absolute_inv_interpolated = interp1d(
        lsnl_nominal_absolute,
        xcoarse,
        kind="linear",
        bounds_error=False,
        fill_value="extrapolate",
    )

    model = model_dayabay(
        concatenation_mode="detector",
        path_data=get_path_data(),
        strict=False,
        process_labels=False,
    )

    final_edges = model.storage["outputs.edges.energy_final"].data
    widths = final_edges[1:] - final_edges[:-1]

    for ad in ["AD11", "AD12", "AD21", "AD22", "AD31", "AD32", "AD33", "AD34"]:
        energies_p = np.load(f"{args.path_tree_events}/dayabay_dataset_events_{ad}.npz")["events"]["energy_prompt_MeV"]
        energies_lsnl_inv = lsnl_nominal_absolute_inv_interpolated(energies_p)
        eh_events_energies[ad_to_eh[ad]].append(np.histogram(energies_lsnl_inv, final_edges)[0])

    lsnl_matrix = model.storage["outputs.detector.lsnl.matrix.AD11"].data
    rebin = model.storage["outputs.detector.rebin.matrix_ibd"].data

    table_prl = np.loadtxt("prl_130_161802/prl-events-by-eh.dat")

    lsnl_matrix_t = lsnl_matrix.toarray().T
    lsnl_matrix_inv = np.nan_to_num(lsnl_matrix_t / lsnl_matrix_t.sum(axis=0), 0.0)

    transformation_inv = rebin @ lsnl_matrix_inv

    for idx, (eh, detectors) in enumerate(eh_to_ads.items()):
        emin, emax, centers, obs6ad, obs8ad, obs7ad, pred6ad, pred8ad, pred7ad = np.loadtxt(
            f"prl_130_161802/DayaBay_IBDPromptSpectrum_{eh}_3158days.txt", unpack=True
        )
        obs_after_lsnl_inv_including_bkg = obs6ad + obs8ad + obs7ad

        model_N = get_observation(model.storage["outputs.data.real.fine"], detectors)

        print(
            f"{eh}: (PRL table)={table_prl[idx]:>10.2f} PRL (file)={obs_after_lsnl_inv_including_bkg.sum():>10.2f}; "
            f"model (initial)={model_N.sum():>10.2f} "
            f"model (events)={(transformation_inv @ model_N).sum():>10.2f} "
            f"model (hist)={(transformation_inv @ model_N).sum():>10.2f}"
        )

        fig, axs = plt.subplots(3, 1, height_ratios=[3, 1, 1], figsize=(6, 6), sharex=True)
        eh_hist = np.vstack(eh_events_energies[eh]).sum(axis=0)
        axs[0].stairs(
            eh_hist / widths,
            final_edges,
            label="open model+lsnl_inv (event by event)",
            linestyle="-",
        )
        axs[0].stairs(
            transformation_inv @ model_N / widths,
            final_edges,
            label="open model+lsnl_inv (hist)",
            linestyle="--",
        )
        axs[0].stairs(
            obs_after_lsnl_inv_including_bkg / widths,
            final_edges,
            label="PRL 130, 161802 (supplementary)",
            linestyle=":",
        )
        for hist, label in zip([eh_hist, transformation_inv @ model_N], ["event by event", "hist"]):
            axs[1].stairs(
                (hist / obs_after_lsnl_inv_including_bkg - 1),
                final_edges,
                label=f"{label} / PRL",
            )
            axs[2].stairs(
                np.abs(hist / obs_after_lsnl_inv_including_bkg - 1),
                final_edges,
                label=f"{label} / PRL",
            )
        formatter = FFormatter()
        formatter.set_powerlimits((0, 3))
        axs[0].yaxis.set_major_formatter(formatter)
        ylim = 8e5 if eh == "EH1" else 9.2e5 if eh == "EH2" else 2.9e5
        ylim1 = 0.45e-2 if eh == "EH1" else 0.195e-2 if eh == "EH2" else 0.85e-2
        axs[0].set_ylim(0, ylim)
        axs[1].set_ylim(-ylim1, ylim1)
        axs[0].set_title(eh)
        axs[0].set_ylabel(r"Entries [MeV$^{-1}$]")
        axs[1].set_ylabel("ratio - 1")
        axs[2].set_ylabel("|ratio - 1|")
        axs[2].set_xlabel("Reconstructed energy [MeV]")
        axs[2].set_yscale("log")
        plt.subplots_adjust(wspace=0, hspace=0, top=0.92, left=0.165, right=0.95)

        for ax in axs:
            ax.legend(loc="upper right")

        plt.savefig(f"results/prl_130_161802/{eh}.pdf")

    if args.show:
        plt.show()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument(
        "--path-tree-events",
        help="Path to directory that contains files with IBD event trees with names `dayabay_dataset_b_events_{ad}.npz`",
    )
    parser.add_argument("-s", "--show", action="store_true", help="Show plots")

    args = parser.parse_args()

    main(args)
