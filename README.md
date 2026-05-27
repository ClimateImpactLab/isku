# isku

[![python-test](https://github.com/climateimpactlab/isku/actions/workflows/python-test.yaml/badge.svg)](https://github.com/climateimpactlab/isku/actions/workflows/python-test.yaml)
[![codecov](https://codecov.io/gh/climateimpactlab/isku/graph/badge.svg?token=G53WDRL97C)](https://codecov.io/gh/climateimpactlab/isku)
[![Documentation](https://github.com/climateimpactlab/isku/actions/workflows/docs.yml/badge.svg)](https://github.com/climateimpactlab/isku/actions/workflows/docs.yml)

Minimalist Python + Xarray-based climate impact projection framework for researchers with little time.

> [!WARNING]
> This package is in early development. It is likely to change in breaking ways.

## Features

* Define and apply three-step models to project climate effects, impacts, and damages.

* Extract regionalized variables from regularly gridded data, such as downscaled general circulation model output.

* Minimalist.

* Loosely coupled components and protocols for quick scripts with functions or gnarly OOP-heavy applications.

* Designed around [Xarray](https://xarray.dev/) to work with larger-than-memory datasets and distributed computing (dask!), GPUs, TPUs, streaming datasets.

* Great for weird ad hoc projects and researchers that love rechunking big data!

## Example

### Projection

Projecting data with a model in `isku` is similar to the preprocess/predict/postprocess workflow you might already be familar with.

In `isku`, we could do a linear model with pre/post-processing like:

```python
import isku

import numpy as np
import xarray as xr

# Some toy input data to work with.
input_data = xr.Dataset(
    {
        "coef": (["region"], [0, 0, 0]),
        "tas": (["region"], [1, 2, 3]),
    }
)

# Define a basic workflow for the projection model, pre/post-processing steps.
def _preprocess(ds):
    my_coef = ds["coef"] + 1
    my_tas = ds["tas"]
    return xr.Dataset({"coef": my_coef, "tas": my_tas})


def _linear_impact_model(ds):
    y = ds["coef"] * 2 + ds["tas"]
    return xr.Dataset({"impact": y})


def _postprocess(ds):
    return ds[["impact"]] + 10


test_impact_model = isku.build_projection_template(
    pre=_preprocess,
    project=_linear_impact_model,
    post=_postprocess,
)

# Put it together and run the projection.
projected = isku.project(input_data, model=test_impact_model)
```

This example uses pure functions to define workflow, or template, steps. This can be useful for quick analysis but `isku` also accepts
custom objects adhering to the select protocols. The intent is that components can be quickly used, ignored, extended or
replaced as needed by a project.

### Extracting regions

The relationship between data transformations and region extraction can be complex in impact and damage research.

Say you have temperature data on a regular latitude-longitude grid. You need to extract regions from this grid, e.g.
political boundaries, but you need to weight each temperature grid point by the proportion of the region's population
exposed to temperature within each region. To make matters more complex you likely need to be specific about additional processing and transformation
before and after regionalization. This is a niche case but a common headache.

We can handle this type of transformation in `isku` like:

```python
import isku

import numpy as np
import xarray as xr


# Define some toy data to transform and regionalize.
gridded_data = xr.DataArray(
    np.arange(25).reshape([5, 5]),
    dims=("lon", "lat"),
    coords={
        "lon": np.arange(5),
        "lat": np.arange(5),
    },
    name="variable1",
).to_dataset()

# Refine regions and how they weight each grid point in the gridded data.
# This is usually read from file, but we're making up a quick example dataset.
my_regions = isku.GridWeightingRegions(
    xr.Dataset(
        {
            "region": (["idx"], ["a", "a", "a", "b"]),
            "weight": (["idx"], [0.3, 0.3, 0.3, 1.0]),
            "lon": (["idx"], [2, 3, 4, 1]),
            "lat": (["idx"], [0, 0, 0, 2]),
        },
    )
)

# Define workflow with pre/post regionalization transformations.
def _add_one(ds):
    return ds[["variable1"]] + 1


def _add_ten(ds):
    return ds[["variable1"]] + 10


my_extraction_workflow = isku.build_extraction_template(
    pre=_add_one,  # Before regionalization.
    post=_add_ten,  # After regionalization.
)


# Put it all together to extract regions from gridded data.
transformed = isku.extract_regions(
    gridded_data,
    template=my_extraction_workflow,
    regions=my_regions,
)
```


## Installation

isku is a Python package [available for download from PyPI](https://pypi.org/project/isku/).

Using `pip` you can install this package with

```
pip install isku
```

best practice suggest installing the package into a virtual environment.

For a `uv` project this is

```
uv add isku
```

Install the unreleased and unstable bleeding-edge version of the package with:

```shell
pip install git+https://github.com/climateimpactlab/isku
```

using `pip` or with a project in `uv`, do

```shell
uv add git+https://github.com/climateimpactlab/isku
```

## Is this any good?

Yes.

## Support

`isku` is open-source software made available under the terms of either the MIT License or the Apache License 2.0, at your option.

Ask questions about usage or general discussion on the project's [discussion page](https://github.com/ClimateImpactLab/isku/discussions).

Please file issues and bugs in the project's [issue tracker](https://github.com/ClimateImpactLab/isku/issues).

Please see the [contributing guide](https://github.com/ClimateImpactLab/isku/blob/main/CONTRIBUTING.md) if you would like to contribute.

Changes for each release are summarized in [the changelog](https://github.com/ClimateImpactLab/isku/blob/main/CHANGELOG.md).
