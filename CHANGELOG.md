# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Minor improvements to README, CONTRIBUTING docs, developer experience. ([@brews](https://github.com/brews), [PR#42](https://github.com/ClimateImpactLab/isku/pull/42))


## [0.3.0] - 2026-05-15

### Added

- Support and testing for Python versions >= 3.12. ([@brews](https://github.com/brews), [PR#33](https://github.com/ClimateImpactLab/isku/pull/33))
- Allow installs with xarray versions earlier than 2026.4.0. ([@brews](https://github.com/brews), [PR#33](https://github.com/ClimateImpactLab/isku/pull/33))

## [0.2.0] - 2026-05-14

### Added

- Documentation in docs/ hosted at https://climateimpactlab.github.io/isku.
- Test and test-coverage badges to README.
- Add pre-commit hooks (via prek) to help developers with format.

### Changed

- Move project repository to https://github.com/climateimpactlab/isku. They own this now.
- BREAKING: `isku.ExtractionWorkflow` is now `isku.ExtractionTemplate`.
- BREAKING: `isku.ProjectionWorkflow` is now `isku.ProjectionTemplate`.
- BREAKING: `isku.build_extraction_workflow` is now `isku.build_extraction_template`.
- BREAKING: `isku.build_projection_workflow` is now `isku.build_projection_template`.
- BREAKING: In `isku.extract_regions`, the `workflow` argument is now `template`.
- BREAKING: `isku.ProjectionTemplate` protocol methods `d` argument is now `ds` to make it consistent with extraction signatures.
- Improved README.
- Improved CONTRIBUTING.
- Add project URLs to package metadata.
- Various improvement to internal code formatting and style.

## [0.1.0] - 2026-05-06

- Initial release.

[Unreleased]: https://github.com/climateimpactlab/isku/compare/v0.3.0...HEAD
[0.3.0]: https://github.com/climateimpactlab/isku/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/climateimpactlab/isku/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/climateimpactlab/isku/releases/tag/v0.1.0
