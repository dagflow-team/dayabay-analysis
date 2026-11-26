# Comparison of data with PRL 130, 161802

Article [PRL **130**, 161802](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.130.161802) contains observation of Daya Bay with applied inverse LSNL transformation.

The script [prl_130_161802/script.py](prl_130_161802/script.py) demonstrates how to build inverse LSNL transformation and how to apply it to the final observation of the Daya Bay.
Consistency between PRL data and obtained with script is on 0.25%.

The script works with final histograms and full tree of IBD events.

## How to run

You need to install `dayabay-model` which dependency is listed in the [requirements.txt](requirements.txt) and download full tree of IBD events in `npz`-format from [Zenodo](https://doi.org/10.5281/zenodo.17587229).
Then run following command:
```bash
python prl_130_161802/script.py --path-tree-events 'path/to/dayabay/trees/dayabay_events_{}.npz' -s
```
The script has two options:

- `--path-tree-events`: path to tree of IBD events. Pay attention that it requires placeholder `{}` for detector name and type of files must be `npz`.
- `-s`, or `--show`: show plots with comparison.
