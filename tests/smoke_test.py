"""
Smoke tests to quickly check the package loads and runs in the most basic way.
"""

import xarray as xr

import isku


def test_basic_projection() -> None:
    """
    Basic test running build_projection_template() with project().
    """
    predictors = xr.Dataset({"foobar": (["idx"], [0, 0, 0])})
    params = xr.Dataset({"ni": (["idx"], [1, 2, 3])})
    expected = xr.Dataset({"impact": (["idx"], [13, 14, 15])})

    def _pre(x: xr.Dataset) -> xr.Dataset:
        out = xr.Dataset()
        out["foobar"] = x["foobar"] + 1
        out["ni"] = x["ni"]
        return out

    def _post(x: xr.Dataset) -> xr.Dataset:
        return x[["impact"]] + 10

    def _model(x: xr.Dataset) -> xr.Dataset:
        return (x["foobar"] * 2 + x["ni"]).to_dataset(name="impact")

    test_impact_model = isku.build_projection_template(
        pre=_pre,
        project=_model,
        post=_post,
    )

    actual = isku.project(xr.merge([predictors, params]), model=test_impact_model)
    xr.testing.assert_allclose(actual, expected)
