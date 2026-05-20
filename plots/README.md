# Plot scripts

These scripts are used to plot fit results in different form: spectrum by detectors/periods, 2 dimensional fit, etc.
File [plots/\_\_init\_\_.py]([plots/__init__.py]) contains useful functions for plotting.

## plot_dayabay_fit_2d.py

The script plots best fit point in 2d plane ($\sin^22\theta_{13}$, $\Delta m^2_{32}$).

It has several options:

- `--input`: `.yaml`-file which contain information about fit values;
- `--output`: where to store output figure;
- `--show`: show figure.

## plot_dayabay_fit_contour.py

- `--chi2map`: `.npz`-file which contains information about 2d $\chi^2$-map;
- `--output`: where to store output figure;
- `--dm32`: use $\Delta m^2_{32}$ as y-axis; if it is not passed, $\Delta m^2_{32}$ will be used;
- `--show`: show figure.

## plot_dayabay_fit_spectra.py

- `--concatenation`, `default="detector_period"`: which granularity of observation will be used: by `detector_period` or `detector`;
- `--data`, `default="asimov"`: choose to which data will be compared fit;
- `--input`: `.yaml`-file which contain information about fit values;
- `--output`: where to store output figures, requires placehoder for the name of detector (two placeholders for detector and period, if `--concatenation detector_period`);
- `--show`: show figure.

## plot_dayabay_fit_spectra_article.py

- `--input`: `.yaml`-file which contain information about fit values;
- `--output`: where to store output figures, requires placehoder for the name of experimental hall;
- `--show`: show figure.
