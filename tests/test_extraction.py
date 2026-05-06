"""
Test isku extraction logic.
"""

import numpy as np
import xarray as xr

import isku


def test_extract_regions():
    """
    Create simple extraction workflow and test basic region extraction.
    """
    input_ds = xr.Dataset({"variable1": (["idx"], [0, 0, 0])})
    expected = xr.Dataset({"variable1": (["idx"], [13.5, 13.5, 13.5])})

    # Each of the transformation steps should add to the variable.
    # We'll know something basic is off if it doesn't add to `expected`.
    def _pre(x):
        return x[["variable1"]] + 1

    def _post(x):
        return x[["variable1"]] + 10

    test_transform = isku.build_extraction_workflow(pre=_pre, post=_post)

    class FakeRegionalization(isku.RegionExtractor):
        """
        Toy implementation of the RegionExtractor protocol
        """

        def extract_regions(self, ds):
            return ds[["variable1"]] + 2.5

    output = isku.extract_regions(
        input_ds,
        workflow=test_transform,
        regions=FakeRegionalization(),
    )

    xr.testing.assert_allclose(output, expected)


def test_gridweightingregions_region_extraction():
    """
    Basic test calling GridWeightingRegions for regionalization with the RegionExtractor protocol.
    """
    # Define some basics so we can instantiate weights and data
    # to regionalize.
    da = xr.DataArray(
        np.arange(25).reshape([5, 5]),
        dims=("lon", "lat"),
        coords={
            "lon": np.arange(5),
            "lat": np.arange(5),
        },
        name="variable1",
    )
    w = xr.Dataset(
        {
            "region": (["idx"], ["a", "a", "a", "b"]),
            "weight": (["idx"], [0.3, 0.3, 0.3, 1.0]),
            "lon": (["idx"], [2, 3, 4, 1]),
            "lat": (["idx"], [0, 0, 0, 2]),
        },
    )

    expected = xr.DataArray(
        np.array([13.5, 7.0]),
        dims="region",
        coords={
            "region": ["a", "b"],
        },
        name="variable1",
    ).to_dataset()

    w = isku.GridWeightingRegions(w)
    actual = w.extract_regions(da.to_dataset())

    xr.testing.assert_allclose(actual, expected)


def test_gridweightingregions_extract_regions_with_extradim():
    """
    Basic GridWeightingRegions regionalization test, but if input data has extra time dim.
    """
    # Define inputs so we can instantiate weights and have data to regionalize.
    # Giving da extra time dim...
    da = xr.DataArray(
        np.arange(125).reshape([5, 5, 5]),
        dims=("lon", "lat", "time"),
        coords={
            "lon": np.arange(5),
            "lat": np.arange(5),
            "time": np.arange(5),
        },
        name="variable1",
    )
    w = xr.Dataset(
        {
            "region": (["idx"], ["a", "a", "a", "b"]),
            "weight": (["idx"], [0.3, 0.6, 0.3, 1.0]),
            "lon": (["idx"], [2, 3, 4, 1]),
            "lat": (["idx"], [0, 0, 0, 2]),
        },
    )

    expected = xr.DataArray(
        np.array([[90.0, 91.2, 92.4, 93.6, 94.8], [35.0, 36.0, 37.0, 38.0, 39.0]]),
        dims=("region", "time"),
        coords={
            "region": ["a", "b"],
            "time": np.arange(5),
        },
        name="variable1",
    ).to_dataset()

    weights = isku.GridWeightingRegions(w)
    actual = weights.extract_regions(da.to_dataset())

    xr.testing.assert_allclose(actual, expected)
