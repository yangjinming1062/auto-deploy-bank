# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Sacred is a Python library for configuring, organizing, logging and reproducing machine learning experiments. It provides:
- Config Scopes and Injection for parameter management
- Command-line interfaces for running experiments with different settings
- Observers for logging experiment data to various backends (MongoDB, S3, file storage, etc.)
- Automatic seeding for reproducibility

## Development Setup

```bash
# Install in editable mode with dev dependencies
pip install -e .
pip install -r dev-requirements.txt

# Install pre-commit hooks (required for contributions)
pre-commit install

# Run pre-commit on all files
pre-commit run --all-files
```

If you encounter `ModuleNotFoundError: No module named 'distutils.spawn'`:
```bash
sudo apt-get update
sudo apt-get install python3-distutils
```

## Common Commands

### Testing
```bash
# Run tests with pytest
pytest

# Run specific test file
pytest tests/test_experiment.py

# Run tests on all Python versions (3.8-3.11) and dependency matrix
tox

# Run tests for specific Python version
tox -e py310

# Test specific dependency versions
tox -e numpy-121
tox -e tensorflow-216

# Run coverage check
pytest --cov sacred
tox -e coverage

# Using Makefile
make test          # Quick test run
make test-all      # Run all tests with tox
make coverage      # Generate coverage report
```

### Code Quality
```bash
# Check style with flake8
flake8 sacred

# Format code with black
black sacred/

# Using Makefile
make lint          # Check style with flake8
```

### Documentation & Packaging
```bash
# Generate Sphinx documentation
make docs

# Create distribution packages
make dist

# Build and upload release (maintainers only)
make release
```

### Cleaning
```bash
make clean         # Remove all build artifacts
make clean-build   # Remove build artifacts only
make clean-pyc     # Remove Python cache files
make clean-test    # Remove test artifacts
```

## Repository Structure

```
sacred/
├── __init__.py              # Main exports: Experiment, Ingredient, observers
├── experiment.py            # Experiment class - central entry point
├── ingredient.py            # Ingredient class - composable experiment components
├── run.py                   # Run class - manages experiment execution
├── commands.py              # Built-in CLI commands (help, config, etc.)
├── arg_parser.py            # Command-line argument parsing
├── dependencies.py          # Dependency tracking and management
├── config/                  # Configuration system
│   ├── config_scope.py      # @ex.config decorator
│   ├── captured_function.py # Function parameter injection
│   ├── signature.py         # Function signature inspection
│   ├── config_dict.py       # Configuration dictionary handling
│   └── ...
├── observers/               # Logging backends for experiments
│   ├── base.py              # Observer interface
│   ├── mongo.py             # MongoDB observer
│   ├── file_storage.py      # File-based storage observer
│   ├── s3_observer.py       # AWS S3 observer
│   ├── sql.py               # SQL database observer
│   └── ...
└── stflow/                  # Sacred TensorFlow integration
```

### Key Classes

- **Experiment** (`sacred/experiment.py:45`): Main class for creating experiments. Inherits from Ingredient.
- **Ingredient** (`sacred/ingredient.py:27`): Base class for composable experiment components. Experiments and ingredients can be nested.
- **Run** (`sacred/run.py:33`): Manages the execution of a single experiment run, handles configuration, observers, and result collection.
- **Observers**: Various backends for storing experiment data (see `sacred/observers/`)

## Architecture Overview

The library follows a layered architecture:

1. **Experiment Layer**: Users create `Experiment` instances and define main functions with `@ex.automain` decorator
2. **Configuration Layer**: `@ex.config` decorators define parameters, which are injected into functions automatically
3. **Execution Layer**: `Run` class orchestrates the experiment execution, capturing stdout, managing randomness, etc.
4. **Observer Layer**: Multiple observer implementations log run metadata to different backends (MongoDB, file system, S3, etc.)
5. **CLI Layer**: Command-line parsing and built-in commands for inspecting configs, dependencies, etc.

### Configuration System

Configuration is defined using the `@ex.config` decorator on functions. The return value becomes the configuration:

```python
@ex.config
def cfg():
    C = 1.0
    gamma = 0.7

@ex.automain
def run(C, gamma):
    # C and gamma are automatically injected
    pass
```

The configuration system inspects function signatures and automatically injects parameters by name (`sacred/config/signature.py:10`).

### Observer Pattern

Observers are attached to experiments and receive lifecycle events (started, completed, failed, etc.):

```python
ex.observers.append(MongoObserver(uri=uri, db_name=db))
```

Built-in observers include MongoDB, file storage, S3, SQL databases, and more (`sacred/observers/`).

## Testing Strategy

- Uses **pytest** for testing
- **tox** for testing across Python 3.8-3.11 and dependency matrices
- Test matrix includes numpy versions (1.20-2.0) and TensorFlow versions
- Pre-commit hooks enforce code style (black, flake8)
- Coverage tracking with `pytest-cov` and coveralls

Test files are in `tests/`, with organization matching the source structure.

## Dependencies

### Core Dependencies (requirements.txt)
- docopt-ng: CLI argument parsing
- jsonpickle: JSON serialization
- munch: Dictionarydot access
- wrapt: Decorators and proxies
- py-cpuinfo: CPU information
- colorama: Cross-platform colored terminal text
- packaging: Version handling
- GitPython: Git integration

### Optional Dependencies
- numpy: For numerical operations support
- pymongo: For MongoDB observer
- tensorflow: For TensorFlow integration

## Code Style & Standards

- **Formatting**: black (configured in `pyproject.toml`)
- **Linting**: flake8 with pep8-naming and flake8-docstrings
- **Docstrings**: NumPy style, but prefer Python type hints over type annotations in docstrings
- **Type hints**: Used throughout the codebase

Example docstring format (from CONTRIBUTING.rst:48-70):
```python
def add(a: int, b: int) -> int:
    """Add two numbers.

    Parameters
    ----------
    a
        The first number.
    b
        The second number.

    Returns
    -------
    The sum of the two numbers.
    """
    return a + b
```

## Documentation

- Main documentation: https://sacred.readthedocs.io/
- Source code documentation via Sphinx
- Examples in `examples/` directory
- Docker examples in `examples/docker/`

## Contribution Guidelines

- Create a branch: `git checkout -b name-of-your-bugfix-or-feature`
- Run full test suite: `tox`
- Ensure pre-commit hooks pass: `pre-commit run --all-files`
- Update documentation for new features
- Include tests for new functionality
- Pull requests should work for all Python versions in setup.py

## GitHub Actions CI/CD

Automated tests run on:
- Python 3.8-3.11
- Ubuntu, macOS, Windows
- Dependency matrix (numpy 1.20-2.0, TensorFlow 2.12-2.16)
- Pre-commit validation
- Coverage reporting

## Notable Implementation Details

- **Automatic seeding**: `sacred/randomness.py:10` provides reproducible randomness
- **Stdout capturing**: `sacred/stdout_capturing.py:10` captures and optionally stores output
- **Host info gathering**: `sacred/host_info.py:10` collects system information
- **Metrics logging**: `sacred/metrics_logger.py:10` handles experiment metrics