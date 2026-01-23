# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build, Test, and Development Commands

```bash
# Install package in development mode
make develop

# Run all tests
make test
pytest

# Run a single test file
pytest tests/test_reader.py

# Run a specific test
pytest tests/test_reader.py::test_function_name

# Check code coverage (Linux + Python 3.7 only)
coverage run -m --source=../mlbox/ pytest
coverage html

# Build distribution packages
make dist

# Generate documentation
make docs

# Clean build artifacts
make clean
```

## Project Overview

MLBox is a powerful Automated Machine Learning (AutoML) Python library for classification and regression tasks. It provides a complete ML pipeline: data reading/preprocessing, hyperparameter optimization, and prediction.

## Architecture

### Main Components

The library is organized around 4 core classes exposed at the top level (`from mlbox import *`):

1. **Reader** (`mlbox.preprocessing.Reader`) - Reads and cleans data from CSV/XLS/JSON/H5 files, handles missing values, converts data types, and extracts date features. Creates train/test splits automatically based on target presence.

2. **Optimiser** (`mlbox.optimisation.Optimiser`) - Optimizes hyper-parameters using Tree Parzen Estimator (hyperopt). Evaluates the full ML pipeline with cross-validation.

3. **Predictor** (`mlbox.prediction.Predictor`) - Fits the final model and generates predictions with feature importance plots.

4. **Encoders** - Two transformers used in the pipeline:
   - `NA_encoder` - Handles missing values (numerical: mean/median/constant, categorical: "<NULL>"/most_frequent)
   - `Categorical_encoder` - Encodes categorical features (label_encoding, dummification, random_projection, entity_embedding)

### Pipeline Structure

The ML pipeline follows this sequence:
```
Data → NA_encoder → Categorical_encoder → [Feature_selector] → [Stacking layers] → Estimator
```

- Feature selection and stacking are optional
- Multiple stacking layers can be added (`stck0`, `stck1`, etc.)
- Parameter syntax: `"ne__numerical_strategy"`, `"ce__strategy"`, `"fs__threshold"`, `"est__max_depth"`

### Model Directory Structure

```
mlbox/model/
├── classification/
│   ├── classifier.py    # Wrapper for sklearn/LightGBM classifiers
│   ├── feature_selector.py  # Variance/RF-based feature selection
│   └── stacking_classifier.py
└── regression/
    ├── regressor.py
    ├── feature_selector.py
    └── stacking_regressor.py
```

Both classification and regression have parallel implementations with identical interfaces.

### Key Dependencies

- **hyperopt** - Hyperparameter optimization (TPE algorithm)
- **tensorflow** - Entity embedding neural networks for categorical encoding
- **lightgbm** - Gradient boosting models
- **scikit-learn** - Base ML models and utilities
- **pandas** - Data manipulation

## Typical Workflow

```python
from mlbox.preprocessing import Reader
from mlbox.optimisation import Optimiser
from mlbox.prediction import Predictor

# 1. Read and prepare data
reader = Reader(sep=",")
data = reader.train_test_split(paths=["train.csv", "test.csv"], target_name="target")

# 2. Optimize hyperparameters
opt = Optimiser(scoring="accuracy", n_folds=3)
space = {
    "ne__numerical_strategy": {"search": "choice", "space": ["mean", "median"]},
    "ce__strategy": {"search": "choice", "space": ["label_encoding"]},
    "est__strategy": {"search": "choice", "space": ["LightGBM", "RandomForest"]}
}
best_params = opt.optimise(space, data)

# 3. Train and predict
pred = Predictor()
pred.fit_predict(best_params, data)
```

## Target Encoding

- Classification: target is encoded as `int` dtype
- Regression: target is encoded as `float` dtype
- Target encoder is saved to `save/target_encoder.obj` during reading and must be present for prediction

## Important Notes

- The Optimiser saves fitted models to `save/joblib/` - clear this directory regularly
- Target dtype determines task type (int=classification, float=regression)
- Feature importances are saved to the output directory with leak detection warnings
- Parallel processing is used via joblib for data cleaning on non-Windows platforms