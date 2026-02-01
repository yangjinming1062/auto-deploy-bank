# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

veScale is a PyTorch Distributed library enabling hyperscale distributed training of LLMs and RLs. It extends PyTorch DTensor with custom sharding strategies, particularly **RaggedShard** - a placement type that shards tensors based on flattened storage rather than traditional dimension-wise sharding.

## Build and Test Commands

```bash
# Install dependencies and package
pip3 install -r requirements.txt && pip3 install -e .

# Run a single test file
pytest test/dtensor/ragged_shard/test_redistribute.py -v

# Run all tests (uses multi-process test runner)
bash scripts/run_test.sh

# Run linter
ruff check vescale/

# Format Python code
black vescale/ test/
```

Python 3.11+ and PyTorch 2.7.1+ are required.

## Architecture

### Core Module: `vescale/dtensor/`

The library extends PyTorch DTensor with custom dispatch and sharding:

| File | Purpose |
|------|---------|
| `_api.py` | Main `DTensor` class and `distribute_tensor()` API |
| `_dispatch.py` | `OpDispatcher` - handles op routing and propagation |
| `_ops/` | Operator implementations and sharding strategies |
| `_redistribute.py` | DTensor redistribution logic |
| `placement_types.py` | `RaggedShard` placement and variants |
| `vescale_utils/checkpoint.py` | Checkpointing utilities |
| `vescale_utils/ragged_shard_utils.py` | RaggedShard utilities |
| `vescale/utils/monkey_patch.py` | PyTorch monkey patches |

### Key Concepts

**RaggedShard Placement**: Unlike `Shard(dim)` which slices along a dimension, `RaggedShard(dims, local_units)` splits tensors based on element counts across devices. Critical for handling variable-length sequences in LLM training.

**DTensor Dispatch Chain**: When an operation runs on a DTensor:
1. `OpDispatcher.__torch_dispatch__` intercepts the op
2. Queries sharding properties from `_sharding_prop.py`
3. Finds a strategy in `_ops/_common_rules.py` or op-specific files (`_tensor_ops.py`, `_pointwise_ops.py`, `_math_ops.py`, `_matrix_ops.py`)
4. Executes local operations with proper collective communication

**Operator Implementation**: Each operation type is registered in `vescale/dtensor/_ops/__init__.py` and implemented in dedicated files based on operation category.

### Test Organization

| Directory | Focus Area |
|-----------|------------|
| `test/dtensor/ragged_shard/` | RaggedShard placement tests |
| `test/dtensor/cpu_only/` | CPU-only DTensor tests |
| `test/dtensor/checkpoint/` | Checkpoint save/load tests |

Tests use `MultiProcessTestCase` from PyTorch's testing framework and require 4 devices minimum. Key test utilities in `test/common_dtensor.py`:
- `DTensorTestBase` - Base class for distributed tests
- `@with_comms` decorator - Initializes process groups for tests
- `DTensorOpTestBase` - Base class for operator tests

## Code Style

- **Linter**: `ruff` with config in `pyproject.toml`
- **Formatter**: `black` (line length: 120)
- **C++ formatter**: `clang-format` (column limit: 80, MLIR style)
- **Style guides**: Google Python style, Google C++ style
- **License**: Apache 2.0

## Key APIs

```python
from vescale import DTensor, distribute_tensor, DeviceMesh, init_device_mesh
from vescale.dtensor import Shard, Replicate, Partial, RaggedShard

# Create device mesh
mesh = DeviceMesh("cuda", list(range(world_size)))

# Distribute tensor
dt = distribute_tensor(tensor, mesh, [Shard(0)])

# Redistribute between placements
dt_redistributed = dt.redistribute(mesh, [Replicate()])
```

## Legacy Code

The `legacy/` directory contains older implementation (v1). The active development is in `vescale/` (v2). When modifying core functionality, work in `vescale/dtensor/`, not `legacy/`.