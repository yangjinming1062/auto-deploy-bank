# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

whylogs is an open-standard library for data logging that generates "profiles" — efficient, mergeable, statistical summaries of datasets. Used for data quality validation, drift detection, and ML observability.

**Multi-language project**: Python (primary), Java, and Protobuf for serialization.

## Commands

All commands run from `/home/ubuntu/deploy-projects/94ef585b8b616909615d4098/python` directory unless noted otherwise.

### Setup & Installation
```bash
# Install dependencies (requires protobuf compiler and Poetry)
make install

# Build everything including protobuf sources
make
```

### Development
```bash
# Run all tests
make test

# Run a single test file
poetry run pytest path/to/test.py

# Linting (flake8)
make lint

# Auto-fix linting and formatting
make fix

# Run pre-commit hooks (black, isort, ruff, etc.)
make format

# Full pre-push checks (linter + type check + tests + build)
make release
```

### Version Management
```bash
make bump-patch   # Bug fixes (x.x.X)
make bump-minor   # New features (x.X.0)
make bump-major   # Breaking changes (X.0.0)
```

### Java Development
Commands run from `/home/ubuntu/deploy-projects/94ef585b8b616909615d4098/java`:
```bash
./gradlew build    # Build
./gradlew test     # Run tests
./gradlew spotlessApply  # Auto-format
```

## Architecture

### Python Package Structure (`python/whylogs/`)

| Directory | Purpose |
|-----------|---------|
| `api/` | Public API (logger, reader, writer, store) |
| `api/logger/` | Main logging API (`whylogs.log()`) |
| `api/writer/` | Output backends (WhyLabs, S3, GCS, local) |
| `core/` | Core profiling logic (columns, metrics, constraints) |
| `viz/` | Profile visualization (NotebookProfileVisualizer) |
| `experimental/` | Experimental features (embeddings, process logging) |
| `datasets/` | Dataset utilities |
| `migration/` | Migration helpers for version upgrades |

### Key Concepts

- **Profiles**: Map-reducible statistical summaries. Designed to merge across distributed systems and time windows.
- **Sketching Algorithms**: Streaming algorithms (HLL for cardinality, KLL for quantiles) for minimal memory footprint.
- **Constraints**: Data validation rules built on profiles.
- **Multi-modal Support**: Tabular data, images, text, and embeddings.
- **Writers/Readers**: Pluggable backends for WhyLabs (SaaS), AWS S3, GCS, and local filesystem.

### Main Entry Point
```python
import whylogs as why
results = why.log(df)  # Returns a ProfileResult
```

### Protobufs
Serialization schema defined in `/proto`. Generated Python code lives in `whylogs/core/proto/`.

## Code Style

- **Formatting**: black (line-length: 120)
- **Linting**: flake8, ruff (for experimental code)
- **Type checking**: mypy with numpy plugin, pyright for experimental code
- **Import sorting**: isort with black profile