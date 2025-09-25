#!/bin/bash

printf "%s\n" \
     "Simple statistic only fit with Pearson's chi-squared function" \
     "Data type: determines from data/ content" \
     "WARNING: make sure that you have data/ directory" \
     "Asimov data" \
     "Final observation concatenated by detector and period" \
     'Minimization parameters: $\Delta m^2_{32}$ and $sin^2 2\theta_{13}$'

./fits/fit_dayabay_dgm.py \
    --statistic stat.chi2p \
    --free-parameters survival_probability.DeltaMSq32 survival_probability.SinSq2Theta13 \
    --output fit-stat-chi2p-free_survival_probability.yaml


printf "%s" \
     "Simple statistic+reactor systematic fit with Pearson's chi-squared function" \
     "Data type: root" \
     "WARNING: make sure that you have data-root/ directory" \
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
     --statistic full.pull.chi2p \
     --concatenation-mode detector \
     --free-parameters survival_probability \
     --constrained-parameters detector \
     --output fit-syst-chi2p-free_survival_probability-constrained_detector.json


printf "%s\n" \
     "Simple statistic+all systematic fit with Neyman's chi-squared function" \
     "Data type: determines from data/ content" \
     "WARNING: make sure that you have data/ directory" \
     "Observed data" \
     "Final observation concatenated by detector and period" \
     "Minimization parameters:" \
     'Free: $\Delta m^2_{32}$, $sin^2 2\theta_{13}$ and $\xi_i, i = \overline{0, 18}$' \
     "where last parameters are parameters of antineutrino spectra shape" \
     "All constrained parameters are used in covariance matrix"

./fits/fit_dayabay_dgm.py \
    --data loaded \
    --statistic full.covmat.chi2n \
    --free-parameters survival_probability neutrino_per_fission_factor \
    --output fit-syst-chi2n-free_survival_probability_neutrino_per_fission_factor-constrained_covmat_all.pickle


printf "%s\n" \
     "Simple statistic fit with Pearson's unbiased chi-squared function" \
     "Data type: tsv" \
     "WARNING: make sure that you have data-tsv/ directory" \
     "Monte-Carlo data based on Asimov data (seed = 1)" \
     "Final observation concatenated by detector" \
     "Minimization parameters:" \
     'Free: $\Delta m^2_{32}$, $sin^2 2\theta_{13}$ and $\xi_i, i = \overline{0, 18}$' \
     "where last parameters are parameters of antineutrino spectra shape" \
     "All constrained parameters are used in covariance matrix"

ipython3 --pdb -- ./fits/fit_dayabay_dgm.py \
    --path-data data-tsv \
    --monte-carlo-mode poisson --seed 1 \
    --concatenation-mode detector \
    --statistic stat.chi2p_unbiased \
    --free-parameters survival_probability neutrino_per_fission_factor \
    --output fit-syst-chi2p_unbiased-free_survival_probability_neutrino_per_fission_factor-mc_poisson_1.yaml
