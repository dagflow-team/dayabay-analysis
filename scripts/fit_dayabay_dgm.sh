#!/bin/bash

echo "Simple statistic only fit with Pearson's chi-squared function\n" \
     "Asimov data\n" \
     "Final observation concatenated by detector and period\n" \
     'Minimization parameters: $\Delta m^2_{32}$ and $sin^2 2\theta_{13}$'

./fits/fit_dayabay_dgm.py \
  --chi2 stat.chi2p \
  --free-parameters survival_probability.DeltaMSq32 survival_probability.SinSq2Theta13 \
  --output fit-stat-chi2p-free_survival_probability.yaml


echo "Simple statistic+reactor systematic fit with Pearson's chi-squared function\n" \
     "Asimov data\n" \
     "Final observation concatenated by detector\n" \
     "Minimization parameters:\n" \
     'Free: $\Delta m^2_{32}$ and $sin^2 2\theta_{13}$' "\n" \
     "Constrained:\n" \
     '- energy resolution: $\sigma_{a}$, $\sigma_{b}$, and $\sigma_{c}$ (3 parameters)' "\n" \
     '- LSNL: $\zeta^{i}_{\mathrm{LSNL}}$ (4 parameters)' "\n" \
     '- IAV scaling: $\eta^{\mathrm{AD}}_{\mathrm{IAV}}$ (8 parameters)' "\n" \
     '- Detector efficiency: $\epsilon^{\mathrm{AD}}$ (8 parameters)' "\n" \
     '- Detector energy scale:  $\eta^{\mathrm{AD}}$ (8 parameters)'

./fits/fit_dayabay_dgm.py \
  --chi2 full.pull.chi2p \
  --concatenation-mode detector \
  --free-parameters survival_probability \
  --constrained-parameters detector \
  --output fit-syst-chi2p-free_survival_probability-constrained_detector.yaml


echo "Simple statistic+all systematic fit with Neyman's chi-squared function\n" \
     "Observed data\n" \
     "Final observation concatenated by detector and period\n" \
     "Minimization parameters:\n" \
     'Free: $\Delta m^2_{32}$, $sin^2 2\theta_{13}$ and $\xi_i, i = \overline{0, 18}$' "\n" \
     "where last parameters are parameters of antineutrino spectra shape\n" \
     "All constrained parameters are used in covariance matrix"

./fits/fit_dayabay_dgm.py \
  --data loaded \
  --chi2 full.covmat.chi2n \
  --free-parameters survival_probability neutrino_per_fission_factor \
  --output fit-syst-chi2p-free_survival_probability_neutrino_per_fission_factor-constrained_all.yaml


echo "Simple statistic fit with Pearson's unbiased chi-squared function\n" \
     "Monte-Carlo data based on Asimov data\n" \
     "Final observation concatenated by detector\n" \
     "Minimization parameters:\n" \
     'Free: $\Delta m^2_{32}$, $sin^2 2\theta_{13}$ and $\xi_i, i = \overline{0, 18}$' "\n" \
     "where last parameters are parameters of antineutrino spectra shape\n" \
     "All constrained parameters are used in covariance matrix"

./fits/fit_dayabay_dgm.py \
  --monte-carlo-mode poisson --seed 1 \
  --concatenation-mode detector \
  --chi2 stat.chi2p_unbiased \
  --free-parameters survival_probability neutrino_per_fission_factor \
  --output fit-syst-chi2p_unbiased-free_survival_probability_neutrino_per_fission_factor-mc_poisson_1.yaml
