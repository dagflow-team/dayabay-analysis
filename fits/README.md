# Fit scripts

Each script contain possible ways to fit Daya Bay model to Asimov/observed/Monte-Carlo data.

Custom functions are located in [\_\_init\_\_.py](fits/__init__.py) file.

## fit_dayabay_dgm.py

Script provides fit procedure within framework.

It has several options:

- `-v`, `--verbose`: verbosity level;
- `--path-data`: path to model data. Default: model will look for data in `./data/` directory;
- `--par`: pair of parameter name and value. Could be used several times to set several parameters in chosen values;
- `--monte-carlo-mode`: type of Monte-Carlo mode. Supports: `asimov`, `normal-stats`, `poisson`. Default: `asimov`. Possible parameters mean:
  - `asimov`: do not do any Monte-Carlo procedure. Just observation under assumption of average parameters;
  - `normal-stats`: do Monte-Carlo of constrained parameters within Normal distribution $\mathcal{N}(0, 1)$. After that new new values will be pushed to model and statistical variation to every bin observation is applied;
  - `poisson`: do Monte-Carlo variation of each bin observation via Poisson distribution $\mathrm{Poisson}(N)$, where $N$ number of events in the bin.
- `--seed`: option to fix pseudo-sequance of random values. Default: 0. Useful for Monte-Carlo modeling;
- `--concatenation-mode`: possible way to concatenate final observation. Supports: `detector`, `detector_period`. Default: `detector_period`;
- `--data`: option to switch between Asimov (Monte-Carlo) and real final observation. Default: Asimov (Monte-Carlo) observation;
- `--constrain-osc-parameters`: constrain oscillation parameters. Might be useful, if minimization procedure fails within non-physical values of $\sin^22\theta_{13}$ or $\Delta m^2_{32}$. After fit with limited oscillation parameters, fit with free oscillation parameters is produced;
- `--profile-parameters`: option provides profiling of minimizable parameters within Minos algorithm;
- `--statistic`: type of chi-squared statistic to be minimized. Supports: `stat.chi2p_iterative`, `stat.chi2n`, `stat.chi2p`, `stat.chi2cnp`, `stat.chi2p_unbiased`, `stat.chi2poisson`, `full.covmat.chi2p_iterative`, `full.covmat.chi2n`, `full.covmat.chi2p`, `full.covmat.chi2p_unbiased`, `full.covmat.chi2cnp`, `full.covmat.chi2cnp_alt`, `full.pull.chi2p_iterative`, `full.pull.chi2p`, `full.pull.chi2cnp`, `full.pull.chi2p_unbiased`, `full.pull.chi2poisson`. Default: `full.pull.chi2cnp`. Quick note about naming:
  - `stat`: referes to chi-squared function that **do not** include pull-terms on constrained parameters;
  - `full.pull`: referes to chi-squared function that include pull-terms on constrained parameters;
  - `full.covmat`: referes to chi-squared function that include constrained parameters via covariance matrix approach;
  - `chi2n`: Neyman's definition of chi-squared function;
  - `chi2p`: Pearson's definition of chi-squared function;
  - `chi2cnp`: combined Neyman-Pearson's definition of chi-squared function;
  - `chi2p_unbiased`: Pearson's definition of chi-squared function with addition logarithm of #FIXME;
  - `chi2poisson`: chi-squared function based on Poisson distribution;
  - `full.covmat.chi2p_iterative`: Pearson's chi-squared function with covariance matrix. Statistical errors are frozen. Could be used in iterative fit procedure;
  - `full.covmat.chi2cnp`: combined Neyman-Pearson's chi-squared as sum of Neyman's chi-squared with covariance matrix and Pearson's chi-squared with covariance matrix;
  - `full.covmat.chi2cnp_alt`: combined Neyman-Pearson's chi-squared from [the paper](https://arxiv.org/pdf/1903.07185) (formula 18);
- `--n-iterations`: number of repeats of fit procedure. Useful for **iterative** statistics;
- `--free-parameters`: list of namespaces of free parameters or full name of free parameters;
- `--constrained-parameters`: list of namespaces of constrained parameters or full name of constrained parameters;
- `--output`: option to save fit result. Supports: `json`, `yaml`, `pickle`.

## fit_dayabay_iminuit_asimov.py

Script provides fit procedure to Asimov data within iminuit package.

It has several options:

- `--path-data`: path to model data. Default: model will look for data in `./data/` directory;
- `--concatenation-mode`: possible way to concatenate final observation. Supports: `detector`, `detector_period`. Default: `detector_period`;
- `--statistic`: type of chi-squared statistic to be minimized. Supports: `stat.chi2p_iterative`, `stat.chi2n`, `stat.chi2p`, `stat.chi2cnp`, `stat.chi2p_unbiased`, `stat.chi2poisson`, `full.covmat.chi2p_iterative`, `full.covmat.chi2n`, `full.covmat.chi2p`, `full.covmat.chi2p_unbiased`, `full.covmat.chi2cnp`, `full.covmat.chi2cnp_alt`, `full.pull.chi2p_iterative`, `full.pull.chi2p`, `full.pull.chi2cnp`, `full.pull.chi2p_unbiased`, `full.pull.chi2poisson`. Default: `full.pull.chi2cnp`. Quick note about naming:
  - `stat`: referes to chi-squared function that **do not** include pull-terms on constrained parameters;
  - `full.pull`: referes to chi-squared function that include pull-terms on constrained parameters;
  - `full.covmat`: referes to chi-squared function that include constrained parameters via covariance matrix approach;
  - `chi2n`: Neyman's definition of chi-squared function;
  - `chi2p`: Pearson's definition of chi-squared function;
  - `chi2cnp`: combined Neyman-Pearson's definition of chi-squared function;
  - `chi2p_unbiased`: Pearson's definition of chi-squared function with addition logarithm of #FIXME;
  - `chi2poisson`: chi-squared function based on Poisson distribution;
  - `full.covmat.chi2p_iterative`: Pearson's chi-squared function with covariance matrix. Statistical errors are frozen. Could be used in iterative fit procedure;
  - `full.covmat.chi2cnp`: combined Neyman-Pearson's chi-squared as sum of Neyman's chi-squared with covariance matrix and Pearson's chi-squared with covariance matrix;
  - `full.covmat.chi2cnp_alt`: combined Neyman-Pearson's chi-squared from [the paper](https://arxiv.org/pdf/1903.07185) (formula 18);
- `--free-spectrum-shape`: add parameters of anineutrino spectrum shape variation as free parameters. Otherwise, the scale parameter on IBD part of observation will be used ($N^{\rm global}$ - global normalization);
- `--use-hubber-mueller-spectral-uncertainties`: add parameters of Huber-Mueller uncertainties for each isotope. **Warning**: it contains 900+ parameters, so fit procedure will take a long time;
- `--output`: option to save fit result. Supports: `json`, `yaml`, `pickle`.

## fit_dayabay_iminuit_data.py

Script provides fit procedure to observed data within iminuit package.

It has several options:

- `--path-data`: path to model data. Default: model will look for data in `./data/` directory;
- `--concatenation-mode`: possible way to concatenate final observation. Supports: `detector`, `detector_period`. Default: `detector_period`;
- `--statistic`: type of chi-squared statistic to be minimized. Supports: `stat.chi2p_iterative`, `stat.chi2n`, `stat.chi2p`, `stat.chi2cnp`, `stat.chi2p_unbiased`, `stat.chi2poisson`, `full.covmat.chi2p_iterative`, `full.covmat.chi2n`, `full.covmat.chi2p`, `full.covmat.chi2p_unbiased`, `full.covmat.chi2cnp`, `full.covmat.chi2cnp_alt`, `full.pull.chi2p_iterative`, `full.pull.chi2p`, `full.pull.chi2cnp`, `full.pull.chi2p_unbiased`, `full.pull.chi2poisson`. Default: `full.pull.chi2cnp`. Quick note about naming:
  - `stat`: referes to chi-squared function that **do not** include pull-terms on constrained parameters;
  - `full.pull`: referes to chi-squared function that include pull-terms on constrained parameters;
  - `full.covmat`: referes to chi-squared function that include constrained parameters via covariance matrix approach;
  - `chi2n`: Neyman's definition of chi-squared function;
  - `chi2p`: Pearson's definition of chi-squared function;
  - `chi2cnp`: combined Neyman-Pearson's definition of chi-squared function;
  - `chi2p_unbiased`: Pearson's definition of chi-squared function with addition logarithm of #FIXME;
  - `chi2poisson`: chi-squared function based on Poisson distribution;
  - `full.covmat.chi2p_iterative`: Pearson's chi-squared function with covariance matrix. Statistical errors are frozen. Could be used in iterative fit procedure;
  - `full.covmat.chi2cnp`: combined Neyman-Pearson's chi-squared as sum of Neyman's chi-squared with covariance matrix and Pearson's chi-squared with covariance matrix;
  - `full.covmat.chi2cnp_alt`: combined Neyman-Pearson's chi-squared from [the paper](https://arxiv.org/pdf/1903.07185) (formula 18);
- `--free-spectrum-shape`: add parameters of anineutrino spectrum shape variation as free parameters. Otherwise, the scale parameter on IBD part of observation will be used ($N^{\rm global}$ - global normalization);
- `--use-hubber-mueller-spectral-uncertainties`: add parameters of Huber-Mueller uncertainties for each isotope. **Warning**: it contains 900+ parameters, so fit procedure will take a long time;
- `--output`: option to save fit result. Supports: `json`, `yaml`, `pickle`.

## fit_dayabay_iminuit_monte_carlo.py

Script provides fit procedure to Monte-Carlo data within iminuit package.

It has several options:

- `--path-data`: path to model data. Default: model will look for data in `./data/` directory;
- `--concatenation-mode`: possible way to concatenate final observation. Supports: `detector`, `detector_period`. Default: `detector_period`;
- `--monte-carlo-mode`: type of Monte-Carlo mode. Supports: `asimov`, `normal-stats`, `poisson`. Default: `poisson`. Possible parameters mean:
  - `normal-stats`: do Monte-Carlo of constrained parameters within Normal distribution $\mathcal{N}(0, 1)$. After that new new values will be pushed to model and statistical variation to every bin observation is applied;
  - `poisson`: do Monte-Carlo variation of each bin observation via Poisson distribution $\mathrm{Poisson}(N)$, where $N$ number of events in the bin.
- `--seed`: option to fix pseudo-sequance of random values. Default: 0. Useful for Monte-Carlo modeling;
- `--statistic`: type of chi-squared statistic to be minimized. Supports: `stat.chi2p_iterative`, `stat.chi2n`, `stat.chi2p`, `stat.chi2cnp`, `stat.chi2p_unbiased`, `stat.chi2poisson`, `full.covmat.chi2p_iterative`, `full.covmat.chi2n`, `full.covmat.chi2p`, `full.covmat.chi2p_unbiased`, `full.covmat.chi2cnp`, `full.covmat.chi2cnp_alt`, `full.pull.chi2p_iterative`, `full.pull.chi2p`, `full.pull.chi2cnp`, `full.pull.chi2p_unbiased`, `full.pull.chi2poisson`. Default: `full.pull.chi2cnp`. Quick note about naming:
  - `stat`: referes to chi-squared function that **do not** include pull-terms on constrained parameters;
  - `full.pull`: referes to chi-squared function that include pull-terms on constrained parameters;
  - `full.covmat`: referes to chi-squared function that include constrained parameters via covariance matrix approach;
  - `chi2n`: Neyman's definition of chi-squared function;
  - `chi2p`: Pearson's definition of chi-squared function;
  - `chi2cnp`: combined Neyman-Pearson's definition of chi-squared function;
  - `chi2p_unbiased`: Pearson's definition of chi-squared function with addition logarithm of #FIXME;
  - `chi2poisson`: chi-squared function based on Poisson distribution;
  - `full.covmat.chi2p_iterative`: Pearson's chi-squared function with covariance matrix. Statistical errors are frozen. Could be used in iterative fit procedure;
  - `full.covmat.chi2cnp`: combined Neyman-Pearson's chi-squared as sum of Neyman's chi-squared with covariance matrix and Pearson's chi-squared with covariance matrix;
  - `full.covmat.chi2cnp_alt`: combined Neyman-Pearson's chi-squared from [the paper](https://arxiv.org/pdf/1903.07185) (formula 18);
- `--free-spectrum-shape`: add parameters of anineutrino spectrum shape variation as free parameters. Otherwise, the scale parameter on IBD part of observation will be used ($N^{\rm global}$ - global normalization);
- `--use-hubber-mueller-spectral-uncertainties`: add parameters of Huber-Mueller uncertainties for each isotope. **Warning**: it contains 900+ parameters, so fit procedure will take a long time;
- `--output`: option to save fit result. Supports: `json`, `yaml`, `pickle`.
