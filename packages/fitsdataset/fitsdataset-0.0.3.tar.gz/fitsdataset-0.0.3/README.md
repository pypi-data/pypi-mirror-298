FITSDataset
===
[![PyPI version](https://badge.fury.io/py/fitsdataset.svg)](https://badge.fury.io/py/fitsdataset) ![PyPI - Downloads](https://img.shields.io/pypi/dm/fitsdataset?color=%23)

This package contains a custom PyTorch Dataset for quick and easy training on FITS files, commonly used in astronomical data analysis. In particular, the `FITSDataset` class caches FITS files as PyTorch tensors for the purpose of increasing training speed.

Contributions and feedback are welcome; please open a pull request or an issue.

## Quickstart
Using Python 3.6+, install from source with
```bash
pip install fitsdataset
```

Create a toy dataset with samples from the
[Hyper Suprime-Cam survey](https://www.naoj.org/Projects/HSC/) with:
```python
>>> from fitsdataset import FITSDataset
>>> dataset = FITSDataset("path/to/examples/hsc/", size=101, label_col="target")
```

Notice that the cached tensors appear in `path/to/examples/hsc/tensors`.

## Preparing a dataset
Prepare your own FITS dataset by creating the following directory structure:
```
path/to/data/
  info.csv
  cutouts/
    img1.fits
    img2.fits
    ...
```
where `info.csv` has a filename column (basename) and a prediction target column. See [here](https://github.com/amritrau/fitsdataset/blob/master/examples/hsc/info.csv) for an example.

## Documentation
```python
>>> from fitsdataset import FITSDataset
>>> help(FITSDataset)
```
