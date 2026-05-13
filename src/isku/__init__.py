from collections.abc import Callable
from dataclasses import dataclass
from typing import Protocol

import xarray as xr

__all__ = [
    "ExtractionWorkflow",
    "GridWeightingRegions",
    "ProjectionWorkflow",
    "RegionExtractor",
    "build_extraction_workflow",
    "build_projection_workflow",
    "extract_regions",
    "project",
]


class ExtractionWorkflow(Protocol):
    """
    Template for pre and post region extraction transformation

    See Also
    --------
    build_extraction_workflow: Quickly build extraction workflow from functions for regionalization with pre/post transformations.
    extract_regions: Apply a workflow to extract a new regionalized dataset from gridded data.
    RegionExtractor: Protocol for regionalizing, or extracting regions from a dataset.
    """

    def pre_extract(self, ds: xr.Dataset) -> xr.Dataset:
        """
        Transform dataset before region extraction
        """
        ...

    def post_extract(self, ds: xr.Dataset) -> xr.Dataset:
        """
        Transform dataset after region extraction
        """
        ...


class RegionExtractor(Protocol):
    """
    Protocol for extracting regions from gridded data

    See Also
    --------
    extract_regions: Apply a workflow to extract a new regionalized dataset from gridded data with pre/post transformations.
    ExtractionWorkflow: Technical protocol for a workflow with pre/post regionalization transformations.
    """

    def extract_regions(self, ds: xr.Dataset) -> xr.Dataset:
        """
        Extract and aggregate gridded dataset points into regionalized dataset
        """
        ...


# This dataclass is a quick and simple way to get a concrete instance of the protocol.
@dataclass(frozen=True)
class _SimpleExtractionWorkflow(ExtractionWorkflow):
    pre_extract: Callable[[xr.Dataset], xr.Dataset]
    post_extract: Callable[[xr.Dataset], xr.Dataset]


def build_extraction_workflow(
    *, pre: Callable[[xr.Dataset], xr.Dataset], post: Callable[[xr.Dataset], xr.Dataset]
) -> ExtractionWorkflow:
    """
    Build a workflow of tranformation steps applied to input gridded data, pre/post regionalization, to create a derived variable as output

    This function is a quick and simple way to build an ExtractionWorkflow from two simple functions.

    These steps should be general. They may contain logic for sanity checks
    on inputs and outputs, calculating derived variables and climate indices,
    adding or checking metadata or units. Avoid including logic for cleaning,
    or harmonizing input data, especially if it is specific to a single
    project's usecase. Generally avoid using a single strategy to output
    multiple unrelated variables.

    See Also
    --------
    extract_regions: Apply a workflow to extract a new regionalized dataset from gridded data.
    build_extraction_workflow: Quickly build extraction workflow from functions for regionalization.
    ExtractionWorkflow: The underlaying protocol for a workflow that extracts a regionalized dataset.
    """
    return _SimpleExtractionWorkflow(pre_extract=pre, post_extract=post)


# Use class for segment weights because we're making assumptions/enforcements about the weight data's content and interactions...
class GridWeightingRegions(RegionExtractor):
    """
    Regions that can be extracted from regularly-gridded data after weighting grid points

    'weights' dataset must have "lat", "lon", "weight", "region".

    Raises
    ------
    ValueError
        If 'weights' is missing "lat", "lon", "weight" or "region" variables.

    See Also
    --------
    extract_regions: Use SegmentWeights in a workflow to extract new regionalized dataset.
    build_extraction_workflow: Quickly build extraction workflow from functions for regionalization.
    RegionExtractor: Protocol for regionalizing, or extracting regions from a dataset.
    """

    def __init__(self, weights: xr.Dataset):
        target_variables = ("lat", "lon", "weight", "region")
        missing_variables = [v for v in target_variables if v not in weights.variables]
        if missing_variables:
            raise ValueError(
                f"input weights is missing required {missing_variables} variable(s)"
            )
        self._data = weights

    def extract_regions(self, ds: xr.Dataset) -> xr.Dataset:
        """
        Regionalize input gridded data after multiplying 'ds' by weights and summing the product within each region.

        'ds' must have "lat", "lon" coordinates exactly matching "lat", "lon" in weights.
        """
        # TODO: See how this errors in different common scenarios. What happens on the
        #  unhappy path?
        region_sel = ds.sel(lat=self._data["lat"], lon=self._data["lon"])
        out = (region_sel * self._data["weight"]).groupby(self._data["region"]).sum()
        # TODO: Maybe drop lat/lon and set 'region' as dim/coord? I feel like we can do
        #  this because we're asking weights to strictly match input's lat/lon. Maybe
        #  make this a req of segment weights we're reading in?
        return out


def extract_regions(
    ds: xr.Dataset, *, workflow: ExtractionWorkflow, regions: RegionExtractor
) -> xr.Dataset:
    """
    Use transformations in 'workflow' to extract 'regions' from gridded dataset, 'ds', returning a regionalized dataset

    This function specifically does not just regionalize through zonal aggregation. It uses 'workflow' to apply pre/post regionalization transformations to create new datasets and variables.

    See Also
    --------
    build_extraction_workflow: Quickly build extraction workflow from functions for regionalization.
    """
    return workflow.post_extract(regions.extract_regions(workflow.pre_extract(ds)))


class ProjectionWorkflow(Protocol):
    """
    Template for projecting a model with pre and post processing.

    See Also
    --------
    build_projection_workflow: Build a projection workflow from simple functions.
    """

    def pre_project(self, d: xr.Dataset) -> xr.Dataset:
        """
        Pre-process a dataset before projection
        """
        ...

    def project(self, d: xr.Dataset) -> xr.Dataset:
        """
        Create a projection from a dataset
        """
        ...

    def post_project(self, d: xr.Dataset) -> xr.Dataset:
        """
        Process a projected dataset
        """
        ...


# This dataclass is a quick and simple way to get a concrete instance of the protocol.
@dataclass(frozen=True)
class _SimpleProjectionWorkflow(ProjectionWorkflow):
    pre_project: Callable[[xr.Dataset], xr.Dataset]
    project: Callable[[xr.Dataset], xr.Dataset]
    post_project: Callable[[xr.Dataset], xr.Dataset]


def build_projection_workflow(
    *,
    pre: Callable[[xr.Dataset], xr.Dataset],
    project: Callable[[xr.Dataset], xr.Dataset],
    post: Callable[[xr.Dataset], xr.Dataset],
) -> ProjectionWorkflow:
    """
    Use simple functions to quickly build a model to project effects, impacts and/or damages.

    This function is a quick and simple way to build an ProjectionWorkflow from three simple functions.

    See Also
    --------
    project: Apply a projection workflow to a dataset.
    ProjectionWorkflow: Technical ProjectionWorkflow protocol.
    """
    return _SimpleProjectionWorkflow(
        pre_project=pre,
        project=project,
        post_project=post,
    )


def project(d: xr.Dataset, *, model: ProjectionWorkflow) -> xr.Dataset:
    """
    Project a dataset of predictors, 'd', with 'model' to return a projected dataset

    See Also
    --------
    build_projection_workflow: Build a projection workflow from simple functions.
    ProjectionWorkflow: Technical ProjectionWorkflow protocol.
    """
    preprocessed = model.pre_project(d)
    projected = model.project(preprocessed)
    postprocessed = model.post_project(projected)

    return postprocessed
