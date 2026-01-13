# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

BentoML is a Python library for building online serving systems optimized for AI apps and model inference. It provides a unified framework for building model inference APIs with support for any ML framework, multi-model serving, Docker containerization, and production deployment.

**Key Components:**
- Model serving framework with REST/gRPC APIs
- Docker containerization and Bento bundle system
- Cloud deployment support (BentoCloud)
- Multi-framework support (PyTorch, TensorFlow, XGBoost, LightGBM, etc.)
- Batching, parallelism, and performance optimization
- Observability with OpenTelemetry

## Development Setup

### Prerequisites
- Python 3.9+
- [PDM](https://pdm.fming.dev/latest/)
- [pre-commit](https://pre-commit.com/)
- Docker (for proto file formatting/linting and some tests)

### Install Development Environment
```bash
make install
```

This installs BentoML in editable mode with all development dependencies and sets up pre-commit hooks.

## Common Development Commands

### Code Quality
```bash
make format              # Format code with black
make lint                # Lint with ruff
make type                # Type check with pyright
make style               # Run format, lint, and proto formatting
pre-commit run --all-files  # Run all pre-commit hooks
```

### Testing
```bash
pdm run nox                                  # Run all tests
pdm run pytest tests/unit                    # Run unit tests only
pdm run pytest tests/unit -k test_name       # Run specific test
pdm run pytest tests/integration/frameworks/test_frameworks.py --framework pytorch  # Framework integration tests
pdm run pytest tests/e2e/bento_server_http   # E2E HTTP tests
pdm run pytest tests/e2e/bento_server_grpc   # E2E gRPC tests
pdm run pytest tests/e2e/bento_new_sdk       # E2E SDK tests
```

### Building & Packaging
```bash
pdm build                          # Build distribution packages
make clean                         # Clean generated files
```

### Documentation
```bash
make watch-docs                    # Build and watch documentation
make spellcheck-docs               # Spell check documentation
```

## Project Structure

```
src/
├── bentoml/                      # Main library
│   ├── _internal/               # Internal implementation
│   │   ├── server/              # HTTP/gRPC server implementations
│   │   ├── runner/              # Model runner system
│   │   ├── service/             # Service orchestration
│   │   ├── frameworks/          # ML framework integrations
│   │   ├── models/              # Model management
│   │   ├── bento/               # Bento bundle system
│   │   ├── cloud/               # Cloud deployment
│   │   ├── container/           # Docker containerization
│   │   ├── configuration/       # Configuration management
│   │   ├── io_descriptors/      # I/O types (JSON, image, pandas, etc.)
│   │   ├── batch/               # Batching system
│   │   ├── marshal/             # Request/response marshaling
│   │   └── utils/               # Internal utilities
│   ├── grpc/                    # gRPC service definitions and generated stubs
│   ├── serving.py               # High-level serving API
│   ├── server.py                # Server configuration
│   ├── models.py                # Model APIs
│   ├── bentos.py                # Bento APIs
│   └── deployment.py            # Deployment APIs
│
├── bentoml_cli/                 # CLI commands
│   ├── cli.py                   # Main CLI entry point
│   ├── serve.py                 # serve command
│   ├── containerize.py          # containerize command
│   ├── cloud.py                 # cloud commands
│   ├── models.py                # model commands
│   ├── bentos.py                # bento commands
│   └── worker/                  # Worker processes
│
├── _bentoml_impl/               # Framework implementation utilities
│   └── frameworks/              # Framework-specific loaders
│
└── _bentoml_sdk/                # SDK components for external use

tests/
├── unit/                        # Unit tests
├── integration/                 # Integration tests
│   └── frameworks/             # Framework-specific tests
├── e2e/                        # End-to-end tests
│   ├── bento_server_http/      # HTTP server tests
│   ├── bento_server_grpc/      # gRPC server tests
│   └── bento_new_sdk/          # New SDK tests
└── monitoring/                 # Monitoring tests
```

## Architecture Overview

### Service Definition Pattern
Services are defined as Python classes with `@bentoml.service` decorator:

```python
@bentoml.service
class MyService:
    def __init__(self):
        # Initialize models
        pass

    @bentoml.api
    def predict(self, input_data: SomeIODescriptor) -> SomeIODescriptor:
        # Handle request
        pass
```

### Runner System
Models run in separate processes (runners) for isolation and performance. Runners communicate with the API server via gRPC or in-process communication.

### Bento Bundle
A Bento is the standardized deployable artifact containing:
- Service code
- Models
- Dependencies
- Configuration
- Metadata

### gRPC Integration
- Proto files: `src/bentoml/grpc/v1alpha1/service.proto` and `src/bentoml/grpc/v1/service.proto`
- Generate stubs: `./scripts/generate_grpc_stubs.sh`
- Format proto files: `make format-proto`
- Lint proto files: `make lint-proto`

## Configuration

- **pyproject.toml**: Python project configuration, dependencies, tool settings (ruff, pyright, coverage, pytest)
- **.pre-commit-config.yaml**: Pre-commit hooks configuration
- **Makefile**: Development commands
- **noxfile.py**: Test automation for different Python versions and test suites
- **BUILD.bazel**: Bazel build rules (mainly for proto files)

## Testing Strategy

The project uses multiple test suites:

1. **Unit Tests** (`tests/unit`): Fast, isolated tests
2. **Framework Integration Tests** (`tests/integration/frameworks`): Test integration with specific ML frameworks
3. **End-to-End Tests** (`tests/e2e`): Full workflow tests including HTTP/gRPC servers and SDK
4. **Monitoring Tests** (`tests/monitoring`): Observability tests

## Framework Support

The codebase supports multiple ML frameworks through `_bentoml_impl/frameworks/`:
- PyTorch, TensorFlow, XGBoost, LightGBM
- Scikit-learn, CatBoost, Diffusers, Transformers
- ONNX, Triton, and more

## Environment Variables

- `BENTOML_DEBUG=TRUE`: Enable debug logging
- `BENTOML_DO_NOT_TRACK`: Disable usage analytics
- `BENTOML_BUNDLE_LOCAL_BUILD=True`: Use local BentoML source in Bento builds
- `--verbose` CLI flag: Enable verbose output

## Key Development Notes

1. **Proto Files**: When editing gRPC proto files, run `./scripts/generate_grpc_stubs.sh` to regenerate Python stubs
2. **CI/CD**: GitHub Actions workflows in `.github/workflows/ci.yml`
3. **Version Management**: Uses hatchling with VCS-based versioning
4. **Type Checking**: Strict type checking enabled via pyright
5. **Python Versions**: Tests run on Python 3.9, 3.10, 3.11, 3.12

## Documentation

- **README.md**: Project overview and getting started guide
- **DEVELOPMENT.md**: Detailed development guide with setup instructions
- **docs/**: Full documentation source (Sphinx)