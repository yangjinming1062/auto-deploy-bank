# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

OpenFL (Open Federated Learning) is a Python 3.6+ distributed machine learning framework developed by Intel. It enables organizations to collaborate on ML projects without sharing sensitive data - the model moves to meet the data. Supports TensorFlow, PyTorch, and other ML frameworks via task runners.

**Key Architecture:** Centralized aggregator pattern where:
1. Aggregator node coordinates the federation
2. Collaborator nodes train locally on private data
3. Model updates are aggregated centrally using mTLS encryption

## Build & Development Commands

```bash
# Install from source
pip install .

# Build wheel package
python setup.py sdist bdist_wheel

# Run tests
pytest tests/

# Lint code (max line length: 99)
flake8 .  # Excludes openfl/protocols

# Build documentation
cd docs && make html

# Build Docker image
bash scripts/build_base_docker_image.sh
```

## Key Entry Points

- **CLI command:** `fx` (entry point: `openfl.interface.cli:entry`)
- **Native API:** `openfl.native.native` - Functions: `setup_plan()`, `init()`, `run_experiment()`, `create_collaborator()`
- **Interactive API:** `openfl.interface.interactive_api` - Classes: `Federation`, `Experiment`

## Important Modules

| Path | Purpose |
|------|---------|
| `openfl/component/aggregator/` | Aggregator node implementation |
| `openfl/component/collaborator/` | Collaborator node implementation |
| `openfl/federated/task/` | ML framework adapters (TF, PyTorch, Keras, FastEstimator) |
| `openfl/transport/` | gRPC communication layer |
| `openfl/pipelines/` | Data compression/encoding (STC, KC, SKC) |

## Code Style Requirements

- **Copyright header required** on all files (Apache 2.0)
- **Docstrings required** on all public functions/classes (enforced by flake8-docstrings)
- **Max line length:** 99 characters (flake8)
- **Python versions:** 3.6 - 3.8

## Configuration

- Linting: `setup.cfg` (ignore W503, exclude `openfl/protocols`)
- Test dependencies: `requirements-test.txt`
- Linting dependencies: `requirements-linters.txt`

## Key Dependencies

- Click>=7.0 (CLI)
- grpcio==1.30.0 (gRPC transport)
- PyYAML>=5.4.1 (configuration)
- cryptography>=3.4.6 (mTLS encryption)
- cloudpickle (serialization)