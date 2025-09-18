# Daya Bay analysis

This repo provides several scripts for obtaining $`3\nu`$ analysis of the Daya Bay experiment and not only $`3\nu`$.

Just run:
```bash
pip install -r requirements.txt
```
or
```bash
pip install dgm-dayabay-dev
```
to install the Daya Bay model.

## List of files

- `fits/fit_dayabay.py`: fit of the Daya Bay model with chosen parameters and chi-squared function;
- `fits/__init__.py`: contains useful functions for fitting;
- `requirements.txt`: contains list of libraries to be installed;
- `pyproject.toml`: configuration file for linters `black` and `isort`;
- `.gitignore`: configuration file for ignoring patterns by `git` utility;
- `.envrc`: controls environment variables within `direnv` utility.
