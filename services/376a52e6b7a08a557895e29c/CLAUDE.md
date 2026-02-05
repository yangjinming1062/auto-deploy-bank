# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

OpenLineage is an open standard for metadata and lineage collection. It defines a generic model of **Runs**, **Jobs**, and **Datasets** identified using consistent naming strategies. The model is extensible through **facets** - atomic, versioned metadata pieces attached to core entities.

### Directory Structure
- **`spec/`**: JSON Schema and OpenAPI definitions (the source of truth)
- **`client/python/`**: Python client library (uses `uv` for dependency management)
- **`client/java/`**: Java client library (Gradle-based, multi-module)
- **`integration/`**: Tool-specific integrations (Spark, Flink, dbt, SQL, etc.)

## Development Commands

### Python Projects
```bash
make setup-client    # Setup Python client
make setup-common    # Setup integration common library
make setup-dbt       # Setup dbt integration

make test-client     # Test Python client
make test-common     # Test integration common
make test-dbt        # Test dbt integration
make test-all        # Run all Python tests

make lint-format     # Run ruff format + check
make lint-types      # Run mypy type checking
make lint-all        # Run all linting
make fix-format      # Auto-fix formatting issues

# Single test
cd client/python && uv run pytest tests/test_client.py
```

### Java Projects
```bash
cd client/java && ./gradlew build        # Build Java client
cd client/java && ./gradlew test         # Test Java client
cd client/java && ./gradlew spotlessApply # Format Java code
cd client/java && ./gradlew pmdMain       # Run PMD static analysis

cd integration/spark && ./gradlew build  # Build Spark integration
cd integration/spark && ./gradlew test   # Test Spark integration
```

### Pre-commit Hooks
```bash
pip install prek && prek install  # Install hooks
prek run --all-files              # Run manually
```

Required before committing: license headers, ruff formatting/linting, mypy type checking, JSON schema validation, and code generation from spec.

## Architecture

### Specification-Driven Design
The OpenAPI spec (`spec/OpenLineage.yml`) and JSON Schema files (`spec/facets/`) are the source of truth. Both Python and Java clients generate code from these specs.

### Core Model Entities
- **Run**: Execution instance with UUID identifier, start/end times, and run facets
- **Job**: Process definition consuming/producing datasets, identified by name + namespace
- **Dataset**: Abstract data representation, identified by name within a datasource namespace
- **Facet**: Atomic, versioned metadata attached to entities (e.g., `DataSourceDatasetFacet`, `SqlJobFacet`)

### Data Flow
1. **Integrations** hook into tools (Spark's `QueryExecutionListener`, dbt callbacks, etc.)
2. Convert tool-specific events to OpenLineage's generic model using **visitors**
3. Client emits events via configurable **transport** (HTTP, Kafka, Console)
4. Backend (e.g., Marquez) receives and stores lineage data

### Key Packages
- **`client/python/src/openlineage/client/`**: Client, events, facets, and transports
- **`integration/common/`**: Shared Python logic for dbt, SQL parsing, and provider utilities
- **`client/java/src/`**: Java client with facet classes, transports, and visitor infrastructure
- **`integration/spark/`**: Spark listeners organized by Spark version (`spark31`, `spark32`, etc.)

## Transport Configuration

Configure via `openlineage.yml` or environment variables:
- `OPENLINEAGE_URL`: HTTP endpoint
- `OPENLINEAGE_TOPIC`: Kafka topic name
- Transport class via `OPENLINEAGE.transport`

Common transports: `HttpTransport`, `KafkaTransport`, `ConsoleTransport` (debug).

## Versioning & Spec Changes

- **Spec changes** follow [SchemaVer](https://docs.snowplank.io) (semver for schemas)
- **Python client** uses `bump2version`, version in `pyproject.toml` and `constants.py`
- **Java client** version in `gradle.properties`

When modifying the spec:
1. Edit JSON Schema files in `spec/facets/`
2. Run `ol-generate-code` or let pre-commit regenerate client code
3. Bump the facet version following SchemaVer rules

## Commit Requirements

- **DCO sign-off**: All commits must include `Signed-off-by: ...` (use `git commit -s`)
- **License headers**: Required in all new files (see `.github/header_templates.md`)
- **PR title format**: `component: description` (e.g., `spark: add Iceberg source visitor`)
- **Tests**: All changes should be accompanied by tests

## Testing

```bash
pytest -m "unit"         # Run unit tests only
pytest -m "integration"  # Run integration tests (may require external services)
```