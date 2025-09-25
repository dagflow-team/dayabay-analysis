#!/bin/bash

echo "Simple statistic+all systematic fit with Neyman's chi-squared function\n" \
     "Asimov observation\n" \
     "Minimization parameters:\n" \
     'Free: $\Delta m^2_{32}$, $sin^2 2\theta_{13}$ and $\xi_i, i = \overline{0, 18}$' "\n" \
     "where last parameters are parameters of antineutrino spectra shape\n" \
     "All constrained parameters are used in covariance matrix"

./fits/fit_dayabay_iminuit_asimov.py \
  --chi2 full.covmat.chi2n \
  --free-spectrum-shape


echo "Simple statistic+all systematic fit with Pearson's chi-squared function\n" \
     "Asimov observation\n" \
     "Minimization parameters:\n" \
     'Free: $\Delta m^2_{32}$, $sin^2 2\theta_{13}$ and $N^{\rm global}$' "\n" \
     "where the last parameter scales observed IBD spectrum in each detector\n" \
     "simultaneously\n" \
     "All constrained parameters are included as pull terms\n" \
     "Uncertainties for spectral parameters are not included"

./fits/fit_dayabay_iminuit_asimov.py \
  --chi2 full.pull.chi2p
