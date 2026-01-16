# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is **Skywork-OR1**, a fork of [VERL (Volcano Engine Reinforcement Learning)](https://github.com/volcengine/verl) - a reinforcement learning framework for training Large Language Models (LLMs) using PPO and other RL algorithms. The project trains math and code reasoning models using rule-based RL with carefully designed datasets.

## Development Commands

### Installation
```bash
# Python 3.10 conda environment
conda create -n verl python=3.10
conda activate verl

# Install dependencies
pip3 install torch==2.4.0 --index-url https://download.pytorch.org/whl/cu124
pip3 install flash-attn --no-build-isolation
pip3 install -e .  # Install verl in editable mode
```

### Code Formatting
```bash
# Format code with yapf (Google style, 120 char limit)
./scripts/format.sh
```

### Running Tests
```bash
# Run all tests
pytest -s -x tests/

# Run specific test categories
pytest -s -x tests/sanity              # Sanity tests
pytest -s -x tests/utility             # Utility tests
pytest -s -x tests/model/              # Model tests
pytest -s -x tests/ray/                # Ray scheduling tests
pytest -s -x tests/rollout/            # Rollout tests

# License check
python3 tests/sanity/check_license.py --directory .
```

### Training (PPO/GRPO)
```bash
# Single node training
export MODEL_PATH=/path/to/model
export CODE_PATH=/path/to/code
bash ./or1_scripts/train/7b_8k.sh

# Multi-node training: start Ray on head node first
ray start --head --dashboard-host=0.0.0.0
# Then on worker nodes:
ray start --address='<head-node-ip>:6379'

# Then run training script
bash ./or1_scripts/train/7b_8k.sh
```

## Architecture

### Core Training Flow

The main entry point is `verl/trainer/main_ppo.py` which uses Hydra for config management. The training pipeline:

1. **Data Loading** (`verl/utils/dataset/rl_dataset.py`): `RLHFDataset` loads prompts from parquet/pickle files
2. **Generation** (`verl/workers/rollout/`): VLLM or HF rollout workers generate responses
3. **Reward Scoring** (`verl/workers/reward_manager/`): Rule-based or model-based reward functions evaluate responses
4. **Advantage Estimation** (`verl/trainer/ppo/core_algos.py`): GAE, GRPO, REINFORCE++, or ReMax
5. **Model Updates**: Actor (policy) and Critic (value) models are updated via FSDP or Megatron

### Key Configuration Structure (YAML)

Training is configured via `verl/trainer/config/ppo_trainer.yaml`:

- `data`: Dataset paths, batch sizes, max sequence lengths
- `actor_rollout_ref`: Actor policy, reference policy, and rollout settings
- `critic`: Value function model and training settings
- `reward_model`: Reward model and reward manager selection
- `algorithm`: Advantage estimator (gae/grpo/reinforce_plus_plus/remax), KL control
- `trainer`: Training loop, logging, checkpointing, validation

### Worker System (Ray-based)

The `RayPPOTrainer` manages worker groups via Ray:
- **ActorRollout**: Generates responses and updates policy
- **Critic**: Estimates value functions (not used for GRPO/ReMax)
- **RefPolicy**: Reference policy for KL penalty computation
- **RewardModel**: Optional model-based reward scoring
- **RewardManager**: Processes rewards (naive/prime/yr implementations)

### Supported Strategies

- **FSDP**: `strategy: fsdp` - Fully Sharded Data Parallel via `verl/workers/fsdp_workers.py`
- **Megatron**: `strategy: megatron` - Tensor/pipeline parallel via `verl/workers/megatron_workers.py`

### Advantage Estimators

The `algorithm.adv_estimator` config controls advantage computation:
- `gae`: Generalized Advantage Estimation (requires critic)
- `grpo`: Group Relative Policy Optimization (no critic)
- `reinforce_plus_plus`: REINFORCE++ (no critic)
- `remax`: ReMax baseline (no critic)

## Key File Locations

| Component | Path |
|-----------|------|
| Main PPO trainer | `verl/trainer/ppo/ray_trainer.py` |
| Training entry point | `verl/trainer/main_ppo.py` |
| Configs | `verl/trainer/config/` |
| Actor/Rollout workers | `verl/workers/actor/`, `verl/workers/rollout/` |
| Critic workers | `verl/workers/critic/` |
| Reward managers | `verl/workers/reward_manager/` |
| Core RL algorithms | `verl/trainer/ppo/core_algos.py` |
| Datasets | `verl/utils/dataset/` |
| Reward scoring | `verl/utils/reward_score/` |
| Test suites | `tests/` |
| Training scripts | `or1_scripts/train/`, `examples/ppo_trainer/` |

## Code Style

- Python formatting: Google style via YAPF (120 char limit)
- Column limit: 120 characters
- Indent width: 4 spaces
- Config files use YAML with Hydra for composition

## Notes

- This is a Skywork fork of verl with customizations for reasoning model training
- Docker images available: `whatcanyousee/verl:vemlp-th2.4.0-cu124-vllm0.6.3-ray2.10-te2.0-megatron0.11.0-v0.0.6`
- The project uses vLLM 0.6.3 specifically (check `pyproject.toml` for exact versions)
- Ray is used for distributed orchestration across nodes