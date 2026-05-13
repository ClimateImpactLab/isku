# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Documentation in docs/ hosted at brews.github.io/isku.
- Test and test-coverage badges to README.
- Add pre-commit hooks (via prek) to help developers with format.

### Changed

- BREAKING: `isku.ExtractionWorkflow` is now `isku.ExtractionTemplate`.
- BREAKING: `isku.ProjectionWorkflow` is now `isku.ProjectionTemplate`.
- BREAKING: `isku.build_extraction_workflow` is now `isku.build_extraction_template`.
- BREAKING: `isku.build_projection_workflow` is now `isku.build_projection_template`.
- BREAKING: In `isku.extract_regions`, the `workflow` argument is now `template`.
- Improved README.
- Improved CONTRIBUTING.
- Add project URLs to package metadata.
- Various improvement to internal code formatting and style.

## [0.1.0] - 2026-05-06

- Initial release.

[Unreleased]: https://github.com/brews/isku/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/brews/isku/releases/tag/v0.1.0
