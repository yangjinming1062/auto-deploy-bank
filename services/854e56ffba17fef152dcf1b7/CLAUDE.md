# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Poutyne is a simplified framework for PyTorch that handles boilerplate training code. It provides a `Model` class that encapsulates a PyTorch network, optimizer, loss function, and metrics - similar to Keras. Key features include callbacks for early stopping, checkpointing, logging, and a `ModelBundle` class for automatic experiment management.

## Common Commands

```bash
# Install development dependencies
pip install -r tests/requirements.txt
pip install -r styling_requirements.txt
pip install -r docs/requirements.txt
python setup.py develop

# Run all tests (with coverage)
pytest tests

# Run a single test file
pytest tests/framework/callbacks/test_earlystopping.py

# Run a specific test
pytest tests/framework/callbacks/test_earlystopping.py::test_some_function

# Code formatting and linting
black .
isort .
flake8 poutyne tests
pylint poutyne tests

# Run pre-commit hooks
pre-commit run --all-files

# Build documentation
cd docs && ./rebuild_html_doc.sh
```

## Architecture

### Core Modules

- **`poutyne/framework/model.py`**: Central `Model` class handling training loop, evaluation, and prediction. Wraps PyTorch modules with epoch/step logic and manages batch/epoch metrics.
- **`poutyne/framework/model_bundle.py`**: `ModelBundle` class for end-to-end experiments with automatic checkpointing, logging, and reproducibility.
- **`poutyne/framework/experiment.py`**: `Experiment` class for version-controlled experiment tracking.
- **`poutyne/framework/callbacks/`**: Callback system for customizing training behavior. Key callbacks:
  - `Callback` (base class) in `callbacks.py` with hooks like `on_epoch_end`, `on_batch_end`
  - `best_model_restore.py` - restore best model checkpoint
  - `checkpoint.py` - periodic checkpoint saving
  - `earlystopping.py` - early stopping based on metric
  - `logger.py` - CSV logging
  - `mlflow_logger.py`, `wandb_logger.py` - experiment tracking integrations
- **`poutyne/framework/metrics/`**: Metric system supporting batch metrics (per-batch computation) and epoch metrics (end-of-epoch computation). Integrates with `torchmetrics`.
- **`poutyne/framework/iterators.py`**: `EpochIterator` and `StepIterator` for managing training/evaluation loops.
- **`poutyne/utils.py`**: Utility functions like `TensorDataset`, batch helpers.
- **`poutyne/plotting.py`**: Training curve plotting utilities.

### Test Structure

Tests mirror the package structure under `tests/`:
- `tests/framework/callbacks/` - Callback tests
- `tests/framework/model/` - Model tests
- `tests/framework/metrics/` - Metric tests
- `tests/framework/experiment/` - Experiment tests
- `tests/test_utils.py`, `tests/test_plotting.py` - Utility tests

All tests use pytest with coverage enabled by default (`--cov`).

## Code Style

- **Formatting**: Black with 120 char line length, isort for imports
- **Linting**: flake8 and pylint (see `.pylintrc` for custom rules)
- **Pre-commit hooks**: Defined in `.pre-commit-config.yaml`
- All Python files include LGPLv3 copyright headers

## Key Conventions

- Branch from `dev` branch for contributions
- String formatting with f-strings (Python 3.8+)
- Type hints used throughout
- All public APIs have docstrings following numpy-style format
- Metrics can be functions, `poutyne.Metric` objects, or `torchmetrics.Metric` objects
- Callbacks receive `params` dict with `epoch` and `steps_per_epoch` keys