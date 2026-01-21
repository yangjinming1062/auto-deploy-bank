# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Compose is a machine learning tool for automated prediction engineering. It structures prediction problems and generates labels for supervised learning by automating the "Label" step of the ML pipeline (often the most time-consuming part of the process). The output is typically fed into Featuretools for feature engineering and then EvalML for AutoML.

## Key Dependencies

- **pandas**: Core data manipulation.
- **matplotlib**, **seaborn**, **tqdm**: Visualization and progress bars.
- **featuretools**, **woodwork**, **evalml**: Used for integration tests and the full ML workflow.

## Commands

### Install Development Environment
```bash
make installdeps  # Installs 'composeml[dev]' including testing and linting tools
```

### Running Tests
Tests are run using `pytest`.
```bash
make test         # Runs all tests in composeml/tests/ in parallel (-n auto)
make testcoverage # Runs tests with coverage reporting
pytest composeml/path/to/test_file.py::test_name # Run a single test
```

### Linting and Formatting
The project uses `black` and `ruff` for code quality.
```bash
make lint         # Check code quality (black check, ruff)
make lint-fix     # Auto-fix issues (black, ruff --fix)
```

### Building Documentation
Documentation is built using Sphinx with nbsphinx for notebooks.
```bash
pip install "composeml[docs]"
cd docs && make html
```

## Architecture

The library consists of three main components:

1. **LabelMaker** (`composeml/label_maker.py`): The primary user-facing class.
    - **`search()`**: The main entry point. It accepts a dataframe and generates `LabelTimes` by applying `labeling_function`(s) to `window_size` chunks of data sliced from the dataframe.
    - **`slice()`**: Returns a generator of `DataSlice` objects, useful for debugging or custom slicing logic.

2. **DataSlice** (`composeml/data_slice/`):
    - Represents a chunk of data extracted based on `window_size`.
    - Context object tracks metadata (e.g., `slice_start`, `slice_number`).

3. **LabelTimes** (`composeml/label_times/`):
    - A subclass of `pandas.DataFrame` that stores the generated labels and cutoff times.
    - Contains `search_settings` metadata.
    - Includes transformations like `threshold()`, `bin()`, `sample()`.

### Data Flow
1. User defines a `LabelMaker` with a target entity (e.g., `customer_id`) and a labeling function (e.g., "total spend in next hour").
2. User calls `label_maker.search(dataframe)`.
3. `search` uses `DataSliceGenerator` to iterate over the dataframe in windows.
4. For each slice, it applies the labeling function and appends results to a list.
5. Returns a `LabelTimes` object containing the training labels.

## Code Style & Patterns

- **Line Length**: 88 characters.
- **Imports**: Sorted by standard library, third-party, local application.
- **Type Hints**: Not strictly enforced everywhere but preferred for new code.
- **Doctests**: Enabled (`pytest --doctest-modules`). Docstrings often contain executable examples.