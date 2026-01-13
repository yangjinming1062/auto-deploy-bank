# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **whylogs** repository - an open-source multi-language data profiling and monitoring library. It provides efficient, customizable, and mergeable statistical summaries (called "profiles") of datasets for data quality monitoring, drift detection, and ML observability.

- **Primary Implementation**: Python package v1.6.4 with Poetry
- **Secondary Implementation**: Java library with Gradle
- **Communication Layer**: Protocol Buffers for cross-language compatibility
- **CI/CD**: GitHub Actions with multi-OS/multi-version testing

## Development Commands

### Common Development Workflow

```bash
# Install dependencies (Poetry required)
make install

# Build everything (protos + distributions)
make

# Run full pre-push checks (lint, format, test, build)
make release

# Run tests
make test

# Run specific test file (after activating poetry shell)
poetry shell
pytest tests/path/to/test_file.py -v

# Code formatting and linting
make pre-commit          # Run pre-commit hooks
make format-fix          # Fix formatting with black, isort
make lint-fix            # Fix linting issues
make fix                 # Both format and lint fixes

# Generate protobuf files
make proto

# Build documentation
make docs
make livedocs            # Live-reloading docs server

# Clean build artifacts
make clean

# Version bumping
make bump-patch          # 1.6.4 -> 1.6.5
make bump-minor          # 1.6.4 -> 1.7.0
make bump-major          # 1.6.4 -> 2.0.0
make bump-release        # Remove dev suffix
make bump-build          # Bump build number

# Publish to PyPI
make publish

# Other useful commands
make coverage            # Generate test coverage report
make jupyter-kernel      # Install Jupyter kernel for development
make telemetry-opt-out   # Disable analytics
```

### Testing

```bash
# Run all tests
make test

# Run with coverage
make coverage

# Run notebooks tests
make test-notebooks

# Test with system Python
make test-system-python

# Run specific test
poetry run pytest tests/test_specific.py -v -k test_name
```

### Dependency Management (Poetry)

```bash
# Activate poetry shell (to access installed binaries)
poetry shell

# Add dependency
poetry add package-name

# Add dev dependency
poetry add --dev package-name

# Update lock file
poetry lock

# Show dependency tree
poetry show --tree

# Export requirements.txt
poetry export -f requirements.txt --output requirements.txt --dev
```

## Code Architecture

### Language Implementations

#### Python (Primary)
Located in `python/`. Main package structure:

```
python/whylogs/
├── api/                    # Public API and logging interfaces
│   ├── logger/            # Logging API and implementations
│   │   ├── experimental/  # Async/actor-based logging
│   │   └── rolling.py     # Rolling logger for log rotation
│   └── whylabs.py         # WhyLabs platform integration
├── core/                  # Core data profiling logic
│   └── proto/            # Generated protobuf files
├── viz/                  # Profile visualization components
├── datasets/             # Dataset utilities
├── experimental/         # Beta features
├── extras/              # Additional integrations
├── migration/           # v0 to v1 migration tools
└── context/             # Context management
```

**Key Entry Points**:
- `python/whylogs/__init__.py` - Main exports: `log()`, `logger()`, `read()`, `write()`
- `python/whylogs/api/__init__.py` - Core API functions
- `python/whylogs/core/__init__.py` - Core profile functionality

#### Java (Secondary)
Located in `java/`. Build system: Gradle with Kotlin DSL.

```
java/
├── core/                 # Core Java library (maven-publish)
│   └── src/main/java/com/whylogs/
│       ├── api/          # Public API
│       │   ├── logger/   # Logging API
│       │   └── writer/   # Output writers
│       └── core/         # Core metrics and schemas
├── spark-bundle/         # Spark integration bundle
└── smoketest/           # Integration tests
```

#### Protocol Buffers
Cross-language communication defined in `proto/`:

```
proto/
├── src/                  # Main protobuf definitions
│   └── whylogs_messages.proto
└── v0/                   # Version 0 (legacy) definitions
    ├── v0_messages.proto
    ├── v0_summaries.proto
    └── v0_constraints.proto
```

Protobuf files are auto-generated into `python/whylogs/core/proto/` and `java/core/src/main/java/`.

### Integration Ecosystem

Optional extras via Poetry extras (see `python/pyproject.toml`):

- **viz**: Visualization (`ipython`, `pybars3`, `numpy`, `scipy`, `Pillow`)
- **spark**: Spark integration (`pyarrow`, `pyspark`)
- **s3**: AWS S3 (`boto3`)
- **gcs**: Google Cloud Storage (`google-cloud-storage`)
- **mlflow**: MLflow integration (`mlflow-skinny`, `databricks-cli`)
- **image**: Image profiling (`Pillow`)
- **datasets**: Pandas integration (`pandas`)
- **embeddings**: ML embeddings (`numpy`, `scikit-learn`)
- **fugue**: Fugue integration (`fugue`)
- **proc**: Process logging (`faster-fifo`, `orjson`)

Install with: `poetry install -E "spark mlflow s3"`

## Build System

### Python (Poetry + Make)
- **Build backend**: Poetry-core
- **Packaging**: `poetry build` (generates wheel and tarball in `dist/`)
- **Protobuf**: Custom Makefile targets with `protoc`
- **Documentation**: Sphinx (`python/docs/`)

Key build artifacts:
- `dist/` - Distribution files (wheel, tarball)
- `build/` - Build artifacts
- `whylogs/core/proto/` - Generated protobuf files

### Java (Gradle)
- **Build tool**: Gradle with Kotlin DSL
- **Plugins**: Protobuf, Maven Publish, Spotless
- **Testing**: TestNG framework
- **Package type**: JAR published to Maven Central

## Configuration Files

### Python
- `python/pyproject.toml` - Poetry config, dependencies, tool settings (mypy, pytest, black, ruff)
- `python/Makefile` - Build automation targets
- `python/.pre-commit-config.yaml` - Git hooks configuration
- `python/.flake8` - Flake8 linting config
- `python/docs/conf.py` - Sphinx documentation config

### Java
- `java/core/build.gradle.kts` - Gradle build configuration
- `java/smoketest/settings.gradle` - Smoketest module settings

### CI/CD
- `.github/workflows/whylogs-ci.yml` - Main CI pipeline (Python 3.8-3.11, Java 8, multi-OS)
- `.github/workflows/push-release.yml` - Release automation
- `.github/workflows/docker-test.yml` - Docker-based testing
- `.github/workflows/test-notebook.yml` - Jupyter notebook testing

## Key Concepts

### Profiles
The core data structure - statistical summaries that are:
- **Efficient**: Compact representation of large datasets
- **Customizable**: Configurable metrics per data type
- **Mergeable**: Can be combined for distributed/streaming systems

### API Usage
```python
import whylogs as why
import pandas as pd

# Basic logging
df = pd.read_csv("data.csv")
results = why.log(df)

# Get profile view
profile_view = results.view()

# Write to various outputs
results.writer("whylabs").write()
results.writer("local").path("./profiles/").write()
```

### Constraints
Data validation framework built on top of profiles:
```python
from whylogs.core.constraints import ConstraintsBuilder
from whylogs.core.constraints.factories import greater_than_number

profile_view = why.log(df).view()
builder = ConstraintsBuilder(profile_view)
builder.add_constraint(greater_than_number("column", 0.15))
constraints = builder.build()
constraints.report()
```

### Experimental Features
- Async logging in `whylogs/api/logger/experimental/`
- Process-based logging in `whylogs/experimental/`
- Actor-based logging patterns

## Development Workflow

### Prerequisites
1. **Install protobuf compiler**: `brew install protobuf` (macOS) or package manager equivalent
2. **Install Poetry**: Follow [Poetry docs](https://python-poetry.org/docs/)
3. **Install dependencies**: `make install`

### Local Development
```bash
# Setup
make install
poetry shell  # Activate environment

# Development cycle
make proto     # If working with proto files
make format-fix
make test      # Run tests
make release   # Full CI simulation

# Add new feature
poetry add new-dependency
# Make changes
make release
# Submit PR
```

### Version Bump & Release Process
1. `make release` - Verify everything passes
2. `make bump-patch|minor|major` - Update version numbers
3. Commit version bump
4. Push to `develop` branch
5. Submit PR to merge to `main` (fast-forward only)
6. Create signed Git tag: `git tag -a -s 1.6.4`
7. Push tag - CI will build and publish

### Running CI Locally
Use [act](https://github.com/nektos/act) to run GitHub Actions locally:
```bash
act -P ubuntu-latest=ubuntu-builder
```

## Testing Strategy

- **Framework**: pytest (Python), TestNG (Java)
- **Coverage**: pytest-cov with codecov integration
- **Integration tests**: Spark, MLflow, cloud storage tests
- **Notebooks**: Jupyter notebook testing with papermill
- **Multi-environment**: Python 3.7-3.11, Ubuntu/macOS

## Code Quality

### Linting & Formatting
- **Black**: Code formatting (120 line length)
- **isort**: Import sorting
- **mypy**: Type checking
- **ruff**: Fast linter (E, F, I, W rules)
- **flake8**: Additional linting
- **pre-commit**: Git hooks (runs automatically in CI)

### Pre-commit Setup
```bash
poetry shell
pre-commit install        # Run before commits
pre-commit install --hook-type pre-push  # Run before pushes
```

## Documentation

- **User docs**: Sphinx in `python/docs/`, deployed to ReadTheDocs
- **API docs**: Auto-generated with sphinx-autoapi
- **Examples**: Jupyter notebooks in `python/examples/`
- **Integration docs**: `python/examples/integrations/`

Build docs: `make docs` or `make livedocs` (live-reload)

## Important Notes

1. **Multi-language project**: Changes may require updates to Python, Java, and protobuf definitions
2. **Protoc required**: Must install protobuf compiler for full builds
3. **Poetry-centric**: All Python development uses Poetry for dependencies
4. **Pre-commit required**: Code won't pass CI without passing pre-commit hooks
5. **Profile serialization**: Uses Protocol Buffers for cross-language compatibility
6. **Performance critical**: Profiling happens in data pipelines - keep overhead minimal (<1% typical)
7. **Telemetry**: Collects anonymous usage stats by default (opt-out with `WHYLOGS_NO_ANALYTICS=true`)