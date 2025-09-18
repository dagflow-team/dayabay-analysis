MODEL_VERSION=v0e
DATASET=b


echo "Simple statistic only fit with Pearson's chi-squared function"
echo "Asimov data (dataset ${DATASET})"
echo 'Minimization parameters: $\Delta m^2_{32}$ and $sin^2 2\theta_{13}$'

./fits/fit_dayabay.py --version ${MODEL_VERSION} \
  --mo "{dataset: ${DATASET}}" \
  --chi2 stat.chi2p \
  --free-parameters oscprob.DeltaMSq32 oscprob.SinSq2Theta13 \
  --output fit-stat-chi2p-free_oscprob.yaml


echo "Simple statistic+reactor systematic fit with Pearson's chi-squared function"
echo "Asimov data (dataset ${DATASET})"
echo 'Minimization parameters:'
echo 'Free: $\Delta m^2_{32}$ and $sin^2 2\theta_{13}$'
echo 'Constrained:'
echo '- energy resolution: $\sigma_{a}$, $\sigma_{b}$, and $\sigma_{c}$ (3 parameters)'
echo '- LSNL: $\zeta^{i}_{\mathrm{LSNL}}$ (4 parameters)'
echo '- IAV scaling: $\eta^{\mathrm{AD}}_{\mathrm{IAV}}$ (8 parameters)'
echo '- Detector efficiency: $\epsilon^{\mathrm{AD}}$ (8 parameters)'
echo '- Detector energy scale:  $\eta^{\mathrm{AD}}$ (8 parameters)'

./fits/fit_dayabay.py --version ${MODEL_VERSION} \
  --mo "{dataset: ${DATASET}}" \
  --chi2 full.pull.chi2p \
  --free-parameters oscprob \
  --constrained-parameters detector \
  --output fit-syst-chi2p-free_oscprob-constrained_detector.yaml


echo "Simple statistic+all systematic fit with Neyman's chi-squared function"
echo "Observed data (dataset ${DATASET})"
echo 'Minimization parameters:'
echo 'Free: $\Delta m^2_{32}$, $sin^2 2\theta_{13}$ and $\xi_i, i = \overline{0, 18}$'
echo 'where last parametrs are parameters of antineutrino spectra shape'
echo 'All constrained parameters are used in covariance matrix'

./fits/fit_dayabay.py --version ${MODEL_VERSION} \
  --mo "{dataset: ${DATASET}}" \
  --data loaded \
  --chi2 full.covmat.chi2n \
  --free-parameters oscprob neutrino_per_fission_factor \
  --output fit-syst-chi2p-free_oscprob_neutrino_per_fission_factor-constrained_all.yaml


echo "Simple statistic fit with Pearson's unbiased chi-squared function"
echo "Monte-Carlo data based on Asimov data (dataset ${DATASET})"
echo 'Minimization parameters:'
echo 'Free: $\Delta m^2_{32}$, $sin^2 2\theta_{13}$ and $\xi_i, i = \overline{0, 18}$'
echo 'where last parametrs are parameters of antineutrino spectra shape'
echo 'All constrained parameters are used in covariance matrix'

./fits/fit_dayabay.py --version ${MODEL_VERSION} \
  --mo "{dataset: ${DATASET}, monte_carlo_mode: poisson, seed: 1}" \
  --chi2 stat.chi2p_unbiased \
  --free-parameters oscprob neutrino_per_fission_factor \
  --output fit-syst-chi2p_unbiased-free_oscprob_neutrino_per_fission_factor-mc_poisson_1.yaml
