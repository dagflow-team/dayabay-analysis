# Description

This directory contains several examples of running fit procedure via scripts from `fits/`.

## fit_dayabay_dgm.sh

Contains several examples of running fit procedure within framework tools.

### The first script

It starts fit to Asimov data with statistical only Pearson's chi-sqaured.

Model will load data in `hdf5`-format (default option).

As free parameters are chosen `$\Delta m^2_{32}$` and `$\sin^2 2\theta_{13}$`.

Final observation concatenated by detectors and periods.

Output of the fit procedure will be dumped in `yaml`-format.

### The second script

It starts fit to Asimov data with Pearson's chi-sqaured that treats pull terms.

Model will load data in `npz`-format.

As free parameters are chosen parameters from `survival_probability` namespace. This namespace contains `$\Delta m^2_{32}$` and `$\sin^2 2\theta_{13}$`.

Also, parameters from `detector` namespace are included as pull terms.

Final observation concatenated by detectors and periods.

Output of the fit procedure will be dumped in `json`-format.

### The third script

It starts fit to observed data with Neyman's chi-sqaured that includes covariance matrix.

Model will load data in `hdf5`-format (default option).

As free parameters are chosen parameters from `survival_probability` and `neutrino_per_fission_factor` namespace. The last namespace contains 19 parameters to variate shape of the antineutrino flux.

All nuisance parameters are treated within covariance matrix.

Final observation concatenated by detectors and periods.

Output of the fit procedure will be dumped in `pickle`-format.


### The forth script

It starts fit to Monte-Carlo ata with statistical only unbiased Pearson's chi-sqaured. Monte-Carlo includes variation of bin observations via Poisson distribution `$\mathrm{Poisson}(N)$`, where `$N$` is number of events in the bin.

Model will load data in `tsv`-format.

As free parameters are chosen from `survival_probability` and `neutrino_per_fission_factor` namespace.

Final observation concatenated by detectors.

Output of the fit procedure will be dumped in `yaml`-format.


## fit_dayabay_iminuit_asimov.sh

Contains several examples of running fit procedure on Asimov data within `iminuit` package.

### The first script

It starts fit to Asimov data with Neyman's chi-sqaured that includes covariance matrix.

Model will load data in `hdf5`-format (default option).

Option `--free-spectrum-shape` includes parameters from the namespace `neutrino_per_fission_factor` as free parameters.

All nuisance parameters are treated within covariance matrix.

Final observation concatenated by detectors and periods.

Output of the fit procedure will be dumped in `json`-format.

### The second script

It starts fit to Asimov data with Neyman's chi-sqaured that includes covariance matrix.

Model will load data in `root`-format.

All nuisance parameters are treated as pull terms.

Final observation concatenated by detectors.

Output of the fit procedure will be dumped in `json`-format.

## fit_dayabay_iminuit_data.sh

Contains several examples of running fit procedure on observed data within `iminuit` package.

### The first script

It starts fit to observed data with Neyman's chi-sqaured that includes covariance matrix.

Model will load data in `hdf5`-format (default option).

Option `--free-spectrum-shape` includes parameters from the namespace `neutrino_per_fission_factor` as free parameters.

All nuisance parameters are treated within covariance matrix.

Final observation concatenated by detectors and periods.

Output of the fit procedure will be dumped in `json`-format.

### The second script

It starts fit to observed data with Neyman's chi-sqaured that includes covariance matrix.

Model will load data in `npz`-format.

All nuisance parameters are treated as pull terms.

Final observation concatenated by detectors.

Output of the fit procedure will be dumped in `json`-format.

