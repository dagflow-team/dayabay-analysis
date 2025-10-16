#!/bin/bash

printf "%s\n" \
     "Calculate chi-squared map based on combined Neyman-Pearson's chi-squared" \
     "Data type: determines from data/ content" \
     "WARNING: make sure that you have data/ directory" \
     "Real data" \
     "Final observation concatenated by detector and period" \
     "Minimization parameters:" \
     'Free: $\Delta m^2_{32}$, $sin^2 2\theta_{13}$ and $\xi_i, i = \overline{0, 18}$' \
     "where last parameters are parameters of antineutrino spectra shape" \
     "All constrained parameters are used in covariance matrix"

./fits/fit_dayabay_dgm_chi2map.py \
    --data real \
    --free-parameters survival_probability neutrino_per_fission_factor \
    --scan-par survival_probability.SinSq2Theta13 0.072 0.098 21 \
    --scan-par survival_probability.DeltaMSq32 2.17e-3 2.77e-3 21 \
    --chi2 full.covmat.chi2cnp \
    --output contour-real-covmat-chi2cnp.npz


printf "%s\n" \
     "Calculate chi-squared map based on combined Neyman-Pearson's chi-squared" \
     "Data type: determines from data/ content" \
     "WARNING: make sure that you have data/ directory" \
     "Real data" \
     "Final observation concatenated by detector and period" \
     "Minimization parameters:" \
     'Free: $\Delta m^2_{32}$, $sin^2 2\theta_{13}$ and $\xi_i, i = \overline{0, 18}$' \
     "where last parameters are parameters of antineutrino spectra shape" \
     "All constrained parameters are treated as pull terms"

./fits/fit_dayabay_dgm_chi2map.py \
    --data real \
    --free-parameters survival_probability neutrino_per_fission_factor \
    --constrained-parameters survival_probability detector reactor background \
    --scan-par survival_probability.SinSq2Theta13 0.072 0.098 21 \
    --scan-par survival_probability.DeltaMSq32 2.17e-3 2.77e-3 21 \
    --chi2 full.pull.chi2cnp \
    --output contour-real-pull-chi2cnp.npz


printf "%s\n" \
     "Calculate chi-squared map based on combined Neyman-Pearson's chi-squared" \
     "Data type: determines from data/ content" \
     "WARNING: make sure that you have data/ directory" \
     "Asimov data" \
     "Final observation concatenated by detector and period" \
     "Minimization parameters:" \
     'Free: $\Delta m^2_{32}$, $sin^2 2\theta_{13}$ and $\xi_i, i = \overline{0, 18}$' \
     "where last parameters are parameters of antineutrino spectra shape" \
     "All constrained parameters are used in covariance matrix"

./fits/fit_dayabay_dgm_chi2map.py \
    --data asimov \
    --free-parameters survival_probability neutrino_per_fission_factor \
    --scan-par survival_probability.SinSq2Theta13 0.072 0.098 21 \
    --scan-par survival_probability.DeltaMSq32 2.17e-3 2.77e-3 21 \
    --chi2 full.covmat.chi2cnp \
    --output contour-asimov-covmat-chi2cnp.npz


printf "%s\n" \
     "Simple statistic+all systematic fit with combined Neyman-Neyman chi-squared function" \
     "Data type: determines from data/ content" \
     "WARNING: make sure that you have data/ directory" \
     "Asimov data" \
     "Final observation concatenated by detector and period" \
     "Minimization parameters:" \
     'Free: $\Delta m^2_{32}$, $sin^2 2\theta_{13}$ and $\xi_i, i = \overline{0, 18}$' \
     "where last parameters are parameters of antineutrino spectra shape" \
     "All constrained parameters are treated as pull terms"

./fits/fit_dayabay_dgm_chi2map.py \
    --data asimov \
    --free-parameters survival_probability neutrino_per_fission_factor \
    --constrained-parameters survival_probability detector reactor background \
    --scan-par survival_probability.SinSq2Theta13 0.072 0.098 21 \
    --scan-par survival_probability.DeltaMSq32 2.17e-3 2.77e-3 21 \
    --chi2 full.pull.chi2cnp \
    --output contour-asimov-pull-chi2cnp.npz
