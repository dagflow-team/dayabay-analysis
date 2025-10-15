# Daya Bay analysis

This repo provides several scripts for obtaining $`3\nu`$ analysis of the Daya Bay experiment and not only $`3\nu`$.

Just run:
```bash
pip install -r requirements.txt
```
to install [the Daya Bay model](https://git.jinr.ru/dagflow-team/dayabay-model-official).

## Content

- [List of files](#list-of-files)
- [Minimal working examples](#minimal-working-examples)
- [Validating results](#validating-results)
  - [results/fits](#results-fits)
  - [results/plots](#results-plots)
- [Known issues](#known-issues)

## List of files

- [fits/README.md](fits/README.md): short description of fit scripts;
- [fits/\_\_init\_\_.py](fits/__init__.py): contains useful functions for fitting;
- [fits/fit_dayabay_dgm.py](fits/fit_dayabay_dgm.py): much flexible example of fit of Daya Bay model based on dag-modeling framework;
- [fits/fit_dayabay_iminuit_asimov.py](fits/fit_dayabay_iminuit_asimov.py): fit of the Daya Bay model Asimov data with chosen chi-squared based on `iminuit` package;
- [fits/fit_dayabay_iminuit_data.py](fits/fit_dayabay_iminuit_data.py): fit of the Daya Bay model observed data with chosen chi-squared based on `iminuit` package;
- [fits/fit_dayabay_iminuit_monte_carlo.py](fits/fit_dayabay_iminuit_monte_carlo.py): fit of the Daya Bay model Monte-Carlo data with chosen chi-squared based on `iminuit` package;
- [plots/README.md](plots/README.md): short description of plot scripts;
- [plots/plot_dayabay_fit_spectra_asimov.md](plots/plot_dayabay_fit_spectra_asimov.md): script for plotting Daya Bay spectra;
- [requirements.txt](requirements.txt): contains list of libraries to be installed;
- [pyproject.toml](pyproject.toml): configuration file for linters `black` and `isort`;
- [.gitignore](.gitignore): configuration file for ignoring patterns by `git` utility;

## Minimal working examples

1. Clone this repo `git clone https://github.com/dagflow-team/dayabay-analysis` and change your directory to the cloned repo `cd dayabay-analysis`
2. Install required packages: `pip install -r requirements`
3. Clone the repository with Daya Bay data `git clone https://github.com/dagflow-team/dayabay-data-official`
  - Make sure that you have `git-lfs` in your system or install it
  - After installing `git-lfs`, run command `git lfs pull` to download more files
  - More details on how to work with data repository you can find in [README.md of the data repository](https://github.com/dagflow-team/dayabay-data-official)
4. Create soft links `ln -s dayabay-data-official/hdf5 data`
5. Set `PYTHONPATH` variable to the current directory: `set PYTHONPATH=$PHYTHONPATH:$PWD`. **Alternative**: set variable value when run example: `PYTHONPATH=PWD ./fits/...`
6. Try to run examples above:
  - Fit script:
```bash
./fits/fit_dayabay_iminuit_asimov.py \
    --statistic full.covmat.chi2cnp \
    --free-spectrum-shape
```
  - Plot script:
```bash
./plots/plot_dayabay_fit_spectra_asimov.py \
    --input examples/fit-result-stat-example.yaml \
    --show
```
  or
```bash
./plots/plot_fit_2d.py \
    --input examples/fit-result-stat-example.yaml \
    --show
```

## Validating results

Daya Bay model can be used in several modes:
- Asimov: means that final observation is based on average values of model parameters. Proper scripts are [fits/fit_dayabay_dgm.py](fits/fit_dayabay_dgm.py) with option `--data asimov` and [fits/fit_dayabay_iminuit_asimov.py](fits/fit_dayabay_iminuit_asimov.py).
- Real data: means that final observation of model will be based on measured data during experiment campaign. Proper scripts are [fits/fit_dayabay_dgm.py](fits/fit_dayabay_dgm.py) with option `--data real` and [fits/fit_dayabay_iminuit_data.py](fits/fit_dayabay_iminuit_data.py).
- Monte-Carlo data: means that final observation of model will be Monte-Carlo observation of Asimov data after Poisson procedure of randomixation: Proper script is [fits/fit_dayabay_iminuit_monte_carlo.py](fits/fit_dayabay_iminuit_monte_carlo.py).

Examples of running scripts are stored in [scripts/](scripts).

Directory [results/](results) contain reference results of fitting and plotting of best fits.

The most closest result to [the PRL 130, 161802](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.130.161802) might be obtained with CNP chi squared with pull terms and free spectrum. For more details check third script from [scripts/fit_dayabay_dgm.sh](scripts/fit_dayabay_dgm.sh) or second script from [scripts/fit_dayabay_iminuit_data.sh](scripts/fit_dayabay_iminuit_data.sh).

Description for each type of chi-squared function, you may find in [fits/README.md](fits/README.md).

**Warning**: some tests contain option `--profile-parameters`. This option activates profiling of parameters to obtain correct values of errors. It might take a long time. If you want to just test, remove `--profile-parameters` key.

### results/fits

Each file contain information about best fit under assumption certain model configurations. Configurations are described in [scripts/README.md](scripts/README.md). Also, configurations are described before starting the fit command in shell script.

After running script from [scripts/](scripts), you may compare results. Central values of best fit are stored under key `xdict`. Errors of best fit are stored under key `errordict` (errors obtained from covariance matrix) or `errordict_profiled` (errors obtained with Minos algorithm).

### results/plots

This directory contains results of running `plots/plot_fit_2d.py` with files from [results/fits/](results/fits).

## Known issues

Matplotlib may pass warning that `UserWarning: FigureCanvasAgg is non-interactive, and thus cannot be shown plt.show()`. Please istall `PyQT5` as python package to solve this issue:
```bash
pip install pyqt5
```
It might works for Linux users.
