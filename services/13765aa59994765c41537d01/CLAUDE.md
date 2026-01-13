# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

TNT (torchtnt) is a PyTorch library providing training tools and utilities. The library offers a Unit-based architecture for building flexible training loops with support for callbacks, automatic optimization, and distributed training.

## Common Development Commands

### Installation
```bash
# Install in editable mode for development
pip install --no-build-isolation -e .

# Install with dev dependencies
pip install -e .[dev]

# Install nightly version
pip install torchtnt-nightly
```

### Testing
```bash
# Run all tests with coverage
pytest --cov=. --cov-report xml tests -vv

# Run tests without coverage
pytest tests -vv

# Run specific test file
pytest tests/framework/test_unit.py -vv

# Run tests with verbose output
pytest tests -v
```

### Linting and Formatting
The project uses pre-commit hooks for automated linting and formatting:
```bash
# Install pre-commit hooks
pre-commit install

# Run all pre-commit hooks
pre-commit run --all-files

# Run specific linters
flake8  # configured via .flake8
black .  # code formatting
usort .  # import sorting
```

### Type Checking
```bash
pyre-check
```

## Code Architecture

### Core Structure

**torchtnt/framework/** - Main training framework
- `unit.py` - Defines base Unit classes (TrainUnit, EvalUnit, PredictUnit) with hooks for lifecycle events
- `auto_unit.py` - AutoUnit: Higher-level API that auto-generates training boilerplate
- `train.py`, `evaluate.py`, `predict.py`, `fit.py` - Loop execution functions that invoke Unit hooks
- `state.py` - State management system tracking modules, optimizers, metrics, and progress
- `callback.py` - Base Callback class for extending functionality
- `callbacks/` - Pre-built callbacks for checkpointing, logging, profiling, etc.

**torchtnt/utils/** - Utility modules
- Data utilities
- Logger implementations (TensorBoard, CSV)
- Helper functions for distributed training, checkpointing, etc.

### Key Concepts

1. **Unit Classes**: The primary building blocks that encapsulate training/evaluation logic
   - Extend `TrainUnit`, `EvalUnit`, or `PredictUnit` for low-level control
   - Extend `AutoUnit` for automatic boilerplate generation
   - Implement lifecycle hooks: `compute_loss`, `on_train_step_end`, `on_eval_step_end`, etc.

2. **Loop Functions**: Entry points for execution
   - `train()`, `evaluate()`, `predict()`, `fit()` - Execute respective loops
   - These functions orchestrate the Unit lifecycle and invoke callbacks

3. **Callbacks**: Extension points for adding functionality
   - Examples: `TorchSnapshotSaver`, `TensorBoardLogger`, `EarlyStopping`, `ThroughputLogger`
   - Can be synchronous or asynchronous
   - Hook into lifecycle events: on_train_start, on_train_end, on_epoch_end, etc.

4. **State Management**: Tracks all stateful objects for checkpointing and monitoring
   - Automatically tracks modules, optimizers, LR schedulers, metrics
   - Supports custom stateful tracking via `AppStateMixin`

### Usage Patterns

**Basic AutoUnit Pattern** (see examples/auto_unit_example.py):
```python
class MyUnit(AutoUnit[Batch]):
    def configure_optimizers_and_lr_scheduler(self, module):
        return torch.optim.SGD(module.parameters(), lr=0.01), scheduler

    def compute_loss(self, state, data):
        inputs, targets = data
        outputs = self.module(inputs)
        loss = criterion(outputs, targets)
        return loss, outputs
```

**Manual Unit Pattern** (see examples/train_unit_example.py):
```python
class MyTrainUnit(TrainUnit):
    def train_step(self, state, data):
        # Custom training step logic
        return step_result
```

## Testing Strategy

- Tests use `pytest` with coverage reporting
- Unit tests organized by module: `tests/framework/`, `tests/utils/`
- Integration examples tested in `examples/` directory
- CI runs on Python 3.8, 3.9 with both stable and nightly PyTorch

## Development Workflow

1. **Setup**:
   ```bash
   pip install -r requirements.txt
   pip install -r dev-requirements.txt
   pre-commit install
   ```

2. **Develop**: Create Units, callbacks, and utilities

3. **Test**: Ensure all tests pass before submitting PR

4. **Lint**: Pre-commit hooks enforce style and formatting

## Important Files

- `setup.py` - Package configuration with nightly build support
- `.flake8` - Linting configuration (120 char line length)
- `.pre-commit-config.yaml` - Pre-commit hooks setup
- `.github/workflows/test.yaml` - CI testing workflow
- `examples/` - Example implementations showing usage patterns

## PyTorch Integration Notes

- Requires PyTorch >= 2.3.0
- Supports distributed training (DDP, FSDP)
- Compatible with PyTorch 2.0+ compile features
- Supports FSDP2 for newer PyTorch versions