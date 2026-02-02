# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Necto/Nexto is a community machine learning Rocket League bot trained with Deep Reinforcement Learning using RLGym. The project consists of two main components: a distributed training system and a bot inference system for RLBot.

## Commands

### Running the Bot (Inference)

```bash
# Install dependencies
pip install -r rlbot-support/Nexto/requirements.txt

# Run with RLBot
python run.py

# Or run with GUI for match configuration
python run_gui.py
```

### Training (requires Redis server with WANDB_KEY and REDIS_PASSWORD environment variables)

```bash
pip install -r training/requirements.txt

# Start a worker (requires host, name, and password arguments)
python -m training.worker <worker_name> <redis_ip> <redis_password>

# Run the learner (training loop)
python -m training.learner <redis_ip>
```

## Architecture

### Distributed Training System (`training/`)

The training uses `rocket_learn` framework with Redis-based rollout collection:

- **`learner.py`** - Main training loop using PPO algorithm. Coordinates with Redis workers and updates the neural network model.
- **`worker.py`** - Runs game instances in parallel, collects experience (observations, actions, rewards), sends rollouts to Redis.
- **`agent.py`** - Neural network architecture wrapping EARL (Efficient Attention for Reinforcement Learning) Perceiver with discrete action head.
- **`obs.py`** - `NectoObsBuilder` encodes game state into query/key/value tensors with entity attention mechanism (players, ball, boost pads).
- **`parser.py`** - `NectoAction` defines 90 discrete actions combining ground and aerial maneuvers.
- **`reward.py`** - Multi-component reward: goal scoring (+10), win probability, ball distance/alignment, boost management, demos, aerial play.
- **`state.py`** - `NectoStateSetter` samples initial game states from replays (70%) or random distributions.
- **`terminal.py`** - Match ends on goal, 30s no-touch timeout, or 5min maximum.

### Bot Inference (`rlbot-support/`)

Two bot versions exist (Necto v1, Nexto v2). Key components:

- **`bot.py`** - RLBot `BaseAgent` subclass. Handles game loop, converts `GameTickPacket` to `GameState`, manages tick skipping (8), hardcoded kickoffs, and beta parameter for action stochasticity.
- **`agent.py`** - Loads TorchScript model (`nexto-model.pt`) and performs inference with action lookup table.
- **`nexto_obs.py`** - `NextoObsBuilder` converts `GameState` to entity-based format matching training, with team inversion and normalization.

### Action Space

The 90 discrete actions combine:
- Ground: throttle (-1, 0, 1) × steer (-1, 0, 1) × boost (0, 1) × handbrake (0, 1), excluding invalid boost combinations
- Aerial: pitch × yaw × roll × jump × boost combinations with handbrake for wavedashes

### Beta Parameter

Controls action selection stochasticity:
- `beta=1` - Greedy (best action)
- `beta=0.5` - Sampling from distribution
- `beta=0` - Uniform random
- `beta=-1` - Worst action

### Key Integration Points

- Model file: `rlbot-support/Nexto/nexto-model.pt` (TorchScript exported from training)
- RLGym compatibility layer in `rlbot-support/Nexto/bot.py` uses `rlgym_compat.GameState`
- Team inversion in `nexto_obs.py` handles orange team observations

## Code Conventions

- Uses 4-space indentation
- NumPy arrays for state/action representation
- Torch for neural network operations
- Entity-based observation format with IS_SELF, IS_MATE, IS_OPP, IS_BALL, IS_BOOST markers