# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

TensorFlow Model Analysis (TFMA) is a library for evaluating TensorFlow models. It computes metrics over different slices of data and supports distributed computation via Apache Beam.

## Development Commands

```bash
# Install package in development mode (requires protoc)
pip install -e .

# Run all unit tests
python -m unittest discover -p "*_test.py"

# Run a single test file
python -m unittest tensorflow_model_analysis.api.model_eval_lib_test

# Run a specific test class
python -m unittest tensorflow_model_analysis.api.model_eval_lib_test.EvalResultTests

# Run pre-commit hooks
pre-commit run --all-files

# Build wheel distribution
python setup.py bdist_wheel
```

**Note**: Requires `protoc` (Protocol Buffer compiler) to generate `_pb2.py` files from `.proto` files during build.

## Code Architecture

### Pipeline Design Pattern

TFMA uses an **Extractors → Evaluators → Writers** pipeline architecture:

1. **Extractors** (`extractors/`): Transform raw input data into `Extracts` containing features, predictions, labels, and other artifacts
2. **Evaluators** (`evaluators/`): Compute metrics, plots, and validations from extracts
3. **Writers** (`writers/`): Write evaluation results to outputs (files, BigQuery, etc.)

### Key Modules

| Module | Purpose |
|--------|---------|
| `api/model_eval_lib.py` | Main public API (`run_model_analysis`, `analyze_raw_data`, etc.) |
| `api/types.py` | Core data types (`EvalSharedModel`, `Extracts`, `FeaturesPredictionsLabels`) |
| `metrics/` | Metric implementations (confusion matrices, calibration, BLEU, etc.) |
| `slicer/` | Slice specification and extraction for sub-population analysis |
| `view/` | Visualization utilities and result types (`EvalResult`) |
| `proto/` | Protocol Buffer definitions for config and results |

### Data Flow

```
Input Data → Extractors → Extracts → Evaluators → Metrics/Plots → Writers → Output
                                    ↓
                              Validations
```

### Evaluator Types

- **MetricsPlotsAndValidationsEvaluator**: Main evaluator computing metrics, plots, and model validations
- **KerasEvaluator**: Handles Keras/TensorFlow 2.x models
- **LegacyEvaluator**: Support for TF 1.x estimators

### Configuration

Configuration is defined in Protocol Buffers (`config.proto`, `metrics_for_slice.proto`, `validation_result.proto`). Use `EvalConfig` to specify:
- Model specifications (`ModelSpec`)
- Metrics specifications (`MetricsSpec`)
- Slicing specifications (`SlicingSpec`)

## Linting & Style

Uses `ruff` for linting (configured in `pyproject.toml`) and `pre-commit` hooks. Key rules:
- Line length: 88 characters (ruff-format)
- Type annotations: Required for public functions (many ignored in practice)
- Docstrings: pydocstyle (D rules)

## Testing Patterns

- Tests follow `*_test.py` naming convention
- Use `unittest` framework (not pytest)
- Test utilities in `tensorflow_model_analysis/utils/test_util.py`
- Integration tests use Apache Beam pipelines

## Key Dependencies

- **TensorFlow**: Model loading and inference
- **Apache Beam**: Distributed computation (local mode by default, supports Dataflow)
- **Apache Arrow**: Internal data representation
- **pandas/numpy**: Data manipulation
- **tfx-bsl**: TFX BSL integration

## Common Tasks

### Adding a New Metric

1. Create metric class in `metrics/`
2. Inherit from appropriate base class in `metric_types.py`
3. Add to `metric_specs.py` to enable via config
4. Add tests for the metric

### Adding a New Extractor

1. Create extractor class inheriting from `extractor.Extractor`
2. Implement `extract` method returning `Extracts`
3. Add to `default_extractors()` in `model_eval_lib.py`