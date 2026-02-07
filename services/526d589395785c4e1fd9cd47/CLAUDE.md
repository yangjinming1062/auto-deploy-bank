# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands

```bash
# Install in development mode
pip install .

# Build wheel from source
python setup.py bdist_wheel

# Build with Jupyter widget JS (requires nodejs/npm)
BUILD_JS=1 pip install -e .

# Install protobuf compiler (required for building protos)
apt install protobuf-compiler
```

## Test Commands

```bash
# Run all tests
python -m unittest discover -p "*_test.py"

# Run a specific test file
python -m unittest tensorflow_model_analysis.evaluators.evaluator_test

# Run a specific test class
python -m unittest tensorflow_model_analysis.evaluators.evaluator_test.EvaluatorTest

# Run a specific test method
python -m unittest tensorflow_model_analysis.evaluators.evaluator_test.EvaluatorTest.test_evaluator
```

## Linting

```bash
# Install pre-commit hooks
pre-commit install --install-hooks

# Run pre-commit on all files
pre-commit run --all-files

# Run ruff linting directly
ruff check .
ruff format .
```

## Architecture Overview

TensorFlow Model Analysis (TFMA) is a library for evaluating TensorFlow models using Apache Beam pipelines for distributed computation.

### Pipeline Flow
The evaluation pipeline consists of four main stages:

1. **Read Inputs**: Converts raw inputs (tf.train.Example, CSV, JSON) into extracts
2. **Extraction**: Runs a series of `Extractor` transforms that add data to extracts
3. **Evaluation**: Runs `Evaluator` transforms that produce evaluation outputs
4. **Write Results**: Writes evaluation results to disk using `Writer` transforms

### Core Data Types

**Extracts** (`Dict[Text, Any]`): Data extracted during pipeline processing, stored in a `PCollection`. Standard keys defined in `constants.py`:
- `INPUT_KEY` ("input"): Raw input bytes
- `FEATURES_KEY` ("features"): Raw features
- `LABELS_KEY` ("labels"): Labels
- `PREDICTIONS_KEY` ("predictions"): Model predictions
- `EXAMPLE_WEIGHTS_KEY` ("example_weights"): Example weights
- `SLICE_KEYS_KEY` ("slice_keys"): Slice key assignments

**Evaluation** (`Dict[Text, PCollection]`): Output from evaluators. Standard keys:
- `METRICS_KEY` ("metrics"): Computed metrics
- `PLOTS_KEY` ("plots"): Plot data
- `ANALYSIS_KEY` ("analysis"): Full extracts for analysis
- `VALIDATIONS_KEY` ("validations"): Validation results

### Key Components

- **Extractors** (`tensorflow_model_analysis/extractors/`): Transform extracts (e.g., `InputExtractor`, `PredictExtractor`, `SliceKeyExtractor`)
- **Evaluators** (`tensorflow_model_analysis/evaluators/`): Produce evaluations from extracts (e.g., `MetricsAndPlotsEvaluator`, `AnalysisTableEvaluator`)
- **Writers** (`tensorflow_model_analysis/writers/`): Serialize and write evaluation output (e.g., `MetricsAndPlotsWriter`)
- **Metrics** (`tensorflow_model_analysis/metrics/`): Post-export metrics computations
- **Slicer** (`tensorflow_model_analysis/slicer/`): Slice key generation and handling
- **View** (`tensorflow_model_analysis/view/`): Visualization and result rendering

### Main Entry Points

- `run_model_analysis()` in `api/model_eval_lib.py`: Primary high-level API for running evaluations
- `default_extractors`, `default_evaluators`, `default_writers`: Default configurations
- Configuration via `EvalConfig` with `SlicingSpec`, `MetricsSpec`, `ModelSpec`

### Important Files

- `tensorflow_model_analysis/__init__.py`: Public API exports
- `tensorflow_model_analysis/constants.py`: Extract/Evaluation keys and constants
- `docs/architecture.md`: Detailed architecture documentation
- `setup.py`: Build configuration, proto generation
- `tensorflow_model_analysis/proto/`: Protocol buffer definitions

### Dependencies

- TensorFlow (required)
- Apache Beam for distributed pipeline execution (local mode by default, supports Dataflow)
- Apache Arrow for internal data representation
- Jupyter widgets for notebook visualization
- Protobuf for serialization

### Proto Compilation

Protos are auto-generated during build via `setup.py`. Proto files are in `tensorflow_model_analysis/proto/`:
- `config.proto`: Evaluation configuration
- `metrics_for_slice.proto`: Metrics serialization
- `validation_result.proto`: Validation results

To regenerate: Run `python setup.py build_py` or `pip install .`