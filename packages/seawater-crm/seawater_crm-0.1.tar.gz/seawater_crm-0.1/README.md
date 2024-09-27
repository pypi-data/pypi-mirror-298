# seawater_crm

![Tests](https://github.com/mvdh7/seawater_crm/workflows/Tests/badge.svg)
[![PyPI version](https://img.shields.io/pypi/v/seawater_crm.svg?style=popout)](https://pypi.org/project/seawater_crm/)
[![Conda Version](https://img.shields.io/conda/vn/conda-forge/seawater_crm.svg)](https://anaconda.org/conda-forge/seawater_crm)
[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.XXXXXXX-informational)](https://doi.org/10.5281/zenodo.XXXXXXX)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Certified values for seawater reference materials as pandas DataFrames.

## Installation

    pip install seawater_crm
    conda install conda-forge::seawater_crm

## Usage

See module and function docstrings for more detailed information.

### Dickson CO<sub>2</sub> CRMs

```python
    import seawater_crm as swcrm

    # Generate pandas DataFrame containing certified values
    crm = swcrm.dickson.get_crm_batches()

    # Access values for (a) given batch(es)
    batches = [205, 206, 208]
    dic_certified = crm.loc[batches].dic
    alkalinity_certified = crm.loc[batches].alkalinity
```

Nutrient, salinity, bottling date and flag columns are also available in the DataFrame, but the data in the nutrient columns are not yet complete.
