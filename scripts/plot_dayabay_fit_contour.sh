#!/bin/bash

printf "%s\n" \
     "Script for creating 2d-plot of Daya Bay fit result with 1/2/3-sigma contours" \
     'in terms of $\Delta m^2_{ee}$ and $sin^2 2\theta_{13}$'

./plots/plot_dayabay_fit_contour.py \
    --chi2map contour.npz \
    --show

printf "%s\n" \
     "Script for creating 2d-plot of Daya Bay fit result with 1/2/3-sigma contours" \
     'in terms of $\Delta m^2_{32}$ and $sin^2 2\theta_{13}$'

./plots/plot_dayabay_fit_contour.py \
    --chi2map contour.npz \
    --dm32 \
    --show
