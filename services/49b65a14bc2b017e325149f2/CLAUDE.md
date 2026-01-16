# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Long-RL is a framework for scaling reinforcement learning (RL) to long sequences, particularly long videos. It extends the verl framework with support for:
- Hour-level long video RL training (3,600+ frames, 256k tokens) with sequence parallelism
- Multi-modal RL (text, image, video, audio) on VILA, Qwen-VL, Qwen-Omni models
- Image/video generation RL on diffusion models (Stable Diffusion, Wan)
- Multiple RL algorithms: GRPO, DAPO, Reinforce

## Common Commands

### Installation
```bash
# Basic installation
pip install -e .

# For Qwen-Omni models, run after install:
bash vllm_replace.sh

# For development with linting tools
pip install -e .[dev]
```

### Training
```bash
# Single-node training (8 GPUs)
bash examples/new_supports/qwen2_5_vl_3b_video_grpo.sh $VIDEO_PATH

# Multi-node training
bash scripts/srun_multi_nodes.sh examples/new_supports/qwen2_5_vl_3b_video_grpo.sh 2

# Run with custom config:
python3 -m verl.trainer.main \
    config=examples/config.yaml \
    data.train_files=path/to/data@train \
    worker.actor.model.model_path=path/to/model
```

### Code Quality
```bash
# Check code quality (ruff)
make quality

# Auto-format code (ruff)
make style

# Run tests
pytest -vv tests/

# Build package
make build
```

## Architecture

### Core Training Pipeline
```
verl/trainer/main.py          # Entry point, uses Ray for distributed execution
verl/trainer/ray_trainer.py   # RayPPOTrainer orchestrates the RL loop
verl/trainer/config.py        # PPOConfig dataclass (DataConfig, AlgorithmConfig, TrainerConfig)
```

### Worker Architecture
Workers run on Ray with FSDP (Fully Sharded Data Parallel) for model parallelism:
- `verl/workers/fsdp_workers.py`: FSDPWorker base class for actor/critic/rollout/ref
- `verl/workers/rollout/vllm_rollout_spmd.py`: vLLM-based rollout worker for generation
- `verl/workers/actor/`: Actor worker for policy updates
- `verl/workers/critic/`: Critic worker (value function for PPO/GAE)
- `verl/workers/reward/`: Reward function manager

### Key Data Flow
1. Data loaded via `verl/trainer/data_loader.py` → `verl/utils/dataset.py`
2. Prompts formatted using jinja templates (`examples/format_prompt/*.jinja`)
3. Rollout worker generates responses using vLLM
4. Reward function computes scores (`examples/reward_function/*.py`)
5. Advantage computed via `verl/trainer/core_algos.py` (GRPO/GAE/DAPO/Reinforce)
6. Actor updated via FSDP backward pass

### Supported Model Configurations
- **VILA models**: Set `data.vila_model=true`, `worker.vila_model=true`, copy `verl/utils/vila_remote_code/*` to model path
- **Qwen-VL models**: Use `worker.actor.ulysses_size` for sequence parallelism
- **Qwen-Omni models**: Run `bash vllm_replace.sh` first, set `data.is_omni=true`
- **Diffusion models**: Use `config_diffusion.yaml`, set `trainer.diffusion=true`

### Critical Configuration
- `examples/config.yaml`: Main training configuration template
- `examples/config_video_diffusion.yaml`: For diffusion model training
- `examples/runtime_env.yaml`: Ray cluster environment variables

### Sequence Parallelism
Sequence parallelism is implemented in `verl/utils/sequence_parallel/`:
- Ring attention (`ring/`) for Ulysses + Ring hybrid parallelism
- Ulysses attention for context parallel on heads
- Used via `worker.actor.ulysses_size` and `worker.actor.padding_free=true`

### Checkpoint Management
```bash
# Merge checkpoints to Hugging Face format
python3 scripts/model_merger.py --local_dir checkpoints/easy_r1/exp_name/global_step_1/actor
```

## Supported Features

| Feature | Configuration |
|---------|--------------|
| Open-ended reward | `worker.rollout.open_ended_reward=True` + `export OPENAI_API_KEY` |
| Cached video embeddings | `data.cache_dir` + `worker.actor.cached_embeds_dir` |
| Chunked gathering | `worker.rollout.num_chunk_seq` (8/16/32) |
| Long video frames | `worker.rollout.num_video_frames` (up to 8192) |

## Code Style

- Line length: 119 characters
- Indent width: 4 spaces
- Target Python: 3.9+
- Linting: ruff (see `pyproject.toml` for exact rules)
- License headers required on new files (Apache 2.0)

## Dependencies

Key pinned versions:
- `transformers==4.52.4`
- `vllm==0.9.1`
- `flash-attn==2.7.3`
- `liger-kernel`, `ray[default]`, `accelerate`, `peft`

## File Organization

```
verl/
├── trainer/           # Training orchestration
├── workers/           # Distributed workers (actor, rollout, critic, reward)
├── models/            # Model-specific code
├── utils/             # Utilities (SP, checkpoint, dataset, etc.)
├── single_controller/ # Ray-based distributed execution
└── protocol.py        # DataProto for batched data handling
examples/
├── new_supports/      # Training scripts for various models
├── config.yaml        # Main config
├── reward_function/   # Reward function implementations
└── format_prompt/     # Jinja prompt templates
scripts/               # Utility scripts (merge checkpoints, multi-node)
```