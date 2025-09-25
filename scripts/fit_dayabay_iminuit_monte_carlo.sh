#!/bin/bash

printf "%s\n" \
     "Simple statistic+all systematic fit with Neyman's chi-squared function" \
     "Data type: determines from data/ content" \
     "WARNING: make sure that you have data/ directory" \
     "Monte-Carlo data (poisson type, seed = 1)" \
     "Final observation concatenated by detector and period" \
     "Minimization parameters:" \
     'Free: $\Delta m^2_{32}$, $sin^2 2\theta_{13}$ and $\xi_i, i = \overline{0, 18}$' \
     "where last parametrs are parameters of antineutrino spectra shape" \
     "All constrained parameters are used in covariance matrix"

./fits/fit_dayabay_iminuit_monte_carlo.py \
    --statistic full.covmat.chi2n \
    --monte-carlo poisson \
    --seed 1 \
    --free-spectrum-shape \
    --output fit-syst-chi2n-free_spectrum_shape-constrained_covmat_all.json


printf "%s\n" \
     "Simple statistic+all systematic fit with Pearson's chi-squared function" \
     "Data type: npz" \
     "WARNING: make sure that you have data-npz/ directory" \
     "Monte-Carlo data (normal-stats type, seed = 3)" \
     "Final observation concatenated by detector" \
     "Minimization parameters:" \
     'Free: $\Delta m^2_{32}$, $sin^2 2\theta_{13}$ and $N^{\rm global}$' \
     "where the last parameter scales observed IBD spectrum in each detector" \
     "simultaneously" \
     "All constrained parameters are included as pull terms" \
     "Uncertainties for spectral parameters are not included"

./fits/fit_dayabay_iminuit_monte_carlo.py \
    --path-data data-npz \
    --monte-carlo normal-stats \
    --seed 3 \
    --concatenation-mode detector \
    --statistic full.pull.chi2p \
    --output fit-syst-chi2p-free_spectrum_shape-constrained_pull_all.yaml
