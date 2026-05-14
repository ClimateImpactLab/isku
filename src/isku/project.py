from collections.abc import Callable
from dataclasses import dataclass
from typing import Protocol

import xarray as xr

__all__ = [
    "ProjectionTemplate",
    "build_projection_template",
    "project",
]


class ProjectionTemplate(Protocol):
    """
    Template for projecting a model with pre and post processing.

    See Also
    --------
    build_projection_template: Build a projection template from simple functions.
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
class _SimpleProjectionTemplate(ProjectionTemplate):
    pre_project: Callable[[xr.Dataset], xr.Dataset]
    project: Callable[[xr.Dataset], xr.Dataset]
    post_project: Callable[[xr.Dataset], xr.Dataset]


def build_projection_template(
    *,
    pre: Callable[[xr.Dataset], xr.Dataset],
    project: Callable[[xr.Dataset], xr.Dataset],
    post: Callable[[xr.Dataset], xr.Dataset],
) -> ProjectionTemplate:
    """
    Use simple functions to quickly build a model to project effects, impacts and/or damages.

    This function is a quick and simple way to build an ProjectionTemplate from three simple functions.

    See Also
    --------
    project: Apply a projection template to a dataset.
    ProjectionTemplate: Technical ProjectionTemplate protocol.
    """
    return _SimpleProjectionTemplate(
        pre_project=pre,
        project=project,
        post_project=post,
    )


def project(d: xr.Dataset, *, model: ProjectionTemplate) -> xr.Dataset:
    """
    Project a dataset of predictors, 'd', with 'model' to return a projected dataset

    See Also
    --------
    build_projection_template: Build a projection template from simple functions.
    ProjectionTemplate: Technical ProjectionTemplate protocol.
    """
    preprocessed = model.pre_project(d)
    projected = model.project(preprocessed)
    postprocessed = model.post_project(projected)

    return postprocessed
