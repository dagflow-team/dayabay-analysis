# Daya Bay analysis

This repo provides several scripts for obtaining $`3\nu`$ analysis of the Daya Bay experiment and not only $`3\nu`$.

Just run:
```bash
pip install -r requirements.txt
```
to install [the Daya Bay model](https://git.jinr.ru/dagflow-team/dayabay-model).

## Content

[TOC]

## General

This repository represents several examples of fitting and plotting results of fit based on [dayabay-model](https://github.com/dagflow-team/dayabay-model).

## List of files

- [covariances/README.md](covariances/README.md): short description of covariance scripts;
- [covariances/covmatrix_mc.py](covariances/covmatrix_mc.py): script for building covariance matrix via MC way;
- [fits/README.md](fits/README.md): short description of fit scripts;
- [fits/\_\_init\_\_.py](fits/__init__.py): contains useful functions for fitting;
- [fits/fit_dayabay_dgm.py](fits/fit_dayabay_dgm.py): much flexible example of fit of Daya Bay model based on dag-modeling framework;
- [fits/fit_dayabay_dgm_chi2map.py](fits/fit_dayabay_iminuit_data_contour.py): create 2D map of the Daya Bay model observed data with chosen chi-squared based on `iminuit` package;
- [fits/fit_dayabay_iminuit_asimov.py](fits/fit_dayabay_iminuit_asimov.py): fit of the Daya Bay model Asimov data with chosen chi-squared based on `iminuit` package;
- [fits/fit_dayabay_iminuit_data.py](fits/fit_dayabay_iminuit_data.py): fit of the Daya Bay model observed data with chosen chi-squared based on `iminuit` package;
- [fits/fit_dayabay_iminuit_monte_carlo.py](fits/fit_dayabay_iminuit_monte_carlo.py): fit of the Daya Bay model Monte-Carlo data with chosen chi-squared based on `iminuit` package;
- [plots/README.md](plots/README.md): short description of plot scripts;
- [plots/plot_dayabay_fit_spectra_asimov.md](plots/plot_dayabay_fit_spectra_asimov.md): script for plotting Daya Bay spectra;
- [requirements.txt](requirements.txt): contains list of libraries to be installed;
- [pyproject.toml](pyproject.toml): configuration file for linters `black` and `isort`;
- [.gitignore](.gitignore): configuration file for ignoring patterns by `git` utility.

## Fit and plot examples

Here are described how to fit and plot scripts and what preparation steps need to be completed.

### Preparation

1. Clone this repo `git clone https://github.com/dagflow-team/dayabay-analysis` and change your directory to the cloned repo `cd dayabay-analysis`
2. Install required packages: `pip install -r requirements.txt`
3. Update `PYTHONPATH` variable to the current directory: `export PYTHONPATH=$PWD:$PHYTHONPATH`. **Alternative**: set variable value when run example: `PYTHONPATH=PWD ./fits/...`

### Simple fit with IMinuit

Following script demonstrates how to run fit procedure for the Daya Bay model based on `asimov` data and combined Neyman-Pearson chi-squared function. All systematic uncertainties are treated via covariance matrix:
```bash
./fits/fit_dayabay_iminuit_asimov.py \
    --statistic full.covmat.chi2cnp
```

### Simple plot of fit

1. Following script demonstrates how to plot spectra of model based on fit data. Fit data is stored in `examples/fit-result-stat-example.yaml`:
  ```bash
  ./plots/plot_dayabay_fit_spectra_asimov.py \
      --input examples/fit-result-stat-example.yaml \
      --show
  ```
2. Following script demonstrates how to plot 2D plot in $`(\sin^22\theta_{13}, \Delta m^2_{32})`$ axes based on fit data. Fit data is stored in `examples/fit-result-stat-example.yaml`:
  ```bash
  ./plots/plot_fit_2d.py \
      --input examples/fit-result-stat-example.yaml \
      --show
  ```

## Validation of the results

Daya Bay model can be used in several modes:
- Asimov: means that final observation is based on average values of model parameters. Proper scripts are [fits/fit_dayabay_dgm.py](fits/fit_dayabay_dgm.py) with option `--data asimov` and [fits/fit_dayabay_iminuit_asimov.py](fits/fit_dayabay_iminuit_asimov.py).
- Real data: means that final observation of model will be based on measured data during experiment campaign. Proper scripts are [fits/fit_dayabay_dgm.py](fits/fit_dayabay_dgm.py) with option `--data real` and [fits/fit_dayabay_iminuit_data.py](fits/fit_dayabay_iminuit_data.py).
- Monte-Carlo data: means that final observation of model will be Monte-Carlo observation of Asimov data after Poisson procedure of randomixation: Proper script is [fits/fit_dayabay_iminuit_monte_carlo.py](fits/fit_dayabay_iminuit_monte_carlo.py).

Examples of running scripts are stored in [scripts/](scripts).

Directory [results/](results) contain reference results of fitting and plotting of best fits.

### Fitting scripts

Each file contain information about best fit under assumption certain model configurations. Configurations are described in [scripts/README.md](scripts/README.md). Also, configurations are described before starting the fit command in each shell script.

After running script from [scripts/](scripts), you may want to compare results with [results/fits/](results/fits). Central values of best fit are stored under key `xdict`. Errors of best fit are stored under key `errordict` (errors obtained from covariance matrix) or `errordict_profiled` (errors obtained with Minos algorithm).

### Plotting scripts

This directory contains results of running [plots/plot_fit_2d.py](plots/plot_fit_2d.py) and [plots/plot_fit_dayabay_asimov.py] with file [results/fits/fit-result-stat-example.yaml](results/fits/fit-result-stat-example.yaml).

## On a χ² choice of function

We provide a few various definitions of the χ² function (statistic) for the analysis. Please, note, that [the official result](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.130.161802) is using Combined Neyman-Pearson's χ² with free (unconstrained) antineutrino spectrum and systematics propagated via the nuisance terms. For more details check third script from [scripts/fit_dayabay_dgm.sh](scripts/fit_dayabay_dgm.sh) or second script from [scripts/fit_dayabay_iminuit_data.sh](scripts/fit_dayabay_iminuit_data.sh).

**Disclaimer**: Please, be warned that the use of alternative to CNP definitions may introduce the bias to the results. Moreover even if the used χ² construction is unbiased the result might be slightly different from the official one. Therefore while the choice of the function is left for the analyzer's discretion, the alternative definitions should be used only when strictly necessary.

The list of provided choices for the statistic includes `stat.chi2p_iterative`, `stat.chi2n`, `stat.chi2p`, `stat.chi2cnp`, `stat.chi2p_unbiased`, `stat.chi2poisson`, `full.covmat.chi2p_iterative`, `full.covmat.chi2n`, `full.covmat.chi2p`, `full.covmat.chi2p_unbiased`, `full.covmat.chi2cnp`, `full.pull.chi2p_iterative`, `full.pull.chi2p`, `full.pull.chi2cnp`, `full.pull.chi2p_unbiased`, `full.pull.chi2poisson`. In more details:
- Options of the propagation of systematic uncertainties:
    * `stat`: refers to χ² function that has no systematic uncertainties included, only statistical one.
    * `full.pull`: refers to χ² function that includes systematic uncertainties via nuisance parameters.
    * `full.covmat`: refers to χ² function that includes systematic uncertainties, included via covariance matrix.
- Different χ² constructions:
    * `chi2cnp`: combined Neyman-Pearson's definition of χ² function ([ref](https://arxiv.org/pdf/1903.07185)). It is empirically designed to suppress the bias mentioned above (at least for the normalization-like parameters). This function is chosen as default for the official analysis and is suggested to be used.
    * `chi2p_unbiased`: Pearson's definition of χ² function with unbiasing term added in the form of log|V| (logarithm of the determinant of the full covariance matrix). This option potentially might be used, however the validity should be checked.
    * `chi2poisson`: χ² function based on the logarithm of the ratio of Poisson functions. It is unbiased by definition, however the systematic uncertainties in this case may only be propagated via nuisance terms only.
    * `chi2n`: Neyman's definition of χ² function. The statistical uncertainties are based on the observation. This one should be used only for Asimov data (no fluctuations). It is advised to never use it for data, unless analyzer knows what he is doing. In the case of presence of fluctuations Neyman's χ² may provide biased result due to presence of fluctuations in the definition of uncertainties.
    * `chi2p`: Pearson's definition of χ² function. The statistical uncertainties are based on the prediction. This one should be used only for Asimov data (no fluctuations). It is advised to never use it for data, unless analyzer knows what he is doing. In the case of presence of fluctuations Pearson's χ² may provide biased result due to interplay between parameter dependent uncertainties and fluctuations.
- Some specific χ² constructions. For all of them the analysis should be thoroughly validated.
    * `full.covmat.chi2p_iterative`: Pearson's χ² function with covariance matrix. The covariance matrix are fixed during the minimization process. Could be used in iterative fit procedure when the covariance matrix is updated at the best fit position and the fit is repeated.
    * `full.covmat.chi2cnp`: combined Neyman-Pearson's χ² with covariance matrix. The statistical part of the covariance matrix is defined according to [the corresponding paper](https://arxiv.org/pdf/1903.07185) (formula 18).

**Warning**: some tests contain option `--profile-parameters`. This option activates profiling of parameters to obtain correct values of errors. It might take a long time. If you want to just test, remove `--profile-parameters` key.

## Known issues

Matplotlib may pass warning that `UserWarning: FigureCanvasAgg is non-interactive, and thus cannot be shown plt.show()`. Please istall `PyQT5` as python package to solve this issue:
```bash
pip install pyqt5
```
It might works for Linux users.
