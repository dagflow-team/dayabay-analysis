# Covariance matrix

## covmatrix_mc.py

Script contains procedure of calculation covariance matrix via Monte-Carlo modeling.

### Script options

- `-v`, `--verbose`: verbosity level;
- `--path-data`: path to model data. Default: model will look for data in `./data/` directory;
- `--concatenation-mode`: possible way to concatenate final observation. Supports: `detector`, `detector_period`. Default: `detector_period`;
- `--par`: pair of parameter name and value. Could be used several times to set several parameters in chosen values;
- `--systematic-parameters-groups`, `--cov`: type of Monte-Carlo mode. Supports: `all`, `survival_probability`, `detector`, `reactor`, `background`, `reactor_antineutrino`. You may modify this option to path specific parameters:
  - `all`: contains all constained parameters;
  - `survival_probability`: contains constrained oscillation parameters;
  - `detector`: contains energy resolution, LSNL, IAV, efficiency, and energy scale related parameters;
  - `reactor`: contains nominal thermal power, energy per fission, SNF, non-equilibrium, and fission fraction scale related parameters;
  - `background`: contains background rates parameters;
  - `reactor_antineutrino`: contains Huber-Mueller spectrum uncertainies for each isotope;
- `--seed`: option to fix pseudo-sequance of random values. Default: 0;
- `--asimov-as-mean`: option to apply Asimov data as mean in process of calculation deviations;
- `--alternative`: calculate covariance matrix via matrix approach (much memory-intensive);
- `--num`: number of Monte-Carlo samples for obtaining covariance matrix: Default: 1000;
- `--output`: option to save fit result. Supports: `dat`, `csv`, `hdf5`.
