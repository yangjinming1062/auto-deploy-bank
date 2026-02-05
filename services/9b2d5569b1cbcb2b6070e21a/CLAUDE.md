# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Feature Selector is a Python library for dimensionality reduction of machine learning datasets. It provides a single `FeatureSelector` class that identifies features to remove using five methods:

1. **Missing Values** - Features with missing percentage above a threshold
2. **Single Unique Values** - Features with only one unique value
3. **Collinear Features** - Features with pairwise correlation above a threshold
4. **Zero Importance Features** - Features with zero importance from a LightGBM model
5. **Low Importance Features** - Features not needed for cumulative importance threshold

## Commands

### Install dependencies
```bash
pip install -r requirements.txt
pip install -e .  # Install package in editable mode for development
```

### Run Jupyter notebooks for examples and testing
```bash
jupyter notebook "Feature Selector Usage.ipynb"
jupyter notebook "Testing.ipynb"
```

### Testing
No automated test suite exists. Manual testing is done via `Testing.ipynb` notebook.

## Architecture

The library has a simple structure:

- `feature_selector/feature_selector.py` - Main `FeatureSelector` class (~688 lines)
- `feature_selector/__init__.py` - Exports the `FeatureSelector` class
- `data/` - Sample datasets for testing (e.g., `credit_example.csv`, `AirQualityUCI.csv`)

### FeatureSelector Class Design

The class follows a two-phase pattern:

1. **Identify phase**: Methods like `identify_missing()`, `identify_collinear()`, etc. detect features to remove and store results in:
   - `self.ops` - Dictionary mapping method names to lists of features to drop
   - `self.record_*` - DataFrames with detailed records for each method
   - `self.feature_importances` - Sorted importances from LightGBM

2. **Remove phase**: Methods like `check_removal()` and `remove()` use the identified features to return cleaned data.

Key attributes:
- `self.data` - Original input DataFrame
- `self.data_all` - DataFrame with one-hot encoded features (created during importance-based methods)
- `self.one_hot_features` - List of one-hot encoded column names
- `self.base_features` - Original column names before one-hot encoding

The `remove()` method handles several scenarios:
- Using `'all'` methods or specific method names
- Including/excluding one-hot encoded features with `keep_one_hot` parameter
- Automatically switches between `self.data` and `self.data_all` based on methods used

### Dependencies

- `lightgbm` - Gradient boosting for feature importance calculation
- `pandas`, `numpy` - Data manipulation
- `scikit-learn` - Train/test split, permutation importance
- `matplotlib`, `seaborn` - Visualization methods

### Usage Pattern

```python
from feature_selector import FeatureSelector

fs = FeatureSelector(data=df, labels=labels)

# Run individual methods
fs.identify_missing(missing_threshold=0.5)
fs.identify_single_unique()
fs.identify_collinear(correlation_threshold=0.9)
fs.identify_zero_importance(task='classification', eval_metric='auc')
fs.identify_low_importance(cumulative_importance=0.99)

# Or run all at once
fs.identify_all(selection_params={
    'missing_threshold': 0.5,
    'correlation_threshold': 0.9,
    'eval_metric': 'auc',
    'task': 'classification',
    'cumulative_importance': 0.99
})

# Check identified features
features_to_remove = fs.check_removal()

# Remove features
clean_data = fs.remove(methods='all')
```