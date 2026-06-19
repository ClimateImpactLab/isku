# Get Started

## Why use isku?

isku is a minimalist Python + Xarray-based climate impact projection framework for researchers with little time.

### Features

* Define and apply three-step models to project climate effects, impacts, and damages.

* Extract regionalized variables from regularly gridded data, such as downscaled general circulation model output.

* Minimalist.

* Loosely coupled components and protocols for quick scripts with functions or gnarly OOP-heavy applications.

* Designed around [Xarray](https://xarray.dev/) to work with larger-than-memory datasets and distributed computing (dask!), GPUs, TPUs, streaming datasets.

* Great for weird ad hoc projects and researchers that love rechunking big data!

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
