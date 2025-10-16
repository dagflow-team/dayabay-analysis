#!/bin/bash

./fits/fit_dayabay_dgm_chi2map.py \
    --free-parameters survival_probability neutrino_per_fission_factor \
    --scan-par survival_probability.SinSq2Theta13 0.072 0.098 15 \
    --scan-par survival_probability.DeltaMSq32 2.22e-3 2.82e-3 15 \
    --chi2 full.covmat.chi2cnp \
    --output contour.npz
