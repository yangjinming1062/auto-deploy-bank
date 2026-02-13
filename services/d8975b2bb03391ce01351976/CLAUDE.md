# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Qlib is Microsoft's AI-oriented Quantitative Investment Platform. It provides a full ML pipeline for quantitative investment including data processing, model training, backtesting, and portfolio analysis. Supports supervised learning, market dynamics modeling, and reinforcement learning paradigms.

## Development Commands

### Setup and Installation
```bash
# Build Cython extensions (required before installation)
make prerequisite

# Install package in editable mode with all dependencies
make dev  # installs .[dev,lint,docs,package,test,analysis,rl,pywinpty]

# Install specific dependency groups
make dependencies    # core package
make lightgbm        # LightGBM support
make rl              # reinforcement learning deps (tianshou, torch)
make lint            # linting tools (black, pylint, mypy, flake8, nbqa)
make test            # test dependencies
make analysis        # analysis dependencies (plotly, statsmodels)
make client          # client dependencies (socketio, tables)
```

### Linting
```bash
make lint                    # Run all linters
make black                   # Black formatting check
make pylint                  # Pylint check (qlib and scripts dirs)
make flake8                  # Flake8 check
make mypy                    # Type checking
make nbqa                    # Jupyter notebook linting
make nbconvert               # Execute notebooks for validation
```

### Testing
```bash
# Install test dependencies first
make test

# Run all tests
pytest tests/ -m "not slow"  # Exclude slow tests

# Run specific test file
pytest tests/test_workflow.py -v

# Run specific test category
pytest tests/data_mid_layer_tests/
pytest tests/dataset_tests/
pytest tests/model/
pytest tests/ops/

# Run with coverage
pytest tests/ --cov=qlib
```

### Building and Releasing
```bash
make build     # Build wheel package
make upload    # Upload to PyPI
make docs-gen  # Generate documentation
```

### Cleanup
```bash
make clean      # Remove intermediate files
make deepclean  # Remove everything including venv
```

## Architecture

### Core Modules (`qlib/`)

- **`data/`** - Data storage, processing, and caching
  - `data.py` - Main Data module interface (`D` object)
  - `cache.py` - Expression caching system
  - `ops.py` - Built-in factor operators (158+ expressions)
  - `dataset/` - Dataset handling with `DatasetH` and `TSDatasetH`
  - `dataset/handler.py` - `DataHandler` for feature engineering
  - `_libs/` - Cython extensions for performance

- **`model/`** - ML forecast models
  - `trainer.py` - Model training utilities
  - `base.py` - Base model interface
  - `ens/` - Ensemble models
  - `meta/` - Meta-learning models
  - `interpret/` - Model interpretation

- **`rl/`** - Reinforcement learning framework
  - `simulator.py` - Trading environment simulation
  - `order_execution/` - Order execution strategies (TWAP, PPO, OPDS)
  - `trainer/` - RL trainers (PPO, SAC, etc.)

- **`backtest/`** - Backtesting engine
  - `executor.py` - Strategy execution
  - `exchange.py` - Order matching simulation
  - `position.py` - Portfolio position management
  - `report.py` - Performance reporting

- **`strategy/`** - Trading strategies (TopkDropoutStrategy, etc.)

- **`workflow/`** - Experiment tracking and task management
  - `__init__.py` - `R` object for experiment management (wraps MLflow)
  - `recorder.py` - `Recorder` class for logging experiments
  - `record_temp.py` - `SignalRecord`, `SigAnaRecord`, `PortAnaRecord`

- **`contrib/`** - Community-contributed components
  - `data/handler.py` - Alpha158 and Alpha360 handlers
  - `model/` - GBDT, LSTM, Transformer models
  - `strategy/` - Strategy implementations

### Configuration Patterns

**Workflow YAML Config** (`examples/benchmarks/*/workflow_config_*.yaml`):
```yaml
qlib_init:           # qlib.init() config
    provider_uri: path
    region: cn|us

task:
    model:           # Model class and kwargs
        class: LGBModel
        module_path: qlib.contrib.model.gbdt
    dataset:         # Dataset and handler config
        class: DatasetH
        module_path: qlib.data.dataset
        handler:
            class: Alpha158
            module_path: qlib.contrib.data.handler
    record:          # Record modules to run
        - class: SignalRecord
        - class: SigAnaRecord
        - class: PortAnaRecord
```

**Key config classes**:
- `qlib.config.C` - Global configuration
- `qlib.data.D` - Data interface
- `qlib.workflow.R` - Experiment recorder

### Data Flow

1. **`qlib.init(provider_uri=...)`** - Initialize with data path
2. **`D.features(instruments, fields, ...)`** - Load features
3. **`DatasetH`** with **`DataHandler`** - Process and segment data
4. **`Model.fit(dataset)`** - Train model
5. **`Recorder`** - Log experiment artifacts
6. **`Strategy` + `Executor`** - Backtest and evaluate

### Offline vs Online Mode

- **Offline mode** (default): Data stored locally in `~/.qlib/qlib_data/`
- **Online mode**: Data served via Qlib-Server with shared caching

### Expression Syntax

The data layer uses expressions for computing features:
- Raw fields: `$close`, `$volume`, `$high`, `$low`, `$open`
- Time-series: `Ref($close, 1)` (previous value), `Ref($close, n)`
- Rolling aggregations: `Mean($close, 3)`, `Std($close, 5)`, `Max($high, 10)`
- Arithmetic: `$close/$open - 1`, `$high - $low`

Expressions are parsed and cached for performance. Use `D.features(instruments, fields, ...)` to load data.

## Key CLI Commands

```bash
# Download data (China market, daily frequency)
python -m qlib.cli.data qlib_data --target_dir ~/.qlib/qlib_data/cn_data --region cn

# Download 1min data
python -m qlib.cli.data qlib_data --target_dir ~/.qlib/qlib_data/cn_data_1min --region cn --interval 1min

# Run automated workflow
qrun examples/benchmarks/LightGBM/workflow_config_lightgbm_Alpha158.yaml
```

## Code Style

- Line length: 120 characters (black formatter)
- Pre-commit hooks: black, flake8
- Type hints: mypy for type checking
- Docstrings: NumPy style preferred

## Important Notes

- Python 3.8-3.12 supported, pandas>=1.1 (note: pandas 2.0+ deprecations apply)
- Cython extensions (`qlib/data/_libs/`) must be built before use (`make prerequisite`)
- Torch models require numpy<2.0 on macOS M1
- RL dependencies need `tianshou<=0.4.10` with torch