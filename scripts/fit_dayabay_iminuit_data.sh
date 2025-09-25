#!/bin/bash

printf "%s\n" \
     "Simple statistic+all systematic fit with Neyman's chi-squared function" \
     "Data type: determines from data/ content" \
     "WARNING: make sure that you have data/ directory" \
     "Observed data" \
     "Final observation concatenated by detector and period" \
     "Minimization parameters:" \
     'Free: $\Delta m^2_{32}$, $sin^2 2\theta_{13}$ and $\xi_i, i = \overline{0, 18}$' \
     "where last parametrs are parameters of antineutrino spectra shape" \
     "All constrained parameters are used in covariance matrix"

./fits/fit_dayabay_iminuit_data.py \
    --statistic full.covmat.chi2n \
    --free-spectrum-shape \
    --output fit-syst-chi2n-free_spectrum_shape-constrained_covmat_all.json


printf "%s\n" \
     "Simple statistic+all systematic fit with Pearson's chi-squared function" \
     "Data type: hdf5" \
     "WARNING: make sure that you have data-hdf5/ directory" \
     "Observed data" \
     "Final observation concatenated by detector" \
     "Minimization parameters:" \
     'Free: $\Delta m^2_{32}$, $sin^2 2\theta_{13}$ and $N^{\rm global}$' \
     "where the last parameter scales observed IBD spectrum in each detector" \
     "simultaneously" \
     "All constrained parameters are included as pull terms" \
     "Uncertainties for spectral parameters are not included"

./fits/fit_dayabay_iminuit_data.py \
    --path-data data-hdf5 \
    --concatenation-mode detector \
    --statistic full.pull.chi2p \
    --output fit-syst-chi2p-free_spectrum_shape-constrained_pull_all.yaml
