#!/bin/bash

./fits/fit_dayabay_dgm_chi2map.py \
    --data real \
    --free-parameters survival_probability neutrino_per_fission_factor \
    --scan-par survival_probability.SinSq2Theta13 0.072 0.098 21 \
    --scan-par survival_probability.DeltaMSq32 2.17e-3 2.77e-3 21 \
    --chi2 full.covmat.chi2cnp \
    --output contour-real-covmat-chi2cnp.npz

./fits/fit_dayabay_dgm_chi2map.py \
    --data real \
    --free-parameters survival_probability neutrino_per_fission_factor \
    --constrained-parameters survival_probability detector reactor background \
    --scan-par survival_probability.SinSq2Theta13 0.072 0.098 21 \
    --scan-par survival_probability.DeltaMSq32 2.17e-3 2.77e-3 21 \
    --chi2 full.covmat.chi2cnp \
    --output contour-real-pull-chi2cnp.npz
