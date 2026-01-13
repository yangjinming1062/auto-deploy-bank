# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Apache Beam Overview

Apache Beam is a unified model for defining both batch and streaming data-parallel processing pipelines. It provides SDKs for Java, Python, and Go, along with multiple runners (DirectRunner, DataflowRunner, FlinkRunner, SparkRunner, JetRunner, Twister2Runner) for executing pipelines on distributed backends.

## Build System

Beam uses **Gradle** as the build system for this monorepo. All commands use `./gradlew` from the repository root.

### Build All Projects
```bash
./gradlew build
```

### Validate Development Environment
```bash
./gradlew :checkSetup
```

### Code Formatting

**Java:**
```bash
# Apply code formatting
./gradlew spotlessApply

# Run formatting checks
./gradlew spotlessCheck
```

**Python:**
```bash
# Install pre-commit hooks (one-time setup)
pre-commit install

# Format code (yapf) and run linting (pylint) will run automatically on commit
# Manual formatting:
yapf -r --in-place sdks/python/apache_beam
```

### CHANGES.md Formatting
```bash
./gradlew formatChanges
```

## Testing Commands

### Java SDK Tests

**Run all tests for a module:**
```bash
./gradlew :sdks:java:core:test
```

**Run specific test:**
```bash
./gradlew :sdks:java:harness:test --tests org.apache.beam.fn.harness.CachesTest
./gradlew :sdks:java:harness:test --tests *CachesTest
./gradlew :sdks:java:harness:test --tests *CachesTest.testClearableCache
```

**Integration tests** (files ending in `*IT.java`):
```bash
# Run with Direct Runner
./gradlew :sdks:java:io:google-cloud-platform:integrationTest

# Run on Dataflow with specific project
./gradlew :runners:google-cloud-dataflow-java:examplesJavaRunnerV2IntegrationTest \
  -PgcpProject=<your_gcp_project> -PgcpRegion=us-central1 \
  -PgcsTempRoot=gs://<your_gcs_bucket>/tmp
```

### Python SDK Tests

**Run Python SDK tests:**
```bash
./gradlew :sdks:python:test
```

**Direct pytest** (requires virtual environment setup from sdks/python):
```bash
# From sdks/python directory with venv activated
pytest apache_beam/runners/worker/operations_test.py
```

**Run unit tests across Python versions:**
```bash
tox
```

**Run WordCount example:**
```bash
./gradlew :sdks:python:wordCount
```

### Go SDK Tests

**Run Go SDK tests:**
```bash
# From repository root
go test ./sdks/go/...

# From sdks/go directory
go test ./...
```

## Running Examples

### Java Examples
```bash
./gradlew :examples:java:wordCount
```

### Python Examples
```bash
./gradlew :sdks:python:wordCount
```

### Go Examples
```bash
./gradlew :sdks:go:examples:wordCount
```

## Repository Structure

This is a **monorepo** containing the entire Apache Beam project:

### Core Directories

- **`model/`** - Beam model definitions (protocol buffers and APIs)
  - `pipeline/` - Pipeline proto definitions
  - `fn-execution/` - Function execution model
  - `job-management/` - Job management APIs

- **`sdks/`** - Software Development Kits
  - `java/` - Java SDK
    - `core/` - Core Java SDK components
    - `harness/` - SDK harness (worker container entrypoint)
    - `io/` - I/O connectors (Google Cloud, Kafka, JDBC, etc.)
  - `python/` - Python SDK (`apache_beam` package)
    - `io/` - I/O connectors
    - `transforms/` - Core transforms
    - `runners/` - Runner implementations
  - `go/` - Go SDK

- **`runners/`** - Pipeline execution engines
  - `direct-java/` - DirectRunner (local execution)
  - `google-cloud-dataflow-java/` - Dataflow Runner
    - `worker/` - Dataflow worker (legacy)
  - `flink/` - Flink Runner
  - `spark/` - Spark Runner
  - `prism/` - PrismRunner (local, portability framework)
  - `samza/`, `jet/`, `twister2/` - Other runners

- **`examples/`** - Example pipelines
  - `java/` - Java examples (wordcount, etc.)
  - `python/` - Python examples
  - `multi-language/` - Cross-language examples

### Supporting Directories

- **`.github/workflows/`** - GitHub Actions CI/CD workflows
- **`learning/`** - Documentation and learning resources
- **`playground/`** - Beam Playground application
- **`contributor-docs/`** - Developer documentation
- **`release/`** - Release automation scripts

## Development Environment Setup

### Prerequisites

- Java JDK 11 (preferred) or 8, 17, 21
- Latest Go 1.x
- Docker (for SDK containers and portable runners)
- Python 3.10-3.13 (for Python SDK development)

### Automated Setup (Linux/macOS)

```bash
./local-env-setup.sh
```

### Container-Based Environment

```bash
./start-build-env.sh
```

### Python Environment

From `sdks/python/`:

```bash
# Create virtual environment
python3 -m venv ~/.virtualenvs/beam
source ~/.virtualenvs/beam/bin/activate

# Install in editable mode with test and GCP deps
pip install -e .[gcp,test]
```

## Code Architecture

### Beam Programming Model

Core abstractions:
- **`PCollection`** - Distributed data collection (bounded or unbounded)
- **`PTransform`** - Transformation computation
- **`Pipeline`** - DAG of transforms and collections
- **`PipelineRunner`** - Execution backend

### SDK Architecture

Each language SDK provides:
1. **Pipeline construction** - DSL for building pipelines
2. **SDK harness** - Worker-side execution environment
3. **I/O connectors** - External system integrations
4. **Runner adapters** - Interface to execution backends

### Portable Execution Model

Beam's portability framework enables cross-language pipelines:
- **SDK harness** - Language-agnostic worker container
- **Fn API** - Function execution API
- **Job API** - Runner-independent job specification
- **Expansion service** - Cross-language transform expansion

### Build Configuration

- **Root build file**: `build.gradle.kts` (licensing, release plugins)
- **Settings file**: `settings.gradle.kts` (project inclusions, Gradle Enterprise)
- **Gradle plugin**: `buildSrc/src/main/groovy/org/apache/beam/gradle/BeamModulePlugin.groovy`
  - Manages dependencies
  - Configures Java, Python, Go, Proto, Docker projects
  - Defines common tasks (`test`, `spotlessApply`, etc.)

## Version Information

- **Current version**: 2.71.0-SNAPSHOT (see `gradle.properties`)
- **Java versions**: 1.8+ (target)
- **Python versions**: 3.10, 3.11, 3.12, 3.13
- **Flink versions**: 1.17, 1.18, 1.19, 1.20

## CI/CD

Beam uses **GitHub Actions** for CI:
- **Pull Request runs** - Validate contributions
- **Direct push/merge runs** - Verify post-merge integrity
- **Scheduled runs** - Nightly builds with dependency verification

Pre-commit hooks enforce:
- Python code formatting (yapf)
- Python linting (pylint)

## Key Development Notes

1. **Monorepo** - Open repository root in IDEs, not individual SDK directories
2. **Gradle** - Single Gradle command orchestrates all language builds
3. **Testing** - Unit tests use `*Test.java`, integration tests use `*IT.java`
4. **Pre-commit** - Python formatting/linting runs automatically on commit
5. **Containers** - Docker required for harness container and portability testing
6. **Cross-language** - Python/Go SDKs leverage Java SDK components via portability APIs

## Documentation Resources

- [Contributing Guide](CONTRIBUTING.md) - Setup and contribution process
- [CI Documentation](CI.md) - Build system and CI workflows
- [Code Change Guide](contributor-docs/code-change-guide.md) - Testing and development workflow
- [Python Tips](contributor-docs/python-tips.md) - Python-specific development guidance