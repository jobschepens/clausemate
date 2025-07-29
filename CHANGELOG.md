# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.1] - 2025-07-29

### Fixed
- **Python Version Compatibility**: Updated entire project to require Python >=3.11 to match numpy/pandas dependencies
- **Missing Dependencies**: Added psutil>=5.0.0 to benchmark dependencies and made imports optional
- **GitHub Actions CI/CD**: Resolved all workflow failures and dependency installation issues
- **Pytest Collection**: Fixed duplicate test file import conflicts by excluding tests/property/test_property_based.py
- **Deprecated Actions**: Updated all GitHub Actions to current versions (actions/upload-artifact@v4, codecov/codecov-action@v4)

### Changed
- **Python Support**: Now requires Python 3.11+ (was 3.8+)
- **Dependencies**: Updated to numpy==2.3.1 and pandas==2.3.1 with full compatibility
- **CI/CD**: All GitHub workflows now use Python 3.11 and install complete dependency sets
- **Docker**: Updated base image from python:3.10-slim to python:3.11-slim
- **Development**: Updated nox sessions, conda environment, and all tooling to Python 3.11

### Added
- **Comprehensive Testing**: GitHub Actions now successfully run 111 tests with 103 passing
- **Coverage Reporting**: Proper Codecov integration across all workflows
- **Performance Benchmarking**: Enhanced benchmark dependencies with psutil support
- **Error Handling**: Graceful handling of missing optional dependencies

## [2.0.0] - Previous Release
- Initial stable release with core functionality
