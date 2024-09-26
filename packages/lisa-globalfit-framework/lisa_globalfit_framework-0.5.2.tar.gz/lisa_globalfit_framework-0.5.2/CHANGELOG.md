# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

- Renamed blocks to modules.

## [0.4.0] - 2024-06-04

### Added

- Added `--n-steps` argument to `start-block` command.
- Added `--input-group-configuration-path` argument to `start-block` command.
- Added `--current-iteration` argument to `start-block` command.
- Added `--expected-groups` argument to `start-engine` command.
- Added `--current-iteration` argument to `start-engine` command.
- Added `--max-iterations` argument to `start-engine` command.
- Added `--output-iteration-decision` to `start-engine` command.
- Added `--output-preprocessed-signal` argument to `preprocess` command.

### Removed

- Removed `--blocks-configuration-map-directory` from `start-engine` command.
- Removed `--n-steps-per-iteration` from `start-engine` command.
- Removed `--n-iterations` from `start-engine` command.
- Removed `--output-blocks-configuration-map-path` from `preprocess` command.

### Changed

- Renamed `--output-data` to `--output-checkpoint` in `start-engine` command.
- Renamed `--checkpoint` to `--input-checkpoint` in `preprocess` command.
- Argument `--pipeline-run-id` is now mandatory.

## [0.3.0] - 2024-04-09

### Added

- Added `--n-iterations` argument to `start-engine` command.
- Added `--n-steps-per-iteration` argument to `start-engine` command.
- Added optional `--iteration-checkpoints-directory` argument to `start-engine` command.
- Added optional `--checkpoint` argument to `preprocess` command.
- Added `--catalog-db` argument to `start-engine` command.

## [0.2.0] - 2024-03-20

### Added

- Added `--output-checkpoint` to write sampler chains to a block-local file.
- Added `plot` subcommand for displaying corner plots of checkpoints.
- Added upload of checkpoints to S3 after each iteration.
- Added initial monitoring server.
- Added initial monitoring web UI.

## [0.1.0] - 2024-02-15

### Added

- Initial release with minimal demo.

[unreleased]: https://gitlab.in2p3.fr/LISA/LDPG/GlobalFitFramework/-/compare/0.4.0...HEAD
[0.4.0]: https://gitlab.in2p3.fr/LISA/LDPG/GlobalFitFramework/-/tags/0.4.0
[0.3.0]: https://gitlab.in2p3.fr/LISA/LDPG/GlobalFitFramework/-/tags/0.3.0
[0.2.0]: https://gitlab.in2p3.fr/LISA/LDPG/GlobalFitFramework/-/tags/0.2.0
[0.1.0]: https://gitlab.in2p3.fr/LISA/LDPG/GlobalFitFramework/-/tags/0.1.0
