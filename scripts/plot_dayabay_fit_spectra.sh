#!/bin/bash

printf "%s\n" \
     "Script for creating spectrum by detectors" \
     "Ratio of fit data to Asimov (must be flat)" \
     "Outputs are saving in results"

./plots/plot_dayabay_fit_spectra.py \
  --data asimov \
  --input results/fits/fit-asimov-syst-chi2cnp-free_spectrum_shape-constrained_pull_all.yaml \
  --show


printf "%s\n" \
     "Script for creating spectrum by detectors" \
     "Ratio of fit data to real data (should not be flat)" \
     "Outputs are saving in results"

./plots/plot_dayabay_fit_spectra.py \
  --data real \
  --input results/fits/fit-real-syst-chi2cnp-free_spectrum_shape-constrained_pull_all.yaml \
  --show
