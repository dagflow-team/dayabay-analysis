#!/bin/bash

printf "%s\n" \
     "Script for creating spectrum by experimental halls" \
     "Like figure 2 from PRL 130, 161802"

./plots/plot_dayabay_fit_spectra_article.py \
    --input results/fits/fit-real-syst-chi2cnp-free_spectrum_shape-constrained_pull_all.yaml \
    --output results/plots/article-spectra/spectrum-{}.pdf \
    --show
