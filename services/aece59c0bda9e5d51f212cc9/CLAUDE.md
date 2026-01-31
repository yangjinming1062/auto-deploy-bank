# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

verl (Volcano Engine Reinforcement Learning) is a flexible, production-ready RL training library for Large Language Models. It implements the HybridFlow architecture that decouples computation from data dependencies, enabling efficient distributed RLHF training.

**Key Features:**
- Support for PPO, GRPO, DAPO, GSPO, SPPO, and other RL algorithms
- Multiple training backends: FSDP, FSDP2, Megatron-LM
- Multiple inference backends: vLLM, SGLang, HF Transformers
- Support for VLMs, multi-turn conversations, and tool calling
- Scales to 671B+ models and hundreds of GPUs

## Development Setup

### Installation

```bash
# Basic installation
pip install -e .

# With test dependencies and vLLM
pip install -e .[test,vllm]

# With test dependencies and SGLang
pip install -e .[test,sglang]

# Full development dependencies
pip install -e .[test,vllm,sglang,gpu,math]
```

### Linting and Formatting

Pre-commit hooks enforce code quality:

```bash
# Install pre-commit hooks
pip install pre-commit
pre-commit install

# Run on staged changes
pre-commit run

# Run on all files
pre-commit run --all-files

# Run specific hooks
pre-commit run --all-files --show-diff-on-failure --color=always ruff
pre-commit run --all-files --show-diff-on-failure --color=always autogen-trainer-cfg
```

## Testing

### Run Tests

```bash
# Run all GPU tests (default, requires GPU)
pytest tests/

# Run all CPU-only tests (files ending with _on_cpu.py)
pytest -s -x --asyncio-mode=auto tests/
echo '[pytest]' > pytest.ini && echo 'python_files = *_on_cpu.py' >> pytest.ini && pytest -s -x tests/

# Run specific test
pytest tests/test_protocol_on_cpu.py -v

# Rerun failures
pytest --rerunfailures=1 tests/
```

### Test Categories

| Directory | Purpose |
|-----------|---------|
| `tests/` | Standard unit tests (run on GPU by default) |
| `tests/**/*_on_cpu.py` | CPU-only unit tests |
| `tests/special_distributed/` | Multi-GPU distributed tests |
| `tests/special_e2e/` | End-to-end training/inference tests |
| `tests/special_npu/` | NPU-specific tests |

### Running Training Examples

```bash
# PPO training example
python3 -m verl.trainer.main_ppo \
    algorithm.adv_estimator=gae \
    data.train_files="['/path/to/train.parquet']" \
    data.val_files="['/path/to/test.parquet']" \
    actor_rollout_ref.model.path=Qwen/Qwen2-7B-Instruct \
    trainer.n_gpus_per_node=8 \
    trainer.nnodes=1

# GRPO training
python3 -m verl.trainer.main_grpo +config=grpo_trainer ...

# SFT training
python3 -m verl.trainer.main_sft ...
```

Configuration is managed via Hydra. Override defaults from `verl/trainer/config/*.yaml` using command-line arguments.

### Regenerating Trainer Config Docs

When modifying trainer configs, regenerate the flattened reference configs:

```bash
bash scripts/generate_trainer_config.sh
```

### Config YAML Format Requirements

Trainer config YAMLs enforce specific formatting on CI:
1. Comments must appear above each field
2. Blank line required between fields
3. No inline comments (after field on same line)
4. Indentation level is respected for nested fields

## Architecture

### Core Modules

```
verl/
├── trainer/           # Training loop implementations
│   ├── main_ppo.py    # PPO entry point (uses Ray)
│   ├── main_grpo.py   # GRPO entry point
│   ├── sft_trainer.py # Supervised fine-tuning
│   ├── ppo/           # PPO-specific logic (ray_trainer.py, core_algos.py, reward.py)
│   └── config/        # Hydra config YAML files (actor, critic, rollout, algorithm, etc.)
│
├── workers/           # Ray workers for distributed execution
│   ├── actor/         # Policy model workers
│   ├── critic/        # Value model workers
│   ├── rollout/       # Generation workers (vLLM, SGLang, HF)
│   ├── reward_model/  # Reward model inference
│   ├── reward_manager # Reward function orchestration
│   ├── engine/        # FSDP/Megatron engine wrappers
│   └── fsdp_workers.py, megatron_workers.py, engine_workers.py # Worker implementations
│
├── models/            # Model architectures and utilities
│   ├── transformer.py
│   └── ...
│
├── single_controller/ # Ray-based distributed infrastructure
│   ├── ray/base.py    # ResourcePoolManager, RayWorkerGroup, create_colocated_worker_cls
│   └── ray/           # RayClassWithInitArgs, RayResourcePool
│
├── utils/             # Utilities
│   ├── dataset/       # Data loading and collation (rl_dataset.py, sft_dataset.py)
│   ├── reward_score/  # Reward scoring functions
│   └── profiler/      # Performance profiling
│
├── protocol.py        # DataProto class for inter-process data transfer using tensordict
└── checkpoint_engine/ # Checkpoint saving/loading
```

### Distributed Training Architecture

verl uses a **hybrid-controller** programming model with Ray for orchestration:

1. **Ray Driver** (`ray_trainer.py`): Main process that coordinates training, runs on head node
2. **Ray Workers**: Remote actors that execute model forward/backward passes
3. **ResourcePoolManager**: Allocates GPU resources to different worker types
4. **Colocated Workers**: Multiple roles (actor, rollout, ref) can share a single GPU via FSDP

Worker types are defined in `verl/trainer/ppo/utils.py`:
- `Role.ACTOR`: Policy model updates
- `Role.ROLLOUT`: Response generation (vLLM/SGLang/HF)
- `Role.REF`: Reference model for KL penalty
- `Role.CRITIC`: Value function updates
- `Role.REWARD_MODEL`: Reward model inference

### Data Flow

1. **Data Loading**: Datasets loaded via `verl/utils/dataset/rl_dataset.py`, collated into `DataProto`
2. **Rollout Generation**: Actor model generates responses via vLLM/SGLang/HF rollout workers
3. **Reward Scoring**: `reward_manager` orchestrates reward functions, returns `token_level_scores`
4. **KL Penalty**: Reference model computes log probs for KL divergence (if `use_kl_loss=True`)
5. **Advantage Estimation**: Algorithm computes advantages (GAE, GRPO, etc.) in `core_algos.py`
6. **Model Update**: Actor and critic are updated via PPO/GRPO updates using FSDP/Megatron

### DataProto Protocol

`DataProto` (in `verl/protocol.py`) is the core data structure for inter-process communication:
- Wraps `tensordict.TensorDict` for efficient tensor operations
- Contains `batch` (non-packed data) and `non_batch` (metadata) fields
- Supports automatic padding for distributed training compatibility
- Use `pad_dataproto_to_divisor()` and `unpad_dataproto()` for tensor parallelism

### Configuration System

verl uses Hydra for configuration composition. Configs are organized hierarchically:

```yaml
# verl/trainer/config/ppo_trainer.yaml
defaults:
  - actor@actor_rollout_ref.actor: dp_actor
  - data@data: legacy_data
  - reward_manager@reward_manager
  - ref@actor_rollout_ref.ref: dp_ref
  - rollout@actor_rollout_ref.rollout: rollout
  - model@actor_rollout_ref.model: hf_model
  - critic@critic: dp_critic
  - reward_model@reward_model: dp_reward_loop
  - algorithm@algorithm.rollout_correction: rollout_correction
  - _self_
```

### Key Classes

| Class | Location | Purpose |
|-------|----------|---------|
| `RayPPOTrainer` | `verl/trainer/ppo/ray_trainer.py` | Main PPO training orchestration |
| `DataProto` | `verl/protocol.py` | Inter-process data transfer using tensordict |
| `ActorRolloutRefWorker` | `verl/workers/fsdp_workers.py` | Combined actor/rollout/reference worker |
| `CriticWorker` | `verl/workers/critic/*.py` | Value function model worker |
| `RolloutWorker` | `verl/workers/rollout/*.py` | Generation worker (vLLM, SGLang, HF) |

## Common Development Patterns

### Adding New Algorithms

1. Define algorithm config in `verl/trainer/config/algorithm/`
2. Implement advantage estimation in `verl/trainer/ppo/core_algos.py`
3. Create trainer or extend existing one

### Adding New Reward Functions

```python
# In your custom reward file
def compute_score(data, **kwargs) -> float:
    """Compute reward for generated response."""
    # Your reward logic
    return reward
```

Configure via `custom_reward_function.path` and `custom_reward_function.name` in YAML.

### Extending Worker Classes

Workers inherit from base classes and implement `forward()` methods that execute on Ray workers. See `verl/workers/fsdp_workers.py` for FSDP worker patterns.

### Common Issues and Solutions

1. **CUDA out of memory**: Reduce `ppo_micro_batch_size_per_gpu` or enable `param_offload`/`optimizer_offload`
2. **Ray hanging on startup**: Ensure `ray_wait_register_center_timeout` is sufficient for large clusters
3. **Training instability**: Adjust KL penalty (`kl_loss_coef`) or advantage normalization settings
4. **Tokenization errors**: Set `filter_overlong_prompts=True` and appropriate `max_prompt_length`

## Documentation

Build documentation locally:

```bash
cd docs
pip install -r requirements-docs.txt
make html
python -m http.server -d _build/html/
```

View at http://localhost:8000