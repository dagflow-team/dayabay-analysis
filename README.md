# Daya Bay analysis

This repo provides several scripts for obtaining $`3\nu`$ analysis of the Daya Bay experiment and not only $`3\nu`$.

Just run:
```bash
pip install -r requirements.txt
```
to install [the Daya Bay model](https://git.jinr.ru/dagflow-team/dayabay-model-official).

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

Fit script:

```bash
./fits/fit_dayabay_iminuit_asimov.py \
    --statistic full.covmat.chi2n \
    --free-spectrum-shape
```

Plot script:

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
