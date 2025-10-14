#!/bin/bash

printf "%s\n" \
     "Simple statistic only fit with combined Neyman-Pearson chi-squared function" \
     "Data type: determines from data/ content" \
     "WARNING: make sure that you have data/ directory" \
     "Asimov data" \
     "Final observation concatenated by detector and period" \
     'Minimization parameters: $\Delta m^2_{32}$ and $sin^2 2\theta_{13}$'

./fits/fit_dayabay_dgm.py \
    --statistic stat.chi2cnp \
    --free-parameters survival_probability.DeltaMSq32 survival_probability.SinSq2Theta13 \
    --output fit-asimov-stat-chi2cnp-free_survival_probability.yaml


printf "%s\n" \
     "Simple statistic+reactor systematic fit with combined Neyman-Pearson chi-squared function" \
     "Data type: npz" \
     "WARNING: make sure that you have data-npz/ directory" \
     "Asimov data" \
     "Final observation concatenated by detector" \
     "Minimization parameters:" \
     'Free: $\Delta m^2_{32}$ and $sin^2 2\theta_{13}$' \
     "Constrained:" \
     '- energy resolution: $\sigma_{a}$, $\sigma_{b}$, and $\sigma_{c}$ (3 parameters)' \
     '- LSNL: $\zeta^{i}_{\mathrm{LSNL}}$ (4 parameters)' \
     '- IAV scaling: $\eta^{\mathrm{AD}}_{\mathrm{IAV}}$ (8 parameters)' \
     '- Detector efficiency: $\epsilon^{\mathrm{AD}}$ (8 parameters)' \
     '- Detector energy scale:  $\eta^{\mathrm{AD}}$ (8 parameters)'

./fits/fit_dayabay_dgm.py \
     --path-data data-root \
     --statistic full.pull.chi2cnp \
     --concatenation-mode detector \
     --free-parameters survival_probability \
     --constrained-parameters detector \
     --output fit-asimov-syst-chi2cnp-free_survival_probability-constrained_detector.pickle


printf "%s\n" \
     "Simple statistic+all systematic fit with combined Neyman-Pearson chi-squared function" \
     "Data type: determines from data/ content" \
     "WARNING: make sure that you have data/ directory" \
     "Real data" \
     "Final observation concatenated by detector and period" \
     "Minimization parameters:" \
     'Free: $\Delta m^2_{32}$, $sin^2 2\theta_{13}$ and $\xi_i, i = \overline{0, 18}$' \
     "where last parameters are parameters of antineutrino spectra shape" \
     "All constrained parameters are used in covariance matrix"

./fits/fit_dayabay_dgm.py \
    --data real \
    --statistic full.covmat.chi2cnp \
    --free-parameters survival_probability neutrino_per_fission_factor \
    --output fit-real-syst-chi2cnp-free_survival_probability_neutrino_per_fission_factor-constrained_covmat_all.json


printf "%s\n" \
     "Simple statistic fit with combined Neyman-Pearson chi-squared function" \
     "Data type: tsv" \
     "WARNING: make sure that you have data-tsv/ directory" \
     "Monte-Carlo data based on Asimov data (seed = 1)" \
     "Final observation concatenated by detector" \
     "Minimization parameters:" \
     'Free: $\Delta m^2_{32}$, $sin^2 2\theta_{13}$ and $\xi_i, i = \overline{0, 18}$' \
     "where last parameters are parameters of antineutrino spectra shape" \
     "All constrained parameters are used in covariance matrix"

./fits/fit_dayabay_dgm.py \
    --path-data data-root \
    --monte-carlo-mode poisson --seed 1 \
    --concatenation-mode detector \
    --statistic stat.chi2cnp \
    --free-parameters survival_probability neutrino_per_fission_factor \
    --output fit-mc_poisson_1-stat-chi2cnp-free_survival_probability_neutrino_per_fission_factor.yaml
