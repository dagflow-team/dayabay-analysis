This directory contains several configuration files that can override loaded parameters of model. Content of file might be mismatch with name of file.

## configurations/dm31/survival_probability-dm31.yaml

Original file contains two parameters: $`\Delta m^2_{32}`$ and $\sin^22\theta_{13}$. Both parameters are free, it follows from `format`, just `value`, and `state` that equal to `variable`. For demonstration porpouses we left in this file just $`\sin^22\theta_{13}`$.

## configurations/dm31/survival_probability_solar-dm31.yaml

Original file contains only solar parameters: $\Delta m^2_{21}$ and $\sin^22\theta_{12}$. However, we put one more parameter: $\Delta m^2_{31}$. This parameter is not "solar", but we want to use this parameter in model and should put it somewhere.

## load_dayabay_model_dm31.py

Example of running the Daya Bay model which use $`\Delta m^2_{31}`$ as leading parameter (not usual usage for the $`3\nu`$ analysis). It can be done via overriding configurations. To run script you need to execute following line from the root of the project:
```bash
python custom-configurations/load_dayabay_model_dm31.py
```
