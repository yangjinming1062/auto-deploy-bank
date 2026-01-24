# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

miceforest is a Python library for Multiple Imputation by Chained Equations (MICE) using LightGBM. It fills in missing values in datasets through iterative predictive modeling.

## Commands

### Install Development Dependencies
```bash
poetry install --with dev --all-extras
```

### Run Tests
```bash
poetry run pytest
```

### Run Single Test File
```bash
poetry run pytest tests/test_ImputationKernel.py
```

### Run Type Checking
```bash
poetry run mypy miceforest --ignore-missing-imports
```

### Check Code Formatting
```bash
poetry run black miceforest tests --check
poetry run isort miceforest --diff
```

### Build Documentation
```bash
poetry run sphinx -b html docs docs/_build/html
```

### Build Package
```bash
poetry build
```

## Architecture

### Core Classes

**ImputedData** (`miceforest/imputed_data.py`)
- Base class that stores raw data and imputation values
- Handles storage of imputed values per variable, iteration, and dataset
- `complete_data(dataset, iteration)` - Returns dataset with imputed values filled in
- Uses parquet serialization for efficient pickle saving

**ImputationKernel** (`miceforest/imputation_kernel.py`)
- Extends ImputedData; main class users interact with
- Implements MICE algorithm via `mice(iterations)` method
- Stores trained LightGBM models: `self.models[(variable, iteration, dataset)]`
- Manages mean matching strategies (normal, fast, shap)
- Can impute new data with existing models: `impute_new_data(new_data)`

### Mean Matching Strategies
- **normal**: K-nearest-neighbors on predictions between candidates and bachelors
- **fast**: Random weighted selection by class probabilities (binary/categorical only)
- **shap**: K-nearest-neighbors on SHAP values (more robust)

### Key Data Structures
- `imputation_values`: Dict[variable, DataFrame] - Stores imputed values with MultiIndex (iteration, dataset)
- `na_where`: Dict[variable, np.ndarray] - Indices of missing values for each variable
- `variable_schema`: Dict[target, List[predictors]] - Feature-target relationships for modeling

### Module Responsibilities
- `default_lightgbm_parameters.py`: Default LGB params and parameter tuning space
- `utils.py`: Utility functions (ampute_data, stratification, hashing, random state management)
- `logger.py`: Timing and progress logging during MICE iterations

### sklearn Integration
ImputationKernel implements `fit()`/`transform()` for use in sklearn pipelines (requires `num_datasets=1`).

## Code Conventions

- Use `ensure_rng()` for random state management (handles int, RandomState, or None)
- Use `_expand_value_to_dict()` to normalize per-variable parameters
- LightGBM categorical columns must use `cat.codes` as labels (not category dtype)
- Parameter aliases are uncovered via `_ConfigAliases._get_all_param_aliases()`