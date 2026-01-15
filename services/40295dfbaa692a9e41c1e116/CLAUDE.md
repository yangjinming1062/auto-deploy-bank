# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

scikit-multiflow is a machine learning framework for streaming data in Python. It follows an incremental learning paradigm where models are updated continuously rather than trained in batches. The project is being merged into [River](https://github.com/online-ml/river/).

## Commands

```bash
# Install in editable mode for development
pip install -e .

# Run all tests
pytest tests --showlocals -v

# Run a single test file
pytest tests/some_module/some_file.py --showlocals -v

# Run tests with coverage
pytest --cov=skmultiflow tests --showlocals -v

# Generate documentation (from docs/ directory)
make html

# Check code style (flake8 max-line-length=99)
flake8
```

## Architecture

### Core Design Patterns

**Estimators (classifiers/regressors)** inherit from `BaseEstimator` and mixins:
- `ClassifierMixin`: Requires `partial_fit()`, `predict()`, `predict_proba()`
- `RegressorMixin`: Requires `partial_fit()`, `predict()`, `predict_proba()`

All estimators support incremental learning via `partial_fit()` rather than batch `fit()`.

**Streams** inherit from `Stream` (in `skmultiflow.core.base.Stream`) and provide:
- `next_sample(batch_size=1)`: Returns `(X, y)` tuple
- `restart()`: Reset stream state
- Stream metadata: `n_features`, `n_targets`, `target_values`, etc.

### Key Modules

| Module | Purpose |
|--------|---------|
| `skmultiflow.core` | Base classes (`BaseEstimator`, `BaseSKMObject`), mixins, pipeline |
| `skmultiflow.data` | Stream generators (e.g., `SEAGenerator`, `RandomRBFGenerator`) |
| `skmultiflow.trees` | Hoeffding trees and variants for streaming |
| `skmultiflow.meta` | Ensemble methods (leveraging bagging, boosting, etc.) |
| `skmultiflow.evaluation` | Evaluators: `EvaluatePrequential`, `EvaluateHoldout` |
| `skmultiflow.drift_detection` | Drift detectors (`ADWIN`, `DDM`) |
| `skmultiflow.utils.validation` | `check_random_state()` for RNG |

### Standard Incremental Learning Loop

```python
from skmultiflow.data import SEAGenerator
from skmultiflow.bayes import NaiveBayes

stream = SEAGenerator(random_state=1)
estimator = NaiveBayes(nominal_attributes=None)

while n_samples < max_samples and stream.has_more_samples():
    X, y = stream.next_sample()
    y_pred = estimator.predict(X)
    estimator.partial_fit(X, y)
```

## Code Style

- **PEP 8** compliance with max line length 99
- **Docstrings**: NumPy/SciPy format (see CONTRIBUTING.md)
- **Random state**: Use `skmultiflow.utils.validation.check_random_state()`
- **Naming**: `<method_name> + <type>` (e.g., `HoeffdingTreeClassifier`)
- Include code examples in docstrings under "Examples" section