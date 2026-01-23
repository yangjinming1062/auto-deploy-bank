# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

NASLib is a modular Neural Architecture Search (NAS) framework written in Python/PyTorch. It provides high-level abstractions for designing search spaces, implementing NAS optimizers, and benchmarking performance predictors.

## Development Commands

**Install the package:**
```bash
pip install --upgrade pip setuptools wheel
pip install -e .
```

**Run tests:**
```bash
cd tests
python -m pytest --forked --durations=20 --timeout=600 --timeout-method=signal -v test
# Or with coverage:
coverage run -m unittest discover -v
coverage report
```

**Run single test file:**
```bash
python -m pytest tests/test_darts_search_space.py -v
```

**Code quality:**
```bash
# Run pre-commit hooks (black, flake8)
pre-commit run --all-files
```

## Architecture

NASLib has three core abstractions that can be combined flexibly:

### 1. Search Spaces (`naslib/search_spaces/`)
Search spaces define the architecture search space as a directed acyclic graph (DAG) using `Graph` class (inherits from `torch.nn.Module` and `networkx.DiGraph`). Each search space implements:
- `Graph.parse()`: Converts the search space to a PyTorch module for training
- `Graph.unparse()`: Reverses parsing for discrete architecture manipulation
- `QUERYABLE`: Set to `True` if the search space can query benchmark results
- `OPTIMIZER_SCOPE`: Defines which nodes/edges are optimizable

Available search spaces:
- `SimpleCellSearchSpace`: Cell-based search space for CIFAR-10
- `DartsSearchSpace`: DARTS-style search space
- `NasBench101SearchSpace`, `NasBench201SearchSpace`: Tabular benchmarks
- `HierarchicalSearchSpace`: Hierarchical architecture search space

### 2. Optimizers (`naslib/optimizers/`)
Optimizers search for architectures within a search space. They inherit from `MetaOptimizer` and must implement:
- `adapt_search_space(search_space, scope, dataset_api)`: Initialize with a search space
- `new_epoch(epoch)`: Called each training epoch
- `step(data_train, data_val)`: Return (logits_train, logits_val, train_loss, val_loss) for oneshot optimizers
- `train_statistics()`: Return (train_acc, valid_acc, test_acc, train_time) for discrete optimizers
- `test_statistics()`: Return anytime results (optional)
- `get_final_architecture()`: Return the best architecture found

Optimizer categories:
- **Oneshot** (`oneshot/`): DARTS, GDAS, DrNAS, RandomNAS - train a supernet with differentiable/continuous relaxations
- **Discrete** (`discrete/`): Random Search, Regularized Evolution, Local Search, BANANAS - search over discrete architectures

### 3. Predictors (`naslib/predictors/`)
Predictors estimate architecture performance without training. They inherit from `Predictor` base class with methods:
- `fit(xtrain, ytrain, info)`: Train on observed architectures
- `query(xtest, info)`: Predict performance for candidate architectures

Used by discrete optimizers (e.g., BANANAS) for surrogate model-based search.

### 4. Trainer (`naslib/defaults/trainer.py`)
The `Trainer` class orchestrates the search and evaluation pipeline:
- `search()`: Runs architecture search with the optimizer
- `evaluate()`: Retrains and evaluates the final architecture
- `evaluate_oneshot()`: Evaluates the one-shot model's weights

### 5. Graph API (`naslib/search_spaces/core/graph.py`)
The `Graph` class is the core data structure:
- Nodes and edges can contain subgraphs as data
- `update_edges(func, scope, private_edge_data)`: Batch modify edges
- `update_nodes(func, scope, private_edge_data)`: Batch modify nodes
- Edges have `EdgeData` with shared attributes (operation) and private attributes (weights)

## Typical Usage Pattern

```python
from naslib.search_spaces import SimpleCellSearchSpace
from naslib.optimizers import DARTSOptimizer
from naslib.defaults.trainer import Trainer
from naslib.utils import utils

config = utils.get_config_from_args()
search_space = SimpleCellSearchSpace()
optimizer = DARTSOptimizer(config)
optimizer.adapt_search_space(search_space)

trainer = Trainer(optimizer, config)
trainer.search()     # Search for architectures
trainer.evaluate()   # Evaluate the best architecture
```

## Key Files

- `naslib/defaults/trainer.py`: Main training orchestration
- `naslib/search_spaces/core/graph.py`: Core graph data structure
- `naslib/search_spaces/core/primitives.py`: Operation primitives (Conv, Pool, Identity, etc.)
- `naslib/optimizers/core/metaclasses.py`: MetaOptimizer base class
- `examples/demo.py`: Working example of NAS search and evaluation

## Configuration

Configs are loaded via `utils.get_config_from_args()` which reads from YAML files. Common config attributes:
- `config.dataset`: cifar10, cifar100, imagenet
- `config.search.epochs`: Number of search epochs
- `config.evaluation.epochs`: Number of evaluation epochs
- `config.optimizer`: Optimizer name