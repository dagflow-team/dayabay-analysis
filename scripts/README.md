# Description

This directory contains several examples of running fit procedure via scripts from [fits/](fits).

## fit_dayabay_dgm.sh

Contains several examples of running fit procedure within framework tools.

### The first script

It starts fit to Asimov data with statistical only combined Neyman-Pearson chi-sqaured.

Data will be loaded from `./data/`. Don't forget to create it before running.

As free parameters are chosen $\Delta m^2_{32}$ and $\sin^2 2\theta_{13}$.

Final observation concatenated by detectors and periods.

Output of the fit procedure will be dumped in `yaml`-format.

### The second script

It starts fit to Asimov data with combined Neyman-Pearson chi-sqaured that treats pull terms.

Data will be loaded from `./data-npz/`. Don't forget to create it before running.

As free parameters are chosen parameters from `survival_probability` namespace. This namespace contains $\Delta m^2_{32}$ and $\sin^2 2\theta_{13}$.

Also, parameters from `detector` namespace are included as pull terms.

Final observation concatenated by detectors and periods.

Output of the fit procedure will be dumped in `json`-format.

### The third script

It starts fit to observed data with combined Neyman-Pearson chi-sqaured that includes covariance matrix.

Data will be loaded from `./data/`. Don't forget to create it before running.

As free parameters are chosen parameters from `survival_probability` and `neutrino_per_fission_factor` namespace. The last namespace contains 19 parameters to variate shape of the antineutrino flux.

All nuisance parameters are treated within covariance matrix.

Final observation concatenated by detectors and periods.

Output of the fit procedure will be dumped in `pickle`-format.


### The forth script

It starts fit to Monte-Carlo ata with statistical only combined Neyman-Pearson chi-sqaured. Monte-Carlo includes variation of bin observations via Poisson distribution $\mathrm{Poisson}(N)$, where $N$ is number of events in the bin.

Data will be loaded from `./data-tsv/`. Don't forget to create it before running.

As free parameters are chosen from `survival_probability` and `neutrino_per_fission_factor` namespace.

Final observation concatenated by detectors.

Output of the fit procedure will be dumped in `yaml`-format.


## fit_dayabay_iminuit_asimov.sh

Contains several examples of running fit procedure on Asimov data within `iminuit` package.

### The first script

It starts fit to Asimov data with combined Neyman-Pearson chi-sqaured that includes covariance matrix.

Data will be loaded from `./data-hdf5/`. Don't forget to create it before running.

Option `--free-spectrum-shape` includes parameters from the namespace `neutrino_per_fission_factor` as free parameters.

All nuisance parameters are treated within covariance matrix.

Final observation concatenated by detectors and periods.

Output of the fit procedure will be dumped in `json`-format.

### The second script

It starts fit to Asimov data with combined Neyman-Pearson chi-sqaured that includes covariance matrix.

Data will be loaded from `./data-root/`. Don't forget to create it before running.

All nuisance parameters are treated as pull terms.

Final observation concatenated by detectors.

Output of the fit procedure will be dumped in `json`-format.

## fit_dayabay_iminuit_data.sh

Contains several examples of running fit procedure on observed data within `iminuit` package.

### The first script

It starts fit to observed data with combined Neyman-Pearson chi-sqaured that includes covariance matrix.

Data will be loaded from `./data/`. Don't forget to create it before running.

Option `--free-spectrum-shape` includes parameters from the namespace `neutrino_per_fission_factor` as free parameters.

All nuisance parameters are treated within covariance matrix.

Final observation concatenated by detectors and periods.

Output of the fit procedure will be dumped in `json`-format.

### The second script

It starts fit to observed data with combined Neyman-Pearson chi-sqaured that includes covariance matrix.

Data will be loaded from `./data-npz/`. Don't forget to create it before running.

All nuisance parameters are treated as pull terms.

Final observation concatenated by detectors.

Output of the fit procedure will be dumped in `json`-format.

