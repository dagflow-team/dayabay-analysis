#!/bin/bash

printf "%s\n" \
     "Simple statistic+all systematic fit with combined Neyman-Neyman chi-squared function" \
     "Data type: determines from data/ content" \
     "WARNING: make sure that you have data/ directory" \
     "Asimov data" \
     "Final observation concatenated by detector and period" \
     "Minimization parameters:" \
     'Free: $\Delta m^2_{32}$, $sin^2 2\theta_{13}$ and $\xi_i, i = \overline{0, 18}$' \
     "where last parameters are parameters of antineutrino spectra shape" \
     "All constrained parameters are used in covariance matrix" \
     '$\Delta m^2_{32}$, $sin^2 2\theta_{13}$ are profiled within Minos procedure'

./fits/fit_dayabay_iminuit_asimov.py \
    --statistic full.covmat.chi2cnp \
    --free-spectrum-shape \
    --profile-parameters survival_probability.DeltaMSq32 survival_probability.SinSq2Theta13 \
    --output fit-asimov-syst-chi2cnp-free_spectrum_shape-constrained_covmat_all.json


printf "%s\n" \
     "Simple statistic+all systematic fit with combined Neyman-Pearson chi-squared function" \
     "Data type: root" \
     "WARNING: make sure that you have data-root/ directory" \
     "Asimov data" \
     "Final observation concatenated by detector" \
     "Minimization parameters:" \
     'Free: $\Delta m^2_{32}$, $sin^2 2\theta_{13}$ and $N^{\rm global}$' \
     "where the last parameter scales observed IBD spectrum in each detector" \
     "simultaneously" \
     "All constrained parameters are included as pull terms" \
     "Uncertainties for spectral parameters are not included"

./fits/fit_dayabay_iminuit_asimov.py \
    --path-data data-root \
    --concatenation-mode detector \
    --statistic full.pull.chi2cnp \
    --output fit-asimov-syst-chi2cnp-free_spectrum_shape-constrained_pull_all.yaml
