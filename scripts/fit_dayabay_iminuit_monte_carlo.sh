#!/bin/bash

printf "%s\n" \
     "Simple statistic+all systematic fit with combined Neyman-Neyman chi-squared function" \
     "Source type: Default (hdf5)" \
     "WARNING: make sure that you have data/ directory" \
     "Monte-Carlo data (poisson type, seed = 1)" \
     "Final observation concatenated by detector and period" \
     "Minimization parameters:" \
     'Free: $\Delta m^2_{32}$, $sin^2 2\theta_{13}$ and $\xi_i, i = \overline{0, 18}$' \
     "where last parameters are parameters of antineutrino spectra shape" \
     "All constrained parameters are used in covariance matrix" \

./fits/fit_dayabay_iminuit_monte_carlo.py \
    --statistic full.covmat.chi2cnp \
    --monte-carlo poisson \
    --seed 1 \
    --output fit-mc_poisson_1-syst-chi2cnp-free_spectrum_shape-constrained_covmat_all.json


printf "%s\n" \
     "Simple statistic+all systematic fit with combined Neyman-Pearson chi-squared function" \
     "Source type: npz" \
     "WARNING: make sure that you have data-npz/ directory" \
     "Monte-Carlo data (normal-stats type, seed = 3)" \
     "Final observation concatenated by detector" \
     "Minimization parameters:" \
     'Free: $\Delta m^2_{32}$, $sin^2 2\theta_{13}$ and $\xi_i, i = \overline{0, 18}$' \
     "where last parameters are parameters of antineutrino spectra shape" \
     "All constrained parameters are included as pull terms" \
     "Uncertainties for spectral parameters are not included"

./fits/fit_dayabay_iminuit_monte_carlo.py \
    --source-type npz \
    --monte-carlo normal-stats \
    --seed 3 \
    --concatenation-mode detector \
    --statistic full.pull.chi2cnp \
    --output fit-mc_poisson_3-syst-chi2cnp-free_spectrum_shape-constrained_pull_all.yaml
