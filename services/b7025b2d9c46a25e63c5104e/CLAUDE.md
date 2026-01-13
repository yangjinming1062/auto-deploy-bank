# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Softlearning is a deep reinforcement learning toolbox for training maximum entropy policies in continuous control domains. It implements Soft Actor-Critic (SAC) and Soft Q-Learning (SQL) algorithms using TensorFlow, with distributed training orchestration via Ray Tune.

## Installation

### Conda Installation
```bash
# Requires MuJoCo license and installation (see README.md for details)
conda env create -f environment.yml
conda activate softlearning
pip install -e .
```

### Docker Installation
```bash
export MJKEY="$(cat ~/.mujoco/mjkey.txt)" \
    && docker-compose \
        -f ./docker/docker-compose.dev.cpu.yml \
        up \
        -d \
        --force-recreate

# Access container
docker exec -it softlearning bash

# Cleanup
docker-compose -f ./docker/docker-compose.dev.cpu.yml down --rmi all --volumes
```

## Common Commands

### Training
```bash
# Train an agent locally
softlearning run_example_local examples.development \
    --algorithm SAC \
    --universe gym \
    --domain HalfCheetah \
    --task v3 \
    --exp-name my-experiment \
    --checkpoint-frequency 1000

# Dry run (show config without executing)
softlearning run_example_dry examples.development --algorithm SAC --universe gym --domain HalfCheetah --task v3

# Debug mode (limits trials for debugging)
softlearning run_example_debug examples.development --algorithm SAC --universe gym --domain HalfCheetah --task v3

# Run with specific resources
softlearning run_example_local examples.development \
    --algorithm SAC \
    --universe gym \
    --domain HalfCheetah \
    --task v3 \
    --cpus 4 \
    --gpus 1
```

### Simulating Policies
```bash
# Simulate trained policy (find checkpoint in ~/ray_results/)
python -m examples.development.simulate_policy \
    ~/ray_results/gym/HalfCheetah/v3/2018-12-12T16-48-37-my-sac-experiment-0/mujoco-runner_0_seed=7585_2018-12-12_16-48-37xuadh9vd/checkpoint_1000/ \
    --max-path-length 1000 \
    --num-rollouts 1 \
    --render-kwargs '{"mode": "human"}'
```

### Testing
```bash
# Run all tests
pytest

# Run specific test module
python -m pytest softlearning/utils/serialization_test.py

# Run example tests
python -m pytest examples/development/main_test.py
```

### Cloud Execution
```bash
# Launch on Google Compute Engine
softlearning launch_example_gce examples.development \
    --algorithm SAC \
    --universe gym \
    --domain HalfCheetah \
    --task v3

# Launch on EC2
softlearning launch_example_ec2 examples.development \
    --algorithm SAC \
    --universe gym \
    --domain HalfCheetah \
    --task v3

# Run on existing cluster
softlearning run_example_cluster examples.development --algorithm SAC --universe gym --domain HalfCheetah --task v3
```

## Code Architecture

### Core Components

The framework follows a modular design with these key components (see `softlearning/` directory):

1. **Algorithms** (`algorithms/`): RL algorithm implementations
   - `RLAlgorithm`: Abstract base class defining the training loop
   - `SAC`: Soft Actor-Critic implementation (softlearning/algorithms/sac.py:1)
   - `SQL`: Soft Q-Learning implementation (softlearning/algorithms/sql.py:1)

2. **Environments** (`environments/`): Environment adapters and wrappers
   - `gym/`: Gym environment wrappers
   - `dm_control/`: DeepMind Control Suite wrappers
   - `adapters/`: Environment compatibility adapters
   - `get_environment_from_params()`: Factory function for environment creation (softlearning/environments/utils.py:1)

3. **Policies** (`policies/`): Policy implementations
   - `GaussianPolicy`: Gaussian policy with feedforward networks
   - `FeedforwardGaussianPolicy`: Standard feedforward Gaussian policy
   - `UniformPolicyMixin`: For exploration/warmup
   - All policies use `policies.get()` factory function for instantiation

4. **Value Functions** (`value_functions/`): Q-function and value function implementations
   - Neural network-based Q-functions
   - Accessed via `value_functions.get()` factory

5. **Replay Pools** (`replay_pools/`): Experience replay buffers
   - Stores and samples experience transitions
   - Accessed via `replay_pools.get()` factory

6. **Samplers** (`samplers/`): Rollout samplers
   - `base_sampler.py`: Abstract sampler interface
   - `remote_sampler.py`: Distributed sampling
   - `goal_sampler.py`: Goal-conditioned sampling
   - Accessed via `samplers.get()` factory

7. **Models** (`models/`): Neural network architectures
   - `feedforward.py`: Feedforward networks
   - `convnet.py`: Convolutional networks

8. **Utils** (`utils/`): Utility functions
   - `tensorflow.py`: GPU memory management
   - `tune.py`: Ray Tune integration helpers
   - `serialization.py`: Object serialization for checkpointing
   - `video.py`: Video saving utilities

### Factory Pattern

The codebase uses a consistent factory pattern across modules. Components are registered and instantiated using `get()` functions:
- `algorithms.get()`: Create algorithm instances
- `policies.get()`: Create policy instances
- `value_functions.get()`: Create value function instances
- `replay_pools.get()`: Create replay pool instances
- `samplers.get()`: Create sampler instances

Components are specified via configuration dictionaries with `'class_name'` and `'config'` keys.

### Training Loop

Training flow (see `examples/development/main.py:25` and `softlearning/algorithms/rl_algorithm.py:147`):
1. `ExperimentRunner` (Ray Tune `Trainable`) receives variant configuration
2. Components are instantiated using factory functions
3. `algorithm.train()` is called, which yields control to `_train()` method
4. Standard RL loop: sample → store → train (repeated for `n_epochs`)
5. Checkpointing saves state every `checkpoint_frequency` steps

### Configuration

Experiment configurations are defined in `examples/development/variants.py`:
- `ALGORITHM_PARAMS_BASE` / `ALGORITHM_PARAMS_ADDITIONAL`: Algorithm hyperparameters
- `GAUSSIAN_POLICY_PARAMS_BASE`: Policy network architecture
- `TOTAL_STEPS_PER_UNIVERSE_DOMAIN_TASK`: Training length by environment
- Environment-specific configurations for Gym and DM Control domains

Configurations use Ray Tune's `tune.sample_from()` for dynamic sampling.

### Examples Structure

- `examples/development/main.py`: Primary training script with `ExperimentRunner` class
- `examples/development/main_test.py`: Integration tests
- `examples/development/simulate_policy.py`: Policy simulation utility
- `examples/development/variants.py`: Experiment configurations
- `examples/development/instrument.py`: Ray Tune orchestration functions
- `examples/multi_goal/`: Multi-goal RL examples

### CLI Interface

Console scripts in `softlearning/scripts/console_scripts.py` provide commands:
- `run_example_local`: Local execution with Ray parallelization
- `run_example_debug`: Debug mode with limited trials
- `run_example_dry`: Show configuration without execution
- `run_example_cluster`: Run on existing Ray cluster
- `launch_example_gce/ec2`: Launch on cloud with autoscaling

## Key Files

- `setup.py`: Package configuration with entry points
- `requirements.txt`: Python dependencies
- `environment.yml`: Conda environment definition
- `softlearning/algorithms/rl_algorithm.py:147`: `_train()` method with main RL loop
- `examples/development/main.py:25`: `ExperimentRunner` class integrating all components
- `examples/development/variants.py`: Experiment configuration presets

## Development Notes

- Checkpointing saves to `~/ray_results/<universe>/<domain>/<task>/<timestamp>-<exp-name>/<trial-id>/<checkpoint-id>/`
- Resume training with `--restore <checkpoint_path>` (feature noted as "currently broken" in README)
- GPU memory growth is enabled by default in `softlearning/utils/tensorflow.py`
- Seeds are set via `softlearning/utils/misc.py::set_seed()`
- Supports eager mode execution with `--run-eagerly` flag