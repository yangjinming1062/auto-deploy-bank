# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

sklearn-genetic-opt is a scikit-learn compatible library for hyperparameter tuning and feature selection using evolutionary algorithms (EAs). It uses [DEAP](https://deap.readthedocs.io/) for the evolutionary computation backbone.

## Commands

```bash
# Install development dependencies
pip install -r dev-requirements.txt -e .

# Run tests (95% coverage minimum)
pytest sklearn_genetic

# Format code with black
black sklearn_genetic/

# Run a single test file
pytest sklearn_genetic/tests/test_genetic_search.py
```

## Architecture

### Main Classes

- **`GASearchCV`** (`genetic_search.py`): Extends sklearn's `BaseSearchCV` for hyperparameter optimization. Individuals represent hyperparameter sets. Fitness is the CV score.
- **`GAFeatureSelectionCV`** (`genetic_search.py`): Extends `MetaEstimatorMixin` and `SelectorMixin` for feature selection. Individuals are binary arrays representing feature selection. Fitness is a tuple of (CV score, -num_features).

### Module Structure

- **`algorithms.py`**: Evolutionary algorithm implementations (eaSimple, eaMuPlusLambda, eaMuCommaLambda). Each algorithm function accepts callbacks for early stopping/logging.
- **`space/`**: Search space definitions - `Integer`, `Continuous`, `Categorical` classes define parameter distributions. `Space` class wraps param_grid.
- **`callbacks/`**: Callbacks invoked after each generation:
  - Early stopping: `ThresholdStopping`, `ConsecutiveStopping`, `DeltaThreshold`, `TimerStopping`
  - Logging: `ProgressBar`, `LogbookSaver`, `TensorBoard`
  - Checkpointing: `ModelCheckpoint`
- **`schedules/`**: Adaptive parameter schedulers for mutation/crossover probabilities:
  - `ConstantAdapter`, `ExponentialAdapter`, `InverseAdapter`, `PotentialAdapter`
- **`utils/`**: Helper utilities for DEAP operations, CV results formatting, random individuals.

### Key Integration Points

1. **DEAP Integration**: Both classes use `base.Toolbox`, `creator.FitnessMax`, and DEAP statistics/logbook. The `evaluate()` method calls `cross_validate()`.
2. **Sklearn Compatibility**: Implements sklearn's estimator protocol (fit, predict, score). Supports classifier, regressor, and outlier detector types.
3. **MLflow**: `mlflow_log.py` provides `MLflowConfig` for logging parameters, scores, and artifacts.
4. **Caching**: Fitness caching avoids re-evaluating duplicate individuals via `fitness_cache` dict.

### Code Conventions

- Fitness values are lists (DEAP requirement): `[score]` or `[score, secondary_metric]`
- `criteria="max"`/`"min"` determines optimization direction via `criteria_sign`
- Callbacks receive `estimator` reference to access state mid-evolution
- Tests use `sklearn.datasets` fixtures; verify attributes after `fit()`