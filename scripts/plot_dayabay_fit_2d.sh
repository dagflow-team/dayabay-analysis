#!/bin/bash

printf "%s\n" \
     "Script for creating simple 2d-plot of Daya Bay fit result" \
     'in terms of $\Delta m^2_{32}$ and $sin^2 2\theta_{13}$'

./plots/plot_dayabay_fit_2d.py \
    --input results/fits/fit-result-stat-example.yaml \
    --show
