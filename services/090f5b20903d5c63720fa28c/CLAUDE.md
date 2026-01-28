# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Libra is an ergonomic machine learning library for non-technical users. It provides a simple query-based API where users pass natural language instructions and Libra automatically selects and trains appropriate ML models.

## Commands

```bash
# Install dependencies and package
pip install -r requirements.txt
pip install .

# Run all tests
python -m unittest discover ./tests "tests.py"

# Run a single test
python -m unittest tests.TestQueries.test_regression_ann
```

## Architecture

### Entry Point
The `client` class in `libra/queries.py` is the main user-facing API. It:
- Takes a dataset path (CSV file or image folder) on initialization
- Provides `*_query()` methods for different ML tasks
- Stores all model results in `self.models` dictionary (keyed by model name like `'regression_ANN'`, `'svm'`, etc.)
- Tracks `self.latest_model` to enable method chaining

### Query Methods (in `libra/query/`)
- **classification_models.py**: K-means, SVM, nearest neighbors, decision tree, XGBoost
- **feedforward_nn.py**: Regression ANN, classification ANN, convolutional neural networks
- **nlp_queries.py**: Text classification, summarization, image captioning, NER, text generation
- **supplementaries.py**: `tune_helper()` for hyperparameter tuning via keras-tuner
- **generative_models.py**: DCGAN implementation
- **recommender_systems.py**: Content-based recommender

### Preprocessing Pipeline (`libra/preprocessing/`)
- **data_preprocessor.py**: `initial_preprocessor()` handles train/test splitting and sklearn pipelines
- Uses `ColumnTransformer` with separate pipelines for numeric, categorical (with optional CA for high-cardinality), and text columns
- Text preprocessing includes lemmatization, stopword removal, and spell correction

### Model Creation (`libra/modeling/`)
- **prediction_model_creation.py**: `get_keras_model_reg()` and `get_keras_model_class()` create feedforward architectures
- **tuner.py**: `tuneReg()`, `tuneClass()`, `tuneCNN()` use keras-tuner for hyperparameter optimization

### Return Format
Model query functions return dictionaries with structure:
```python
{
    'id': 'uuid',
    'model': trained_model,
    'target': 'target_column_name',
    'preprocessor': fitted_pipeline,
    'interpreter': label_encoder,  # for classification inverse transform
    'test_data': {'X': X_test, 'y': y_test},
    'plots': {},  # if generate_plots=True
    'accuracy': {...},
    'losses': {...}
}
```

### Utilities
- **logger()**: Hierarchical logging function duplicated across modules - prints indented progress
- **clearLog()**: Resets logger counter, called at end of most methods
- **DataReader** (`data_reader.py`): Handles CSV and image folder reading

## Key Patterns

1. **Model Storage**: All queries append to `client.models` dict; same client can run multiple queries
2. **Preprocessing**: Uses sklearn `Pipeline` and `ColumnTransformer` fitted during training, stored for inference
3. **Label Encoding**: Custom label encoder needed due to train/test split to preserve inverse transform capability
4. **Dimensionality Reduction**: Uses Multiple Correspondence Analysis (MCA via `prince`) when categorical columns have too many unique values (>25% of dataset size)
5. **NLP Pipeline**: Text columns use TF-IDF vectorization then custom sum embedding before feeding to models