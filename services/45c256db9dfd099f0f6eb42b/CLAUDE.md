# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

GraphStorm is an enterprise-grade distributed graph machine learning framework designed for billion-scale graphs. It provides single-command training/inference and built-in GNN models (R-GCN, R-GAT, SAGE, GAT, GATv2, HGT) with support for link prediction, node classification/regression, and edge classification/regression tasks.

**Key dependencies:** PyTorch 1.13+, DGL 1.0+, transformers 4.3.0+, Python 3.8+

## Development Commands

```bash
# Install for development
pip install -e '.[test]'  # Installs with test dependencies

# Run unit tests (requires multi-GPU instance setup)
export NCCL_IB_DISABLE=1; export NCCL_SHM_DISABLE=1
NCCL_NET=Socket NCCL_DEBUG=INFO python3 -m pytest -x ./tests/unit-tests -s

# Run a single test file
python3 -m pytest ./tests/unit-tests/test_gnn.py -s

# Run SageMaker-specific tests
python3 -m pytest -x ./tests/sagemaker-tests -s

# Run linting
pylint --rcfile=./tests/lint/pylintrc ./python/graphstorm/

# Process graph data for training
python tools/partition_graph.py --dataset ogbn-arxiv --num-parts 1 --output /tmp/output

# Single-command training examples
python -m graphstorm.run.gs_node_classification --workspace /tmp/ws --num-trainers 1 --num-servers 1 --part-config /path/to/config.json --cf /path/to/config.yaml
python -m graphstorm.run.gs_link_prediction --workspace /tmp/ws --num-trainers 1 --num-servers 1 --part-config /path/to/config.json --cf /path/to/config.yaml --num-epochs 2
```

## Architecture

### Core Package Structure (python/graphstorm/)

- **config/** - `GSConfig` class parses YAML configuration files defining model, training, and task parameters
- **data/** - Built-in datasets (OGB, MAG, MovieLens) and utilities for graph data loading
- **dataloading/** - Data loaders and samplers for node/edge/link prediction tasks, including negative samplers and distributed data handling
- **model/** - GNN encoders (R-GCN, R-GAT, SAGE, GAT, GATv2, HGT), decoders, embeddings, and loss functions
- **trainer/** - Task-specific trainers: `np_trainer.py` (node), `ep_trainer.py` (edge), `lp_trainer.py` (link prediction), `mt_trainer.py` (multi-task)
- **inference/** - Inference classes for each task type, with mini-batch and full-graph inference methods
- **run/** - Entry point modules for each task (e.g., `gs_node_classification.py`, `gs_link_prediction.py`)
- **distributed/** - Distributed training primitives using DGL's distributed API
- **gconstruct/** - Graph construction utilities for processing raw data into DGL graphs
- **gpartition/** - Graph partitioning utilities (Metis, random) and GraphBolt conversion
- **eval/** - Evaluators and metrics for classification, regression, and link prediction
- **tracker/** - Training progress tracking (TensorBoard, SageMaker)

### Training Flow

1. **Entry point** (`python -m graphstorm.run.gs_*`) parses YAML config and CLI args
2. **Config parsing** creates `GSConfig` object that defines model architecture and training hyperparameters
3. **Data loading** creates `GSgnnData` from partitioned graph metadata, then instantiates task-specific data loaders
4. **Model creation** uses `gsf.py` factory functions (`create_builtin_*_model`) to construct encoder + decoder based on task type
5. **Distributed initialization** via `gs.initialize(ip_config=...)` sets up communication backend
6. **Training loop** executes in trainer class, handling forward/backward passes and evaluation
7. **Inference** uses `do_mini_batch_inference()` or `do_full_graph_inference()` for predictions

### Task Types (defined in config/config.py)

- `node_classification`, `node_regression`
- `edge_classification`, `edge_regression`
- `link_prediction`
- `multi_task`
- `reconstruct_node_feat`, `reconstruct_edge_feat`

### Key Configuration Patterns

YAML configs follow GSF schema:
```yaml
version: 1.0
gsf:
  basic:
    model_encoder_type: rgcn  # gat, rgat, sage, gatv2, hgt
    graph_name: my_graph
  gnn:
    fanout: "15,10"
    num_layers: 2
    hidden_size: 128
  hyperparam:
    dropout: 0.5
    lr: 0.001
    num_epochs: 10
  node_classification:  # or edge_classification, link_prediction
    target_ntype: "paper"
    label_field: "labels"
    num_classes: 40
```

### Custom Model Development

To add a custom GNN encoder:
1. Inherit from `GraphConvEncoder` in `model/gnn_encoder_base.py`
2. Implement the `forward()` method returning node/edge embeddings
3. Register in `gsf.py::create_builtin_gnn_model()` factory function

### Distributed Mode

GraphStorm supports both standalone and distributed modes:
- **Standalone:** No `ip_config` needed; uses single process
- **Distributed:** Requires `ip_config` file listing machine IPs and `num_trainers` > 1
- SageMaker integration available in `sagemaker/` for managed distributed training