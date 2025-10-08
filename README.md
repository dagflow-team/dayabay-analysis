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

## List of files

- `fits/README.md`: short description of fit scripts;
- `fits/__init__.py`: contains useful functions for fitting;
- `fits/fit_dayabay_dgm.py`: much flexible example of fit of Daya Bay model based on dag-modeling framework;
- `fits/fit_dayabay_iminuit_asimov.py`: fit of the Daya Bay model Asimov data with chosen chi-squared based on `iminuit` package;
- `fits/fit_dayabay_iminuit_data.py`: fit of the Daya Bay model observed data with chosen chi-squared based on `iminuit` package;
- `fits/fit_dayabay_iminuit_monte_carlo.py`: fit of the Daya Bay model Monte-Carlo data with chosen chi-squared based on `iminuit` package;
- `plots/README.md`: short description of plot scripts;
- `plots/plot_dayabay_fit_spectra_asimov.md`: script for plotting Daya Bay spectra;
- `requirements.txt`: contains list of libraries to be installed;
- `pyproject.toml`: configuration file for linters `black` and `isort`;
- `.gitignore`: configuration file for ignoring patterns by `git` utility;
- `.envrc`: controls environment variables within `direnv` utility.

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
    --statistic full.covmat.chi2n \
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
