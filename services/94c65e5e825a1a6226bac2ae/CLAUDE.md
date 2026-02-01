# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

VeOmni is a PyTorch-native distributed training framework for single- and multi-modal models. It follows a trainer-free design philosophy, exposing the entire training logic in linear scripts for maximum transparency and control. The framework supports large-scale training across NVIDIA GPUs and Ascend NPUs.

## Development Commands

### Installation

```bash
# Install with development dependencies
pip install -e ".[dev]"

# Install with GPU dependencies
pip install -e ".[gpu]"

# Install with NPU dependencies
pip install -e ".[npu]"
```

### Code Quality

```bash
# Run pre-commit hooks (required before commit)
make commit

# Check code quality without modifying
make quality

# Auto-format code
make style

# Run all tests
pytest tests/

# Run a single test file
pytest tests/parallel/test_parallel_state.py -v
```

### Building

```bash
# Build package
make build
python3 setup.py sdist bdist_wheel
```

### Training

Training uses `torchrun` via the provided `train.sh` wrapper script:

```bash
# Basic training command
bash train.sh <training_script> <config.yaml> --model.model_path <path> --data.train_path <path>

# Example: Training Qwen2.5 VL
bash train.sh tasks/omni/train_qwen2_vl.py configs/multimodal/qwen2_vl/qwen2_vl.yaml \
    --model.model_path Qwen/Qwen2-VL-7B-Instruct \
    --data.train_path /path/to/data

# With Ulysses sequence parallelism (ulysses_size = number of GPUs for SP)
bash train.sh tasks/omni/train_qwen2_vl.py configs/multimodal/qwen2_vl/qwen2_vl.yaml \
    --model.model_path Qwen/Qwen2-VL-7B-Instruct \
    --data.train_path /path/to/data \
    --train.ulysses_parallel_size 4

# Multi-node training
NNODES=2 NODE_RANK=1 MASTER_ADDR=192.168.1.1 bash train.sh <script> <config>
```

Environment variables:
- `CUDA_VISIBLE_DEVICES` or `ASCEND_RT_VISIBLE_DEVICES`: GPU/NPU device assignment
- `NCCL_TIMEOUT`: NCCL operation timeout in seconds

## Architecture

### Core Design Principles

1. **Trainer-Free**: Training scripts are linear and explicit (see `tasks/train_torch.py`)
2. **Modular**: Components can be replaced independently
3. **Torch-Native**: Uses PyTorch's distributed APIs directly

### Key Directories

- `veomni/`: Main framework code
- `tasks/`: Training script entry points (e.g., `train_torch.py`, `omni/train_qwen3_omni.py`)
- `configs/`: YAML configuration files organized by model type
- `tests/`: Unit tests
- `docs/`: Documentation with examples

### Framework Components

**Distributed Training** (`veomni/distributed/`):
- `fsdp/` and `fsdp2/`: FSDP1 and FSDP2 sharding implementations
- `sequence_parallel/`: Ulysses SP implementation with async support
- `moe/`: Expert parallelism for MoE models
- `parallel_state.py`: Process group initialization for DP/TP/EP/CP/SP

**Models** (`veomni/models/`):
- `transformers/`: HuggingFace-compatible model implementations with SP/EP support
- `seed_omni/`: Custom Seed-Omni model implementations
- Model registration system via `MODEL_CONFIG_REGISTRY`, `MODELING_REGISTRY`, `MODEL_PROCESSOR_REGISTRY`

**Data Handling** (`veomni/data/`):
- `data_collator.py`: Batch padding and sequence packing
- `dynamic_batching.py`: Dynamic batch sizing for variable-length sequences
- `multimodal/`: Audio/video/image preprocessing and chat templates

**Checkpointing** (`veomni/checkpoint/`):
- DCP (Distributed Checkpoint) support via `torch.distributed.checkpoint`

**Operations** (`veomni/ops/`):
- Custom CUDA/attention operations and fused MoE kernels

### Configuration System

Training uses YAML configs with three main sections:
- `model`: Model path, tokenizer, attention implementation
- `data`: Dataset path, max sequence length, batching strategy
- `train`: Parallelism settings, optimizer, LR scheduler, checkpointing

Key parallelism settings:
- `data_parallel_mode`: "fsdp1" or "fsdp2"
- `tensor_parallel_size`: TP degree
- `expert_parallel_size`: EP degree for MoE
- `ulysses_parallel_size`: Sequence parallelism degree

### Adding New Models

1. Create model implementation in `veomni/models/transformers/` or `veomni/models/seed_omni/`
2. Register the model using the registry system:
   ```python
   from veomni.models.loader import MODEL_CONFIG_REGISTRY, MODELING_REGISTRY

   @MODEL_CONFIG_REGISTRY.register("your_model")
   def register_config():
       from .configuration_your_model import YourModelConfig
       return YourModelConfig

   @MODELING_REGISTRY.register("your_model")
   def register_modeling(architecture):
       from .modeling_your_model import YourModelForCausalLM
       return YourModelForCausalLM
   ```
3. Add YAML config in `configs/model_configs/`
4. For SP support, implement sequence parallel modifications using `gather_seq_scatter_heads` and `gather_heads_scatter_seq`
5. For EP support in MoE models, define parallel plans in `get_parallel_plan()`

### Parallelism Details

**FSDP2 + EP** (see `docs/key_features/ep_fsdp2.md`):
- Experts are sharded along dim-0, FSDP2 shards along dim-1
- Requires `MultiOptimizer` and `MultiLRScheduler` for mixed sharding

**Ulysses Sequence Parallelism** (see `docs/key_features/ulysses.md`):
- Splits sequences across GPUs, uses all-to-all for attention
- Requires attention implementation supporting `gather_seq_scatter_heads`
- Async Ulysses overlaps communication and computation

## Important Conventions

- Logging uses `logger = helper.create_logger(__name__)` with `logger.info_rank0()` for rank-0 only logs
- Model assets (config, tokenizer) saved separately from weights
- Use `save_args()` to save configuration to output directory
- DCP checkpoints saved to `save_checkpoint_path` with state dict conversion
- Use `get_parallel_state()` to access process groups